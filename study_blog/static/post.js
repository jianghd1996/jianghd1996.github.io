const slug = window.POST_SLUG;
const viewEl = document.getElementById("view");
const editorEl = document.getElementById("editor");
const mdEl = document.getElementById("md");
const previewEl = document.getElementById("preview");
const editBtn = document.getElementById("edit-btn");
const doneBtn = document.getElementById("done-btn");
const keyBtn = document.getElementById("key-btn");
const saveStatus = document.getElementById("save-status");

let content = "";
let dirty = false;
let saveTimer = null;
let ws = null;

async function load() {
  const res = await api(`/api/posts/${slug}`);
  const post = await res.json();
  content = post.content || "";
  document.title = post.title + " · 可在线编辑";
  renderView(content);
  editBtn.classList.remove("hidden");
  if (window.EDIT_PROTECTED) keyBtn.classList.remove("hidden");
  if (new URLSearchParams(location.search).get("edit") === "1") startEdit();
  connectWS();
}

function renderView(src) { viewEl.innerHTML = renderMarkdown(src); highlightIn(viewEl); }
function renderPreview(src) { previewEl.innerHTML = renderMarkdown(src); highlightIn(previewEl); }

function setStatus(state, text) {
  saveStatus.className = "save-status " + (state || "");
  saveStatus.textContent = text || "";
}

async function startEdit() {
  mdEl.value = content;
  renderPreview(content);
  viewEl.classList.add("hidden");
  editorEl.classList.remove("hidden");
  editBtn.classList.add("hidden");
  doneBtn.classList.remove("hidden");
  document.body.classList.add("editing");
  mdEl.focus();
}

function stopEdit() {
  editorEl.classList.add("hidden");
  viewEl.classList.remove("hidden");
  editBtn.classList.remove("hidden");
  doneBtn.classList.add("hidden");
  document.body.classList.remove("editing");
  setStatus("", "");
  dirty = false;
}

function scheduleSave() {
  dirty = true;
  setStatus("saving", "保存中…");
  clearTimeout(saveTimer);
  saveTimer = setTimeout(save, 700);
}

async function save() {
  try {
    const res = await api(`/api/posts/${slug}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: mdEl.value }),
    });
    const post = await res.json();
    content = mdEl.value;
    dirty = false;
    setStatus("saved", "已保存 " + new Date().toLocaleTimeString());
    renderPreview(content);
  } catch (e) {
    if (e.message === "need-key") {
      setStatus("saving", "需编辑密码才能保存（点 🔑）");
      keyBtn.classList.remove("hidden");
    } else {
      setStatus("saving", "保存失败，重试中…");
      saveTimer = setTimeout(save, 1500);
    }
  }
}

mdEl.addEventListener("input", () => { renderPreview(mdEl.value); scheduleSave(); });
mdEl.addEventListener("scroll", () => {
  const denom = (mdEl.scrollHeight - mdEl.clientHeight) || 1;
  const ratio = mdEl.scrollTop / denom;
  previewEl.scrollTop = ratio * (previewEl.scrollHeight - previewEl.clientHeight);
});

document.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") {
    e.preventDefault();
    if (!editorEl.classList.contains("hidden")) { clearTimeout(saveTimer); save(); }
  }
  if (e.key === "Escape" && !editorEl.classList.contains("hidden")) stopEdit();
});

editBtn.addEventListener("click", startEdit);
doneBtn.addEventListener("click", () => {
  clearTimeout(saveTimer);
  if (dirty) save().then(stopEdit); else stopEdit();
});

keyBtn.addEventListener("click", async () => {
  try {
    await ensureEditKey();
    keyBtn.textContent = "🔑 已设密码";
    if (dirty) save(); else setStatus("saved", "已设置编辑密码");
  } catch (e) { /* 用户取消，继续本地编辑，不强制 */ }
});

function connectWS() {
  if (!window.WebSocket) return;
  const proto = location.protocol === "https:" ? "wss" : "ws";
  ws = new WebSocket(`${proto}://${location.host}${BP}/ws/${slug}`);
  ws.onmessage = async (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.type !== "saved" || msg.slug !== slug) return;
    const fresh = await (await api(`/api/posts/${slug}`)).json();
    if (editorEl.classList.contains("hidden")) {
      content = fresh.content; renderView(content);
    } else if (!dirty) {
      content = fresh.content; mdEl.value = content; renderPreview(content);
    } else {
      toast("内容已被其他人更新，点击重新载入", {
        label: "重载",
        fn: async () => { content = fresh.content; mdEl.value = content; renderPreview(content); },
      });
    }
  };
}

load().catch(e => console.error(e));
