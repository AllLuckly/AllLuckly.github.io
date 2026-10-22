# 验证记录

日期：2026-10-22。

## 教程扩充与关于页改版

- 新增 57 篇、扩写 3 篇入门，共 60 篇；Aquarell、漫阅+、VectorPaint 各 20 篇，序号分别连续 1–20。
- 正文按中文汉字统计共 100,519 字，单篇 1,601–1,874 字；每篇有操作步骤、常见问题、相关教程及版本来源。字数检查只用于发现缺稿，不能替代内容审阅。
- Ruby 4.0.1 / Jekyll 3.10 完整构建成功；`python3 scripts/validate_site.py`、`node --check assets/js/studio.js`、`git diff --check` 通过。
- 244 个 JSON-LD graph 可解析，244 条 sitemap URL 唯一且对应实际产物与 canonical；Atom feed 可解析。
- 71 个新建或更新页面的内部链接、资源、锚点和唯一 H1 检查通过。3 个 SoftwareApplication 分别关联 20 篇教程；没有虚构价格或评分。
- 教程中心和三个学习路线在 HTML 中直接提供全部文章链接，不依赖 JavaScript 才能被读取。首页各展示两篇教程，兼顾三个应用。
- Safari 桌面验证“透明 PNG”搜索得到三篇；再选漫阅+出现空结果提示；清空搜索后恢复漫阅+全部 20 篇。补充初始化与 pageshow 同步，处理返回页面时搜索文字恢复的情况。
- Safari 390×844 响应式模式检查教程中心、关于页及教程正文；手机目录可展开，中文长标题与正文正常换行。静态复核上一篇/下一篇按同应用序号关联，首尾边界正确。
- 关于页删除早期作品及旧友情链接，移除内部项目标识和生硬身份说明，以个人介绍、三个应用的实际用途和交流入口重新组织。
- 独立复核了 PSD、透明 PNG、取色、SVG 导入、图片矢量化和原稿备份六篇高风险教程。修正 VectorPaint 预览无放大入口以及原图与结果同层时不能直接隐藏的问题。
- 产品资料与源码证据见 `tutorial-evidence-aquarell.md`、`tutorial-evidence-manyue.md`、`tutorial-evidence-vectorpaint.md`。使用公开版本能力核对，未将未发布开发功能写成已上线承诺。

以上为发布前本地验证。应用教程未逐篇真机执行，未进行跨软件、打印或私人服务器测试；未提交 Search Console 或 Bing Webmaster Tools，不能据此确认搜索收录或 AI 引用。

## 首轮改版基线

首轮 173 个 JSON-LD graph、173 条 sitemap URL、3 篇入门教程构建及浏览器检查通过；本轮在该已发布版本上扩展。旧文章地址保留，feed 输出层继续过滤非法 XML 控制字符。
