# 产品内容证据与维护记录

核对日期：2026-10-22（Asia/Shanghai）。本记录为站点编辑维护资料，未包含凭据、私人漫画内容或用户作品。

## 线上事实

通过 Python `urllib.request` 直接读取 Apple 公共 iTunes Lookup JSON。三个接口均返回一条相应应用记录；本次版本、名称与系统要求采用实时公共查询结果。

| 项目 | 中国区商店名称 | App Store ID | 当前版本 | 最低系统 | 当前版本发布时间（Apple 原始 UTC） |
| --- | --- | --- | --- | --- | --- |
| pastel | Aquarell 水彩绘画与手绘画板 | 1591340577 | 1.0.5 | 15.0 | 2026-10-10T14:24:44Z |
| man_yue | 漫阅+ 漫画阅读器 | 6753895889 | 2.0.2 | 15.0 | 2026-10-19T15:22:11Z |
| draw_illustration | VectorPaint-矢量绘图与Logo设计 | 1587272880 | 1.0.7 | 17.0 | 2026-10-20T01:10:33Z |

公开查询地址：

- [Aquarell Lookup](https://itunes.apple.com/lookup?id=1591340577&country=cn)
- [ManYue Lookup](https://itunes.apple.com/lookup?id=6753895889&country=cn)
- [VectorPaint Lookup](https://itunes.apple.com/lookup?id=1587272880&country=cn)

三者 `sellerName` 均为 `Anyi County Bingzhiyi Trading Co., Ltd.`。不将博客作者的个人身份替代商店销售方，也不在结构化数据中捏造评分、评论、获奖或免费价格。

公开下载链接采用 `/cn/app/id{ID}`。Apple 查询返回的 `trackViewUrl` 带中文名称 slug，但稳定 ID 与上述链接一致。Aquarell 与 VectorPaint 的 `sellerUrl` 为空；ManYue 返回 `http://www.bzy168.top`。本地 ManYue `docs/discovery/site/deployment.json` 中 `published:false`、`base_url:null`，因此不能把该本地站点宣称为已经上线的官网。博客本次新建的产品页使用当前博客域名与自身路径。

## 内容与操作入口证据

以下路径用于本地维护核对，不代表这些私有源代码已经公开。三篇教程说明其根据公开版本说明与项目入口整理，不声称真机实测。项目当前源码可能先于线上版本，界面名称和位置存在变化；导入预览等可选页面使用条件描述。

### Aquarell

- 正式名称与公开能力：`pastel/appstore/metadata/zh-Hans/name.txt`、`description.txt`。
- 创建画布、宽高、DPI、透明背景和创建按钮：`pastel/Classes/SwiftUICanvasPresetView.swift`，关键行 36、58、76、116、129。
- 图层与本地化名称：`pastel/zh-Hans.lproj/Localizable.strings`，`Add Layer` 第 23 行、`Layers` 第 234 行、`Brush Studio` 第 420 行。
- 笔刷参数与真实桥接模型：`pastel/Classes/BrushStudioView.swift`、`BrushStudioBridge.swift`。
- 原生作品、PNG、JPEG、PSD 导出：`pastel/Classes/SwiftUIExportView.swift`，关键行 450–545。
- PSD 边界：同文件第 755 行明确 `PSD exports pixel layers. Editable text and layer groups stay editable only in the native artwork.`
- 核实产品主名为 Aquarell；开发项目名 pastel 仅作别名说明，避免与其他同名产品混淆。

### 漫阅

- 公开能力与限制：`man_yue/appstore/metadata/zh-Hans/description.txt`。
- 已核实 App Store ID：`man_yue/lib/foundation/membership/membership_constants.dart` 第 112 行。
- 主页导入：`man_yue/lib/pages/home_page.dart` 第 538 行。
- 选择文件、文件夹、加入书架与文件选择器：`man_yue/lib/pages/import_comics_dialog.dart` 第 58–112、204 行。
- 导入预览、确认导入与查看书架：`man_yue/lib/pages/comic_import_session_page.dart` 第 293、393、460 行。
- 中文按钮文案：`man_yue/assets/translations/zh_CN.json`，键 `Import local comics`、`Select file`、`Add to bookshelf`、`Import preview`、`Confirm import`、`View bookshelf`。
- 源文件导入：`man_yue/lib/pages/comic_source_page.dart` 第 609–683 行。
- NAS 入口：`man_yue/lib/pages/nas_library_page.dart`、`webdav_page.dart`、`smb_page.dart`。
- 不把 README 中上游 Venera 的跨平台功能全部视为漫阅 App Store 能力；以实时商店描述为内容边界。
- 明确文件与来源由用户提供；区分本地离线、远程目录、阅读状态同步与漫画文件同步；不承诺任意加密压缩包支持。
- 明确 Pro / Ultra 功能边界，但不在站点中固化价格。普通整包 OPDS 与 OPDS-PSE 的逐页阅读不同。

### VectorPaint

- 公开能力与限制：`draw_illustration/appstore/metadata/zh-Hans/description.txt`。
- 新建画布、尺寸单位、创建按钮：`draw_illustration/DrawIllustration/Modern/StudioCanvasSetup.swift` 第 51、80、104、120 行。
- 工具、填充、描边与导出：`draw_illustration/DrawIllustration/Modern/StudioEditor.swift` 第 103–128 行（格式）、1181 行（导出与分享）、1202 行（形状与路径）、2606–2623 行（描边与填充）、4526 行（透明背景）。
- 导出模型通过 `IllustrationBridge.m` 的真实引擎快照处理，不只是 UI 占位能力。
- 公开说明明确 SVG / PDF 可能包含位图；矢量化与直接导出不同。照片描摹效果受原图与颜色量化影响，不使用「无损一键转矢量」表述。

## 图标来源与图片使用

仅复制以下三个项目品牌图标，已目视检查。未使用私人书库、漫画页、用户原作或生成的伪操作截图：

| 站点资源 | 本地来源 |
| --- | --- |
| `/assets/images/apps/pastel.png` | `pastel/Pastel/Images.xcassets/AppIcon.appiconset/AppStoreIcon.png` |
| `/assets/images/apps/man_yue.png` | `man_yue/ios/Runner/Assets.xcassets/AppIcon.appiconset/AppIcon (1).png` |
| `/assets/images/apps/draw_illustration.png` | `draw_illustration/DrawIllustration/Assets.xcassets/AppIcon.appiconset/AppStoreIcon.png` |

已有 App Store 截图部分属于旧界面且包含绘画内容，未据此推定原作授权，也未将它们当作本次教程的实测截图。后续展示作品时应记录作者、授权、应用版本与创作过程，再配对应正文和图片说明。

## 后续更新

新版本发布后复查 Apple Lookup 与三个产品页中的版本日期；若涉及入口变化，应更新教程。实机演示应记录真实操作版本和设备，再明确标注为实测。新增教程围绕可复现的具体任务，不将已列出的能力扩张为尚未核实的兼容性、性能或推荐保证。
