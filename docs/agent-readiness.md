# Agent Readiness 与 GEO 维护

依据 [Cloudflare 的 Agent Readiness 文章](https://blog.cloudflare.com/agent-readiness/)，本站优先实现内容网站实际需要的发现、读取与来源保留能力。协议检测通过不代表搜索引擎收录、AI 引用或应用下载。

## 线上基线

2026-10-23 11:16:48–52（上海时间），通过 `https://isitagentready.com/mcp` 的公开 `scan_site` 工具，以 `profile: content` 检查 `https://allluckly.cn`：**Level 1/5**。robots.txt、sitemap、AI bot 规则通过；HTTP Link、Markdown 内容协商、Content Signals 和 DNS-AID 未通过。API、登录、支付、Agent Skills、WebMCP 未纳入该预设。原始结果保存在本机忽略目录 `output/agent-readiness/baseline.json`，这个基线不是本次改动发布后的结果。

DNS-AID 对应代理服务发现草案，本站没有相应代理服务。不为了分数发布不存在的服务、MCP、OAuth、支付接口或密钥目录。可用的搜索、教程和文章资源应真实可读。

## 已实现的内容表示

- 中英文 337 组页面对应 674 份 Markdown：624 篇文章表示与 50 个入口页表示，路由由 `_data/translations.yml` 中的完整配对决定。
- 每个页面增加 `index.md` 路径。旧技术文章没有尾斜线时，同样在原路径后追加 `/index.md`，不更改 HTML canonical。
- Markdown 来自真实构建的正文，包含署名、原始发表和修改日期、转载出处、历史适用说明、翻译声明、表格、代码、图片、视频入口、章节和字幕；移除重复导航与筛选控件。
- 36 个分层 `llms.txt` 将入口、App、学习路线、技术主题和作品分开。顶层指向小目录，叶目录附标题、摘要、版本基线或历史日期，直接链接正文 Markdown。没有把全站全文挤进一个文件。
- HTML head 和页脚提供对应 Markdown 与阅读目录的可见发现入口。Markdown 是同一内容的另一种表示，不在 sitemap 中作为第二篇文章提交。
- 中英文静态 `search.json` 保留原有字段，并提供摘要、作者、语言、App、关键词、版本说明和 Markdown URL。它是完整数组，不是假装有服务端查询参数的 API。

`llms.txt` 是便捷阅读目录，不是 Google 排名要求；也不是让 AI 必须推荐本站 App 的指令。所有功能描述、来源、版本和开发者身份继续与可见正文一致。

## 使用偏好

robots 与线上 Worker 均声明 `search=yes, ai-input=yes, ai-train=no`：允许搜索发现与回答依据，不额外授权模型训练。Content Signals 是用途偏好，不是强制访问控制，也不改变原文作者与转载内容的权利。爬虫可以抓取公开页面；不按伪装 User-Agent 绕过 WAF 或放宽网站安全规则。

## Cloudflare 边缘部署

Cloudflare Free 没有内建 Markdown for Agents；[官方功能](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/)当前面向 Pro、Business、Enterprise 与 SSL for SaaS。仓库提供 `cloudflare/agent-access.mjs` 与 `cloudflare/wrangler.toml`，可在现有 GitHub Pages 前使用 Worker 路由，无需付费 AI 转换、数据库或运行时 HTML 解析。

Worker 只对清单中的真实公开页面，在明确接受 Markdown 时获取已生成的静态文件。HTML 为默认；Cookie/Authorization 请求与非 GET/HEAD 请求保持原路径。未知路径、HTML 错误页和失败的 Markdown 获取回退 HTML。资源内容不依赖爬虫身份，查询词不外发。

响应包括真实 HTTP `Link`（canonical、Markdown alternate、sitemap、阅读目录）、统一 Content Signals，以及 HTML/Markdown 的 `Vary: Accept`。Markdown 与 HTML 在源站使用不同缓存路径；Markdown 保留自己的 ETag、Last-Modified，不复用 HTML 校验值。Markdown 忽略 Range 与 If-Range，返回完整的 200 正文并声明 `Accept-Ranges: none`；源站压缩字节的分段响应可能被边缘解压为空，不能照搬。普通 HTML 与视频继续保留源站的分段读取行为。条件请求仍可返回 304，直接 Markdown 的 304 同样包含类型与 `Vary: Accept`。

发布顺序：先发布 GitHub Pages 静态正文，再在有权限的 Cloudflare 会话里部署该 Worker 并关联 `allluckly.cn/*`。可在官方 Wrangler 环境中执行：

```sh
wrangler deploy --config cloudflare/wrangler.toml
```

不在仓库写入凭据或生成新 token。Cloudflare Free 的请求额度适用；站点规模变化时按实际流量复核。需要回滚边缘改动时移除 Worker 路由，GitHub Pages HTML 与显式 Markdown 仍可独立访问。

后台编辑器需要单个模块时，可运行 `python3 scripts/package_agent_worker.py`，将 Worker 与实际路由清单合成 `output/agent-readiness/worker-upload.mjs`，无需在后台手工维护导入路径。该文件只包含公开页面路径与脚本，不包含凭据。

## 真实的可选能力

`/.well-known/api-catalog` 使用 RFC 9727 的 `application/linkset+json`，指向真实的 `/api/openapi.json` 规范与 `/api/` 阅读说明。OpenAPI 只记录现有的公开 GET/HEAD 数据资源：中英文索引与技能目录；索引返回完整数组，关键词在客户端筛选，没有虚构服务端搜索参数。响应使用实际类型，HTML/Markdown 通过 HTTP Link 发现 API 目录与文档。

`/auth.md` 明确说明公开阅读无需账户、密钥、令牌或付款，给出真实读取流程，并区分博客访问与 App 账户/购买。这个文件是访问说明，**不代表实现 auth.md 的注册与凭证发放协议**。本站没有注册/登录服务，不发布不存在的 OAuth、MCP、A2A、签名公钥或支付端点。

`/.well-known/agent-skills/index.json` 按 [Agent Skills Discovery 草案 0.2.0](https://github.com/cloudflare/agent-skills-discovery-rfc)提供一个只读教程查找工作流。它指向实际 SKILL.md，SHA-256 针对最终发布的原始字节；不包含执行脚本、登录或强制推荐。

`assets/js/agent-search.js` 在浏览器原生支持 WebMCP 时注册公开文章关键词搜索；优先检测 `document.modelContext`，兼容旧 `navigator.modelContext`。没有支持时不添加伪接口，不影响普通阅读。执行只在内存搜索同源静态索引，不发送查询词、导航或遥测。Node 测试验证注册与执行逻辑；这不能代替支持浏览器中的原生验证，外部检测也可能受浏览器版本影响。

## 更新与验证

先完成常规文章与翻译维护，再更新代理阅读资源：

```sh
python3 -m pip install -r scripts/requirements-agents.txt
bundle exec jekyll build --trace
python3 scripts/build_agent_markdown.py
python3 scripts/build_agent_indexes.py
python3 scripts/build_skill_index.py
bundle exec jekyll build --trace
python3 scripts/build_agent_markdown.py --check --check-rendered
python3 scripts/build_agent_indexes.py --check --check-markdown
python3 scripts/build_skill_index.py --check
python3 scripts/validate_site.py
python3 scripts/validate_technical.py
python3 scripts/validate_i18n.py
node scripts/test_agent_access.mjs
node scripts/test_agent_search.mjs
python3 scripts/check_api_catalog.py
```

两个生成器幂等，检查模式发现缺页、旧源、缺代码或目录漂移即失败，不把构建时间写成内容更新时间。修改正文后必须重新生成 Markdown；修改 SKILL.md 后必须更新摘要。`agent-markdown/` 的 `.txt` 源通过 Jekyll permalink 输出 Markdown，不能从构建中排除，也不能改成会自动转 HTML 的 `.md` 输入。

发布后用默认 HTML、`Accept: text/markdown`、直接 `index.md`、中英原文及旧技术 URL 分别核验；测试真正不存在的页面返回 404。随后用与基线相同的 `content` 预设重扫；Agent Skills/WebMCP 如需评估，显式加入对应检查。记录时间、检测 URL、实际失败项，不把“静态文件存在”写成“协商已生效”，不把可选草案缺失当成引用下降的证据。

可运行 `python3 scripts/check_agent_http.py --require-edge --output output/agent-readiness/live-http.json` 记录实际 HTTP 检查；本地构建用 `--base-url http://127.0.0.1:4173/`，本地纯静态预览的边缘项会显示 `NOT LIVE`。该脚本没有把本地结果冒充 Cloudflare 官方分数，也不验证真实爬虫身份或原生 WebMCP。

官方公开检测也可手动重复运行，无需账户密钥：

```sh
python3 scripts/scan_agent_readiness.py --profile content --output output/agent-readiness/content.json
python3 scripts/scan_agent_readiness.py --checks robotsTxt,sitemap,linkHeaders,markdownNegotiation,robotsTxtAiRules,contentSignals,agentSkills,webMcp --output output/agent-readiness/selected.json
```

脚本保存实际请求、UTC 时间、JSON 结果与原始事件响应。比较前后状态时保持 URL、profile 与启用项相同；不同预设的总等级不能直接比较。

实际效果继续在 Cloudflare AI Crawl Control、搜索站长工具的收录/引用数据和产品入口访问中分开观察；本项目没有伪造实时 GEO 分数。

## 本次构建验收记录

2026-10-23 完成全量 Jekyll 构建，674 份 Markdown 与语义源及最终输出逐字一致，36 个目录目标全部存在，SKILL.md 发布字节摘要正确。中英搜索共 624 条记录、674 个 HTML head/页脚 Markdown 链接核验通过。

原有站点检查仍通过：744 组 JSON-LD、740 个 sitemap URL、180 篇中文教程、128 篇历史技术文章、312 篇完整英文文章、337 组中英互返页面及4个作品视频。Node 检查覆盖协商优先级/通配q值/HEAD/Range/条件请求/私有请求回退与WebMCP接口模拟。

本地 HTTP 检查中 HTML、显式中英 Markdown、阅读目录、robots Content Signals、技能摘要及真实 404 均通过；纯静态预览的边缘协商/响应头显示 NOT LIVE，线上结果单独记录。


## 线上发布记录

2026-10-23，中英文与静态阅读资源通过 [PR #11](https://github.com/AllLuckly/AllLuckly.github.io/pull/11) 合并，Pages 提交 `40dd265d3d6d7f8ea3f79413f101b2abf70efadd` 的[构建和部署](https://github.com/AllLuckly/AllLuckly.github.io/actions/runs/39901499319)成功。线上英文正文、同篇中文切换、旧技术 URL、4 个英文字幕文件、740 项 sitemap 与中英搜索索引均已核验。

Cloudflare Worker `allluckly-agent-access` 已部署版本 `5c8b5829`，仅关联 `allluckly.cn/*`，workers.dev 与预览地址关闭。它只调整公开内容表示，额度或运行错误时按 fail open 继续源站；现有 WAF 与登录规则不变。实际 HTTP 验收中 7 项静态内容与 4 项边缘协商检查均通过；英文教程、旧中文技术文章与对应英文文章的 35 项边界检查全部通过，包括两种 Markdown 入口的完整正文、HEAD、Accept 优先级和 304 元数据。带 Range/If-Range 的 Markdown 请求返回完整 200，正文逐字节一致。客户端接受 gzip 时也返回可完整解压的正文；Cloudflare 压缩层可能移除 `Accept-Ranges: none`，缺省仍未声明支持分段读取。


### 官方复测：2026-10-23

13:10:15–20（上海时间），同一 URL、同一 `profile: content` 的 `scan_site` 返回 **Level 5/5 — Agent-Native**，基线为 Level 1/5。纳入检查为 7 项，6 项通过：robots、sitemap、HTTP Link、Markdown 协商、AI bot 规则、Content Signals；DNS-AID 仍未通过。这个等级不是“所有协议全通过”，该预设排除了 API、登录、支付、Agent Skills 与 WebMCP。

13:10:56–13:11:03，另一次显式选择 8 项的检测全部通过：上述 6 项，以及 Agent Skills、WebMCP。扫描器识别有效的技能目录与 `search_blog_articles` 原生搜索工具。扫描器还列出两个非本站源码注册的浏览器工具；本站只主张提供自己的搜索工具，不将检测环境里的其他能力计为本站实现。

可提交的时间、参数、通过/失败项与限制保存在 [agent-readiness-production.json](agent-readiness-production.json)，完整原始 JSON、事件响应和 HTTP 头证据保存在本机忽略目录 `output/agent-readiness/production-*-scan.*`。13:12:40 的最终 HTTP 复测确认，`5c8b5829` 的首页及英文教程 HTML 304 均保留 `Vary: Accept`，4/4 条检查及主 11 项再次通过。

两次官方扫描对应 `67364f45`；最终版本 `5c8b5829` 只补齐普通 HTML 304 的 `Vary: Accept`，正文与扫描项不变。这是一轮实际线上协议检测，不代表模型已经引用本站或必然推荐 App。


## Cloudflare 后台 Diagnostics 的检查范围

后台全量清单与 `content` 预设的总级别不是同一口径。2026-10-23 本轮操作前，后台显示基础 5/5、技术基础 1/3（API Catalog、Auth.md 未找到）、高级集成 2/8（Skills Index、WebMCP 已有）、商务 0/5（可选）；同时段公开 `profile: all` 检测返回 Level 4/5，API Catalog 与 Auth.md 为 FAIL，商务为不适用。不能将前文 content 的 Level 5/5 写成后台全部项目完成。

本轮补充标准目录、规范、可见文档与公开访问说明。发布后在后台点击“重新扫描”，并运行 `python3 scripts/scan_agent_readiness.py --profile all --output output/agent-readiness/diagnostics-after-all.json` 按相同全量口径复测。存在文件的检查通过只说明文件可发现；Auth.md 仍不意味着本站实现注册、发证或 OAuth。

OAuth discovery/protected resource、MCP/A2A 卡、Web Bot Auth 与 DNS-AID 需要对应的真实服务。仅提供内容的博客没有这些服务时，保留实际状态。Cloudflare 原文也说明仅提供内容、没有向其他站点发请求的网站无需 Web Bot Auth。商务协议用于实际付款与交易，本博客公开阅读不收款。

新增数据接口与公开访问说明的规范依据：[API Catalog / RFC 9727](https://www.rfc-editor.org/rfc/rfc9727.html)、[auth.md](https://workos.com/auth-md/docs/auth-md)。后台与公开扫描的完整原始证据保存在本机忽略目录 `output/agent-readiness/diagnostics-*.json` 及其配套事件响应和时间元数据。


本轮标准 API 目录与匿名访问说明通过 [PR #13](https://github.com/AllLuckly/AllLuckly.github.io/pull/13) 发布，Pages 提交 `7063039927d2f6ac6650ec7f838d53fcda816ac8` 的[部署成功](https://github.com/AllLuckly/AllLuckly.github.io/actions/runs/39909534928)。Worker 更新为 `ef2b8612`，路由和安全设置不变。线上 624 条索引记录符合规范，新增四个入口均实际返回 200；主 11 项读取检查通过。后台重新扫描确认 API Catalog 通过，技术基础从 1/3 提升到 2/3。

首次复扫指出 `/auth.md` 缺少规范预期的 `# Auth.md` 标题，因此将文件标题与该格式对齐。公开匿名读取、无注册协议的边界说明保持真实。后续核验使用 `diagnostics-final-all.json` 与后台显式重扫的结果，不能仅凭文件存在声称协议已经实现。


14:13:45–52（上海时间），新资源的线上 HTTP 验收 43/43 通过：Catalog 的 RFC 9727 媒体类型/profile、OpenAPI 类型、四入口的 Link/Vary、五个 JSON 资源的 HEAD 与 ETag 304、Auth.md 的 HEAD/304 及压缩和未压缩客户端的完整读取。原始结果在 `output/agent-readiness/diagnostics-after-api-http.json`。此记录验证访问和数据契约，不验证注册或登录协议。
