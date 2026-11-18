"""把 knowledge-base/（LLM Wiki）轉成可瀏覽的網頁 wiki/index.html，並更新 assets/wiki-titles.js。

用法（在專案根目錄執行）：python3 tools/build_wiki.py
  - 讀：knowledge-base/wiki/、knowledge-base/raw/、knowledge-base/SCHEMA.md、knowledge-base/checks/
  - 寫：wiki/index.html（網站上的 Wiki 頁）、assets/wiki-titles.js（講義頁尾顯示 Wiki 頁名用）
  - 不要手改這兩個輸出檔；改 knowledge-base/ 之後重跑本程式。
"""
import re, sys, html, json, pathlib
import markdown, networkx as nx

proj = pathlib.Path(__file__).resolve().parent.parent
root = proj / "knowledge-base"
out = proj / "wiki" / "index.html"
slides_url = ""

def anchor(path):  # path 相對於 root
    p = path.replace(".md", "")
    p = p[5:] if p.startswith("wiki/") else p
    return re.sub(r"[^a-z0-9]+", "-", p.lower()).strip("-")

def title_of(text, fallback):
    for l in text.splitlines():
        if l.startswith("# "):
            return l[2:].strip()
    return fallback

files = []
order = ["wiki/index.md", "wiki/overview.md", "wiki/glossary.md"]
groups = [("開始", order),
          ("概念", [f"wiki/concepts/{n}.md" for n in ["recommender-system", "signals-and-footprints", "content-based-filtering",
                   "collaborative-filtering", "three-stage-pipeline", "cold-start", "filter-bubble", "phone-listening-myth",
                   "online-tracking", "privacy-self-defense"]]),
          ("實體", sorted(str(p.relative_to(root)) for p in (root / "wiki/entities").glob("*.md"))),
          ("來源摘要 S1–S8", sorted(str(p.relative_to(root)) for p in (root / "wiki/sources").glob("*.md"))),
          ("查詢成果", sorted(str(p.relative_to(root)) for p in (root / "wiki/outputs").glob("*.md"))),
          ("維護紀錄", ["wiki/log.md", "SCHEMA.md"]),
          ("原始資料 raw/", sorted(str(p.relative_to(root)) for p in (root / "raw").glob("*.md"))),
          ("檢查紀錄 checks/", sorted((str(p.relative_to(root)) for p in (root / "checks").glob("*.md")),
                                     key=lambda s: (s.split("-run-")[0], int(re.search(r"run-(\d+)", s).group(1)))))]
ORDER_CHECK = {"checks/lint": 0, "checks/plan-check": 1, "checks/render-check": 2}
groups[-1] = (groups[-1][0], sorted(groups[-1][1], key=lambda s: (ORDER_CHECK.get(s.split("-run-")[0], 9), int(re.search(r"run-(\d+)", s).group(1)))))

LINK = re.compile(r"\]\(([^)]+?\.md)\)")
URL = re.compile(r"(?<![\(\"'>])(https?://[^\s)<|]+)")

pages, G = {}, nx.Graph()
for gname, lst in groups:
    for rel in lst:
        text = (root / rel).read_text(encoding="utf-8")
        a = anchor(rel)
        base = (root / rel).parent
        def fix(m):
            tgt = (base / m.group(1)).resolve()
            try:
                r = str(tgt.relative_to(root))
            except ValueError:
                return m.group(0)
            if rel.startswith("wiki/") and r.startswith("wiki/") and not {rel, r} & {"wiki/log.md", "wiki/index.md"}:
                G.add_edge(anchor(rel), anchor(r))
            return f"](#{anchor(r)})"
        body = LINK.sub(fix, text)
        if rel.startswith("raw/"):  # front matter 顯示成程式碼區塊
            parts = body.split("---")
            if len(parts) >= 3:
                body = "```yaml" + parts[1] + "```\n" + "---".join(parts[2:])
        body = URL.sub(lambda m: f"<{m.group(1)}>", body)
        h = markdown.markdown(body, extensions=["tables", "fenced_code"])
        h = h.replace("✅", '<span class="ok">✅</span>').replace("⚠", '<span class="warn">⚠</span>')
        t = title_of(text, rel)
        pages[a] = {"rel": rel, "title": t, "group": gname, "html": h}
        files.append(a)

# 知識圖譜（只畫 wiki 頁，不含 log）
for a in files:
    if pages[a]["rel"].startswith("wiki/") and pages[a]["rel"] not in ("wiki/log.md", "wiki/index.md"):
        G.add_node(a)
pos = nx.spring_layout(G, seed=7, k=0.55, iterations=300)
xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
def sx(x): return 40 + (x - min(xs)) / (max(xs) - min(xs)) * 820
def sy(y): return 30 + (y - min(ys)) / (max(ys) - min(ys)) * 460
COLOR = {"開始": "#1F2A44", "概念": "#E4572E", "實體": "#F2C14E", "來源摘要 S1–S8": "#2A9D8F", "查詢成果": "#7B5EA7"}
def short(a):
    t = pages[a]["title"]
    t = re.split(r"[：:（(｜|]", t)[0].strip() if not pages[a]["rel"].startswith("wiki/sources") else t.split("｜")[0]
    return t[:9]
svg = ['<svg viewBox="0 0 900 520" class="graph" role="img" aria-label="Wiki 頁面連結圖">']
for u, v in G.edges():
    svg.append(f'<line x1="{sx(pos[u][0]):.0f}" y1="{sy(pos[u][1]):.0f}" x2="{sx(pos[v][0]):.0f}" y2="{sy(pos[v][1]):.0f}"/>')
for a in G.nodes():
    c = COLOR.get(pages[a]["group"], "#999"); r = 8 + min(G.degree(a), 14)
    x, y = sx(pos[a][0]), sy(pos[a][1])
    svg.append(f'<a href="#{a}"><circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c}"/><text x="{x:.0f}" y="{y + r + 15:.0f}" text-anchor="middle">{html.escape(short(a))}</text></a>')
svg.append("</svg>")
legend = "".join(f'<span><i style="background:{c}"></i>{g}</span>' for g, c in COLOR.items())
graph_html = (f'<h1>知識圖譜</h1><p>每個圓點是一頁 Wiki，線代表兩頁互相連結；點越大，連結越多。點一下就能打開那一頁。</p>'
              f'<div class="legend">{legend}</div>{"".join(svg)}'
              f'<p class="muted">共 {G.number_of_nodes()} 頁、{G.number_of_edges()} 條連結（不含 index 與 log）。</p>')
pages["graph"] = {"rel": "（由 networkx 自動產生）", "title": "知識圖譜", "group": "開始", "html": graph_html}
files.insert(1, "graph")

nav = []
for gname, lst in groups:
    items = [anchor(r) for r in lst]
    if gname == "開始":
        items.insert(1, "graph")
    lis = "".join(f'<li><a href="#{a}" data-a="{a}">{html.escape(pages[a]["title"] if a != "index" else "目錄（index）")}</a></li>' for a in items)
    open_attr = " open" if gname in ("開始", "概念", "實體", "來源摘要 S1–S8", "查詢成果") else ""
    nav.append(f'<details{open_attr}><summary>{gname}</summary><ul>{lis}</ul></details>')

articles = "".join(
    f'<article id="p-{a}" data-a="{a}" hidden>{pages[a]["html"]}<footer class="src">檔案：<code>{html.escape(pages[a]["rel"])}</code></footer></article>'
    for a in files)
slides_btn = '<a class="slides-btn" href="../index.html">← 回講義庫</a>'
slides_view = ""

CSS = """
:root{--paper:#FBF8F3;--ink:#1F2A44;--coral:#E4572E;--teal:#2A9D8F;--mustard:#F2C14E;--soft:#E8E2D6;--muted:#5B6478;
--sans:"Noto Sans TC","Noto Sans CJK TC","PingFang TC","Microsoft JhengHei",sans-serif;--serif:"Noto Serif TC","Noto Serif CJK TC",serif}
*{box-sizing:border-box}body{margin:0;font-family:var(--sans);color:var(--ink);background:var(--paper);line-height:1.75}
header{position:sticky;top:0;z-index:3;display:flex;align-items:center;gap:16px;padding:12px 24px;background:var(--ink);color:#fff}
header h1{font-family:var(--serif);font-size:20px;margin:0;font-weight:900}header .tag{font-size:13px;opacity:.75}
.slides-btn{margin-left:auto;background:var(--coral);color:#fff;text-decoration:none;padding:6px 16px;border-radius:999px;font-weight:700;font-size:14px}
#menu{display:none;background:none;border:1px solid #fff5;color:#fff;border-radius:8px;padding:4px 10px;font:inherit}
.wrap{display:flex;min-height:calc(100vh - 52px)}
nav{width:290px;flex:none;border-right:1px solid var(--soft);padding:16px 12px 40px;background:#F5F0E7;position:sticky;top:52px;height:calc(100vh - 52px);overflow:auto}
nav input{width:100%;padding:8px 12px;border:1px solid var(--soft);border-radius:10px;font:inherit;margin-bottom:10px;background:#fff}
nav summary{font-weight:700;cursor:pointer;padding:6px 6px;font-size:14px;color:var(--muted)}
nav ul{list-style:none;margin:0 0 6px;padding:0}nav li a{display:block;padding:4px 10px;border-radius:8px;color:var(--ink);text-decoration:none;font-size:14px;line-height:1.5}
nav li a:hover{background:var(--soft)}nav li a.on{background:var(--ink);color:#fff}
main{flex:1;min-width:0;padding:32px clamp(20px,5vw,72px) 80px;max-width:980px}
article h1{font-family:var(--serif);font-size:32px;line-height:1.35;margin:0 0 18px}
article h2{font-family:var(--serif);font-size:23px;margin:34px 0 10px;padding-bottom:6px;border-bottom:2px solid var(--mustard)}
article h3{font-size:18px;margin:24px 0 6px}
article a{color:#17675d;text-decoration:none;border-bottom:1px solid #2A9D8F66}article a:hover{background:#2A9D8F1f}
article table{border-collapse:collapse;width:100%;margin:12px 0;font-size:15px;display:block;overflow-x:auto}
article th,article td{border:1px solid var(--soft);padding:7px 10px;text-align:left;vertical-align:top}article th{background:#F0EADF}
article blockquote{margin:12px 0;padding:8px 16px;border-left:4px solid var(--teal);background:#2A9D8F12}
article code{background:#EFE9DE;padding:1px 6px;border-radius:5px;font-size:.9em}article pre{background:#1F2A44;color:#F5F0E7;padding:14px;border-radius:10px;overflow:auto}
article pre code{background:none;color:inherit}
.src{margin-top:40px;font-size:13px;color:var(--muted)}.warn{color:var(--coral);font-weight:700}
.graph{width:100%;height:auto;background:#fff;border:1px solid var(--soft);border-radius:14px}
.graph line{stroke:#1F2A4433;stroke-width:1.3}.graph text{font-size:12px;fill:var(--ink);font-family:var(--sans)}.graph circle{stroke:#fff;stroke-width:2}
.graph a:hover circle{stroke:var(--ink)}.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:14px;margin-bottom:10px}
.legend i{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:6px;vertical-align:-1px}.muted{color:var(--muted);font-size:14px}
#slides-view{position:fixed;left:0;right:0;bottom:0;top:52px;z-index:10;background:#EDE7DC}#slides-view iframe{width:100%;height:100%;border:0;display:block}
@media(max-width:820px){#menu{display:block}nav{position:fixed;left:0;top:52px;z-index:4;transform:translateX(-100%);transition:.2s;box-shadow:4px 0 20px #0002}
 nav.open{transform:none}.slides-btn{padding:6px 12px}header .tag{display:none}}
"""
JS = """
const arts=[...document.querySelectorAll('article')],links=[...document.querySelectorAll('nav li a')];
const sv=document.getElementById('slides-view'),sb=document.getElementById('slides-btn');
function go(){if(sv){const on=location.hash==='#slides';sv.hidden=!on;sb.textContent=on?'← 回到 Wiki':'▶ 看教學簡報';sb.href=on?'#index':'#slides';
 if(on){const f=document.getElementById('slides-frame');setTimeout(()=>f.focus(),50);return}}
 let a=location.hash.slice(1)||'index';if(!document.getElementById('p-'+a))a='index';
 arts.forEach(x=>x.hidden=x.dataset.a!==a);links.forEach(l=>l.classList.toggle('on',l.dataset.a===a));
 const on=links.find(l=>l.dataset.a===a);if(on){on.closest('details').open=true}
 window.scrollTo(0,0);document.querySelector('nav').classList.remove('open')}
addEventListener('hashchange',go);go();
addEventListener('message',e=>{if(e.data&&typeof e.data.wiki==='string')location.hash=e.data.wiki});
document.getElementById('q').addEventListener('input',e=>{const v=e.target.value.trim().toLowerCase();
 links.forEach(l=>{const art=document.getElementById('p-'+l.dataset.a);const hit=!v||l.textContent.toLowerCase().includes(v)||(art&&art.textContent.toLowerCase().includes(v));
 l.parentElement.style.display=hit?'':'none';if(v&&hit)l.closest('details').open=true})});
document.getElementById('menu').onclick=()=>document.querySelector('nav').classList.toggle('open');
"""
doc = f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>知識庫 Wiki｜演算法生活課</title><link rel="icon" href="../assets/favicon.svg">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&family=Noto+Serif+TC:wght@900&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<header><button id="menu" aria-label="目錄">☰</button><h1>演算法生活課 Wiki</h1><span class="tag">你的手機為什麼知道你想買什麼？｜8 篇來源・{len([a for a in files if pages[a]['rel'].startswith('wiki/')])} 頁</span>{slides_btn}</header>
<div class="wrap"><nav><input id="q" type="search" placeholder="搜尋 Wiki…" aria-label="搜尋">{''.join(nav)}</nav>
<main>{articles}</main></div>{slides_view}<script>{JS}</script></body></html>"""
out.write_text(doc.replace('id="p-wiki-index"', 'id="p-index"').replace('data-a="wiki-index"', 'data-a="index"').replace('href="#wiki-index"', 'href="#index"'), encoding="utf-8")
titles = {pages[a]["rel"][5:]: short(a) if not pages[a]["rel"].startswith("wiki/sources") else pages[a]["title"].split("｜")[0]
          for a in files if pages[a]["rel"].startswith("wiki/")}
(proj / "assets" / "wiki-titles.js").write_text("/* 由 tools/build_wiki.py 自動產生，請勿手改。 */\nwindow.WIKI_TITLES = " + json.dumps(titles, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
print(f"wrote {out} ({len(doc)//1024} KB, {len(files)} pages, graph {G.number_of_nodes()} nodes / {G.number_of_edges()} edges)")
