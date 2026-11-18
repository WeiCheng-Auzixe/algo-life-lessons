# log：操作流水帳（只增不改）

## [2026-11-18 15:49] discuss | 選定主題
- 第一輪討論：使用者先選了「AI Agents」，觀眾設定為「完全沒技術背景的人」。
- 已讀 6 篇 AI Agents 資料並列出重點，使用者反問「可以推薦主題嗎」→ 提供 7 個候選主題。

## [2026-11-18 15:54] discuss | 改主題
- 使用者改選「你的手機為什麼知道你想買什麼？（推薦演算法）」。AI Agents 的資料不沿用。

## [2026-11-18 16:00] collect | 蒐集 6 篇
- S1 Google ML 課程、S2 Amazon 2003、S3 Netflix、S4 TikTok 2020、S5 東北大學 2018、S6 FTC。

## [2026-11-18 16:05] discuss | 重點確認（先討論、後生成）
- 列出 6 篇重點與簡報故事線請使用者確認。
- 使用者決定：**多放隱私與自保的內容**。→ 寫進 SCHEMA（隱私投影片 ≥ 35%）。
- 發現缺口：「自保」只有 FTC 的通用建議，缺 iPhone／Android 的具體設定 → 回到 collect。

## [2026-11-18 16:08] collect | 補 2 篇
- S7 Apple App 追蹤透明度、S8 Google 廣告 ID。

## [2026-11-18 16:10] ingest | S1–S8 共 8 篇
- 建立來源頁 8 頁、概念頁 10 頁、實體頁 3 頁、overview、glossary、index。
- S5 原始筆記中混入一筆不屬於該來源的調查數字 → 在來源頁標註「不採用」。

## [2026-11-18 16:20] lint | 第 1 輪：5 個問題
- L5 ×2：collaborative-filtering.md 寫「2017 年回顧文說 Amazon 1998 年上線」並標 S2，但這句其實來自另一篇（Smith & Linden 2017），只在搜尋摘要看過、沒有 ingest → **刪除**。
- L3：index.md 漏列 S8 → 補上。
- L2 ×2：overview、glossary 只有 index 連進來 → 從「推薦系統」頁加導覽連結。

## [2026-11-18 16:22] lint | 第 2 輪：0 個問題 ✅

## [2026-11-18 16:30] query | 「怎麼把這個主題教給沒有技術背景的人？」
- 讀 index → 10 個概念頁 → 產生 slides/plan.json（17 張投影片，每張列出 wiki_refs）。

## [2026-11-18 16:32] check | 簡報規劃檢查 run 1–5
- run 1：3 個問題（封面「約 15 分鐘」無根據；封面用了「演算法」沒解釋；「回饋」沒解釋）。
- run 2–3：發現**檢查器自己有漏洞**：數字比對時被連結裡的「S3」和清單編號「3.」騙過，讓總結頁「花 3 分鐘」這個沒有根據的數字通過 → 修正比對規則後抓到。
- run 4：修正簡報規劃後 0 個問題。
- run 5：新增 C7（每張投影片的來源要明確指定，且必須出現在它引用的 Wiki 頁面）→ 0 個問題。

## [2026-11-18 16:40] render-check | 版面檢查 run 1–2
- run 1：11 個問題（頁尾來源列過長 ×6、插圖文字超出邊界 ×3、插圖文字重疊 ×1、測驗頁溢出 4px ×1）。
- 看截圖時另外發現：頁尾列出的是「整個 Wiki 頁面引用過的所有來源」，iPhone 那頁也掛上 Netflix、TikTok → 出處錯誤。改為在規劃階段逐頁指定來源（即上面的 C7）。
- run 2：0 個問題。

## [2026-11-18 16:45] file-back | 簡報大綱存回 wiki/outputs/slide-outline.md
- lint run 3：新頁面成為孤兒頁 → 從 overview 連過去 → lint run 4：0 個問題。

## [2026-11-18 16:39] publish | Wiki 網站與簡報上線
- Wiki：https://claude.ai/artifact/KuCtMgHbu3gpuUn7xvoCc6
- 簡報：https://claude.ai/artifact/KmR8HJwmakSRe6FpjRzMKP
- 加上 Wiki 連結重新生成簡報 → plan-check run 6：0 個問題；render-check run 3：0 個問題。

## [2026-11-18 16:55] schema | 依第一次執行的反思修訂 SCHEMA
- 加入 C7（來源在規劃階段指定）、版面問題分「排版／內容」兩種退回、存回後必跑 lint、檢查器要用已知錯誤例子自我測試、待辦：collect 節點檢查 raw 筆記純度。
- 報告文件：https://claude.ai/artifact/8yZBm422hf5W48RPSLT9oj

## [2026-11-18 16:58] fix | 「看教學簡報」按鈕會跳到登入頁
- 原因：按鈕開新分頁連到另一個獨立頁面，該分頁未登入。
- 修正：簡報直接內嵌在 Wiki 網站裡（同頁切換），簡報頁尾的 Wiki 標籤可跳回對應 Wiki 頁。render-check run 4：0 個問題。

## [2026-11-18 17:30] project | 建立「演算法生活課」講義網站
- 把 Wiki 與教學簡報搬進新專案 algo-life-lessons，訂出 CLAUDE.md / AGENTS.md 規則。
- 講義 1 recsys-intro：由上一份教學簡報轉成新格式。check.py 第一輪抓到 7 個問題：data-explains 用空白分隔把「廣告 ID」拆開（改用逗號）、插圖裡的假廣告 ID 數字、回顧頁插圖用 1 2 3 編號（改 ①②③）。
- 講義 2 privacy-checkup：照 CLAUDE.md 第 9 節 SOP 新增（使用者授權直接製作，大綱未另行確認）。原定標題「10 分鐘」沒有根據，改為「幫手機做一次隱私健檢」。check.py 第一次即通過。
- 範本 _template：寫作說明裡的「2～3」「90 字」被 K7 擋下 → 改成不含數字的說明。

## [2026-11-18 17:30] lesson | privacy-checkup

## [2026-11-18 17:20] fix | 站內連結在本機打不開
- 使用者直接雙擊 index.html 開啟（file://），連結寫成 `lessons/recsys-intro/` 只會顯示資料夾清單。
- 所有站內連結改為明確指到 index.html；check.py K10 新增「不可只寫到資料夾」，並用舊寫法確認會被擋下。
