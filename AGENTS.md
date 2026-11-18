# AGENTS.md

本專案的完整規則寫在 **[`CLAUDE.md`](CLAUDE.md)**，所有 AI 工具（Codex、Cursor、Copilot、Claude Code⋯）都以那份為準。開始修改前請先讀完它。

## 最重要的 6 條（摘要）

1. **知識庫優先**：講義上的事實只能來自 `knowledge-base/wiki/`，且那頁有來源標註。Wiki 沒有的內容先補 Wiki（照 `knowledge-base/SCHEMA.md`），再寫講義。
2. **照範本做**：新講義從 `lessons/_template/` 複製，放在 `lessons/<小寫英文-slug>/index.html`，並在首頁 `index.html` 的 `LESSONS:START/END` 之間加卡片。
3. **每頁標出處**：每張投影片的 `<footer class="refs">` 寫 `data-wiki`（Wiki 頁）與 `data-sources`（S1、S2⋯），只寫這頁真的用到的。
4. **純靜態**：HTML＋CSS＋原生 JS，不加框架、不加建置工具；講義內不寫 `<style>`，共用樣式只放 `assets/`。
5. **不手改自動產生的檔案**：`wiki/index.html`、`assets/wiki-titles.js` 由 `python3 tools/build_wiki.py` 產生。
6. **提交前跑檢查**：`python3 tools/check.py` 全部通過才算完成。

常用指令：

```bash
python3 tools/build_wiki.py      # 改了 knowledge-base 之後
python3 tools/check.py           # 每次提交前
python3 -m http.server           # 本機預覽 http://localhost:8000
```
