# 內容過濾（Content-based Filtering）

## 白話比喻
「你喜歡這本**推理小說**，那這本也是推理小說，你應該也會喜歡。」——只看**東西本身長什麼樣**。

## 怎麼運作
- 給每個東西貼上特徵標籤（例如 App 的「教育」「休閒」「健康」、發行商），也把你的喜好放在同一組標籤上 [S1](../sources/s1-google-recsys.md)。
- 算你和每個東西有幾個標籤相同，相同越多分數越高。Google 課程的例題裡，教育類 App 得 2 分最高、健康類 1 分、休閒遊戲 0 分 [S1](../sources/s1-google-recsys.md)。

## 優點
- 不需要別人的資料，只看你自己 [S1](../sources/s1-google-recsys.md)。
- 能抓到很小眾的興趣 [S1](../sources/s1-google-recsys.md)。

## 缺點
- 標籤多半要人工設計，標籤不好推薦就不好 [S1](../sources/s1-google-recsys.md)。
- 幾乎只推「跟你已經喜歡的很像」的東西，很難拓展興趣 [S1](../sources/s1-google-recsys.md) → 與 [同溫層](filter-bubble.md) 有關。

## 對照
另一種猜法是 [協同過濾](collaborative-filtering.md)。
