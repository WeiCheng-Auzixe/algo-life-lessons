# 訊號與足跡：系統從哪裡知道你喜歡什麼？

## 白話定義
你在 App 裡的每個動作都像在沙灘上留下**腳印**。推薦系統把這些腳印叫做「訊號」或「回饋」。

## 兩種回饋
- **明確回饋**：你直接告訴它，例如打星星、按讚 [S1](../sources/s1-google-recsys.md)。
- **隱含回饋**：你沒說，但系統從行為推測，例如你把一部電影看完 [S1](../sources/s1-google-recsys.md)。

## 各平台公開說會用的訊號
| 平台 | 會用的訊號 | 來源 |
|---|---|---|
| Netflix | 觀看紀錄、評分、口味相近的會員、片子類型與演員、時段、語言、裝置、看了多久 | [S3](../sources/s3-netflix.md) |
| TikTok | 按讚、分享、追蹤、留言、自己發的影片；影片的字幕、音樂、hashtag；語言、國家、裝置 | [S4](../sources/s4-tiktok.md) |
| Amazon | 你買過、評分過的商品；購物車裡的商品 | [S2](../sources/s2-amazon-item-to-item.md) |

## 強訊號 vs 弱訊號
不是每個腳印都一樣重。TikTok 說把一支較長影片看完是**強訊號**，跟創作者同一個國家只是**弱訊號** [S4](../sources/s4-tiktok.md)。Netflix 也說**近期**的行為比舊的行為重要 [S3](../sources/s3-netflix.md)。

## 平台說「不用」的
Netflix 表示年齡、性別這類人口資料不參與推薦決策 [S3](../sources/s3-netflix.md)。

## 跨出平台的足跡
平台外的足跡（你逛過的其他網站、用過的其他 App）要靠 [線上追蹤](online-tracking.md) 才連得起來 [S6](../sources/s6-ftc-tracking.md)。

## 相關
[推薦系統](recommender-system.md)、[隱私自保](privacy-self-defense.md)
