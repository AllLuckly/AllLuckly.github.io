# 博客内容与搜索维护手册

本手册用于维护 https://allluckly.cn。它描述实现约定和上线后的待办事项，不代表网站已经部署、验证所有权、提交 sitemap 或被搜索引擎收录。资料核对日期：2026-10-22。

## 目标与优先级

让读者和搜索系统明确知道：这是什么 App、解决什么问题、怎样完成任务、实际结果如何、在哪里获取。先保证产品事实和原创案例可靠，再优化呈现、抓取与衡量。不能承诺立即被 AI 抓取、引用或推荐。

1. 每个 App 保留一个稳定专题页，清楚写明正式名称、公开别名、开发者关系、平台、适用场景及 App Store 入口。
2. 从专题页链接到对应教程和作品；每篇内容解决一个主要任务。保留原技术文章的主题和 URL。
3. 提供原创截图、步骤、版本与结果；需要视频时补充文字步骤或字幕摘要。
4. 检查 canonical、内部链接、XML sitemap 和爬虫访问，再观察实际收录、展示与下载入口点击。

## 产品事实的唯一来源

`_data/apps.yml` 为数组；`id` 是文章 `app_id` 的关联键，当前使用 `pastel`、`man_yue`、`draw_illustration`、`nas_book`、`icouldplay`、`yearn`。产品字段包括 `name`、可选的 `alternate_name`、`tagline`、`description`、`url`、`store_url`、`icon`、`category`、`os`、`version` 与 `verified`；教程字段为 `guide_url`、`guide_intro`、`minimum_guides`。内部关联键不作为对读者展示的产品名。

- 正式产品名、开发者、版本、系统要求和商店链接以已核实来源为准。项目目录名不能直接当作商店名。
- 产品专题页必须展示结构化数据包含的产品事实；不得在 JSON-LD 偷加正文没有的功能、评分或价格。
- 修改产品数据时同步核对教程适用版本；不要自动把旧教程改成“适用于最新版”。
- 标记开发者本人撰写的内容，避免把产品介绍包装成独立第三方评价。

## 教程写作模板

建议文件：`_posts/YYYY-MM-DD-descriptive-slug.md`。下例是待填写模板，不能直接发布占位文字；日期须为实际发布日期。

```yaml
---
layout: guide
title: "用具体 App 完成一个明确任务"
description: "说明适合谁、会完成什么、需要哪些条件。"
app_id: pastel
series_order: 21  # 在该 App 的学习路线中连续编号
topic: 创作练习
level: 进阶
reading_time: 8  # 估计阅读分钟数，不含动手练习
permalink: /guides/descriptive-slug/
date: 2026-10-22 10:00:00 +0800
author: Bison
# modified: 2026-10-25 10:00:00 +0800  # 只有实质修改才填写
# image: /assets/images/guides/actual-result.webp
# image_alt: 对实际作品的准确描述
---
```

正文至少交代：

1. **目标与结果**：最终效果、适合的任务、限制；先展示真实结果图。
2. **准备条件**：App 名称、实际测试版本、系统、所需素材。未操作验证的内容标为方案或待验证，不写成完成后的体验。
3. **具体步骤**：按界面实际名称写操作，每个关键步骤配截图或参数。使用语义标题，避免把全文做成一张长图。
4. **结果与导出**：格式、尺寸、质量检查；只写确实支持的选项。
5. **常见问题**：围绕实际失败、功能边界、替代路径回答。FAQ 是帮助读者的正文，不承诺搜索富结果。
6. **下一步**：链接到该 App 专题、相关作品、官方商店入口。

作品页可使用相同文章结构，补充创作目的、素材来源、过程图、关键选择、导出结果和可复用经验。不要虚构作品或用占位图片冒充 App 真实产出。

## 元数据与结构化数据约定

`_includes/seo.html` 供新旧布局共用；每页仅包含一次，避免旧 head 重复输出 title、canonical、OG、Twitter、JSON-LD。`site.url` 应为 `https://allluckly.cn`，不要使用协议相对地址。

- `WebSite` 和 `Person` 表达博客及维护者；没有添加虚假的站内搜索 `SearchAction`。
- 文章用 `BlogPosting`，产品教程的 `about` 指向专题页的 `#app` 实体。
- 只有 `layout: app` 且关联到有效产品时输出 `SoftwareApplication`。
- 应用目录、教程目录和学习路线使用 `CollectionPage` 与 `ItemList`，条目和顺序须与可见链接一致；单应用学习路线的 `about` 关联对应 `#app`。
- `BreadcrumbList` 描述首页、教程栏目与关联产品或文章归档、当前内容的路径；产品页为首页、我的应用、当前 App。
- 支持图片字符串、`image.path` / `image.url`、旧 `image.feature` / `image.thumb`、`cover` 和 `imagefeature`；旧裸文件名解析到 `/images/`。优先为新文章提供准确封面，而不是长期依赖 App 图标回退。
- `author` 可为名称，也可为 `{ name: ..., url: ... }`；有明确投稿作者的历史文章应补充该字段，并同步更新可见署名，不用旧 `description` 猜作者。文章没有显式 `author` 时，JSON-LD 仅保留站点发布者，不将 Bison 强行标为原作者。
- `noindex: true` 会输出 noindex 并从 sitemap 和 feed 排除；`sitemap: false` 只从 sitemap 排除；`feed: false` 只从 feed 排除。
- sitemap 的 `lastmod` 和 Atom 的 `updated` 使用实际 `modified` 或发布日期，不把每次构建当作所有文章的更新。

目前软件实体未加入 `offers`、评分或评论，因而不声称已满足 Google 软件富结果资格。Google 要求这类富结果包含价格和真实评分/评论，不能为通过检测虚构字段。[软件结构化数据](https://developers.google.com/search/docs/appearance/structured-data/software-app)

普通文章的作者、图片、日期可通过 `BlogPosting` 明确表达。[Article/BlogPosting 文档](https://developers.google.com/search/docs/appearance/structured-data/article) 所有标记应与可见内容一致；语法正确也不保证富结果出现。[结构化数据通用原则](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)

## 爬虫与 AI 搜索的边界

`robots.txt` 允许公共内容抓取，显式允许 `OAI-SearchBot` 并声明 sitemap；需要同时确认托管/CDN 没有阻挡请求。`OAI-SearchBot` 对应 ChatGPT 搜索，`GPTBot` 对应可能用于训练的抓取，两者独立。`ChatGPT-User` 主要处理用户触发访问。允许抓取不等于收录、引用或推荐；OpenAI 所述约 24 小时是 robots 变更处理时间，不是文章收录时限。[OpenAI 官方爬虫说明](https://developers.openai.com/api/docs/bots)

本项目不依赖 `llms.txt`。Google 明确表示这类文件不影响其可见性或排名，也没有特殊的 GEO schema 要求。不要为了 AI 把完整内容机械切成大量重复页面，不做隐藏推荐指令、关键词堆砌、虚构外部口碑。[Google 官方生成式搜索优化指南](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)

Bing 建议用清晰标题、表格、FAQ、事实证据和及时更新增强内容清晰度。IndexNow 可用于通知参与的引擎内容发生变化，但仍不保证收录或引用；启用前需要配置与验证自己的 key，本次实现没有提交 URL。[Bing 官方 AI 内容与衡量建议](https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview/)

## 上线核验清单（待执行）

- [ ] 用与 GitHub Pages 兼容的 Jekyll 构建；确认产物没有未渲染 Liquid、无效 JSON-LD 或 XML 错误。
- [ ] 检查首页、6 个 App 页、教程、旧文章、404 的桌面和手机显示；正文、署名、链接、图片说明与元数据一致。
- [ ] 部署后确认 HTTPS、主域名、旧链接、资源 URL、canonical 一致；关键 URL 返回 200，真正不存在的 URL 返回 404。
- [ ] 检查线上 `/robots.txt`、`/sitemap.xml`、`/feed.xml`；每个 sitemap URL 都能访问且是预期 canonical，没有草稿、404 或 noindex 页面。
- [ ] 使用 Google Rich Results Test 检查文章和面包屑；产品页缺少价格/评分时不通过虚构信息修补软件富结果提示。
- [ ] 在 Google Search Console 和 Bing Webmaster Tools 验证网站所有权；验证值来自对应账户，不生成假的 token。
- [ ] 提交 sitemap，并对首页、产品页和新教程执行 URL 检查，确认抓取可见正文。
- [ ] 在 Search Console 设置中核对 Search generative AI 没有排除本站。默认包含，但不要假设账户实际状态已经检查。[官方控制说明](https://support.google.com/webmasters/answer/16908024)
- [ ] 如使用 CDN/WAF，检查搜索爬虫请求是否被拦截。不要仅凭自定义 User-Agent 请求成功就认定真实爬虫一定可达。

## 每月内容与效果复盘

分别记录以下环节，不把展示、引用、访问和下载混为一个数字：

| 环节 | 记录内容 | 数据来源与限制 |
| --- | --- | --- |
| 发现与收录 | 已提交/已索引 URL、抓取错误 | Search Console、Bing Webmaster Tools；提交不等于收录 |
| 搜索展示与访问 | 页面、主题、展示、点击 | 搜索站长工具；按相同时间范围比较 |
| AI 搜索展示 | Google 生成式搜索展示页面与趋势 | [Generative AI performance report](https://support.google.com/webmasters/answer/16984139)；展示不足时可能没有报告 |
| AI 引用 | Bing 引用次数、被引用 URL、主题 | Bing AI Performance；引用不是点击或下载 |
| 产品入口点击 | 哪个页面、哪款 App、点击次数 | 后续配置的站点分析；当前模板不声称已接入分析 |
| 实际获取 | 商店产品页访问及下载 | 开发者自己的商店分析；需账户数据，不能由外链点击推定 |

保持每篇教程有独立任务、具体操作与真实边界，再从实际搜索问题补充内容。对比基线与发布后数周的数据，不承诺固定收录天数或推荐名次。

## 教程库维护

每个 App 的完整目录位于 `/guides/aquarell/`、`/guides/manyue/`、`/guides/vectorpaint/`、`/guides/nasbook/`、`/guides/icouldplay/` 和 `/guides/yearn/`。`series_order` 从 1 连续编号，同一 App 内不重复；目录、上一篇和下一篇都依据该字段排序。学习阶段的范围应完整覆盖所有教程且不重叠。新增内容时保持原 URL 稳定，更新必要的相关教程链接。

`/guides/` 的应用筛选与关键词搜索只筛选页面已包含的链接，关闭 JavaScript 仍可阅读全部目录。搜索包含公开应用名和别名。首页按每个 App 各一篇入门教程展示，避免一次集中发布后只出现一种应用。

运行 `python3 scripts/validate_site.py` 会按 `minimum_guides` 核验各应用教程数量（目前原三款各 40 篇、新三款各 20 篇），并检查连续编号、独立标题和 URL、正文规模、阶段覆盖、目录结构化数据、内部链接与锚点。字数检查只是发布底线，不能替代功能核对和逐篇编辑；证据维护于 `docs/tutorial-evidence-*.md`。不要用同义改写、重复段落或与任务无关的提醒凑数量和篇幅。
