"""演算法生活課：規則檢查（對應 CLAUDE.md 第 6～8、12 節）。

用法（在專案根目錄）：python3 tools/check.py [--report 報告.md]
全部通過 → 結束碼 0；有任何問題 → 列出問題並以結束碼 1 結束（GitHub Actions 會顯示失敗）。

  K1  首頁卡片 ↔ lessons/ 資料夾一一對應；slug 為小寫英文＋連字號
  K2  首頁卡片的 data-pages ＝ 講義投影片數
  K3  講義骨架：<title>、description、deck.css、三支 script 順序正確、沒有 <style>
  K4  每張投影片有合法的 data-kind；除了資料來源頁，都有 footer.refs（Wiki 1～3 頁、來源 1～4 個）
  K5  data-wiki 指到存在的 Wiki 頁；data-sources 都登錄在 assets/sources.js
  K6  標示的來源，真的被該頁引用的 Wiki 頁引用（防止出處標錯）
  K7  投影片上的數字（含插圖文字）都能在引用的 Wiki 頁找到（防止編造數字）
  K8  內容頁條列加起來不超過 90 字
  K9  術語表裡的詞，第一次出現時要寫在該頁或更早頁的 data-explains
  K10 相對連結與資源路徑都存在，且要明確寫到 index.html（不可只寫到資料夾）
  K11 assets/sources.js 與 knowledge-base/wiki/sources/ 一致
  K12 Wiki lint（tools/wiki_lint.py）通過
"""
import re, sys, json, pathlib, subprocess, html as H

ROOT = pathlib.Path(__file__).resolve().parent.parent
KB = ROOT / "knowledge-base" / "wiki"
issues = []
def bad(code, where, msg): issues.append((code, where, msg))

def text_of(fragment):
    t = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", H.unescape(t)).strip()

# ---------- 來源與術語 ----------
sjs = (ROOT / "assets/sources.js").read_text(encoding="utf-8")
SOURCES = json.loads(sjs[sjs.index("{"):sjs.rindex("}") + 1])
src_pages = {p.name.split("-")[0].upper(): p for p in (KB / "sources").glob("s*.md")}
for sid, p in src_pages.items():
    if sid not in SOURCES:
        bad("K11", "assets/sources.js", f"Wiki 有來源頁 {p.name}，但 sources.js 沒有 {sid}")
    else:
        url = [l.split("：", 1)[1].strip() for l in p.read_text(encoding="utf-8").splitlines() if l.startswith("- **網址**：")]
        if url and url[0] != SOURCES[sid]["url"]:
            bad("K11", "assets/sources.js", f"{sid} 網址和 Wiki 來源頁不一致")
for sid in SOURCES:
    if sid not in src_pages:
        bad("K11", "assets/sources.js", f"{sid} 在 Wiki 沒有來源頁")

terms = []
for line in (KB / "glossary.md").read_text(encoding="utf-8").splitlines():
    if line.startswith("| ") and not line.startswith("| 術語") and not line.startswith("|---"):
        for t in re.split(r"[／（）()]", line.split("|")[1]):
            if t.strip():
                terms.append(t.strip())

def wiki_facts(rels):
    txt = ""
    for r in rels:
        p = KB / r
        if p.exists():
            txt += p.read_text(encoding="utf-8")
    cites = set(re.findall(r"\[(S\d+)\]\(", txt)) | {r.split("/")[1].split("-")[0].upper() for r in rels if r.startswith("sources/")}
    facts = re.sub(r"\]\([^)]*\)", "]", txt)
    facts = re.sub(r"\[S\d+\]", "", facts)
    facts = re.sub(r"(?m)^\s*\d+\.\s", "", facts)
    return facts, cites

# ---------- 首頁卡片 ----------
home = (ROOT / "index.html").read_text(encoding="utf-8")
block = home[home.index("<!-- LESSONS:START"):home.index("<!-- LESSONS:END")]
cards = {m.group(1): int(m.group(2)) for m in re.finditer(r'data-lesson="([^"]+)" data-pages="(\d+)"', block)}
folders = sorted(p.name for p in (ROOT / "lessons").iterdir() if p.is_dir() and not p.name.startswith("_"))
for f in folders:
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", f):
        bad("K1", f"lessons/{f}", "資料夾名稱要用小寫英文＋連字號")
    if f not in cards:
        bad("K1", "index.html", f"lessons/{f}/ 沒有首頁卡片")
    if not (ROOT / "lessons" / f / "index.html").exists():
        bad("K1", f"lessons/{f}", "缺少 index.html")
for c in cards:
    if c not in folders:
        bad("K1", "index.html", f"卡片 {c} 指到不存在的講義")

# ---------- 每份講義 ----------
KINDS = {"cover", "content", "quiz", "checklist", "sources"}
lesson_files = [ROOT / "lessons" / f / "index.html" for f in folders] + [ROOT / "lessons/_template/index.html"]
for lf in lesson_files:
    if not lf.exists():
        continue
    rel = lf.relative_to(ROOT).as_posix()
    doc = lf.read_text(encoding="utf-8")
    # K3
    if not re.search(r"<title>[^<]+｜演算法生活課</title>", doc): bad("K3", rel, "<title> 要是「講義標題｜演算法生活課」")
    if 'name="description"' not in doc: bad("K3", rel, "缺少 meta description")
    if "../../assets/deck.css" not in doc: bad("K3", rel, "沒有載入 ../../assets/deck.css")
    if "<style" in doc: bad("K3", rel, "講義裡不可以寫 <style>")
    scripts = re.findall(r'<script[^>]*src="([^"]+)"', doc)
    if scripts != ["../../assets/sources.js", "../../assets/wiki-titles.js", "../../assets/deck.js"] or doc.count("<script") != 3:
        bad("K3", rel, f"script 必須依序只有 sources.js、wiki-titles.js、deck.js（目前：{scripts}）")
    sections = re.findall(r"(<section\b[^>]*>)(.*?)</section>", doc, flags=re.S)
    slug = lf.parent.name
    if slug in cards and cards[slug] != len(sections):
        bad("K2", "index.html", f"{slug} 卡片寫 {cards[slug]} 頁，實際 {len(sections)} 頁")
    explained = set()
    for i, (tag, body) in enumerate(sections, 1):
        where = f"{rel} 第 {i} 頁"
        kind = (re.search(r'data-kind="([^"]+)"', tag) or [None, None])[1]
        if kind not in KINDS:
            bad("K4", where, f"data-kind 不合法：{kind}"); continue
        if kind == "sources":
            continue
        f = re.search(r'<footer class="refs" data-wiki="([^"]*)" data-sources="([^"]*)"', body)
        if not f:
            bad("K4", where, "缺少 <footer class=\"refs\" data-wiki=… data-sources=…>"); continue
        wikis, srcs = f.group(1).split(), f.group(2).split()
        if not 1 <= len(wikis) <= 3: bad("K4", where, f"data-wiki 要 1～3 頁（目前 {len(wikis)}）")
        if not 1 <= len(srcs) <= 4: bad("K4", where, f"data-sources 要 1～4 個（目前 {len(srcs)}）")
        for w in wikis:
            if not (KB / w).exists(): bad("K5", where, f"Wiki 頁不存在：{w}")
        for s in srcs:
            if s not in SOURCES: bad("K5", where, f"來源 {s} 沒有登錄在 sources.js")
        facts, cites = wiki_facts(wikis)
        for s in srcs:
            if s in SOURCES and s not in cites:
                bad("K6", where, f"標示來源 {s}，但 {' '.join(wikis)} 沒有引用它")
        visible = text_of(body)
        nums_text = re.sub(r"\bQ\d+\b", "", visible)
        for n in re.findall(r"\d[\d,]*", nums_text):
            n = n.rstrip(",")
            if not re.search(rf"(?<![\d,]){re.escape(n)}(?![\d,])", facts):
                bad("K7", where, f"數字「{n}」在 {' '.join(wikis)} 找不到")
        if kind == "content":
            ul = re.search(r'<div class="text">.*?<ul>(.*?)</ul>', body, flags=re.S)
            if ul:
                n_chars = len(text_of(ul.group(1)).replace(" ", ""))
                if n_chars > 90: bad("K8", where, f"條列共 {n_chars} 字，超過 90 字")
        explained |= {x.strip() for x in (re.search(r'data-explains="([^"]*)"', tag) or [None, ""])[1].split(",") if x.strip()}
        prose = text_of(re.sub(r"<svg.*?</svg>", " ", body, flags=re.S))
        for t in terms:
            if t in prose and t not in explained:
                bad("K9", where, f"術語「{t}」第一次出現沒有解釋（請在這頁或更早的頁面寫進 data-explains）")

# ---------- K10 相對連結 ----------
for page in [ROOT / "index.html"] + [p for p in lesson_files if p.exists()]:
    doc = page.read_text(encoding="utf-8")
    for link in re.findall(r'(?:href|src)="([^"#:]+)(?:#[^"]*)?"', doc):
        if link.startswith(("//", "data")) or not link:
            continue
        if link.endswith("/"):
            bad("K10", page.relative_to(ROOT).as_posix(), f"連結「{link}」只寫到資料夾，請明確寫成「{link}index.html」（直接打開檔案時才連得到）")
            continue
        target = (page.parent / link).resolve()
        if not target.exists():
            bad("K10", page.relative_to(ROOT).as_posix(), f"連結指到不存在的檔案：{link}")

# ---------- K12 Wiki lint ----------
r = subprocess.run([sys.executable, str(ROOT / "tools/wiki_lint.py"), str(ROOT / "knowledge-base"), "/tmp/wiki-lint-report.md"],
                   capture_output=True, text=True)
if r.returncode != 0:
    for line in r.stdout.splitlines():
        if line.startswith("| L"):
            bad("K12", "knowledge-base", line.strip("| "))

# ---------- 報告 ----------
lines = ["# check.py 報告", "", f"- 講義：{len(folders)} 份（另含範本）", f"- 問題數：**{len(issues)}**", ""]
lines += (["| 代碼 | 位置 | 問題 |", "|---|---|---|"] + [f"| {c} | {w} | {m} |" for c, w, m in issues]) if issues else ["✅ 全部通過"]
report = "\n".join(lines)
print(report)
if "--report" in sys.argv:
    pathlib.Path(sys.argv[sys.argv.index("--report") + 1]).write_text(report + "\n", encoding="utf-8")
sys.exit(1 if issues else 0)
