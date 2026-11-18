# S1｜Google 機器學習課程：Recommendation Systems

- **類型**：線上教材（Google for Developers），共讀 4 個單元
- **原始筆記**：`raw/S1-google-ml-recommendation-course.md`
- **網址**：https://developers.google.com/machine-learning/recommendation/overview/types

## 一句話摘要
推薦系統把「多到看不完」的東西縮成一小串值得給你看的清單，常見做法是三階段流程，再搭配兩種猜你喜好的方法。

## 重點
- 三階段：候選生成 → 打分數 → 重新排序（詳見 [三階段流程](../concepts/three-stage-pipeline.md)）。
- YouTube 的候選生成會把數十億支影片縮小到數百到數千支。
- [內容過濾](../concepts/content-based-filtering.md)：找「和你喜歡的東西很像」的東西；不用別人的資料，但很難拓展你的興趣。
- [協同過濾](../concepts/collaborative-filtering.md)：找「和你很像的人也喜歡」的東西；會有驚喜，但有 [冷啟動](../concepts/cold-start.md) 問題。
- 回饋分成「明確」與「隱含」兩種（見 [訊號與足跡](../concepts/signals-and-footprints.md)）。

## 被哪些頁面引用
推薦系統、三階段流程、內容過濾、協同過濾、冷啟動、訊號與足跡、同溫層
