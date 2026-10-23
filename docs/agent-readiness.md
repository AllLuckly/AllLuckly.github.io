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

robots 与准备部署的 Worker 均声明 `search=yes, ai-input=yes, ai-train=no`：允许搜索发现与回答依据，不额外授权模型训练。Content Signals 是用途偏好，不是强制访问控制，也不改变原文作者与转载内容的权利。爬虫可以抓取公开页面；不按伪装 User-Agent 绕过 WAF 或放宽网站安全规则。

## Cloudflare 边缘部署

Cloudflare Free 没有内建 Markdown for Agents；[官方功能](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/)当前面向 Pro、Business、Enterprise 与 SSL for SaaS。仓库提供 `cloudflare/agent-access.mjs` 与 `cloudflare/wrangler.toml`，可在现有 GitHub Pages 前使用 Worker 路由，无需付费 AI 转换、数据库或运行时 HTML 解析。

Worker 只对清单中的真实公开页面，在明确接受 Markdown 时获取已生成的静态文件。HTML 为默认；Cookie/Authorization 请求与非 GET/HEAD 请求保持原路径。未知路径、HTML 错误页和失败的 Markdown 获取回退 HTML。资源内容不依赖爬虫身份，查询词不外发。

响应包括真实 HTTP `Link`（canonical、Markdown alternate、sitemap、阅读目录）、统一 Content Signals，以及 HTML/Markdown 的 `Vary: Accept`。Markdown 与 HTML 在源站使用不同缓存路径；Markdown 的 ETag、Last-Modified、Range 与长度属于它自己的字节，不复用 HTML 校验值。**只有 Worker 实际部署且 HTTP 核验通过，才能声称线上支持 Accept 内容协商和这些响应头。**

发布顺序：先发布 GitHub Pages 静态正文，再在有权限的 Cloudflare 会话里部署该 Worker 并关联 `allluckly.cn/*`。可在官方 Wrangler 环境中执行：

```sh
wrangler deploy --config cloudflare/wrangler.toml
```

不在仓库写入凭据或生成新 token。Cloudflare Free 的请求额度适用；站点规模变化时按实际流量复核。需要回滚边缘改动时移除 Worker 路由，GitHub Pages HTML 与显式 Markdown 仍可独立访问。

后台编辑器需要单个模块时，可运行 `python3 scripts/package_agent_worker.py`，将 Worker 与实际路由清单合成 `output/agent-readiness/worker-upload.mjs`，无需在后台手工维护导入路径。该文件只包含公开页面路径与脚本，不包含凭据。

## 真实的可选能力

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
```

两个生成器幂等，检查模式发现缺页、旧源、缺代码或目录漂移即失败，不把构建时间写成内容更新时间。修改正文后必须重新生成 Markdown；修改 SKILL.md 后必须更新摘要。`agent-markdown/` 的 `.txt` 源通过 Jekyll permalink 输出 Markdown，不能从构建中排除，也不能改成会自动转 HTML 的 `.md` 输入。

发布后用默认 HTML、`Accept: text/markdown`、直接 `index.md`、中英原文及旧技术 URL 分别核验；测试真正不存在的页面返回 404。随后用与基线相同的 `content` 预设重扫；Agent Skills/WebMCP 如需评估，显式加入对应检查。记录时间、检测 URL、实际失败项，不把“静态文件存在”写成“协商已生效”，不把可选草案缺失当成引用下降的证据。

可运行 `python3 scripts/check_agent_http.py --require-edge --output output/agent-readiness/live-http.json` 记录实际 HTTP 检查；本地构建用 `--base-url http://127.0.0.1:4173/`，本地纯静态预览的边缘项会显示 `NOT LIVE`。该脚本没有把本地结果冒充 Cloudflare 官方分数，也不验证真实爬虫身份或原生 WebMCP。

实际效果继续在 Cloudflare AI Crawl Control、搜索站长工具的收录/引用数据和产品入口访问中分开观察；本项目没有伪造实时 GEO 分数。

## 本次本地验收记录

2026-10-23 完成全量 Jekyll 构建，674 份 Markdown 与语义源及最终输出逐字一致，36 个目录目标全部存在，SKILL.md 发布字节摘要正确。中英搜索共 624 条记录、674 个 HTML head/页脚 Markdown 链接核验通过。

原有站点检查仍通过：744 组 JSON-LD、740 个 sitemap URL、180 篇中文教程、128 篇历史技术文章、312 篇完整英文文章、337 组中英互返页面及4个作品视频。Node 检查覆盖协商优先级/通配q值/HEAD/Range/条件请求/私有请求回退与WebMCP接口模拟。

本地 HTTP 检查中 HTML、显式中英 Markdown、阅读目录、robots Content Signals、技能摘要及真实404均通过；纯静态预览的边缘协商/响应头显示 NOT LIVE，符合其尚未部署的状态。GitHub Pages 新版本与 Cloudflare Worker 尚待实际发布和线上复测，不能把本节当作线上成功记录。
