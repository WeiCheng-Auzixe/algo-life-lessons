# 三階段流程：從幾十億個挑出 10 個

## 白話比喻：選秀節目
1. **海選**（候選生成）：從幾十億報名者裡，很快挑出幾百到幾千人。YouTube 的候選生成就是把數十億支影片縮小到數百到數千支 [S1](../sources/s1-google-recsys.md)。
2. **評審打分**（打分數）：人少了，評審可以仔細看，用更精細的模型排序，選出大約 10 個給你看 [S1](../sources/s1-google-recsys.md)。
3. **節目製作人最後調整**（重新排序）：拿掉你說過不喜歡的、讓新內容多一點機會、照顧多樣性與公平性 [S1](../sources/s1-google-recsys.md)。

## 實際例子
- TikTok 的「最後調整」：不連續推同一個創作者或同一段音樂、排除看過與重複的內容 [S4](../sources/s4-tiktok.md)。
- Netflix 把最推薦的放在每一列的最左邊、首頁最上面 [S3](../sources/s3-netflix.md)。

## 相關
[推薦系統](recommender-system.md)、[同溫層](filter-bubble.md)
