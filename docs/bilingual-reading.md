# 中英文文章与维护

中文原地址继续使用；英文入口为 `/en/`。页面右上角的「中 / EN」直接切换同一页，不强制按浏览器语言跳转。文章全文、目录、上下篇、应用介绍、视频章节、字幕和英文 RSS 使用各自语言。

2026-10-23 首次覆盖 312 篇文章：180 篇教程、128 篇技术归档、4 篇作品；加上 25 个入口与说明页，共 337 组对应页面。

## 内容与索引

- 中文正文保留在 `_posts/`；英文全文放在独立的 `_translations/` collection，避免把中文教程数量和 RSS 翻倍。
- `_data/translations.yml` 记录已完成的对应地址。两边各自 canonical，输出相互对应的 `zh-CN` / `en` hreflang；英文文章以 `translationOfWork` 关联原文。
- 作者、转载来源、首次发布日期、原代码与媒体文件保留。翻译时间独立记录；历史文章的弃用提醒和阅读勘误也有英文版。
- 英文正文的自动翻译会在页面说明。应用英文介绍、文章元数据、九条技术阅读勘误和四部视频的英文步骤另行检查；这不等于所有技术示例已在当前系统重新运行。
- 视频复用原 MP4 和作品 PNG，提供英文与中文字幕。画面仍是实际录制时的中文界面，录屏语言不会误标为英文。
- 作者昵称、既有文件名、中文排版练习中的示例标题以及原代码是内容本身，保留原字样，周围说明译为英文。
- 英文 Atom 为 `/en/feed.xml`，静态搜索数据为 `/en/search.json`。两种语言均进入普通 sitemap；视频 sitemap 收录两种观看页。

## 修改中文之后

英文版是仓库里可审核、可直接部署的静态内容。访客不需要安装翻译工具，线上也不调用翻译 API。新增或修改中文文章后，维护者需要补全相应译文，而不是把中文正文复制到英文地址。

1. 按平常方式构建中文原文，然后导出 Jekyll 实际解析出的地址（旧技术文的 URL 不能仅靠文件名推测）：

   ```sh
   bundle exec jekyll build --trace
   bundle exec ruby scripts/export_i18n_sources.rb
   ```

2. 使用独立 Python 环境安装 `scripts/requirements-i18n.txt`，运行：

   ```sh
   python scripts/prepare_translations.py extract
   ```

   待译文本输出在被 Git 忽略的 `output/bilingual/translation-queue.json`。代码节点跳过，标题、描述与图片替代文本也纳入检查。正文分段翻译缓存位于 `_i18n/segments/`，以源文本的 SHA-256 前 16 位为键；品牌和原作者表在 `_i18n/glossary.json`。旧文跨行内代码拆句的地方，另用 `_i18n/paragraph-overrides/` 和 `paragraph-overrides.json` 保存整段英语，`[[CODE0]]` 等标记按原顺序插回完整代码标签。

3. 完整翻译待译段落并检查上下文。英文句子跨越链接、加粗或行内代码时，要核对语序；不能只看单个片段是否是英语。元数据分别维护在 `guide_metadata_en.yml`、`technical_articles_en.yml`。修改原文后，重新审阅这些数据和手写作品译文，再更新其源文件哈希；不要在未审阅时仅刷新哈希。

4. 生成并检查全文：

   ```sh
   python scripts/prepare_translations.py render
   bundle exec jekyll build --trace
   python scripts/validate_site.py
   python scripts/validate_technical.py
   python scripts/validate_i18n.py
   ```

   `render` 遇到缺译会停止；开发选项 `--allow-partial` 会将过期的自动译文移出发布 collection，不会把缺译内容标为完成。编辑版译文和元数据的源哈希变化会要求重新审阅。HTML 快照每次从最新构建的中文正文提取。

5. 浏览器检查中英文互切、英语断行与正文语序、桌面/手机目录，以及视频字幕和章节。提交完整英文正文、数据、缓存及语言对应表后再部署。

`_i18n/`、`docs/`、`scripts/` 和 `output/` 不作为站点公共页面输出；正常 GitHub Pages 构建只使用已经提交的内容，不下载模型或依赖外部翻译服务。
