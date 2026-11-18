# CLAUDE.md：演算法生活課（Algo Life Lessons）

> 給 AI 的專案說明書。開始任何修改前，請先讀完這份檔案。
> 其他 AI 工具（Codex、Cursor 等）讀的 `AGENTS.md` 指向這裡，規則以本檔為準。

## 1. 專案目的

做一個**給完全沒有技術背景的人**看的講義網站，主題是「生活中的演算法」：推薦系統、線上追蹤、隱私自保。

- 每份講義是一份可以在瀏覽器翻頁的簡報（像上課投影片），放在 GitHub Pages 上公開瀏覽。
- 所有內容都來自同一個知識庫 `knowledge-base/`（LLM Wiki）。**講義只能講 Wiki 裡有來源的事。**
- 目標是可以一直**照同一套方式新增講義**，而不是每次從零設計。

## 2. 一分鐘看懂專案結構

```
algo-life-lessons/
├── CLAUDE.md                ← 本檔：AI 的規則（最重要）
├── AGENTS.md                ← 給其他 AI 工具的入口，指向本檔
├── README.md                ← 給人看的介紹
├── index.html               ← 首頁「講義庫」：每份講義一張卡片
├── .nojekyll                ← 讓 GitHub Pages 不經過 Jekyll（_template 才不會被隱藏）。不要刪
├── assets/                  ← 全站共用，講義不可各自複製一份
│   ├── deck.css             ← 講義（簡報）樣式
│   ├── deck.js              ← 翻頁、頁尾來源、測驗、勾選清單、資料來源頁
│   ├── site.css             ← 首頁樣式
│   ├── sources.js           ← 來源清單 S1、S2⋯（手動維護）
│   ├── wiki-titles.js       ← Wiki 頁名（自動產生，勿手改）
│   └── favicon.svg
├── lessons/
│   ├── _template/index.html ← 新講義範本，每種元件都有示範
│   ├── recsys-intro/        ← 講義 1：你的手機為什麼知道你想買什麼？
│   └── privacy-checkup/     ← 講義 2：幫手機做一次隱私健檢
├── wiki/index.html          ← 網站上的 Wiki 頁（自動產生，勿手改）
├── knowledge-base/          ← LLM Wiki 本體（Markdown）
│   ├── SCHEMA.md            ← Wiki 的維護規則（ingest／query／lint）
│   ├── raw/                 ← 原始資料筆記，不可修改
│   ├── wiki/                ← 概念頁、來源頁、術語表、index、log
│   └── checks/              ← 過去的檢查報告
├── tools/
│   ├── check.py             ← 規則檢查（提交前必跑）
│   ├── build_wiki.py        ← knowledge-base → wiki/index.html + assets/wiki-titles.js
│   ├── wiki_lint.py         ← Wiki 健康檢查
│   └── render_check.py      ← 選用：用瀏覽器截圖檢查版面
└── .github/workflows/check.yml ← 每次 push 自動跑檢查
```

## 3. 內容規則：知識庫優先

1. 講義上的每一個事實，都要能在 `knowledge-base/wiki/` 找到，而且那一頁有標來源（S1、S2⋯）。
2. Wiki 裡沒有的內容：**先補進 Wiki，再寫講義**。補 Wiki 的流程照 `knowledge-base/SCHEMA.md`（先跟使用者討論重點，再寫）。
3. 投影片上的**數字**一定要在它引用的 Wiki 頁裡出現。不可以自己加「約 15 分鐘」「花 3 分鐘」這種聽起來合理、但沒有根據的數字。
4. 每張投影片在**寫的時候**就決定它根據哪幾頁 Wiki、哪幾個來源（寫在頁尾的 `data-wiki`、`data-sources`）。不要事後用程式推測。
5. 平台自己的說法（例如 TikTok 說會避免同溫層）要寫成「平台說⋯」，不可寫成已證實的事實。

## 4. 視覺風格

- **調性**：清爽教科書風。米白紙張、淡淡的點點底紋、深藍文字、圓角卡片。
- **顏色**：只用這 6 個變數，不新增顏色（要新增先問使用者並更新本節）。

  | 變數 | 色碼 | 用途 |
  |---|---|---|
  | `--paper` | #FBF8F3 | 背景 |
  | `--ink` | #1F2A44 | 文字、深色區塊 |
  | `--coral` | #E4572E | 強調、kicker、警告 |
  | `--teal` | #2A9D8F | 正面、完成、Wiki 連結、隱私標籤 |
  | `--mustard` | #F2C14E | 重點底色、清單符號 |
  | `--soft` | #E8E2D6 | 淺色區塊 |

- **字體**：標題 Noto Serif TC（粗 900），內文 Noto Sans TC。
- **說話方式**：像在跟長輩或國中生解釋。每個抽象概念都配一個**生活比喻**（店員、選秀節目、背包貼紙⋯）。
- **插圖**：手寫 inline SVG，`viewBox="0 0 400 320"`，只用 `deck.css` 裡的顏色 class（`ink-fill`、`coral-fill`、`teal-soft`⋯），不寫死色碼。不用照片、不用外部圖片、不畫任何品牌商標或知名角色（平台名稱用文字即可）。
- **舞台**：每張投影片固定 1280×720，由 `deck.js` 等比縮放。

## 5. 頁面結構

| 頁面 | 檔案 | 怎麼產生 |
|---|---|---|
| 首頁（講義庫） | `index.html` | 手寫。講義卡片放在 `<!-- LESSONS:START -->` 和 `<!-- LESSONS:END -->` 之間 |
| 講義 | `lessons/<slug>/index.html` | 手寫 HTML，從 `lessons/_template/index.html` 複製 |
| Wiki | `wiki/index.html` | `python3 tools/build_wiki.py` 自動產生 |

### 一份講義的投影片順序

1. **封面**（`cover`）：kicker＝講義類型，h1＝問題式標題，一句「給誰看」，一個關鍵名詞的白話定義。
2. **開場**：一個生活情境或迷思，讓人想知道答案。
3. **內容頁**（`content`）× 5～12：一頁一個重點。
4. **小測驗**（`quiz`）或**勾選清單**（`checklist`）：至少一個互動頁。
5. **重點回顧**：三件事帶走。
6. **資料來源**（`sources`）：空的 section，`deck.js` 自動填。

## 6. 講義 HTML 格式（照抄，不要自創結構）

### 6.1 檔案骨架

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>講義標題｜演算法生活課</title>
<meta name="description" content="一到兩句講義簡介（和首頁卡片的簡介相同）">
<link rel="icon" href="../../assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&family=Noto+Serif+TC:wght@900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../assets/deck.css">
</head>
<body>
<main id="deck">
  <!-- 每張投影片一個 section，前面加一行註解，例如「03｜標題」 -->
</main>
<script src="../../assets/sources.js"></script>
<script src="../../assets/wiki-titles.js"></script>
<script src="../../assets/deck.js"></script>
</body>
</html>
```

- 不可在講義裡寫 `<style>` 或另外的 `<script>`；需要新樣式就加到 `assets/deck.css`（並在本檔記下）。

### 6.2 投影片類型

**內容頁**（最常用）：

```html
<section class="slide" data-kind="content" data-privacy="false" data-explains="協同過濾">
  <div class="inner">
    <div class="text">
      <p class="kicker">猜法二</p>
      <h2>協同過濾：跟你很像的人也喜歡</h2>
      <ul>
        <li>口味跟你很像的同學都愛這家店 → 你可能也會喜歡。</li>
        <li>⋯</li>
      </ul>
    </div>
    <div class="art"><svg viewBox="0 0 400 320" aria-hidden="true">⋯</svg></div>
  </div>
  <footer class="refs" data-wiki="concepts/collaborative-filtering.md" data-sources="S1 S2"></footer>
</section>
```

| 屬性 | 說明 |
|---|---|
| `data-kind` | `cover`／`content`／`quiz`／`checklist`／`sources`，必填 |
| `data-privacy` | 這頁講隱私或自保就寫 `true`，會自動出現「🔒 隱私」標籤 |
| `data-explains` | 這頁**第一次解釋**的術語（術語表裡的詞），**用半形逗號分隔**（術語本身可能有空白，例如「廣告 ID」） |
| `footer data-wiki` | 這頁根據的 Wiki 頁（相對 `knowledge-base/wiki/` 的路徑），空白分隔，1～3 個 |
| `footer data-sources` | 這頁用到的來源編號，空白分隔，1～4 個 |

**封面**：`<section class="slide cover" data-kind="cover">`，內文用 `h1`，加上 `p.cover-sub`、`p.cover-note`、`p.hint`。

**小測驗**：`.quiz` 裡放多個 `.q`；每題 `<p class="q-text"><b>Q1</b> 題目</p>`，選項 `<button class="opt" data-ok="1">` 正確、`data-ok="0"` 錯誤，最後 `<p class="q-fb" aria-live="polite"></p>`。

**勾選清單**：`<ul class="checklist">` 每項 `<li><label><input type="checkbox"> 文字</label></li>`，後面接 `<p class="check-progress"></p>`。勾選狀態不存檔（不使用 localStorage）。

**設定路徑**：`<p class="path"><span>設定</span><i>→</i><span>隱私權</span></p>`，用在「去哪裡按」的步驟。

**資料來源頁**：`<section class="slide sources" data-kind="sources"></section>`，放最後一張，內容自動產生。

## 7. 投影片寫作規則

- 標題是**一句重點**（「三個平台，各看什麼？」），不是名詞（「平台介紹」）。
- 每頁 2～3 個條列，**條列加起來不超過 90 字**。
- 術語表（`knowledge-base/wiki/glossary.md`）裡的詞，第一次出現的那頁要白話解釋，並寫進 `data-explains`。
- 一張投影片只講一件事；放不下就拆兩張，不要縮小字。
- 順序編號用 ①②③（投影片與插圖都是）；阿拉伯數字只用在有來源的數據上，`check.py` 會檢查每個阿拉伯數字。
- 插圖裡的文字也算投影片內容，一樣不能出現 Wiki 沒有的數字。
- 首頁卡片的頁數（`data-pages`）要等於講義的投影片數（含資料來源頁）。

## 8. 命名與放置

| 東西 | 規則 | 例子 |
|---|---|---|
| 講義資料夾 | `lessons/<slug>/index.html`，slug 用小寫英文＋連字號，**不用中文、空白、底線開頭** | `lessons/privacy-checkup/` |
| 講義專用圖片 | `lessons/<slug>/img/`，檔名小寫英文 | `lessons/privacy-checkup/img/step-1.svg` |
| 共用樣式／程式 | 只放 `assets/` | `assets/deck.css` |
| Wiki 頁 | `knowledge-base/wiki/concepts/<英文>.md`，標題用中文 | `concepts/cold-start.md` |
| 來源 | 編號 S1、S2⋯ 依加入順序，不重用編號 | 下一個是 S9 |
| 以 `_` 開頭的資料夾 | 範本或草稿，不會出現在首頁 | `lessons/_template/` |
| 站內連結 | 一律相對路徑，**明確寫到 `index.html`**，不可只寫到資料夾（直接雙擊打開檔案時，資料夾連結會變成檔案清單） | `lessons/privacy-checkup/index.html` |

## 9. 新增一份講義（SOP）

1. **先問**：主題、給誰看、想要的互動（測驗或清單）。和使用者確認大綱（每頁一行）再動手。
2. **查 Wiki**：讀 `knowledge-base/wiki/index.md`，列出每張投影片會用到的 Wiki 頁與來源。缺內容 → 先照 SCHEMA 補 Wiki。
3. **複製範本**：`cp -r lessons/_template lessons/<slug>`。
4. **寫投影片**：照第 6、7 節。每頁寫好 `data-wiki`、`data-sources`、`data-explains`。
5. **加首頁卡片**：在 `index.html` 的 `LESSONS:START/END` 之間加一張，`href="lessons/<slug>/index.html"`、`data-lesson="<slug>"`、`data-pages` 填頁數。
6. **跑檢查**：`python3 tools/check.py`，全部通過才算完成。有裝 playwright 就再跑 `python3 tools/render_check.py`。
7. **本機預覽**：`python3 -m http.server`，打開 http://localhost:8000。
8. **記錄**：在 `knowledge-base/wiki/log.md` 追加一筆 `## [日期] lesson | <slug>`。
9. **提交**：commit 訊息格式 `lesson: 新增 <slug>（<中文標題>）`。

## 10. 修改知識庫

- 新增或修改 Wiki 內容，照 `knowledge-base/SCHEMA.md`；`raw/` 裡的原始筆記不可修改。
- 改完一定要跑 `python3 tools/build_wiki.py`（更新 `wiki/index.html` 和 `assets/wiki-titles.js`），再跑 `python3 tools/check.py`。
- 新增來源時，同時更新 `assets/sources.js`（`check.py` 會比對兩邊是否一致）。

## 11. AI 修改時必須遵守

**要做**
- 動手前先讀本檔和相關 Wiki 頁；不確定就問使用者。
- 保持純靜態網站：HTML＋CSS＋原生 JavaScript，不加框架、不加打包工具、不加 npm。
- 每次修改後跑 `python3 tools/check.py`。
- 只改被要求改的地方；改了共用的 `assets/` 要檢查**所有**講義。

**不要做**
- 不要手改自動產生的檔案：`wiki/index.html`、`assets/wiki-titles.js`。
- 不要修改 `knowledge-base/raw/`。
- 不要刪除 `.nojekyll`，也不要刪除或改名已發布的講義資料夾（網址會壞掉）。
- 不要在講義裡寫 `<style>`、不要用外部圖片或圖片網址、不要新增顏色。
- 不要編造數字、引用或來源；Wiki 沒有的就先補 Wiki。

## 12. 檢查與發布

- `tools/check.py` 檢查項目：首頁卡片和講義資料夾一一對應、頁數正確、每頁都有 Wiki 和來源標註且存在、來源真的被該 Wiki 頁引用、數字能在 Wiki 找到、條列不超過 90 字、術語第一次出現有解釋、講義骨架正確、相對連結沒有斷、`sources.js` 和 Wiki 來源頁一致，並順便跑 Wiki lint。
- GitHub Actions（`.github/workflows/check.yml`）在每次 push 時自動跑：重新產生 Wiki 頁並確認沒有差異，再跑 `check.py`。
- 發布：GitHub repo → Settings → Pages → Build and deployment → Source 選 **Deploy from a branch**，Branch 選 **main**、資料夾 **/(root)**。

## 13. 過去踩過的坑（不要再犯）

| 坑 | 正確做法 |
|---|---|
| 把只在搜尋摘要看過的事實，標成某個已讀來源 | 只引用真的讀過、寫進 `raw/` 的來源 |
| 頁尾列出「整頁 Wiki 引用過的所有來源」，導致 iPhone 頁掛上 Netflix | 每頁手動指定 `data-sources`，只寫這頁真的用到的 |
| 自己加上「約 15 分鐘」這類沒有根據的數字 | 數字一律來自 Wiki；`check.py` 會擋 |
| 檢查程式把連結裡的「S3」當成數字 3，放過錯誤 | 改檢查程式後，用一個已知錯誤的例子確認它抓得到 |
| `data-explains` 用空白分隔，「廣告 ID」被拆成兩個詞 | 用半形逗號分隔 |
| 插圖裡畫了一串假的廣告 ID 數字、用 1 2 3 當編號 | 插圖不放沒根據的數字；編號用 ①②③ |
| 獨立頁面互相連結，未登入或沒權限的人打不開 | 所有頁面都在同一個網站內，用相對路徑連結 |
| 連結寫成 `lessons/recsys-intro/`，在電腦上直接打開時只看到資料夾清單 | 連結寫到 `index.html`；`check.py` 的 K10 會擋 |
