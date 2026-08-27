import os
import re
import json
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import yaml

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "posts")
POSTS = os.path.abspath(RAW)


def read_raw(name):
    with open(os.path.join(POSTS, f"_raw_{name}.html"), encoding="utf-8") as f:
        return f.read()


def parse_index_meta():
    soup = BeautifulSoup(read_raw("index"), "lxml")
    meta = {}
    for li in soup.select("#list-container li"):
        a = li.find("a")
        if not a:
            continue
        href = a.get("href", "")
        slug = href.replace("./", "").replace(".html", "")
        meta_div = li.select_one(".article-meta")
        desc_div = li.select_one(".article-desc")
        date = None
        tags = []
        if meta_div:
            parts = [p.strip() for p in meta_div.get_text(" ", strip=True).split("·")]
            parts = [p for p in parts if p]
            if parts:
                date = re.sub(r"[（(].*?[)）]", "", parts[0]).strip()
                tags = [p for p in parts[1:] if p]
        meta[slug] = {
            "title": a.get_text(strip=True),
            "date": date,
            "tags": tags,
            "summary": desc_div.get_text(" ", strip=True) if desc_div else "",
        }
    return meta


def extract_body(name):
    soup = BeautifulSoup(read_raw(name), "lxml")
    container = soup.select_one("#article-container")
    # remove back-link
    back = container.select_one("#back-link")
    if back:
        back.extract()
    # remove subtitle, capture date
    subtitle = container.select_one(".subtitle")
    sub_date = None
    if subtitle:
        m = re.search(r"最后更新：(\d{4}-\d{2}-\d{2})", subtitle.get_text())
        if m:
            sub_date = m.group(1)
        subtitle.extract()
    text = md(str(container), heading_style="ATX", bullets="-", code_language="")
    # normalize blank lines
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text, sub_date


def main():
    meta = parse_index_meta()
    slugs = list(meta.keys())
    posts = []
    for slug in slugs:
        body, sub_date = extract_body(slug)
        m = meta[slug]
        date = m["date"] or sub_date
        front = {
            "title": m["title"],
            "slug": slug,
            "date": date,
            "tags": m["tags"],
            "summary": m["summary"],
        }
        content = "---\n" + yaml.safe_dump(front, allow_unicode=True, sort_keys=False) + "---\n\n" + body + "\n"
        out = os.path.join(POSTS, f"{slug}.md")
        with open(out, "w", encoding="utf-8") as f:
            f.write(content)
        posts.append(front)
        print(f"wrote {slug}.md ({len(body)} chars)")
    with open(os.path.join(POSTS, "..", "posts_index.json"), "w", encoding="utf-8") as f:
        json.dump(sorted(posts, key=lambda p: p.get("date") or "", reverse=True), f, ensure_ascii=False, indent=2)
    print("total posts:", len(posts))


if __name__ == "__main__":
    main()
