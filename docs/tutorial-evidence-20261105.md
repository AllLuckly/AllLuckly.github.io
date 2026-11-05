# 2026-11-05：五款应用各新增 10 篇教程

本次每日批次，新增 50 篇中文教程及 50 篇完整英文版。Aquarell、VectorPaint、漫阅+ 新增第 101–110 篇，书屿新增第 81–90 篇，云映新增第 61–70 篇。全站中文教程共 510 篇，Yearn 保持 20 篇。

## 公开版本与边界

2026 年 11 月 5 日重新核对 Apple 中国区公开版本；应用目录与本批新教程采用当日资料，旧文章保留历史版本说明。

| 应用 | 公开版本 | 最低系统 | 来源 |
| --- | --- | --- | --- |
| Aquarell | 1.0.7 | iOS / iPadOS 15.0 | [App Store](https://apps.apple.com/cn/app/id1591340577)、[Apple Lookup](https://itunes.apple.com/lookup?id=1591340577&country=cn) |
| VectorPaint | 1.0.8 | iOS / iPadOS 17.0 | [App Store](https://apps.apple.com/cn/app/id1587272880)、[Apple Lookup](https://itunes.apple.com/lookup?id=1587272880&country=cn) |
| 漫阅+ | 2.0.4 | iOS / iPadOS 15.0 | [App Store](https://apps.apple.com/cn/app/id6753895889)、[Apple Lookup](https://itunes.apple.com/lookup?id=6753895889&country=cn) |
| 书屿 | 1.1.3 | iOS / iPadOS 15.6 | [App Store](https://apps.apple.com/cn/app/id6766198898)、[Apple Lookup](https://itunes.apple.com/lookup?id=6766198898&country=cn) |
| 云映 | 1.1.1 | iOS / iPadOS 15.0 | [App Store](https://apps.apple.com/cn/app/id6755653178)、[Apple Lookup](https://itunes.apple.com/lookup?id=6755653178&country=cn) |

- Aquarell：沙漏、折扇、邮票齿孔、卷曲铅笔屑、木桶、马蹄莲、长颈鹿、蕨叶、六角雪花与漂浮玩具的手绘构造。笔刷、颜色、图层和保存用于手工练习，不宣称颗粒模拟或自动建模。
- VectorPaint：双翅、台灯、伞面、杯腔和棋子剪影，条栅摩尔纹、自设双旗编码、阶梯双视图、虚构分区与六向花窗。结构、规则和对应关系由读者手工核对，不作为工程施工、真实通信或自动分析工具。
- 漫阅+：嵌入画格、持续时间、人物身份、运动符号与画面比例，纪实证据、教程步骤、虚构棋局、宣传文字与原创阅读反馈。阅读记录不冒充自动分析或识别。
- 书屿：概率事件、实验变量、对数图、叙述证据和菜谱文本，访谈、跨节参照、定义条件、表格符号与嵌套引文。采用阅读与人工清单，区分书内命题、读者推理和未验证结论。
- 云映：依据 1.1.1 公开更新加入 Kodi、OpenList / AList 与 S3 兼容存储教程；分别核对连接、目录、权限、媒体交付、对象键、临时凭据、访问方式、来源切换与跳转后字幕。已有凭据、视频和服务器由读者自己提供，未执行任何私人来源操作。

云映新来源边界同时只读对照本机项目 `lib/screens/add_media_server/kodi_config_form.dart`、`lib/services/kodi_service.dart`、`lib/screens/add_storage/openlist_storage_form.dart`、`lib/screens/add_storage/network_storage_forms.dart` 以及 OpenList/S3 适配器；未修改应用工程、账号或凭据。源码入口只用于核对字段与边界，公开能力仍以当日商店更新为基础，不把开发代码存在当作全部发行环境已验收。

可靠概念来源包括 [Kodi 控制设置](https://kodi.wiki/view/Settings/Services/Control)与 [JSON-RPC 说明](https://kodi.wiki/view/JSON-RPC_API)、[OpenList API 入口](https://docs.oplist.org/guide/api/)及[存储通用配置](https://docs.oplist.org/guide/drivers/common)、AWS [对象前缀](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html)、[对象键名](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html)、[访问方式](https://docs.aws.amazon.com/AmazonS3/latest/userguide/VirtualHosting.html)与[临时凭据](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)，以及 [W3C WebVTT](https://www.w3.org/TR/webvtt1/)。教程中的域名、单位、事件与媒体均为明确教学样本，不包含真实私人配置。

## 新增清单

汉字数量不含 frontmatter，含资料说明；长度只用于发现缺稿，不能替代内容、逻辑与完整英文复核。

| 应用 | 序号 | 教程 | 正文汉字 |
| --- | ---: | --- | ---: |
| Aquarell | 101 | [用 Aquarell 画沙漏：让沙流、余量与堆积表示同一瞬间](/guides/aquarell-hourglass-sand-transfer/) | 1768 |
| Aquarell | 102 | [用 Aquarell 画折扇：让山折、谷折与扇骨汇到同一枢轴](/guides/aquarell-folding-fan-pleat-pivot/) | 1788 |
| Aquarell | 103 | [用 Aquarell 画邮票边框：让齿孔沿四边与转角连续](/guides/aquarell-postage-stamp-perforation-corners/) | 1845 |
| Aquarell | 104 | [用 Aquarell 画卷曲铅笔屑：让薄带、木纹与彩边连续转向](/guides/aquarell-pencil-shaving-curled-ribbon/) | 1844 |
| Aquarell | 105 | [用 Aquarell 画木桶：让桶板收束、桶箍和桶口共享体积](/guides/aquarell-barrel-staves-hoop-wrap/) | 1768 |
| Aquarell | 106 | [用 Aquarell 画马蹄莲：让卷合花面围出清楚开口](/guides/aquarell-calla-spathe-curled-opening/) | 1633 |
| Aquarell | 107 | [用 Aquarell 画长颈鹿：让斑块绕着颈部转面](/guides/aquarell-giraffe-neck-patch-wrap/) | 1647 |
| Aquarell | 108 | [用 Aquarell 画蕨叶：让主轴、羽片与小叶形成层级](/guides/aquarell-fern-frond-branch-hierarchy/) | 1650 |
| Aquarell | 109 | [用 Aquarell 画六角雪花：让六条主臂使用同一分枝规则](/guides/aquarell-snowflake-six-arm-branch-rule/) | 1632 |
| Aquarell | 110 | [用 Aquarell 画漂浮橡皮鸭：让水线说明露出与浸没](/guides/aquarell-floating-rubber-duck-waterline/) | 1625 |
| VectorPaint | 101 | [VectorPaint 蝴蝶双翅：从镜像骨架到有意保留的差异](/guides/vectorpaint-butterfly-wing-baseline/) | 1608 |
| VectorPaint | 102 | [VectorPaint 关节台灯：让支臂围绕铰点并接到灯罩](/guides/vectorpaint-articulated-desk-lamp/) | 1563 |
| VectorPaint | 103 | [VectorPaint 打开雨伞：让伞骨、分片和伞柄共享顶点](/guides/vectorpaint-umbrella-panel-ribs/) | 1581 |
| VectorPaint | 104 | [VectorPaint 杯子剖示：区分杯壁、内腔与把手空隙](/guides/vectorpaint-cup-cutaway-cavity/) | 1598 |
| VectorPaint | 105 | [VectorPaint 马头棋子剪影：用轮廓转折保留额鼻与颈部负形](/guides/vectorpaint-horse-knight-silhouette/) | 1586 |
| VectorPaint | 106 | [VectorPaint 两层条栅：用静态叠层观察摩尔纹与输出差异](/guides/vectorpaint-moire-line-overlays/) | 1636 |
| VectorPaint | 107 | [VectorPaint 自设双旗编码卡：用行列核对十六种组合](/guides/vectorpaint-invented-two-flag-code/) | 1605 |
| VectorPaint | 108 | [VectorPaint 三级阶梯双视图：让俯视踏面对应侧视高度](/guides/vectorpaint-three-step-two-view/) | 1583 |
| VectorPaint | 109 | [VectorPaint 虚构分区着色：按共边关系检查相邻颜色](/guides/vectorpaint-fictional-region-colouring/) | 1581 |
| VectorPaint | 110 | [VectorPaint 六重花窗：围绕共同中心核对旋转对称](/guides/vectorpaint-sixfold-window-rosette/) | 1663 |
| 漫阅+ | 101 | [漫阅+ 画中画阅读：核对嵌入小格的范围与视点](/guides/manyue-inset-panel-viewpoint-boundaries/) | 1623 |
| 漫阅+ | 102 | [漫阅+ 场景时长阅读：把画格数量与故事经过时间分开](/guides/manyue-scene-duration-evidence/) | 1623 |
| 漫阅+ | 103 | [漫阅+ 人物身份核对：面对乔装与画风变化保留证据](/guides/manyue-character-identity-disguise-check/) | 1627 |
| 漫阅+ | 104 | [漫阅+ 动态符号阅读：分开运动线、箭头与物件路径](/guides/manyue-motion-symbol-path-reading/) | 1606 |
| 漫阅+ | 105 | [漫阅+ 画面比例回查：用参照条件区分大小与远近](/guides/manyue-visual-scale-reference-check/) | 1599 |
| 漫阅+ | 106 | [漫阅+ 纪实漫画阅读：分开档案引文、画面重构与推测](/guides/manyue-documentary-comic-source-layers/) | 1673 |
| 漫阅+ | 107 | [漫阅+ 教程漫画跟读：逐格核对步骤状态与遗漏条件](/guides/manyue-instruction-comic-state-audit/) | 1604 |
| 漫阅+ | 108 | [漫阅+ 漫画内棋局回查：按已知规则核对前后局面](/guides/manyue-fictional-board-position-evidence/) | 1570 |
| 漫阅+ | 109 | [漫阅+ 封面与正文对读：分开宣传信息、想象构图与剧情事实](/guides/manyue-cover-promotion-story-boundary/) | 1614 |
| 漫阅+ | 110 | [漫阅+ 原创稿评阅：交付能返回原页的一项问题说明](/guides/manyue-original-comic-review-packet/) | 1646 |
| 书屿 | 81 | [书屿概率例题阅读：用四种结果分清互斥与独立](/guides/nasbook-probability-exclusive-independent-grid/) | 1686 |
| 书屿 | 82 | [书屿实验描述阅读：把操纵变量、测量结果与未控条件分开](/guides/nasbook-experiment-factor-response-reading/) | 1877 |
| 书屿 | 83 | [书屿对数坐标图阅读：把等距离读成倍数而非等差](/guides/nasbook-log-axis-ratio-reading/) | 1766 |
| 书屿 | 84 | [书屿叙述者线索笔记：把自述、事件与个人猜测分开](/guides/nasbook-unreliable-narrator-clues/) | 1709 |
| 书屿 | 85 | [书屿菜谱文字核对：把份数、材料清单与步骤用量对应](/guides/nasbook-cookbook-text-crosscheck/) | 1690 |
| 书屿 | 86 | [书屿访谈集细读：分清提问前提、回答范围与编者连接](/guides/nasbook-interview-question-answer-scope/) | 1679 |
| 书屿 | 87 | [书屿 EPUB 交叉参照检查：把参见文字与实际目标对应](/guides/nasbook-epub-cross-reference-target-check/) | 1667 |
| 书屿 | 88 | [书屿定义精读：分清必要条件、充分条件与反例](/guides/nasbook-definition-necessary-sufficient-boundary/) | 1650 |
| 书屿 | 89 | [书屿数据表阅读：分开零值、空白、横线与未说明](/guides/nasbook-table-zero-blank-symbols/) | 1609 |
| 书屿 | 90 | [书屿套层引语阅读：把原作者、转述者与被引人分开](/guides/nasbook-nested-quotation-attribution-chain/) | 1633 |
| 云映 | 61 | [云映连接 Kodi：用受信任网络核对 HTTP 服务与媒体库](/guides/icouldplay-kodi-http-library-setup/) | 1743 |
| 云映 | 62 | [云映 Kodi 列表可见却不能播放：区分资料目录与真实媒体路径](/guides/icouldplay-kodi-library-playback-path/) | 1772 |
| 云映 | 63 | [云映接入 OpenList 或 AList：分清站点地址与起始目录](/guides/icouldplay-openlist-source-setup/) | 1778 |
| 云映 | 64 | [云映 OpenList 权限核对：分开账号、目录密码与媒体链接](/guides/icouldplay-openlist-directory-access-layers/) | 1766 |
| 云映 | 65 | [云映连接 S3 兼容存储：分开端点、桶、区域与凭据](/guides/icouldplay-s3-compatible-source-setup/) | 1785 |
| 云映 | 66 | [云映 S3 对象前缀核对：别把目录外观当成真实键名](/guides/icouldplay-s3-object-prefix-identity/) | 1661 |
| 云映 | 67 | [云映 S3 临时凭据核对：让密钥、会话令牌与有效期对应](/guides/icouldplay-s3-temporary-session-expiry/) | 1777 |
| 云映 | 68 | [云映 S3 访问方式对照：核对桶在路径还是主机名中](/guides/icouldplay-s3-path-style-endpoint-check/) | 1700 |
| 云映 | 69 | [云映来源切换核对：让文件身份、观看位置与字幕状态对应](/guides/icouldplay-source-switch-playback-state/) | 1763 |
| 云映 | 70 | [云映跳转后字幕核对：比较顺播、向前定位与向后回看](/guides/icouldplay-seek-caption-reentry-check/) | 1773 |

## 维护与验证

英文按正文段落保留操作、例子、条件、检查与排查，绑定中文源文件 SHA-256；学习阶段、应用目录、计数、语言路由、搜索、Markdown、阅读目录与技能摘要同步维护。具体构建及检查结果见[验证记录](verification.md)。本次网站验证不代表 50 篇应用任务逐项真机或私人服务器实测；部署状态需在推送后单独确认，发布也不等同于搜索收录或引用保证。
