# 成果：教學簡報大綱（由 Query 產生、存回 Wiki）

- 問題：「你的手機為什麼知道你想買什麼？」要怎麼教給完全沒有技術背景的人？
- 產生方式：讀 [index](../index.md) → 讀相關概念頁 → 規劃每張投影片 → 通過 `plan_check.py` 檢查
- 投影片數：17（另加 1 張自動產生的資料來源頁）

| # | 標題 | 根據的 Wiki 頁面 | 來源 | 隱私 |
|---|---|---|---|---|
| 1 | 你的手機為什麼知道你想買什麼？ | [overview](../overview.md)、[glossary](../glossary.md) | [S3](../sources/s3-netflix.md) |  |
| 2 | 你有過這種經驗嗎？ | [phone-listening-myth](../concepts/phone-listening-myth.md) | [S5](../sources/s5-northeastern-listening.md) | 🔒 |
| 3 | 大學研究：測了 17,000 多個 App | [phone-listening-myth](../concepts/phone-listening-myth.md)、[s5-northeastern-listening](../sources/s5-northeastern-listening.md) | [S5](../sources/s5-northeastern-listening.md) | 🔒 |
| 4 | 答案：一位很懂你的「店員」 | [recommender-system](../concepts/recommender-system.md) | [S1](../sources/s1-google-recsys.md) [S2](../sources/s2-amazon-item-to-item.md) [S3](../sources/s3-netflix.md) [S4](../sources/s4-tiktok.md) |  |
| 5 | 每個動作都是一個「訊號」 | [signals-and-footprints](../concepts/signals-and-footprints.md) | [S1](../sources/s1-google-recsys.md) [S4](../sources/s4-tiktok.md) |  |
| 6 | 內容過濾：跟你喜歡的東西很像 | [content-based-filtering](../concepts/content-based-filtering.md) | [S1](../sources/s1-google-recsys.md) |  |
| 7 | 協同過濾：跟你很像的人也喜歡 | [collaborative-filtering](../concepts/collaborative-filtering.md) | [S1](../sources/s1-google-recsys.md) [S2](../sources/s2-amazon-item-to-item.md) |  |
| 8 | 像選秀節目：從幾十億挑出 10 個 | [three-stage-pipeline](../concepts/three-stage-pipeline.md) | [S1](../sources/s1-google-recsys.md) |  |
| 9 | 三個平台，各看什麼？ | [amazon](../entities/amazon.md)、[netflix](../entities/netflix.md)、[tiktok](../entities/tiktok.md) | [S2](../sources/s2-amazon-item-to-item.md) [S3](../sources/s3-netflix.md) [S4](../sources/s4-tiktok.md) |  |
| 10 | 冷啟動與同溫層 | [cold-start](../concepts/cold-start.md)、[filter-bubble](../concepts/filter-bubble.md) | [S1](../sources/s1-google-recsys.md) [S3](../sources/s3-netflix.md) [S4](../sources/s4-tiktok.md) |  |
| 11 | 廣告為什麼會「跟著你跑」？ | [online-tracking](../concepts/online-tracking.md) | [S6](../sources/s6-ftc-tracking.md) [S8](../sources/s8-android-ad-id.md) | 🔒 |
| 12 | 一個開關，關掉跨 App 追蹤 | [privacy-self-defense](../concepts/privacy-self-defense.md)、[s7-apple-att](../sources/s7-apple-att.md) | [S7](../sources/s7-apple-att.md) | 🔒 |
| 13 | 刪掉你的廣告 ID | [privacy-self-defense](../concepts/privacy-self-defense.md)、[s8-android-ad-id](../sources/s8-android-ad-id.md) | [S8](../sources/s8-android-ad-id.md) [S6](../sources/s6-ftc-tracking.md) | 🔒 |
| 14 | 兩個常見迷思 | [privacy-self-defense](../concepts/privacy-self-defense.md)、[s6-ftc-tracking](../sources/s6-ftc-tracking.md) | [S6](../sources/s6-ftc-tracking.md) | 🔒 |
| 15 | 你也可以反過來教演算法 | [privacy-self-defense](../concepts/privacy-self-defense.md) | [S4](../sources/s4-tiktok.md) [S3](../sources/s3-netflix.md) [S6](../sources/s6-ftc-tracking.md) | 🔒 |
| 16 | 考考你 | [phone-listening-myth](../concepts/phone-listening-myth.md)、[collaborative-filtering](../concepts/collaborative-filtering.md)、[privacy-self-defense](../concepts/privacy-self-defense.md) | [S5](../sources/s5-northeastern-listening.md) [S2](../sources/s2-amazon-item-to-item.md) [S6](../sources/s6-ftc-tracking.md) |  |
| 17 | 重點回顧 | [overview](../overview.md)、[privacy-self-defense](../concepts/privacy-self-defense.md) | [S5](../sources/s5-northeastern-listening.md) [S1](../sources/s1-google-recsys.md) [S7](../sources/s7-apple-att.md) [S8](../sources/s8-android-ad-id.md) |  |

## 故事線
迷思開場（手機偷聽？）→ 研究揭曉 → 推薦系統是什麼 → 兩種猜法 → 三階段 → 平台案例 → 副作用 → 線上追蹤 → 四步自保 → 小測驗 → 回顧

相關：[總覽](../overview.md)、[隱私自保](../concepts/privacy-self-defense.md)
