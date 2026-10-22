# Aquarell 教程事实与源码证据

资料核对日期：2026-10-22（Asia/Shanghai）。本次只读检查 `pastel` 应用项目，未修改应用工程、商店资料或任何凭据。已阅读 `AGENTS.md`、`agent.md`、`appstore/AGENTS.md` 与 `appstore/AI_CONSTRAINTS.md`。商店写入与上传规则不适用于本次博客内容编写，本次没有运行发布脚本。

## 公开版本依据

Apple 公共查询 `https://itunes.apple.com/lookup?id=1591340577&country=cn` 返回一条记录：

- trackName：Aquarell 水彩绘画与手绘画板
- trackId：1591340577
- version：1.0.5
- minimumOsVersion：15.0
- currentVersionReleaseDate：2026-10-10T14:24:44Z
- sellerName：Anyi County Bingzhiyi Trading Co., Ltd.

本次重新通过 Python `urllib.request` 读取公开 JSON，返回描述与本地 `appstore/metadata/zh-Hans/description.txt` 一致。公开入口：[商店页面](https://apps.apple.com/cn/app/id1591340577)、[版本查询](https://itunes.apple.com/lookup?id=1591340577&country=cn)。公共商店网页的文本抓取不稳定，采用 Apple 公共接口核对，未使用任何私有 API 凭据。

`description.txt` 关键行：第 4 行自定义笔刷大小/不透明度/间距；第 7 行图层、不透明度、混合模式、选区与蒙版；第 10 行颜色、色板、取色、画布、文字与字体；第 13 行 PNG/JPEG/PDF/TIFF、像素图层 PSD 与原生作品。仅把这些公开能力作为已发布版本基础。当前源代码可能包含后续开发内容，不能仅凭源码存在就认定已经在 1.0.5 上架。

## 源码定位索引

路径均相对于 `pastel` 应用项目，行号为本次只读查看时的位置。

| 编号 | 文件与相关行 | 支持核对的内容 |
| --- | --- | --- |
| C1 | `Classes/SwiftUICanvasPresetView.swift:36`、`:58`、`:76`、`:116`、`:129` | 新建、宽高、分辨率、透明背景、创建；分辨率与色彩高级选项没有作为所有版本前提 |
| B1 | `Classes/BrushStudioView.swift:143`、`:144`、`:145` | 笔刷大小、不透明度、间距及单位；不使用同文件更高级动力学能力作为教程前提 |
| L1 | `Classes/LayerPanelBridge.swift:175`、`:180`、`:476`、`:575`、`:649` | 图层不透明度、可见性、新增图层及真实引擎 setter |
| P1 | `Classes/SwiftUIColorPickerView.swift:22`；`Classes/ColorCompanionView.swift:488`；`Classes/ColorCompanionBridge.swift:18` | 颜色与色板模型/界面；只对公开的色板保存能力作稳定介绍 |
| P2 | `Classes/BZYCanvas.m:968`、`:989`、`:1009` | 画布取色、长按入口、合成采样与颜色 alpha；正文提醒边缘/叠色影响采样 |
| T1 | `Classes/SwiftUITextToolView.swift:48`、`:60`、`:328`、`:345` | 字体导入与有效性检查、文字颜色及应用入口；文中不承诺所有字体支持中文 |
| E1 | `Classes/SwiftUIExportView.swift:450`、`:467`、`:475`、`:503`、`:511`、`:532`、`:755`、`:859` | 原生/PNG/JPEG/PSD、可选尺寸/质量与 PSD 边界；第 755 行明确可编辑文字和图层分组留在原生作品 |
| N1 | `Classes/BZYPaintingManager.m:32`、`:383`、`:427`；`Classes/BZYBrowserController.m:1490` | 原生文件扩展名和作品导入入口；教程不要求手动改名扩展名 |
| S1 | `Classes/CanvasMenuBridge.swift:1756`；`Classes/CanvasChromeView.swift:200`、`:206` | 绘制选区与完成/取消交互；不把同文件的保存选区等新能力自动认定已发布 |
| M1 | `Classes/LayerGroupListView.swift:791`；`Classes/LayerPanelBridge.swift:159`、`:167` | 添加/移除蒙版与当前蒙版状态；正文使用测试副本和实际入口条件 |

## 逐篇核对

“中文字符”统计正文中的 Unicode 中文字符，排除 front matter，不以链接长度或符号充数。每篇至少五个二级标题、两个常见问题和两条相关教程链接。练习数值是编辑建议，未写成设备上限、官方预设或实测结果。

| 顺序 | 路径 | 中文字符 | 源码 | 公开能力支持 | 限制与核对结论 |
| --- | --- | ---: | --- | --- | --- |
| 1 | `/guides/aquarell-getting-started/` | 1635 | C1、L1、E1 | 公开说明第 4、7、10、13 行：画布、画笔、图层与导出。 | 入门路径按公开能力组织；界面随版本变化，未进行实机操作验收。 |
| 2 | `/guides/aquarell-canvas-size-dpi/` | 1684 | C1 | 第 10 行：自定义画布尺寸。 | DPI 字段以实际界面为条件；像素与打印尺寸换算为通用数学，不声称新建界面选项已经在所有安装版本提供。 |
| 3 | `/guides/aquarell-brush-size-opacity/` | 1667 | B1、L1 | 第 4 行：大小与不透明度。 | 8/24/64 px 和 25/50/100% 是练习参数；不承诺硬件压感或固定笔刷名称。 |
| 4 | `/guides/aquarell-brush-spacing/` | 1632 | B1 | 第 4 行：间距调整。 | 源码中间距为倍数；正文仅在界面使用倍数时建议 0.05/0.3/1.0，否则按滑块比较。 |
| 5 | `/guides/aquarell-three-layer-workflow/` | 1683 | L1、E1 | 第 7 行：图层组织与不透明度。 | 图层命名按实际版本可见入口；无新增分组、批量图层等高级能力承诺。 |
| 6 | `/guides/aquarell-layer-opacity/` | 1689 | L1、B1 | 第 7 行：不透明度与混合模式。 | 只用不透明度进行教程；不固定推荐混合模式，不承诺颜色一致。 |
| 7 | `/guides/aquarell-limited-palette/` | 1664 | P1、C1 | 第 10 行：选择颜色、保存色板。 | 色值输入、色板命名按实际界面条件处理；不要求自动配色或照片色板。 |
| 8 | `/guides/aquarell-canvas-color-picking/` | 1672 | P2、B1、L1 | 第 10 行：从画布取色。 | 源码取色使用画布合成结果并保留当前颜色 alpha；明确边缘/透明叠色采样不等于恢复原始颜色。 |
| 9 | `/guides/aquarell-paint-leaf/` | 1620 | C1、B1、L1、E1 | 第 1、4、7、10、13 行：插画、笔刷、分层、颜色与输出。 | 叶子步骤是原创练习方案；不宣称已有完成稿，不承诺真实水彩物理模拟。 |
| 10 | `/guides/aquarell-paint-flower/` | 1615 | C1、B1、L1、P1 | 第 1、4、7、10 行：插画与基础创作。 | 花朵造型/配色为绘画建议；未使用外部作品或生成伪示范图。 |
| 11 | `/guides/aquarell-paint-cup/` | 1616 | C1、B1、L1、P1 | 第 1、4、7、10 行：插画与基础创作。 | 椭圆与光照为手绘方法，不要求自动形状或材质识别功能。 |
| 12 | `/guides/aquarell-paint-landscape/` | 1661 | C1、L1、E1 | 第 1、7、10、13 行：风景、图层、颜色与导出。 | 远近配色是入门构图选择，不声明自动渐变、滤镜或物理大气效果。 |
| 13 | `/guides/aquarell-illustrated-card/` | 1694 | T1、L1、E1 | 第 10 行：文字与字体导入；第 13 行：原生作品/PSD。 | 字体是否覆盖中文字形需检查，字体许可独立判断；可编辑文字以原生文件为准。 |
| 14 | `/guides/aquarell-icon-series/` | 1639 | C1、B1、L1、E1 | 第 1、4、7、10、13 行：绘画、颜色与图片输出。 | 系列规则为人工创作方法；不宣称专用图标排版或矢量导出。 |
| 15 | `/guides/aquarell-transparent-png/` | 1640 | C1、E1 | 第 13 行：PNG 导出；应用公开关键词包含透明背景。 | 透明画布和像素内容分别检查；PNG 不会自动抠白，发布平台二次转换另行核对。 |
| 16 | `/guides/aquarell-jpeg-for-blog/` | 1621 | E1 | 第 13 行：JPEG 输出。 | 图片尺寸与 JPEG 质量控件仅在当前界面提供时使用；无固定压缩率、体积或性能保证。 |
| 17 | `/guides/aquarell-psd-handoff/` | 1614 | E1、T1、L1 | 第 13 行明确 PSD 为像素图层。 | 原生文字/分组不承诺跨软件编辑；没有运行 Photoshop 兼容测试，正文提供检查清单。 |
| 18 | `/guides/aquarell-native-artwork-backup/` | 1698 | E1、N1 | 第 13 行：原生作品用于继续创作。 | 文件留档是手动流程，不声称自动云同步或跨版本无条件兼容。 |
| 19 | `/guides/aquarell-export-blur-check/` | 1691 | C1、E1、B1 | 第 4、10、13 行：画笔、画布尺寸与导出。 | 模糊排查使用像素/显示/压缩一般原理，无超分辨率、锐化或自动修复能力承诺。 |
| 20 | `/guides/aquarell-selection-local-color/` | 1651 | S1、M1、L1 | 第 7 行明确选区与蒙版。 | 基本选区与蒙版按公开能力写；形状、羽化、完成/取消、添加蒙版等按当前可见入口条件描述；不纳入高级来源选区、智能抠图、蒙版复制等未核实发布功能。 |

## 真实性与素材边界

十九篇新增教程及补充入门均为文字操作与原创练习方案，没有生成或引用伪操作截图，没有读取或使用用户原画、私人漫画、账号信息。叶子、花朵、杯子、山景、卡片和图标是读者可执行的创作任务，不把它们包装为已经在应用中完成的作品案例。

教程主体尽量直接表达任务、数值示例、检查与排查；未把源码文件名或内部实现写进产品步骤。没有执行真机或模拟器绘画测试，公开能力核对与源码入口核对不能代替安装版本逐步实测。DPI 字段、色值输入、色板命名、JPEG 质量/尺寸、选区细化等可能随版本变化的控件均使用条件说明。

## 自查方式与未覆盖项

使用 PyYAML 解析所有 front matter，核对 `app_id: pastel`、日期/时区、唯一 permalink、`series_order` 1–20、topic 与 reading_time。扫描正文 Liquid 相对链接，对照仓库页面与文章 permalink；检查中文字符数、标题数、FAQ 数与空白。构建和完整站点检查由主任务统一运行，避免与其他应用教程并行写入冲突。

没有验证具体打印材料、字体授权、第三方图像查看器、云盘同步成功、Photoshop 跨软件合成一致性或真实输入设备性能。对应内容写作采用可执行检查步骤与明确功能边界，不预先宣称检查已经通过。

本次静态自查结果：20 篇，序号连续 1–20，permalink 唯一，日期与时区一致，全部 front matter 可解析；正文中文字符总计 33,086，单篇 1,614–1,698（含已有入门补充）。所有正文内部链接可映射到现有页面/文章 permalink，二级标题与 FAQ 数量满足要求。`git diff --check` 通过。未提交、未推送。
