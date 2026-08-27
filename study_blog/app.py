import os
import re
from pathlib import Path
from datetime import datetime

import yaml
from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "posts"
STATIC_DIR = str(BASE / "static")
_SLUG_RE = re.compile(r"^[a-zA-Z0-9_\-]+$")


def slug_to_path(slug: str) -> Path:
    if not _SLUG_RE.match(slug):
        raise HTTPException(400, "invalid slug")
    return DATA / f"{slug}.md"


def split_frontmatter(text: str):
    if text.startswith("---"):
        m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
        if m:
            fm = yaml.safe_load(m.group(1)) or {}
            return fm, text[m.end():]
    return {}, text


def updated_at(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds")


def summarize(path: Path) -> dict:
    fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    fm["slug"] = path.stem
    fm["updated_at"] = updated_at(path)
    fm.setdefault("title", path.stem)
    fm.setdefault("date", "")
    fm.setdefault("tags", [])
    fm.setdefault("summary", "")
    return {k: fm.get(k) for k in ("slug", "title", "date", "tags", "summary", "updated_at")}


def list_posts():
    posts = []
    for p in DATA.glob("*.md"):
        if p.name.startswith("_raw") or p.name == "posts_index.json":
            continue
        try:
            posts.append(summarize(p))
        except Exception:
            continue
    posts.sort(key=lambda x: (x.get("date") or "", x.get("updated_at") or ""), reverse=True)
    return posts


def get_post(slug: str):
    path = slug_to_path(slug)
    if not path.exists():
        raise HTTPException(404, "not found")
    fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
    fm["slug"] = slug
    fm["updated_at"] = updated_at(path)
    fm["content"] = body
    fm.setdefault("title", slug)
    fm.setdefault("date", "")
    fm.setdefault("tags", [])
    fm.setdefault("summary", "")
    return fm


def save_post(slug: str, data: dict, create: bool = False):
    path = slug_to_path(slug)
    if create and path.exists():
        raise HTTPException(409, "slug exists")
    if not create and not path.exists():
        raise HTTPException(404, "not found")
    existing, _ = split_frontmatter(path.read_text(encoding="utf-8")) if path.exists() else ({}, "")
    for k in ("title", "date", "tags", "summary"):
        if k in data and data[k] is not None:
            existing[k] = data[k]
    existing["slug"] = slug
    body = data.get("content", "")
    out = "---\n" + yaml.safe_dump(existing, allow_unicode=True, sort_keys=False) + "---\n\n" + body + "\n"
    path.write_text(out, encoding="utf-8")
    return get_post(slug)


def slugify(title: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_\-一-鿿]+", "-", title).strip("-")
    return s or f"post-{datetime.now().strftime('%Y%m%d%H%M%S')}"


class Hub:
    def __init__(self):
        self.conns: dict[str, set[WebSocket]] = {}

    async def connect(self, slug: str, ws: WebSocket):
        await ws.accept()
        self.conns.setdefault(slug, set()).add(ws)

    def disconnect(self, slug: str, ws: WebSocket):
        s = self.conns.get(slug)
        if s:
            s.discard(ws)
            if not s:
                self.conns.pop(slug, None)

    async def broadcast(self, slug: str, msg: dict):
        for ws in list(self.conns.get(slug, set())):
            try:
                await ws.send_json(msg)
            except Exception:
                self.disconnect(slug, ws)


hub = Hub()
router = APIRouter()
ws_router = APIRouter()


def check_key(request: Request):
    if not request.app.state.edit_protected:
        return
    if request.headers.get("X-Edit-Key") != request.app.state.edit_key:
        raise HTTPException(403, "invalid edit key")


@router.get("/")
async def index(request: Request):
    return _render("index.html", request, {})


@router.get("/p/{slug}")
async def post_page(request: Request, slug: str):
    return _render("post.html", request, {"slug": slug})


@router.get("/api/config")
async def config(request: Request):
    return {"edit_protected": request.app.state.edit_protected}


@router.get("/api/posts")
async def api_list():
    return list_posts()


@router.get("/api/posts/{slug}")
async def api_get(slug: str):
    return get_post(slug)


@router.post("/api/posts")
async def api_create(request: Request, payload: dict):
    check_key(request)
    title = payload.get("title") or "未命名文章"
    slug = payload.get("slug") or slugify(title)
    return save_post(slug, payload, create=True)


@router.put("/api/posts/{slug}")
async def api_update(request: Request, slug: str, payload: dict):
    check_key(request)
    post = save_post(slug, payload, create=False)
    await hub.broadcast(slug, {"type": "saved", "slug": slug, "updated_at": post["updated_at"]})
    return post


@router.delete("/api/posts/{slug}")
async def api_delete(request: Request, slug: str):
    check_key(request)
    path = slug_to_path(slug)
    if not path.exists():
        raise HTTPException(404, "not found")
    path.unlink()
    await hub.broadcast(slug, {"type": "deleted", "slug": slug})
    return {"ok": True}


@ws_router.websocket("/ws/{slug}")
async def ws(websocket: WebSocket, slug: str):
    if not _SLUG_RE.match(slug):
        await websocket.close()
        return
    await hub.connect(slug, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        hub.disconnect(slug, websocket)


def make_app(base_path: str = "", edit_key: str | None = None):
    base_path = (base_path or "").rstrip("/")
    if edit_key is None:
        edit_key = os.environ.get("STUDY_EDIT_KEY", "")
    app = FastAPI(title="Study Blog")
    app.state.edit_key = edit_key
    app.state.edit_protected = bool(edit_key)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    templates = Jinja2Templates(directory=str(BASE / "templates"))
    templates.env.globals["base_path"] = base_path
    templates.env.globals["edit_protected"] = bool(edit_key)
    app.state.templates = templates
    app.include_router(router)
    app.include_router(ws_router)
    return app


def _render(name: str, request: Request, ctx: dict):
    return request.app.state.templates.TemplateResponse(request=request, name=name, context=ctx)


app = make_app(base_path=os.environ.get("BASE_PATH", "").rstrip("/"))
