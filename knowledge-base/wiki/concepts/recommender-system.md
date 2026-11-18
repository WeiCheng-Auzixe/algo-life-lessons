# 推薦系統（Recommender System）是什麼？

## 白話定義
推薦系統就像一位**很懂你的店員**：店裡東西多到你看不完，他根據你以前的樣子，先幫你挑出一小串「你大概會喜歡」的東西。技術上說，它把非常大量的候選項目縮小成一小串值得給你看的清單 [S1](../sources/s1-google-recsys.md)。

## 它在哪裡？
- 購物網站：同一間網路商店，對不同顧客會長得不一樣，軟體工程師看到程式書、新手媽媽看到嬰兒玩具 [S2](../sources/s2-amazon-item-to-item.md)。
- 影音平台：Netflix 首頁的哪一列出現、列裡放哪些片、順序怎麼排，都是個人化的結果 [S3](../sources/s3-netflix.md)。
- 短影音：TikTok 的「為你推薦」每個人都不一樣 [S4](../sources/s4-tiktok.md)。

## 它怎麼猜？
1. 收集你的 [訊號與足跡](signals-and-footprints.md)。
2. 用兩種主要猜法：[內容過濾](content-based-filtering.md)（跟你喜歡的東西很像）與 [協同過濾](collaborative-filtering.md)（跟你很像的人也喜歡）。
3. 透過 [三階段流程](three-stage-pipeline.md) 從大量候選挑出最後幾個。

## 推薦 vs 廣告
推薦系統多半用你**在這個平台上**的行為；而跨網站、跨 App 的廣告，常靠 [線上追蹤](online-tracking.md) 把不同地方的資料連起來 [S6](../sources/s6-ftc-tracking.md) [S7](../sources/s7-apple-att.md)。（推論：這就是為什麼你在 A 網站看過的東西，會在 B App 的廣告出現。）

## 相關
[冷啟動](cold-start.md)、[同溫層](filter-bubble.md)、[手機偷聽迷思](phone-listening-myth.md)

← 回到 [總覽](../overview.md)｜看不懂的詞查 [術語表](../glossary.md)
