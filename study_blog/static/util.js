const BP = window.BASE_PATH || "";

async function api(path, opts = {}) {
  opts.headers = opts.headers || {};
  const key = sessionStorage.getItem("editKey");
  if (key) opts.headers["X-Edit-Key"] = key;
  const res = await fetch(BP + path, opts);
  if (res.status === 403) { sessionStorage.removeItem("editKey"); throw new Error("need-key"); }
  if (!res.ok) throw new Error("HTTP " + res.status);
  return res;
}

async function ensureEditKey() {
  if (!window.EDIT_PROTECTED) return true;
  let key = sessionStorage.getItem("editKey");
  if (key) return key;
  key = prompt("编辑需要输入编辑密钥：");
  if (key == null) throw new Error("cancelled");
  sessionStorage.setItem("editKey", key);
  return key;
}

function renderMarkdown(src) {
  const html = marked.parse(src || "", { gfm: true, breaks: false });
  return DOMPurify.sanitize(html);
}

function highlightIn(el) {
  el.querySelectorAll("pre code").forEach(b => { try { hljs.highlightElement(b); } catch (e) {} });
}

let _toastTimer = null;
function toast(msg, action) {
  const t = document.getElementById("toast");
  t.innerHTML = "";
  t.appendChild(document.createTextNode(msg));
  if (action) {
    const b = document.createElement("button");
    b.className = "btn";
    b.textContent = action.label;
    b.onclick = () => { t.classList.add("hidden"); action.fn(); };
    t.appendChild(b);
  }
  t.classList.remove("hidden");
  clearTimeout(_toastTimer);
  _toastTimer = setTimeout(() => t.classList.add("hidden"), action ? 6000 : 2500);
}
