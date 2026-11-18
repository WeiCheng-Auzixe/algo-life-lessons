---
id: S1
title: Recommendation Systems（Google Machine Learning 課程，共 4 個單元）
publisher: Google for Developers
urls:
  - https://developers.google.com/machine-learning/recommendation/overview/types
  - https://developers.google.com/machine-learning/recommendation/content-based/basics
  - https://developers.google.com/machine-learning/recommendation/content-based/summary
  - https://developers.google.com/machine-learning/recommendation/collaborative/basics
  - https://developers.google.com/machine-learning/recommendation/collaborative/summary
published: 未標示（線上課程，持續更新）
captured: 2026-11-18
---
# 擷取筆記（改寫，不是原文）

## 架構（overview/types）
- 常見三階段：候選生成（從巨大資料庫快速挑出小集合，可有多個候選來源）→ 打分數（較精細的模型排序，挑出約 10 個顯示）→ 重新排序（移除使用者明確不喜歡的、提高新內容、照顧多樣性與公平性）。
- 例子：YouTube 的候選生成把數十億支影片縮小到數百到數千支。

## 內容過濾（content-based）
- 推薦「和使用者已經喜歡的東西相似」的項目；靠項目特徵 + 使用者過去行為或明確回饋；不需要其他使用者的資料。
- App 商店例子：特徵有「教育」「休閒」「健康」、發行商；使用者也放在同一組特徵上；用內積（共同特徵數）打分數。例題中教育類 App 得 2 分最高、健康類 1 分、休閒遊戲 0 分。
- 優點：不需要別人的資料、容易擴充；能抓到小眾興趣。
- 缺點：特徵多半要人工設計，模型好壞受限於特徵；大多只推薦和既有興趣相符的東西，很難拓展興趣。

## 協同過濾（collaborative）
- 同時利用「使用者之間」與「項目之間」的相似度；可以因為「相似的人喜歡」而推薦你沒接觸過的東西（意外的驚喜）。
- 回饋矩陣：列是使用者、欄是項目；回饋分「明確」（打分數）與「隱含」（從行為推測，例如看完一部片）。
- 電影例子：用「兒童↔成人」「大片↔藝術片」兩個軸，把使用者和電影放進同一個空間，越靠近越可能喜歡；實務上這些座標（embedding）是從資料自動學出來的。
- 優點：不需領域知識；有驚喜；只需回饋矩陣就能起步。
- 缺點：冷啟動——訓練時沒看過的新項目無法產生 embedding；年齡、國家等附加特徵不好放進去。
