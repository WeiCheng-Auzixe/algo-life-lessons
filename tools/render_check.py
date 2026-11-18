"""選用：用無頭瀏覽器逐頁打開每份講義，檢查版面並存截圖。

需要：pip install playwright && python3 -m playwright install chromium
用法（在專案根目錄）：python3 tools/render_check.py [截圖資料夾，預設 /tmp/algo-screens]
  R1 內容溢出（文字被切掉）　R2 頁尾來源列超過 2 行　R3 插圖文字超出插圖
  R4 插圖文字彼此重疊　R5 瀏覽器錯誤
"""
import sys, pathlib, os
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
shots = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/algo-screens"); shots.mkdir(parents=True, exist_ok=True)
PROBE = r"""() => {
 const s = document.querySelector('.slide.active'), out = [], inner = s.querySelector('.inner');
 if (inner && inner.scrollHeight > inner.clientHeight + 2) out.push(['R1', `內容高度 ${inner.scrollHeight}px > 可用 ${inner.clientHeight}px`]);
 const f = s.querySelector('.refs'); if (f && f.getBoundingClientRect().height > 80) out.push(['R2', '頁尾超過 2 行']);
 const boxes = [];
 s.querySelectorAll('svg').forEach(svg => { const sr = svg.getBoundingClientRect();
   svg.querySelectorAll('text').forEach(t => { const r = t.getBoundingClientRect();
     if (r.left < sr.left - 1 || r.right > sr.right + 1 || r.top < sr.top - 1 || r.bottom > sr.bottom + 1) out.push(['R3', `插圖文字「${t.textContent}」超出邊界`]);
     boxes.push([t.textContent, r]); }); });
 for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) { const [ta, a] = boxes[i], [tb, b] = boxes[j];
   if (Math.min(a.right, b.right) - Math.max(a.left, b.left) > 4 && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 4) out.push(['R4', `「${ta}」和「${tb}」重疊`]); }
 return out; }"""
lessons = sorted(p for p in (ROOT / "lessons").glob("*/index.html"))
issues = []
with sync_playwright() as p:
    exe = os.environ.get("CHROME_PATH")
    b = p.chromium.launch(**({"executable_path": exe} if exe else {}), args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1300, "height": 740})
    errs = []
    pg.on("pageerror", lambda ex: errs.append(str(ex)))
    pg.route("**/fonts.googleapis.com/**", lambda r: r.abort())
    for lf in lessons:
        slug = lf.parent.name
        pg.goto(lf.as_uri()); pg.wait_for_timeout(300)
        n = pg.evaluate("document.querySelectorAll('.slide').length")
        for i in range(1, n + 1):
            pg.evaluate(f"location.hash = '#s{i}'"); pg.wait_for_timeout(400)
            for code, msg in pg.evaluate(PROBE):
                issues.append((code, f"{slug} 第 {i} 頁", msg))
            pg.screenshot(path=str(shots / f"{slug}-{i:02d}.png"))
    for name, url in [("home", (ROOT / "index.html").as_uri()), ("wiki", (ROOT / "wiki/index.html").as_uri())]:
        pg.set_viewport_size({"width": 1280, "height": 900}); pg.goto(url); pg.wait_for_timeout(300)
        pg.screenshot(path=str(shots / f"_{name}.png"), full_page=(name == "home"))
    for e in errs:
        issues.append(("R5", "瀏覽器", e))
    b.close()
print(f"# 版面檢查\n\n- 講義 {len(lessons)} 份，截圖在 {shots}\n- 問題數：**{len(issues)}**\n")
print("\n".join(f"| {c} | {w} | {m} |" for c, w, m in issues) if issues else "✅ 全部通過")
sys.exit(1 if issues else 0)
