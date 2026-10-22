# VectorPaint 教程证据记录

核对日期：2026-10-22。仅只读使用应用源码；没有改动应用项目或 App Store 资料。

## 公开事实与版本边界

- Apple 公共查询接口确认 VectorPaint 线上版本 1.0.7，最低系统 iOS 17.0，公开版本日期为 2026-10-20。
- 公开来源：[商店说明](https://apps.apple.com/cn/app/id1587272880)、[Apple 版本查询](https://itunes.apple.com/lookup?id=1587272880&country=cn)。
- 商店明确列出钢笔/手绘/形状/贝塞尔节点、对齐分布/网格辅助线、图层分组/填充描边渐变/路径文字/蒙版、图片矢量化、SVG/PDF/PNG/原稿输出及作品管理。
- 额外只读比对发布前的源文件 SHA256 记录：本次涉及的 12 个核心界面/桥接/矢量化/管理文件与 1.0.7 发布前快照相同。此项用于排除仅有当前开发实现的假定，不等同于每条教程经过设备实测。
- 不承诺照片无损矢量化、任意 SVG/PDF 完整兼容、每一步无限历史、固定自动备份周期、自动云同步、真实硬件笔性能或 AI 推荐结果。
- 所有尺寸、配色、文案及作品名称是练习设定，没有伪造 App 内截图或声称完成真实作品。

## 逐篇核实

源码位置均相对 draw_illustration 项目根目录。Swift 与桥接文件位于 `DrawIllustration/Modern/`；引擎位于 `DrawIllustration/BZYInkpad-Core/`。

| 序号 | 教程路径 | 公开能力与实际入口 | 重要限制 |
| --- | --- | --- | --- |
| 1 | `/guides/vectorpaint-getting-started/` | `StudioCanvasSetup.swift` 创建画布；`StudioEditor.swift` 工具、填充、导出 | 区分矢量、位图与原稿；仅给练习步骤。 |
| 2 | `/guides/vectorpaint-canvas-units/` | `StudioCanvasSetup.swift:StudioCreateCanvasView`; `IllustrationBridge.h:canvasSize / canvasUnitSymbol / exportPNGWithPixelSize` | 文档单位、视图缩放与 PNG 像素分开；纸面尺寸不等于印刷认证。 |
| 3 | `/guides/vectorpaint-basic-shapes/` | `StudioEditor.swift:StudioTool.rectangle / ellipse / pen`; `IllustrationBridge.m:selectTool / duplicate commands` | 练习比例不是内置模板或已完成作品；图形仍需正确选择。 |
| 4 | `/guides/vectorpaint-fill-stroke/` | `StudioEditor.swift:fillMode / strokeEnabled / strokeWidth / strokeCap`; `IllustrationBridge.h:strokeWidth comment (pt)` | 描边宽度使用 pt；无填充不等于白色填充；混合属性需核对。 |
| 5 | `/guides/vectorpaint-pen-curves/` | `StudioEditor.swift:pen / anchor tools`; `BZYInkpad-Core/Tools/BZYPenTool.m；Model/WDPath.m；Model/WDBezierNode.m` | 不承诺自动/无损描摹；闭合顺序与控制柄需人工检查。 |
| 6 | `/guides/vectorpaint-bezier-nodes/` | `StudioEditingExtensions.swift:StudioNode panels`; `IllustrationBridge.m:nodes / update node setters` | 文字/图片不等同普通路径；转轮廓改变文字可编辑性。 |
| 7 | `/guides/vectorpaint-layers-groups/` | `StudioEditor.swift:StudioLayersView`; `IllustrationBridge.m:group / ungroup command map` | 分组不是栅格化；锁定/隐藏不同；交换格式层级需复核。 |
| 8 | `/guides/vectorpaint-align-distribute/` | `StudioEditor.swift:alignLeft / alignCenter / alignMiddle / distributeHorizontal`; `StudioEditingExtensions.swift:alignment controls` | 中心分布与边缘空隙不同，实际对齐范围以界面为准。 |
| 9 | `/guides/vectorpaint-grid-guides/` | `StudioEditor.swift:gridVisible / snapToGrid / dynamicGuides`; `StudioPrecisionWorkbench.swift:guide controls` | 网格显示与吸附不同；普通线段可能输出，辅助线不作为成品。 |
| 10 | `/guides/vectorpaint-text-layout/` | `StudioEditor.swift:text tool / fontSize / textAlignment`; `IllustrationBridge.h:setSelectedTextContent / setTextAlignment` | 不承诺嵌入字体；换字体后检查换行；转曲保留原稿。 |
| 11 | `/guides/vectorpaint-text-on-path/` | `IllustrationBridge.m:placeTextOnPath command`; `BZYInkpad-Core:WDTextPath / drawing controller text path methods` | 短标题练习；字体和路径文字跨软件需检查。 |
| 12 | `/guides/vectorpaint-gradients/` | `StudioEditor.swift:linear / radial / gradientStops`; `IllustrationBridge.h:gradientStartColor / gradientEndColor` | 不承诺真实光照；透明渐变受背景影响；复杂交换需验证。 |
| 13 | `/guides/vectorpaint-masks/` | `StudioEditor.swift:mask / unmask menu`; `IllustrationBridge.m:makeMask / releaseMask command mapping` | 蒙版不等于删除或矢量化；复杂嵌套没有全兼容保证。 |
| 14 | `/guides/vectorpaint-svg-import-edit/` | `StudioGallery.swift:import workflow`; `IllustrationBridge.m:SVG import / export`; `IllustrationImportDiagnostics.m:SVG diagnostics` | 支持格式不表示所有对象或扩展均可编辑；SVG可以含位图。 |
| 15 | `/guides/vectorpaint-image-vectorization/` | `StudioVectorizeWorkbench.swift:preview and confirmation`; `IllustrationVectorizeExtensions.m:threshold / quantization / generated paths` | 线稿/平涂适合入门；预览是无缩放入口的静态图片，只比较整体。保留原件，在练习副本勾选“确认时替换原图片”，确认后回画布放大检查；原图与生成路径同层，不能用隐藏整层单独排除原图。照片量化存在取舍，无损不作承诺。 |
| 16 | `/guides/vectorpaint-transparent-png/` | `StudioEditor.swift:StudioExportView / transparent / pngSize`; `IllustrationBridge.m:exportPNGWithPixelSize` | 透明设置不会删除背景对象，也不会自动抠图片白边。 |
| 17 | `/guides/vectorpaint-export-formats/` | `StudioEditor.swift:StudioExportFormat`; `IllustrationBridge.m:export format branches`; `StudioExportPresets.swift:PNG parameters` | SVG/PDF可以含位图；PNG不保留原稿编辑结构。 |
| 18 | `/guides/vectorpaint-monochrome-icon/` | `StudioEditor.swift:pen / shapes / fill / export`; `IllustrationBridge.m:geometry / export` | 练习不是品牌认证；小尺寸需实查，未伪造作品图。 |
| 19 | `/guides/vectorpaint-geometric-poster/` | `StudioEditor.swift:shapes / text / layers / export`; `StudioCanvasSetup.swift:custom canvas` | 示例文案非真实活动；横竖版要重新布局。 |
| 20 | `/guides/vectorpaint-save-backup/` | `StudioEditor.swift:editable native export`; `StudioLibraryExtensions.swift:library actions`; `IllustrationLibraryProtection.m:recovery / backup`; `StudioCreationProtection.swift:version implementation (not automatic promise)` | 主流程是原稿导出/导入复核；不承诺固定自动版本、无限历史或云同步。 |

## 技术概念参考

- [W3C SVG 2 路径](https://www.w3.org/TR/SVG2/paths.html)：锚点/曲线/闭合路径概念。
- [W3C SVG 2 填充与描边](https://www.w3.org/TR/SVG2/painting.html)：fill、stroke、端点和连接语义。
- [W3C SVG 2 文字](https://www.w3.org/TR/SVG2/text.html)：文本与路径文字是文档结构，不等同字体文件已随输出提供。
- [W3C PNG 规范](https://www.w3.org/TR/png/)：固定像素、透明度与栅格图像边界。

以上规范用于解释通用格式概念，不据此推断应用实现了规范中的全部功能。最终稿未引用私有账号、密钥、设备标识或发布认证信息。

## 关键实现定位

- `DrawIllustration/Modern/StudioCanvasSetup.swift:9`：默认尺寸；`:75`：px/pt/mm 选择与换算提示。
- `DrawIllustration/Modern/StudioEditor.swift:9`：基础工具枚举；`:102`：实际导出格式；`:2516`：描边；`:2610`：填充与渐变；`:1697`：对齐分布；`:1740`：吸附；`:1820`：网格。
- `DrawIllustration/Modern/StudioEditor.swift:1788`：路径文字命令；引擎 `DrawIllustration/BZYInkpad-Core/Controllers/BZYDrawingController.m:1673` 实际放置文字。
- `DrawIllustration/BZYInkpad-Core/Controllers/BZYDrawingController.m:1104`：实际创建蒙版。
- `DrawIllustration/Modern/StudioVectorizeWorkbench.swift:19`：颜色数量、阈值、处理尺寸、预览与确认；`IllustrationVectorizeExtensions.m:83`：生成路径实现。
- `DrawIllustration/Modern/IllustrationBridge.m:3843`：PNG 像素/背景参数；`:3971`：范围与格式导出；`:4475`：带单位创建文档。
- `DrawIllustration/Modern/IllustrationLibraryProtection.m:752`：保存恢复/备份记录；`:779`：恢复；`:953`：完整备份导出。教程以显式原稿副本和恢复检查为主，不把内部自动条件写成用户承诺。

## 本次内容验收

- 共 20 篇：原有入门扩写，新增 19 篇；`series_order` 连续 1–20。
- 正文按中文汉字计数均超过 1600，包含具体练习、完成检查与至少 3 个问答；各有 3 条同应用教程内链。
- Jekyll 3.10 完整构建通过；20 个页面均已生成，JSON-LD 能解析，生成的同应用教程链接均存在。
- 最后按引擎入口纠正路径文字的单路径分支，并补充矢量化阈值与处理像素的练习值；最终整站构建由主任务统一执行。

## 矢量化流程复核修正

- `StudioVectorizeWorkbench.swift` 的预览是限制高度的静态图片，没有放大交互；正文改为预览比较整体，确认后回画布检查细节。
- 保留原图片时，生成路径与图片位于同一图层；正文及延伸练习均改为先保留原件，只在练习副本勾选“确认时替换原图片”，不再要求隐藏原图所在图层。
- “验收标准”改为“判断标准”。本轮仅改矢量化教程与此证据记录，未重新构建，最终构建由主任务统一执行。
