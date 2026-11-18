"""Wiki lint：健康檢查（LLM Wiki 的 lint 操作）。

用法：python3 pipeline/lint.py <wiki_root> <report_path>
檢查項目：
  L1 斷掉的連結
  L2 孤兒頁（沒有任何其他頁面連進來）
  L3 index.md 漏列的頁面
  L4 概念／實體／總覽頁中，含數字的句子沒有標來源
  L5 數字對不上原始資料（數字必須出現在被引用來源的 raw 筆記正文裡）
  L6 沒有被任何概念頁引用的來源
"""
import re, sys, pathlib, json

root = pathlib.Path(sys.argv[1]).resolve()
wiki = root / "wiki"
raw = root / "raw"
report_path = pathlib.Path(sys.argv[2])

LINK = re.compile(r"\]\(([^)#]+\.md)\)")
CITE = re.compile(r"\[(S\d)\]\(")
NUM = re.compile(r"\d[\d,\.]*")

pages = sorted(p for p in wiki.rglob("*.md"))
rel = {p: p.relative_to(wiki).as_posix() for p in pages}
issues = []

def body_lines(p):
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        yield i, line

# raw 正文（去掉 front matter）
raw_body = {}
for r in raw.glob("S*.md"):
    t = r.read_text(encoding="utf-8")
    sid = r.name.split("-")[0]
    parts = t.split("---")
    raw_body[sid] = parts[2] if len(parts) >= 3 else t

inbound = {rel[p]: set() for p in pages}
cited_by_concepts = set()

for p in pages:
    for i, line in body_lines(p):
        for target in LINK.findall(line):
            tp = (p.parent / target).resolve()
            if not tp.exists():
                issues.append(("L1", rel[p], i, f"斷掉的連結 → {target}"))
            elif tp != p and tp in rel:
                inbound[rel[tp]].add(rel[p])

# L2 孤兒頁
for page, srcs in inbound.items():
    if page in ("index.md", "log.md"):
        continue
    others = {s for s in srcs if s not in ("index.md", "log.md")}
    if not others:
        issues.append(("L2", page, 0, "孤兒頁：除了 index 以外沒有頁面連到這裡"))

# L3 index 漏列
index_text = (wiki / "index.md").read_text(encoding="utf-8")
listed = {(wiki / t).resolve() for t in LINK.findall(index_text)}
for p in pages:
    if rel[p] in ("index.md", "log.md"):
        continue
    if p.resolve() not in listed:
        issues.append(("L3", rel[p], 0, "index.md 沒有列出這一頁"))

# L4/L5 數字與來源
checked_dirs = ("concepts/", "entities/")
for p in pages:
    r = rel[p]
    if not (r.startswith(checked_dirs) or r == "overview.md"):
        continue
    for i, line in body_lines(p):
        if line.startswith("#"):
            continue
        cites = set(CITE.findall(line))
        if r.startswith("concepts/"):
            cited_by_concepts |= cites
        clean = re.sub(r"\]\([^)]*\)", "]", line)       # 去掉連結網址
        clean = re.sub(r"\[S\d\]", "", clean)              # 去掉來源標籤
        clean = re.sub(r"^\s*(\d+\.|-|\|)\s*", "", clean)  # 去掉清單編號
        nums = [n.rstrip(".,") for n in NUM.findall(clean)]
        nums = [n for n in nums if n]
        if not nums:
            continue
        if not cites:
            issues.append(("L4", r, i, f"含數字 {nums} 但沒有標來源"))
            continue
        for n in nums:
            if not any(n in raw_body.get(c, "") for c in cites):
                issues.append(("L5", r, i, f"數字「{n}」在引用來源 {sorted(cites)} 的原始筆記正文中找不到"))

# L6 未被引用的來源
for sid in sorted(raw_body):
    if sid not in cited_by_concepts:
        issues.append(("L6", f"sources/{sid.lower()}-*", 0, "沒有任何概念頁引用這個來源"))

lines = [f"# Lint 報告：{report_path.stem}", "", f"- 頁面數：{len(pages)}", f"- 問題數：**{len(issues)}**", ""]
if issues:
    lines += ["| 代碼 | 頁面 | 行 | 問題 |", "|---|---|---|---|"]
    for code, page, ln, msg in issues:
        lines.append(f"| {code} | {page} | {ln or '—'} | {msg} |")
else:
    lines.append("✅ 全部通過")
report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
json.dump([list(x) for x in issues], open(report_path.with_suffix(".json"), "w"), ensure_ascii=False)
sys.exit(1 if issues else 0)
