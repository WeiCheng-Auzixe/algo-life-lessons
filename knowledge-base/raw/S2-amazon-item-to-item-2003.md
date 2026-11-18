---
id: S2
title: "Amazon.com Recommendations: Item-to-Item Collaborative Filtering"
authors: Greg Linden, Brent Smith, Jeremy York
venue: IEEE Internet Computing, Vol. 7, No. 1, pp. 76–80（2003 年 1–2 月）
url: https://www.cs.umd.edu/~samir/498/Amazon-Recommendations.pdf
doi: 10.1109/MIC.2003.1167344
related: Smith & Linden, "Two Decades of Recommender Systems at Amazon.com", IEEE Internet Computing 2017（回顧文，提到 Amazon 於 1998 年上線以商品為基礎的協同過濾）
captured: 2026-11-18
---
# 擷取筆記（改寫，不是原文）
- 核心想法：不是去找「和你相似的顧客」，而是針對你買過或評分過的每一件商品，找「相似的商品」，再合併成推薦清單（商品配商品，而不是人配人）。
- 離線先算好「相似商品表」：顧客常一起買的商品；相似度用 cosine 計算。
- 線上步驟很快：只跟你買過／評過的商品數量有關，跟商品目錄大小、顧客總數無關，所以能即時推薦。
- 傳統（以使用者為基礎的）協同過濾規模一大就吃不消：文中說大約 1,000 萬名顧客、100 萬件商品時就不實際，除非抽樣或縮減資料，但會犧牲品質。
- 例子：網站會依顧客改變，軟體工程師看到程式設計書，新手媽媽看到嬰兒玩具。
- 購物車推薦：依購物車裡的東西推薦，像超市結帳台旁的衝動購買商品，但是為每個人量身挑選。
- 作者主張：精準推薦的點擊率與轉換率遠高於橫幅廣告、暢銷榜這類不分對象的內容（作者自述，文中未獨立驗證）。
