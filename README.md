# 演算法生活課 Algo Life Lessons

給**完全沒有技術背景的人**的講義網站：用生活比喻看懂推薦演算法、線上追蹤，以及怎麼保護自己的隱私。

- 🌐 **網站**：`https://<你的 GitHub 帳號>.github.io/algo-life-lessons/`（開啟 GitHub Pages 後的網址）
- 📘 **AI 規則**：[`CLAUDE.md`](CLAUDE.md)（其他 AI 工具看 [`AGENTS.md`](AGENTS.md)）

## 目前的講義

| 講義 | 類型 | 頁數 |
|---|---|---|
| [你的手機為什麼知道你想買什麼？](lessons/recsys-intro/) | 入門・概念 | 18 頁・含小測驗 |
| [動手做：幫手機做一次隱私健檢](lessons/privacy-checkup/) | 實作・隱私 | 12 頁・含勾選清單 |
| [演算法生活課 Wiki](wiki/) | 知識庫 | 26 頁・8 篇來源 |

## 這個專案的做法

和「一次把網頁做出來」不同，這個專案是先建立**一套規則**，之後的講義都照同一套方式快速新增：

```
knowledge-base/（LLM Wiki，有來源的知識）
        │  講義只能用 Wiki 裡的內容
        ▼
lessons/_template/ ──複製──▶ lessons/<新講義>/  ──▶ 首頁加一張卡片
        │
        ▼
tools/check.py 自動檢查（出處、數字、字數、術語、連結）──▶ GitHub Pages 發布
```

- 規則寫在 `CLAUDE.md`：專案目的、視覺風格、頁面結構、HTML 格式、命名方式、新增講義 SOP、AI 不能做的事。
- 第 2 份講義「幫手機做一次隱私健檢」就是照著 `CLAUDE.md` 的 SOP 新增的，用來驗證這套規則。

## 本機預覽

```bash
python3 -m http.server
# 打開 http://localhost:8000
```

直接雙擊 `index.html` 也能看（講義用相對路徑，不需要伺服器）。

## 檢查

```bash
pip install markdown networkx      # build_wiki.py 需要
python3 tools/build_wiki.py         # 改了 knowledge-base/ 之後
python3 tools/check.py              # 規則檢查
python3 tools/render_check.py       # 選用：需要 playwright，逐頁截圖檢查版面
```

每次 push 到 GitHub，`.github/workflows/check.yml` 會自動跑檢查。

## 資料來源

內容整理自 8 篇公開資料（Google 機器學習課程、Amazon 2003 年論文、Netflix 說明中心、TikTok 官方說明、美國東北大學研究、美國 FTC、Apple 支援文件、Google Play 說明），完整清單見各講義最後一頁或 [Wiki](wiki/)。
