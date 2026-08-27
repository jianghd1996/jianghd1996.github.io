const listEl = document.getElementById("post-list");
const emptyEl = document.getElementById("empty");
const searchEl = document.getElementById("search");
const newBtn = document.getElementById("new-btn");
const countEl = document.getElementById("count");
let posts = [];

async function load() {
  const res = await api("/api/posts");
  posts = await res.json();
  countEl.textContent = posts.length + " 篇文章";
  newBtn.classList.remove("hidden");
  render();
}

function render() {
  const q = searchEl.value.trim().toLowerCase();
  const filtered = posts.filter(p => {
    if (!q) return true;
    const hay = [p.title, p.summary, (p.tags || []).join(" ")].join(" ").toLowerCase();
    return hay.includes(q);
  });
  listEl.innerHTML = "";
  emptyEl.classList.toggle("hidden", filtered.length > 0);
  for (const p of filtered) {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.className = "title";
    a.href = `${BP}/p/${p.slug}`;
    a.textContent = p.title;
    li.appendChild(a);

    const meta = document.createElement("div");
    meta.className = "post-meta";
    meta.textContent = [p.date, (p.tags || []).join(" · ")].filter(Boolean).join("   |   ");
    li.appendChild(meta);

    if (p.summary) {
      const s = document.createElement("p");
      s.className = "post-summary";
      s.textContent = p.summary;
      li.appendChild(s);
    }
    if (p.tags && p.tags.length) {
      const tg = document.createElement("div");
      tg.className = "tags";
      for (const t of p.tags) {
        const span = document.createElement("span");
        span.className = "tag";
        span.textContent = t;
        tg.appendChild(span);
      }
      li.appendChild(tg);
    }
    listEl.appendChild(li);
  }
}

searchEl.addEventListener("input", render);

newBtn.addEventListener("click", async () => {
  try { await ensureEditKey(); } catch (e) { return; }
  const title = prompt("新文章标题：");
  if (!title) return;
  try {
    const res = await api("/api/posts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    const post = await res.json();
    location.href = `${BP}/p/${post.slug}?edit=1`;
  } catch (e) {
    alert(e.message === "need-key" ? "编辑密钥错误" : "创建失败：" + e.message);
  }
});

load().catch(e => console.error(e));
