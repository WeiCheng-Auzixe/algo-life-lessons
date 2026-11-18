# 協同過濾（Collaborative Filtering）

## 白話比喻
「和你口味很像的同學都愛這家店，那你應該也會喜歡。」——看的是**人和人、東西和東西之間的關係**，不用知道東西本身是什麼。

## 怎麼運作
- 把「誰對什麼有興趣」排成一張大表格：每一列是一個人，每一欄是一個東西 [S1](../sources/s1-google-recsys.md)。
- 系統自動學出每個人、每個東西在「口味地圖」上的位置；口味相近的人會靠在一起，被同一群人喜歡的東西也會靠在一起 [S1](../sources/s1-google-recsys.md)。這個位置叫做 embedding（嵌入向量）。

## Amazon 的版本：「買了這個的人也買了⋯」
- Amazon 不去找和你相似的顧客，而是找**和你買過的商品相似的商品**，叫做 item-to-item 協同過濾 [S2](../sources/s2-amazon-item-to-item.md)。
- 「相似商品表」事先離線算好，所以你一上網就能即時給推薦 [S2](../sources/s2-amazon-item-to-item.md)。
- 原因：傳統「找相似顧客」的做法，在約 1,000 萬名顧客、100 萬件商品的規模就不實際了 [S2](../sources/s2-amazon-item-to-item.md)。

## 優點
- 會有**驚喜**：可以推薦你從沒接觸過、但相似的人喜歡的東西 [S1](../sources/s1-google-recsys.md)。
- 不需要人工設計標籤 [S1](../sources/s1-google-recsys.md)。

## 缺點
- [冷啟動](cold-start.md)：全新的東西還沒有人互動過，系統不知道把它放在地圖哪裡 [S1](../sources/s1-google-recsys.md)。

## 對照
[內容過濾](content-based-filtering.md)；實際平台通常混著用，例如 Netflix 同時看「相似會員」和「片子資訊」 [S3](../sources/s3-netflix.md)。
