# 漫阅+ 20 篇教程内容证据

资料日期：2026-10-22（Asia/Shanghai）。本记录用于编辑维护，不是用户操作正文，不包含私人服务器、账号或漫画文件。

## 版本与核对范围

- 实时 Apple Lookup：中国区名称“漫阅+ 漫画阅读器”，版本 **2.0.2**，最低 iOS 15.0，当前版本发布时间 `2026-10-19T15:22:11Z`。
- [App Store 公开说明](https://apps.apple.com/cn/app/id6753895889)；[Apple 公共查询](https://itunes.apple.com/lookup?id=6753895889&country=cn)。
- 源码取自 `man_yue` 仓库 Git 提交 `5448f0158daacaf5524478d3338a9845726a12d9`，该提交 `pubspec.yaml` 为 `2.0.2+31`；逐篇路径行号均以 `git show 5448f0158daacaf5524478d3338a9845726a12d9:路径` 为准。
- 当前工作区 `pubspec.yaml` 已改为 `2.0.3+36`，并存在阅读器、Wi-Fi 导入、图片/PDF缓存等未提交变更。本次不把这些变更当作 2.0.2 已发布事实；未读取 `output/` 副本，也未修改 App 仓库或 App Store 元数据。
- 已读 `appstore/AGENTS.md` 与 `appstore/AI_CONSTRAINTS.md`。本任务仅只读核实发布资料，未执行文案上传、提交审核或同步发布操作。
- 版本号与源码入口本身不能独立证明某一二进制中的所有细节，因此公共能力以实时商店说明为主，细项入口在必要处使用当前界面可见条件，不宣称所有服务器或文件都已真机测试。

## 公开能力基础

公开说明列出 CBZ/CBR/CB7/ZIP/RAR/7z/PDF、本地离线、书架分组/历史/书签/待阅读、WebDAV/SMB、Komga/Kavita/OPDS等服务器书库、横竖屏和单双页、iCloud/WebDAV 状态同步。Pro 与 Ultra 权益仅说明相关功能层级，文章未固化价格。

2.0.2 公开更新记录明确清理本地副本可保留收藏与阅读进度。本文将它与删除漫画、移出书架、删除下载任务、清缓存分别说明，未宣称所有删除入口等价。

## 逐篇证据与主要限制

| 顺序 | 教程 | 源码入口（基准提交行号） | 公开依据与限制 |
| --- | --- | --- | --- |
| 1 | 导入本地漫画并离线阅读 | `lib/pages/import_comics_dialog.dart:58-112`；`lib/pages/comic_import_session_page.dart:293,393,460` | 商店本地与离线能力；先单文件后批次，显示封面不等于完整离线。 |
| 2 | [漫阅+ 文件格式指南：选择 CBZ、CBR、CB7 或 PDF，并检查页序](../_posts/2026-10-22-manyue-formats-and-page-order.md) | `lib/foundation/comic_format_manager.dart:8-23`；`lib/utils/import_comic.dart:729-798,895-958`；`lib/utils/local_comic_pages.dart:113,217-233` | 公开格式清单；后缀支持不保证加密、分卷或损坏变体，页序须看实际画面。 |
| 3 | [漫阅+ 图片文件夹导入：把散页整理成一本书或多个章节](../_posts/2026-10-22-manyue-image-folder-import.md) | `lib/pages/import_comics_dialog.dart:68-112,222-260`；`lib/utils/import_comic.dart:729-798,875-958` | 公开图片/本地整理能力；顶层文件批次与章节目录不同，混合结构需整理。 |
| 4 | [漫阅+ 导入失败怎么办：从文件可用性、格式和目录层级逐项排查](../_posts/2026-10-22-manyue-import-troubleshooting.md) | `lib/pages/import_comics_dialog.dart:68-112,222-260`；`lib/utils/import_comic.dart:239-315,729-798,916-923`；`lib/pages/comic_import_session_page.dart:293,393,460` | 公开导入能力；故障诊断是建议流程，不声称特定错误只有唯一原因。 |
| 5 | [漫阅+ 书架整理：用分组安排待阅读、正在读和已完成](../_posts/2026-10-22-manyue-bookshelf-organization.md) | `lib/pages/favorites/local_favorites_page.dart:476-535,837-905,1133-1246,1534-1544`；`lib/pages/local_comics_page.dart:66-111,144-150` | 公开书架分组；移动/复制关系与删除文件分开，批量入口取决于权益。 |
| 6 | [漫阅+ 阅读布局：设置方向、单页双页与跨页检查](../_posts/2026-10-22-manyue-reading-layout.md) | `lib/pages/settings/reader.dart:245-295,353-362,483-558,640-675`；`lib/pages/reader/bookmarks.dart:32-81` | 公开横竖屏/单双页/缩放；具体设置按可见范围，源文件错序不能靠布局修复。 |
| 7 | [漫阅+ 书签与笔记：保存一页、写下提醒，再准确回到原处](../_posts/2026-10-22-manyue-page-bookmarks.md) | `lib/pages/reader/bookmarks.dart:10-18,54-103,112-175,186-282,330-385`；`lib/foundation/reading_bookmarks.dart` | 公开书签；源章节删除或改页会影响旧书签定位，未承诺跨来源自动匹配。 |
| 8 | [漫阅+ 离线阅读准备：出发前确认整本漫画真的在设备上](../_posts/2026-10-22-manyue-offline-preflight.md) | `lib/pages/download_manager_page.dart:95-114,359-389`；`lib/pages/local_comics_page.dart:325-369`；`lib/pages/sync_center_page.dart:375-387`；`lib/pages/webdav_page.dart:221-251` | 公开已导入/已下载可离线；远程目录、缓存、收藏不等于完整副本。 |
| 9 | [漫阅+ 下载管理：安排队列、处理失败，并确认本地副本](../_posts/2026-10-22-manyue-download-queue.md) | `lib/pages/download_manager_page.dart:95-162,359-389,493-527`；`lib/pages/webdav_page.dart:221-251`；`lib/pages/smb_page.dart:131-156` | 公开下载管理；任务完成仍检查实际内容，删除确认中的文件范围需读清。 |
| 10 | [漫阅+ 连接 WebDAV 漫画书库：从地址核对到下载检查](../_posts/2026-10-22-manyue-webdav-library.md) | `lib/pages/nas_library_page.dart:1270-1300,1394-1445`；`lib/pages/webdav_page.dart:67-117,221-251`；`lib/pages/sync_center_page.dart:270-296` | 公开WebDAV；漫画读取与WebDAV数据同步分开，读写权限按任务核对。 |
| 11 | [漫阅+ 连接 SMB：在局域网中浏览 NAS 漫画并保存离线副本](../_posts/2026-10-22-manyue-smb-library.md) | `lib/pages/nas_library_page.dart:1295-1302,1394-1445`；`lib/pages/smb_page.dart:111-156,184-196` | 公开SMB；局域网可达性、共享权限与离线副本分别检查，不建议公网暴露SMB。 |
| 12 | [漫阅+ 连接 Komga：从账号权限到系列、章节和离线检查](../_posts/2026-10-22-manyue-komga-library.md) | `lib/pages/server_library_page.dart:506-643`；`lib/features/server_library/data/komga_repository.dart:7-14,24-37,48-119`；https://komga.org/docs/guides/user-accounts/ | 公开Komga；系列映射书籍条目；逐页读取与下载权限参考Komga官方文档。 |
| 13 | [漫阅+ 连接 Kavita：使用账号登录并检查书库与阅读权限](../_posts/2026-10-22-manyue-kavita-library.md) | `lib/features/server_library/domain/server_library_service_descriptor.dart:62-65`；`lib/features/server_library/data/kavita_repository.dart:61-88,268-280,452-457`；`lib/pages/server_library_page.dart:506-643`；https://wiki.kavitareader.com/guides/admin-settings/users/ | 公开Kavita；使用用户名密码登录，基础地址不混用OPDS/API Key，权限参考官方文档。 |
| 14 | [漫阅+ 连接 OPDS：为什么能看到目录，却不能直接逐页阅读](../_posts/2026-10-22-manyue-opds-pse-library.md) | `lib/features/server_library/domain/server_library_service_descriptor.dart:74-82`；`lib/features/server_library/data/opds_repository.dart:15-38,300-314,503-610`；https://anansi-project.github.io/docs/opds-pse/intro | 公开明确OPDS-PSE边界；普通整包OPDS不承诺直接逐页阅读，下载后本地导入是另一流程。 |
| 15 | [漫阅+ 服务器连接排查：把网络、登录、目录和页面分开检查](../_posts/2026-10-22-manyue-server-connection-troubleshooting.md) | `lib/pages/server_library_page.dart:506-643`；`lib/features/server_library/domain/server_library_service_descriptor.dart:29-81`；`lib/pages/webdav_page.dart:100-108`；`lib/pages/smb_page.dart:111-114`；`lib/pages/download_manager_page.dart:359-389` | 公开多类服务器能力；按失败阶段缩小范围，不保证错误码对应唯一原因。 |
| 16 | [漫阅+ iCloud 同步：把阅读进度和书架带到另一台设备](../_posts/2026-10-22-manyue-icloud-sync.md) | `lib/pages/icloud_sync_page.dart:108-164,205-285,303-402`；`lib/pages/sync_center_page.dart:306-319,375-387`；`lib/utils/icloud_sync_service.dart:249-284,340-387` | 公开iCloud状态同步；新设备文件另行恢复，先备份并明确初始上传/下载方向。 |
| 17 | [漫阅+ WebDAV 数据同步：建专用目录，选择首次上传或下载](../_posts/2026-10-22-manyue-webdav-sync.md) | `lib/pages/settings/app.dart:481-540,612-750`；`lib/pages/sync_center_page.dart:270-296,375-387`；`lib/utils/data_sync.dart:242-314,342-409` | 公开WebDAV状态同步；专用目录与写权限，冲突提示保留备份，不手改同步版本文件。 |
| 18 | [漫阅+ 换设备指南：先恢复阅读状态，再补回漫画文件](../_posts/2026-10-22-manyue-device-migration.md) | `lib/pages/sync_center_page.dart:370-421`；`lib/utils/data.dart:146-179,228-242`；`lib/pages/import_comics_dialog.dart:68-112` | 公开多设备状态同步；源码同步中心明确排除漫画文件/下载记录/NAS索引/设备凭据。 |
| 19 | [漫阅+ 手动备份与恢复：保留应用数据，单独保存漫画原件](../_posts/2026-10-22-manyue-backup-and-restore.md) | `lib/pages/settings/app.dart:131-171`；`lib/pages/sync_center_page.dart:387-421`；`lib/utils/data.dart:146-179,228-242`；`lib/pages/sync_recovery_page.dart:40-76,178-183,245` | 手动导出/导入入口和同步中心范围说明；本地备份可能含Cookie/WebDAV设置，漫画原件独立保存。 |
| 20 | [漫阅+ 存储清理：分清缓存、本地副本、下载任务与书架关系](../_posts/2026-10-22-manyue-storage-cleanup.md) | `lib/pages/my_library_page.dart:2306-2310,2397-2450`；`lib/pages/settings/app.dart:77-113`；`lib/pages/download_manager_page.dart:493-527`；`lib/pages/local_comics_page.dart:424-484`；`lib/pages/server_library_page.dart:171-178`；`Apple Lookup releaseNotes 2.0.2:清理本地副本并保留收藏与阅读进度` | 2.0.2公开更新记录；多类删除对象分开，操作前说明原件及不可撤销边界。 |

## 额外官方技术资料

- [Komga 用户权限](https://komga.org/docs/guides/user-accounts/)：书库共享、Page Streaming 与 File Download 权限可分别控制。
- [Kavita 用户权限](https://wiki.kavitareader.com/guides/admin-settings/users/)：共享书库、登录与下载等角色；不把管理员可见范围当普通账号范围。
- [OPDS-PSE 项目定义](https://anansi-project.github.io/docs/opds-pse/intro)：在目录中提供逐页请求信息，区别于完整文件获取。

## 图片与示例

教程使用自制/有权阅读的小样作为操作练习建议，未伪造作品或截图。所有服务示例使用 `example.com` 及明确的占位账户，不包含真实连接资料。源码日志与集成测试中的账号、主机和书库信息未进入正文或本记录。

## 编辑检查

正文至少五个二级标题，含具体操作、实例、完成检查、两条以上常见问题及相关教程链接。`series_order` 为1–20，`reading_time` 为整数；日期统一2026-10-22。完整站点构建、最终链接检查和发布由主任务统一完成，本记录不声称已经发布新增教程。
