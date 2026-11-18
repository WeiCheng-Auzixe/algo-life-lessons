# S2｜Amazon 論文：Item-to-Item Collaborative Filtering（2003）

- **作者**：Greg Linden、Brent Smith、Jeremy York
- **出處**：IEEE Internet Computing 第 7 卷第 1 期（2003 年 1–2 月）
- **原始筆記**：`raw/S2-amazon-item-to-item-2003.md`
- **網址**：https://www.cs.umd.edu/~samir/498/Amazon-Recommendations.pdf

## 一句話摘要
Amazon 把「找和你相似的人」改成「找和你買過的東西相似的商品」，事先算好相似商品表，所以能對大量顧客即時推薦。

## 重點
- 是「買了這個的人也買了⋯」功能背後的經典做法（見 [協同過濾](../concepts/collaborative-filtering.md)）。
- 傳統做法在約 1,000 萬名顧客、100 萬件商品的規模就不實際。
- 例子：軟體工程師看到程式書，新手媽媽看到嬰兒玩具。
- 購物車推薦就像超市結帳台旁的商品，但每個人看到的不同。
- 作者自述：精準推薦的點擊與購買比例遠高於不分對象的橫幅廣告（⚠ 作者主張，未獨立驗證）。

## 相關頁面
[Amazon](../entities/amazon.md)、[協同過濾](../concepts/collaborative-filtering.md)
