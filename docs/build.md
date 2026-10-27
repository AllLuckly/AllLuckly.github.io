# 本地预览与构建

站点使用 Jekyll 3.10，核心 Markdown、Liquid 和语法高亮依赖与 [GitHub Pages 官方版本表](https://pages.github.com/versions/)保持一致。`Gemfile.lock` 记录实际安装版本，请随 `Gemfile` 一起提交。这里只安装本站需要的依赖，无需安装完整的 `github-pages` 插件集合。

本次本地验证环境：Ruby 4.0.1、Bundler 4.0.3、Jekyll 3.10.0。

## 安装

建议使用 Ruby 3.3 或更新版本，并使用项目锁定的 Bundler。macOS 自带的旧 Ruby 不适合这套依赖。若通过 Homebrew 安装 Ruby，先让当前终端找到它：

```sh
export PATH="$(brew --prefix ruby)/bin:$PATH"
ruby --version
bundle --version
```

在仓库目录运行：

```sh
bundle config set --local path vendor/bundle
bundle install
```

依赖仅安装到仓库内的 `vendor/bundle`，无需 `sudo`，也不会改动其他项目的 gem。`.bundle`、`vendor/bundle` 和生成的网站均已忽略。

## 检查与预览

```sh
bundle exec jekyll build --trace
bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

预览地址：<http://127.0.0.1:4000/>。生成文件位于 `_site/`。预览时 URL 与正式域名不同是正常现象；canonical 和结构化数据应继续使用正式域名。

发布前检查首页、六个 App 专题与学习路线、教程详情、`/page2/`、`/sitemap.xml`和 `/robots.txt`。分页由 `jekyll-paginate` 生成，主页必须使用 `index.html`，`paginate_path` 使用 `page:num/`，使分页内链与 canonical 的尾斜线一致；历史 `/pageN` 地址继续由托管服务重定向至 `/pageN/`。

## 常见问题

- 网络环境无法访问 `index.rubygems.org` 时，可尝试 `bundle install --full-index`，直接读取 RubyGems 完整索引。不要关闭 HTTPS 证书校验。
- Ruby 3.4 / 4 移除了部分默认附带的标准库；Gemfile 已显式声明 `base64`、`bigdecimal`、`csv`、`logger` 和本地预览需要的 `webrick`。
- 更新依赖需先核对 GitHub Pages 的版本表，再调整 Gemfile 并运行 `bundle update`，不要直接删除 lock 文件后部署。
- 本地构建不等于线上发布成功。推送后仍须检查 GitHub Pages 的部署结果，并确认最终自定义域名的页面、重定向和抓取入口。

构建后执行 `python3 scripts/validate_site.py`，检查 JSON-LD、sitemap、Atom、应用关系、教程数量、学习阶段覆盖与页面内部链接；再执行 `python3 scripts/validate_technical.py`，检查原技术文章、专题与更新说明。脚本使用 PyYAML 读取文章元数据，缺少时可用 `python3 -m pip install PyYAML==6.0.2` 安装。执行 `node --check assets/js/studio.js` 检查脚本语法。

可使用 `python3 scripts/preview.py` 在 `http://127.0.0.1:4173` 预览生产构建。该服务支持 GitHub Pages 的无扩展名旧文章路径，且不会改变 canonical 的生产域名。

文章或翻译更新后，还需运行 [Agent Readiness 构建与验证流程](agent-readiness.md#更新与验证)，重新生成对应 Markdown、分层阅读目录与技能文件摘要，再进行最终构建。GitHub Pages 直接发布已提交的静态源；不会在服务端替你运行 Python 生成器。

此工作副本采用 Git 稀疏检出，已包含旧文章的 `images/` 与新应用资源，部分历史静态目录仍未展开；它们仍在 Git 仓库中，没有删除。需要完整检出时，可运行 `git sparse-checkout disable`。

## 规范网址与 HTTPS

2026-10-26（Asia/Shanghai）检查 Search Console 时，HTTP 属性报告的「备用网页（有适当的规范标记）」仅涉及 `http://allluckly.cn/`；网址检查显示，用户声明与 Google 选择的规范网址均为 `https://allluckly.cn/`。这是 HTTP 别名被排除，HTTPS 首页仍是预期规范网址。当天已在原报告提交修复验证，界面显示 `Validation started`（Started: 26/10/2026）；最终结果仍由 Google 后续抓取决定。 原账户只有 HTTP 属性，已用现有 HTML 验证文件自动验证并添加 `https://allluckly.cn/` URL-prefix 属性，用于后续查看实际主站数据。已提交 `https://allluckly.cn/sitemap.xml`，Search Console 显示 `Sitemap processed successfully`，发现 750 个线上页面。 HTTPS 首页的 URL Inspection 同时显示 `URL is on Google`、`Page is indexed`，确认主站首页已收录。

修复前，HTTP 首页返回 200，部分 HTTPS 路径补尾斜线时还会重定向至 HTTP。已在线上启用 Cloudflare **Always Use HTTPS**，并发布 Worker 版本 `882f607d`：根域名 HTTP 的 GET/HEAD 请求升级至 HTTPS，源站返回的同主机 HTTP `Location` 也升级为 HTTPS。Cloudflare Single Redirect 规则 **www to canonical HTTPS** 使用条件 `(http.host eq "www.allluckly.cn")`，目标为 `concat("https://allluckly.cn", http.request.uri.path)`，返回 301，并保留查询参数。

Cloudflare SSL/TLS 模式仍为 Flexible：当前源站尚未提供匹配根域名的有效证书，取得并确认有效证书前不要切换至 Full (strict)。本地 `_config.yml` 的导航尾斜线与 `paginate_path: "page:num/"` 已对齐 canonical；这部分配置尚未发布，需要下一次 GitHub Pages 部署后才会在线上生效。

修改后运行以下检查；部署后还需复查 HTTP→HTTPS、www→根域名及补尾斜线的重定向，确认查询参数保留、没有 HTTPS 降级或循环：

```sh
node scripts/test_agent_access.mjs
bundle exec jekyll build --trace
python3 scripts/validate_site.py
```
