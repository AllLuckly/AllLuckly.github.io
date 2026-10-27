# 2026-10-26：四款应用各新增 20 篇教程

本轮新增 80 篇中文详细教程，并维护 80 篇完整英文译文。原有文章与作品编号保留：Aquarell、VectorPaint、漫阅+ 分别新增第 41–60 篇，书屿新增第 21–40 篇。全站中文教程合计 260 篇。

## 来源核对

2026 年 10 月 26 日通过 Apple 中国区公开查询接口逐款获取当前说明；没有把开发工作区中存在某个入口等同于商店版完整提供该功能。

| 应用 | 公开版本 | 最低系统 | 公开资料 |
| --- | --- | --- | --- |
| Aquarell | 1.0.5 | iOS / iPadOS 15.0 | [App Store](https://apps.apple.com/cn/app/id1591340577)、[Apple Lookup](https://itunes.apple.com/lookup?id=1591340577&country=cn) |
| VectorPaint | 1.0.7 | iOS / iPadOS 17.0 | [App Store](https://apps.apple.com/cn/app/id1587272880)、[Apple Lookup](https://itunes.apple.com/lookup?id=1587272880&country=cn) |
| 漫阅+ | 2.0.3 | iOS / iPadOS 15.0 | [App Store](https://apps.apple.com/cn/app/id6753895889)、[Apple Lookup](https://itunes.apple.com/lookup?id=6753895889&country=cn) |
| 书屿 | 1.1.3 | iOS / iPadOS 15.6 | [App Store](https://apps.apple.com/cn/app/id6766198898)、[Apple Lookup](https://itunes.apple.com/lookup?id=6766198898&country=cn) |

漫阅+ 本轮公开版为 2.0.3，新增自动阅读暂停检查仅使用该版公开更新中可确认的行为。旧教程的 2.0.2 核对说明保留历史语境，应用介绍与目录版本更新至 2.0.3。

## 内容范围与实现边界

- Aquarell：自然形态、食物与材质、氛围景物和连续创作练习；用手工笔触、图层和现有导出流程完成，不引入未核实自动绘画工具。
- VectorPaint：信息版式、空间插画、曲线表现与文件维护；保留可编辑原稿，区分矢量路径、嵌入位图和显示图片。
- 漫阅+：自制样本、分卷与版本、跨页与小字、远端路径权限及多设备维护；跨来源身份与文件传输不承诺自动合并。
- 书屿：文件抽查、图文与小众格式、修订版和系列、笔记复盘、下载与迁移；MOBI、AZW、AZW3、CBR、DJVU 的管理范围不写成直接阅读。

源码复核使用对应本机项目中的笔刷/图层、矢量对象、阅读器、文件导入、服务器连接和同步入口。书屿重点参照 `Bookshelf/BZYImportPreviewController.swift`、`Bookshelf/BZYBookEntity.swift`、`Reader/BZYComicReaderController.swift`、`Notes/` 与 `Sync/`；未将工作区的 AI、OCR、超分或其他新功能写成公开版必备步骤。服务器权限与重扫补充参照 [Komga 用户说明](https://komga.org/docs/guides/user-accounts/)及[扫描与刷新说明](https://komga.org/docs/guides/scan-analysis-refresh/)。

阅读记录同步与原始书籍/漫画文件分别说明；可读笔记导出与完整恢复备份分别核对。涉及删除、重新导入、目录搬迁与换机的教程先保存原件与记录，再按实际界面确认影响范围。文中没有声明对全部教程进行了真机、私人服务器或每种文件的集成测试。

英文译文逐段对应中文，使用独立 collection、原文哈希与编辑版维护，后续自动渲染不会覆盖这些成稿。学习阶段、语言配对、目录、搜索和 Markdown 表示随正文一起更新。

## 新增清单

字数仅用于发现缺稿，不替代正文与功能审阅。统计不含 frontmatter，包含正文中的版本资料段。

| 应用 | 序号 | 教程 | 正文汉字 |
| --- | ---: | --- | ---: |
| Aquarell | 41 | [用 Aquarell 画松果：让鳞片沿着弧线转动](/guides/aquarell-pinecone-spirals/) | 1591 |
| Aquarell | 42 | [用 Aquarell 画仙人掌：先画棱面，再安排刺的节奏](/guides/aquarell-cactus-spines/) | 1625 |
| Aquarell | 43 | [用 Aquarell 画小鸟：把羽毛归成有方向的色块](/guides/aquarell-bird-feather-groups/) | 1628 |
| Aquarell | 44 | [用 Aquarell 画水中锦鲤：把鱼身、花斑与水面分开](/guides/aquarell-koi-underwater/) | 1616 |
| Aquarell | 45 | [用 Aquarell 画扇贝：让放射纹随着壳面起伏](/guides/aquarell-seashell-ridges/) | 1602 |
| Aquarell | 46 | [用 Aquarell 画草莓：让籽粒贴着果面转动](/guides/aquarell-strawberry-seeds/) | 1622 |
| Aquarell | 47 | [用 Aquarell 画柠檬切片：区分果皮、白瓤与透光果肉](/guides/aquarell-lemon-slice/) | 1620 |
| Aquarell | 48 | [用 Aquarell 画可颂：让层酥跟随卷起的体积](/guides/aquarell-croissant-folds/) | 1606 |
| Aquarell | 49 | [用 Aquarell 画金属壶：用宽窄亮带表达反射](/guides/aquarell-metal-kettle/) | 1642 |
| Aquarell | 50 | [用 Aquarell 画藤篮：让编织纹理服从篮体转折](/guides/aquarell-wicker-basket/) | 1647 |
| Aquarell | 51 | [用 Aquarell 画雾中松林：靠对比递减建立距离](/guides/aquarell-fog-pine-forest/) | 1641 |
| Aquarell | 52 | [用 Aquarell 画湖面倒影：保留对应关系，再打断细节](/guides/aquarell-lake-reflection/) | 1655 |
| Aquarell | 53 | [用 Aquarell 画雪中小屋：给白雪安排有颜色的暗面](/guides/aquarell-snow-cabin/) | 1649 |
| Aquarell | 54 | [用 Aquarell 画沙丘：用风脊和投影组织连绵曲面](/guides/aquarell-desert-dunes/) | 1618 |
| Aquarell | 55 | [用 Aquarell 画一角房间：用同一消失点组织室内透视](/guides/aquarell-interior-one-point/) | 1685 |
| Aquarell | 56 | [用 Aquarell 画旅行手账跨页：让主图、路线与文字留白协调](/guides/aquarell-travel-journal-spread/) | 1746 |
| Aquarell | 57 | [用 Aquarell 画图解食谱：让食材、动作和结果一一对应](/guides/aquarell-illustrated-recipe/) | 1729 |
| Aquarell | 58 | [用 Aquarell 画植物首字母：让枝叶衬托可读的字形](/guides/aquarell-botanical-initial/) | 1700 |
| Aquarell | 59 | [用 Aquarell 画四季同景：固定构图，只改变环境线索](/guides/aquarell-seasonal-scene-quartet/) | 1700 |
| Aquarell | 60 | [Aquarell 作品复盘：整理阶段预览，找到下一张的练习目标](/guides/aquarell-artwork-review-sheet/) | 1772 |
| VectorPaint | 41 | [VectorPaint 活动入场券：区分主联、副联与核验信息](/guides/vectorpaint-event-ticket/) | 1632 |
| VectorPaint | 42 | [VectorPaint 专题封面：用一套网格安排标题、导语与期号](/guides/vectorpaint-editorial-cover/) | 1610 |
| VectorPaint | 43 | [VectorPaint 咖啡菜单：让品名、说明与价格容易横向比较](/guides/vectorpaint-cafe-menu/) | 1639 |
| VectorPaint | 44 | [VectorPaint 方案对照表：用一致列宽展示三种选择](/guides/vectorpaint-comparison-sheet/) | 1579 |
| VectorPaint | 45 | [VectorPaint 判断流程图：让分支条件与箭头方向一致](/guides/vectorpaint-decision-flowchart/) | 1638 |
| VectorPaint | 46 | [VectorPaint 房间布置示意：用俯视形状检查家具与通道](/guides/vectorpaint-room-layout/) | 1599 |
| VectorPaint | 47 | [VectorPaint 拆解示意图：用对齐和引线说明三层结构](/guides/vectorpaint-exploded-diagram/) | 1569 |
| VectorPaint | 48 | [VectorPaint 配送车插画：用重复形状统一车轮与车窗](/guides/vectorpaint-flat-delivery-van/) | 1571 |
| VectorPaint | 49 | [VectorPaint 折叠飘带：用前后层叠表达转折](/guides/vectorpaint-folded-ribbon/) | 1560 |
| VectorPaint | 50 | [VectorPaint 钟面设计：手工校对刻度、数字和指针](/guides/vectorpaint-clock-face/) | 1580 |
| VectorPaint | 51 | [VectorPaint 鱼形剪影：用少量曲线区分身体、尾鳍和负形](/guides/vectorpaint-fish-silhouette/) | 1537 |
| VectorPaint | 52 | [VectorPaint 羽毛曲线：让主轴、外缘和细节沿同一方向生长](/guides/vectorpaint-feather-curves/) | 1557 |
| VectorPaint | 53 | [VectorPaint 帆船插画：用共用顶点连接桅杆、船帆与船体](/guides/vectorpaint-sailboat-scene/) | 1535 |
| VectorPaint | 54 | [VectorPaint 纸灯笼插画：用曲线、明暗和层叠表现鼓起的表面](/guides/vectorpaint-paper-lantern/) | 1551 |
| VectorPaint | 55 | [VectorPaint 自行车线稿：用圆心和三角关系检查车架](/guides/vectorpaint-bicycle-linework/) | 1574 |
| VectorPaint | 56 | [VectorPaint 小图标光学校正：分别检查十六、三十二与六十四像素](/guides/vectorpaint-optical-icon-sizes/) | 1674 |
| VectorPaint | 57 | [VectorPaint 图片框适配：用蒙版制作横版、方版与竖版](/guides/vectorpaint-photo-frame-variants/) | 1621 |
| VectorPaint | 58 | [VectorPaint SVG 兼容排查：用最小副本定位缺图、蒙版和渐变问题](/guides/vectorpaint-svg-compatibility-check/) | 1684 |
| VectorPaint | 59 | [VectorPaint 字体替换排查：保留可编辑文字并验证交付外观](/guides/vectorpaint-font-fallback-proof/) | 1714 |
| VectorPaint | 60 | [VectorPaint 作品库复盘：用分组、标签和收藏找回可继续编辑的版本](/guides/vectorpaint-library-project-review/) | 1716 |
| 漫阅+ | 41 | [漫阅+ 自制测试漫画：用六张编号页检查导入结果](/guides/manyue-sample-archive-check/) | 1591 |
| 漫阅+ | 42 | [漫阅+ 多卷漫画命名：把卷号、版本与番外分清楚](/guides/manyue-volume-filename-plan/) | 1631 |
| 漫阅+ | 43 | [漫阅+ 大图漫画排查：区分文件体积、图片尺寸与加载问题](/guides/manyue-large-image-diagnostics/) | 1649 |
| 漫阅+ | 44 | [漫阅+ 加密与分卷压缩包：导入前整理成可读副本](/guides/manyue-split-encrypted-archives/) | 1662 |
| 漫阅+ | 45 | [漫阅+ 同名不同版：比较黑白、彩色与修订漫画副本](/guides/manyue-edition-comparison/) | 1649 |
| 漫阅+ | 46 | [漫阅+ 双页封面配对：找出从哪一页开始成对显示](/guides/manyue-cover-spread-pairing/) | 1629 |
| 漫阅+ | 47 | [漫阅+ 混合横竖页漫画：让短篇集中的插页完整显示](/guides/manyue-mixed-page-anthology/) | 1660 |
| 漫阅+ | 48 | [漫阅+ 小字看不清：区分缩放比例、原图细节与显示处理](/guides/manyue-small-lettering-check/) | 1656 |
| 漫阅+ | 49 | [漫阅+ 重读专题笔记：用章节与画面锚点组织线索](/guides/manyue-rereading-anchor-notes/) | 1630 |
| 漫阅+ | 50 | [漫阅+ 自动阅读暂停检查：切换应用后从正确位置接着看](/guides/manyue-auto-reading-pause-check/) | 1668 |
| 漫阅+ | 51 | [漫阅+ NAS 目录搬迁：改路径前后核对书库与本地副本](/guides/manyue-nas-folder-relocation/) | 1634 |
| 漫阅+ | 52 | [漫阅+ 服务器权限核对：能登录、能看目录与能下载分别检查](/guides/manyue-server-permission-matrix/) | 1732 |
| 漫阅+ | 53 | [漫阅+ HTTPS 与代理子路径：浏览器能打开后还要检查什么](/guides/manyue-https-proxy-base-path/) | 1701 |
| 漫阅+ | 54 | [漫阅+ 家中与外出连接：给同一书库保留清楚的访问身份](/guides/manyue-home-away-endpoints/) | 1695 |
| 漫阅+ | 55 | [漫阅+ 服务器重新扫描后：检查章节变化与旧书签定位](/guides/manyue-server-rescan-identity/) | 1736 |
| 漫阅+ | 56 | [漫阅+ 两台设备交接阅读：先结束一台，再核对另一台](/guides/manyue-two-device-handoff/) | 1638 |
| 漫阅+ | 57 | [漫阅+ 恢复演练：在清理旧设备前核对备份能恢复什么](/guides/manyue-backup-recovery-rehearsal/) | 1678 |
| 漫阅+ | 58 | [漫阅+ 下载容量规划：用样本估算一周离线漫画空间](/guides/manyue-download-storage-budget/) | 1647 |
| 漫阅+ | 59 | [漫阅+ 更换漫画来源：用章节与情节迁移阅读位置](/guides/manyue-source-change-reading-map/) | 1685 |
| 漫阅+ | 60 | [漫阅+ 个人书库巡检：用五本样本发现文件与记录的缺口](/guides/manyue-library-maintenance-audit/) | 1700 |
| 书屿 | 21 | [书屿批量导入检查：把一批旧书分组搬进新书架](/guides/nasbook-batch-import-audit/) | 1581 |
| 书屿 | 22 | [书屿出行书包：断网前准备小说、资料与笔记](/guides/nasbook-offline-travel-pack/) | 1590 |
| 书屿 | 23 | [书屿手机与 iPad 接着读：同一章节采用两套阅读布局](/guides/nasbook-phone-tablet-layout/) | 1636 |
| 书屿 | 24 | [书屿图文 EPUB 检查：确认插图、注释和目录都跟着正文走](/guides/nasbook-epub-image-check/) | 1628 |
| 书屿 | 25 | [书屿 FB2 阅读：检查章节、正文与转换后的内容](/guides/nasbook-fb2-reading-check/) | 1607 |
| 书屿 | 26 | [书屿 CBZ 扫描资料阅读：按图像页检查顺序与清晰度](/guides/nasbook-cbz-scan-reading/) | 1636 |
| 书屿 | 27 | [书屿格式转换怎么选：给可管理但不能直读的书准备副本](/guides/nasbook-format-conversion-choice/) | 1633 |
| 书屿 | 28 | [书屿更换修订版：保留旧笔记，再核对新版本阅读位置](/guides/nasbook-edition-replacement/) | 1642 |
| 书屿 | 29 | [书屿多卷系列整理：让卷次、书名与阅读顺序一致](/guides/nasbook-series-volume-order/) | 1661 |
| 书屿 | 30 | [书屿文件命名与显示书名：建立能回到原件的书库清单](/guides/nasbook-library-file-naming/) | 1658 |
| 书屿 | 31 | [书屿主题复习路线：用书签串起跨章节的关键段落](/guides/nasbook-bookmark-study-route/) | 1655 |
| 书屿 | 32 | [书屿跨书对照笔记：把两本书的观点放回各自语境](/guides/nasbook-comparative-reading-notes/) | 1662 |
| 书屿 | 33 | [书屿长书摘制卡：压缩内容后检查出处与断句](/guides/nasbook-quote-card-proofreading/) | 1685 |
| 书屿 | 34 | [书屿搜不到正文怎么办：区分范围、关键词与可提取文本](/guides/nasbook-search-no-results-check/) | 1658 |
| 书屿 | 35 | [书屿月度阅读复盘：把统计、完成书目和笔记一起核对](/guides/nasbook-monthly-reading-review/) | 1684 |
| 书屿 | 36 | [书屿远端书下载失败：分开检查目录、文件与本地阅读](/guides/nasbook-remote-download-diagnosis/) | 1666 |
| 书屿 | 37 | [书屿 NAS 换地址或改目录：先验证新入口，再接回书库](/guides/nasbook-server-address-change/) | 1685 |
| 书屿 | 38 | [书屿 Calibre 目录搬迁检查：让 metadata.db 与书籍路径保持一致](/guides/nasbook-calibre-path-repair/) | 1665 |
| 书屿 | 39 | [书屿双设备同步交接：避免手机和平板同时改同一条记录](/guides/nasbook-sync-handoff-check/) | 1714 |
| 书屿 | 40 | [书屿换机验收：书籍、笔记和远端连接逐项恢复](/guides/nasbook-new-device-restore-check/) | 1711 |

## 验证记录

具体构建、结构化数据、双语配对、Markdown 产物与页面抽查结果见 [验证记录](verification.md)。本文件只记录内容范围与证据边界，不把本地构建结果当作线上已发布或已收录。
