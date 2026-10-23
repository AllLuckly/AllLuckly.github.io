#!/usr/bin/env python3
"""Build small, hierarchical llms.txt reading indexes from the built bilingual site.

Run after Jekyll and export_i18n_sources.rb. Canonical URLs, visible titles,
descriptions and publication dates come from built HTML; Jekyll's exported post
inventory supplies article identities, layouts and lesson order. Language routes
come exclusively from _data/translations.yml. No URL slug is synthesized.

The Markdown representation contract is canonical_path.rstrip('/') + '/index.md'.
This applies to the historical extensionless article URLs too. llms.txt files are
plain static assets, with no Jekyll front matter, Liquid, or concatenated bodies.

    python3 scripts/build_agent_indexes.py
    python3 scripts/build_agent_indexes.py --check
    python3 scripts/build_agent_indexes.py --check --check-markdown

Design reference: https://blog.cloudflare.com/agent-readiness/
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
BRAND_SOURCES = (
    'https://github.com/AllLuckly/AllLuckly.github.io/blob/master/_data/apps.yml',
    'https://github.com/AllLuckly/AllLuckly.github.io/blob/master/_data/apps_en.yml',
)


def text(value) -> str:
    """Keep metadata on one line without losing punctuation or literal brackets."""
    return re.sub(r'\s+', ' ', unescape(str(value or ''))).strip()


def label(value) -> str:
    return text(value).replace('\\', '\\\\').replace('[', '\\[').replace(']', '\\]')


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def path_key(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.query or parsed.fragment:
        raise ValueError(f'Page URL must not contain query or fragment: {url}')
    route = unquote(parsed.path)
    if not route.startswith('/') or '..' in route.split('/'):
        raise ValueError(f'Invalid absolute page path: {url}')
    return route


def markdown_url(url: str) -> str:
    return url.rstrip('/') + '/index.md'


def directory_url(url: str) -> str:
    return url.rstrip('/') + '/llms.txt'


class Head(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.canonicals = []
        self.meta = {}
        self.lang = ''
        self.graph = []
        self.json_ld = None
        self.feed(source.partition('</head>')[0])

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang', '')
        elif tag == 'link' and 'canonical' in attrs.get('rel', '').split():
            self.canonicals.append(attrs.get('href', ''))
        elif tag == 'meta':
            self.meta[attrs.get('name') or attrs.get('property')] = attrs.get('content', '')
        elif tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.json_ld = ''

    def handle_data(self, data):
        if self.json_ld is not None:
            self.json_ld += data

    def handle_endtag(self, tag):
        if tag == 'script' and self.json_ld is not None:
            document = json.loads(self.json_ld)
            self.graph.extend(document.get('@graph', [document]) if isinstance(document, dict) else document)
            self.json_ld = None


@dataclass(frozen=True)
class Page:
    url: str
    title: str
    description: str
    lang: str
    published: str = ''
    modified: str = ''


class Indexes:
    def __init__(self, site_dir: Path):
        config = read_yaml(ROOT / '_config.yml')
        self.origin = config['url'].rstrip('/')
        baseurl = config.get('baseurl', '') or ''
        if baseurl:
            raise ValueError('This site uses root canonical paths; a baseurl needs an explicit route migration.')
        self.site_dir = site_dir
        self.pairs = read_yaml(ROOT / '_data/translations.yml')
        self.apps = {a['id']: a for a in read_yaml(ROOT / '_data/apps.yml')}
        self.apps_en = {a['id']: a for a in read_yaml(ROOT / '_data/apps_en.yml')}
        self.topics = read_yaml(ROOT / '_data/technical_topics.yml')
        self.topics_en = {t['id']: t for t in read_yaml(ROOT / '_data/technical_topics_en.yml')}
        self.technical = read_yaml(ROOT / '_data/technical_articles.yml')
        self.technical_en = read_yaml(ROOT / '_data/technical_articles_en.yml')
        self.posts = json.loads((ROOT / 'output/bilingual/posts-source.json').read_text())
        self.pages = {}
        self.outputs = {}
        self.markdown_targets = set()
        self.index_targets = set()
        self.english_by_zh = {}
        self._read_pages()
        self._check_inputs()

    def _read_pages(self):
        if not self.site_dir.is_dir():
            raise ValueError(f'Build the site first: {self.site_dir} is missing')
        for file in sorted(self.site_dir.rglob('*.html')):
            head = Head(file.read_text(encoding='utf-8'))
            if not head.canonicals:
                continue
            if len(head.canonicals) != 1:
                raise ValueError(f'Expected one canonical URL: {file}')
            url = head.canonicals[0]
            if urlsplit(url).netloc != urlsplit(self.origin).netloc:
                raise ValueError(f'Unexpected canonical origin in {file}: {url}')
            # Percent-encode Unicode paths while retaining existing canonical URL identity.
            route = path_key(url)
            canonical = self.origin + quote(route, safe="/:@-._~!$&'()*+,;=")
            articles = [g for g in head.graph if isinstance(g, dict) and g.get('@type') == 'BlogPosting']
            article = articles[0] if articles else {}
            page = Page(canonical, text(head.meta.get('og:title')),
                        text(head.meta.get('description')), head.lang,
                        text(article.get('datePublished')), text(article.get('dateModified')))
            if route in self.pages:
                raise ValueError(f'Duplicate built canonical URL: {url}')
            self.pages[route] = page

    def _check_inputs(self):
        if set(self.apps) != set(self.apps_en):
            raise ValueError('Chinese and English app identities do not match')
        if {t['id'] for t in self.topics} != set(self.topics_en):
            raise ValueError('Chinese and English technical topics do not match')
        zh_routes, en_routes = [], []
        for source, pair in self.pairs.items():
            if pair.get('status') != 'complete':
                raise ValueError(f'Incomplete language pair must not enter public agent indexes: {source}')
            if path_key(source) != path_key(pair['zh_url']):
                raise ValueError(f'Mismatched Chinese route in language map: {source}')
            self.page(pair['zh_url'], 'zh')
            self.page(pair['en_url'], 'en')
            self.english_by_zh[path_key(pair['zh_url'])] = pair['en_url']
            zh_routes.append(path_key(pair['zh_url']))
            en_routes.append(path_key(pair['en_url']))
        if len(zh_routes) != len(set(zh_routes)):
            raise ValueError('Duplicate Chinese URLs in the language map')
        if len(en_routes) != len(set(en_routes)):
            raise ValueError('Duplicate English URLs in the language map')
        counts = Counter(row['data']['layout'] for row in self.posts)
        if set(counts) != {'guide', 'post', 'work'}:
            raise ValueError(f'Unexpected article layouts: {counts}')
        if len({row['path'] for row in self.posts}) != len(self.posts):
            raise ValueError('Duplicate source identities in post inventory')
        if len({path_key(row['url']) for row in self.posts}) != len(self.posts):
            raise ValueError('Duplicate canonical article URLs in post inventory')
        for row in self.posts:
            pair = self.pairs.get(row['url'])
            if not pair or pair.get('source_path') != row['path']:
                raise ValueError(f'Post inventory and language map disagree: {row["path"]}')
            for language in ('zh', 'en'):
                page = self.local_page(row['url'], language)
                if not page.published:
                    raise ValueError(f'Built article has no original publication date: {page.url}')
                original_date = text(row['data']['date'])[:10]
                if page.published[:10] != original_date:
                    raise ValueError(f'Built article changed its original publication date: {page.url}')
        post_paths = {r['path'] for r in self.posts if r['data']['layout'] == 'post'}
        if post_paths != set(self.technical) or post_paths != set(self.technical_en):
            raise ValueError('Technical metadata must cover the exact historical post inventory')
        for app_id in self.apps:
            lessons = self.lessons(app_id)
            positions = [r['data']['series_order'] for r in lessons]
            if positions != list(range(1, len(lessons) + 1)):
                raise ValueError(f'Lesson order is incomplete or duplicated: {app_id}')

    def page(self, route: str, lang: str) -> Page:
        page = self.pages.get(path_key(route))
        if not page or not page.title or not page.description:
            raise ValueError(f'Missing built page, title or description: {route}')
        expected = 'en' if lang == 'en' else 'zh'
        if not page.lang.lower().startswith(expected):
            raise ValueError(f'Wrong built language: {route} ({page.lang})')
        return page

    def local_page(self, zh_route: str, lang: str) -> Page:
        if lang == 'en':
            route = self.english_by_zh.get(path_key(zh_route))
            if not route:
                raise ValueError(f'Missing English counterpart: {zh_route}')
            return self.page(route, lang)
        return self.page(zh_route, lang)

    def link(self, page: Page, *, index=False, title=None, detail=None):
        url = directory_url(page.url) if index else markdown_url(page.url)
        (self.index_targets if index else self.markdown_targets).add(url)
        return f'- [{label(title or page.title)}]({url}): {text(detail or page.description)}'

    def emit(self, page: Page, sections):
        lines = [f'# {page.title}', '', f'> {page.description}', '']
        for heading, content in sections:
            if heading:
                lines.extend([f'## {heading}', ''])
            lines.extend(content)
            lines.append('')
        path = Path(path_key(directory_url(page.url)).lstrip('/'))
        if path in self.outputs:
            raise ValueError(f'An index would be emitted twice: {path}')
        self.outputs[path] = '\n'.join(lines).rstrip() + '\n'

    def lessons(self, app_id):
        return sorted((r for r in self.posts if r['data']['layout'] == 'guide' and r['data'].get('app_id') == app_id),
                      key=lambda r: (r['data']['series_order'], r['url']))

    @staticmethod
    def boundaries(lang):
        if lang == 'en':
            return ['These are guides and product information from Bison, the developer of the six apps; they are not independent reviews or rankings.',
                    'Markdown is another representation of the same HTML content. Read feature limits, source attributions and version notes in the linked page. English pages are translations of the Chinese originals.']
        return ['本站作者 Bison 是这六款应用的开发者；这里是开发者撰写的产品介绍、教程与创作记录，不是独立第三方评测或排名。',
                'Markdown 是对应 HTML 页面的另一种表示，内容保持一致。功能边界、原文署名与版本说明以具体页面为准；英文页为中文原文的翻译。']

    @staticmethod
    def history(lang):
        if lang == 'en':
            return ['Historical development notes from 2015–2017. Their original publication dates and source attribution are retained; translation or catalog updates do not make the examples current.',
                    'The examples were not rerun for this reorganization. Old Swift syntax, APIs, dependencies, service addresses and App Store rules may be obsolete; check current official documentation before applying them.']
        return ['这里保留 2015–2017 年的历史技术记录及原文归属。条目日期是本站原始发布日期，翻译或目录整理不表示示例已更新到当前版本。',
                '本次整理未重新运行验证旧示例。旧 Swift 语法、API、依赖、服务地址与审核规则可能过期，实际使用前须对照当前官方文档。']

    def publication(self, page, lang):
        return (f'Originally published: {page.published[:10]}.' if lang == 'en'
                else f'本站原始发布：{page.published[:10]}。')

    def build(self):
        for lang in ('zh', 'en'):
            self.build_language(lang)
        generated_urls = {self.origin + '/' + p.as_posix() for p in self.outputs}
        missing = self.index_targets - generated_urls
        if missing:
            raise ValueError(f'Links to ungenerated subindexes: {sorted(missing)}')
        expected_articles = {markdown_url(self.local_page(row['url'], lang).url)
                             for row in self.posts for lang in ('zh', 'en')}
        if not expected_articles <= self.markdown_targets:
            raise ValueError(f'Articles missing from leaf indexes: {sorted(expected_articles - self.markdown_targets)}')
        return self.outputs

    def build_language(self, lang):
        en = lang == 'en'
        local = lambda route: self.local_page(route, lang)
        home, guides, journal, works, apps, about = [local(r) for r in ('/', '/guides/', '/journal/', '/works/', '/apps/', '/about/')]
        counterpart = self.local_page('/', 'zh' if en else 'en')
        self.emit(home, [
            ('Reading context' if en else '阅读说明', self.boundaries(lang)),
            ('Directories' if en else '按内容进入', [self.link(p, index=True) for p in (guides, apps, works, journal)]),
            ('About and languages' if en else '作者与语言', [self.link(about), self.link(counterpart, index=True)]),
        ])
        self.emit(guides, [
            ('Reading context' if en else '阅读说明', self.boundaries(lang)),
            ('App learning paths' if en else '按应用学习', [self.link(local(a['guide_url']), index=True) for a in self.apps.values()]),
        ])
        for app_id, app in self.apps.items():
            route = local(app['guide_url'])
            app_page = local(app['url'])
            version = f"Version listed: {app['version']}; checked {app['verified']}; {app['os']}." if en else f"目录记录版本：{app['version']}；资料核对：{app['verified']}；{app['os']}。"
            note = ('This is the catalog baseline, not a promise that every release has identical UI. Individual guides specify their own version context.' if en else '这是产品目录的版本基线，不表示所有版本界面完全相同；各篇教程另有资料与版本说明。')
            entries = []
            for row in self.lessons(app_id):
                page = local(row['url'])
                entries.append(self.link(page, title=f"{row['data']['series_order']}. {page.title}",
                                         detail=f'{page.description} {self.publication(page, lang)}'))
            self.emit(route, [
                ('App and version' if en else '应用与版本', [self.link(app_page), version, note]),
                ('Lessons in learning order' if en else '按学习顺序阅读', entries),
            ])
        self.emit(journal, [
            ('Historical context' if en else '历史版本说明', self.history(lang)),
            ('Technical topics' if en else '按技术主题进入', [self.link(local(t['url']), index=True) for t in self.topics]),
        ])
        for topic in self.topics:
            rows = sorted((r for r in self.posts if r['data']['layout'] == 'post' and self.technical[r['path']]['topic'] == topic['id']),
                          key=lambda r: (r['data']['date'], r['url']))
            entries = []
            for row in rows:
                page = local(row['url'])
                metadata = (self.technical_en if en else self.technical)[row['path']]
                details = [page.description, self.publication(page, lang), metadata.get('version_note', ''), metadata.get('credit', '')]
                entries.append(self.link(page, detail=' '.join(text(v) for v in details if v)))
            self.emit(local(topic['url']), [
                ('Historical context' if en else '历史版本说明', self.history(lang)),
                ('Articles by original publication date' if en else '按本站原始发布日期阅读', entries),
            ])
        work_entries = []
        for row in sorted((r for r in self.posts if r['data']['layout'] == 'work'), key=lambda r: (r['data']['date'], r['url']), reverse=True):
            page = local(row['url'])
            # Recording conditions are specific to each work, not inferred from a store version.
            data = row['data']
            if en:
                source = ROOT / '_translations' / (Path(row['path']).stem + '.html')
                if not source.exists():
                    raise ValueError(f'Missing English work source: {source}')
                data = yaml.safe_load(source.read_text(encoding='utf-8').split('---', 2)[1])
            note = text(data.get('recording_note'))
            if not note:
                raise ValueError(f'A creation recording needs its actual build/device note: {row["path"]}')
            work_entries.append(self.link(page, detail=f'{page.description} {self.publication(page, lang)} {note}'))
        self.emit(works, [
            ('Reading context' if en else '阅读说明', self.boundaries(lang) + [
                'Read each recording note for simulator, local-build and editing details; footage does not establish feature parity with the store release.' if en else '模拟器、本地构建与视频剪辑条件见各作品实录说明；演示内容不代表商店所有版本具有完全相同的功能。']),
            ('Creation walkthroughs' if en else '作品与创作过程', work_entries),
        ])
        app_entries = []
        for app_id, app in self.apps.items():
            translated = self.apps_en[app_id]
            page = local(app['url'])
            names = translated['name']
            if app['name'] != names:
                names += f" / {app['name']}"
            alias = f"Product: {names}; internal content key: `{app_id}`; catalog version {app['version']}, checked {app['verified']}." if en else f"产品名：{names}；本站内部关联键：`{app_id}`；目录版本 {app['version']}，核对日期 {app['verified']}。"
            store = f"[{'Official App Store listing' if en else '官方 App Store 页面'}]({app['store_url']})"
            app_entries.append(self.link(page, detail=f'{page.description} {alias} {store}'))
        provenance = ('Internal keys come from the site product catalogs; they are content-association identifiers, not alternative store product names. Product names and store identities are documented by the app pages and their official App Store links.' if en else '内部关联键来自本站产品目录，只用于文章与产品关联，不是商店产品别名。产品名称与商店身份见应用介绍及各自官方 App Store 链接。')
        sources = f"[{'Chinese product data' if en else '中文产品目录源数据'}]({BRAND_SOURCES[0]}) · [{'English product data' if en else '英文产品目录源数据'}]({BRAND_SOURCES[1]})"
        self.emit(apps, [
            ('Authorship and naming' if en else '作者与名称依据', self.boundaries(lang) + [provenance, sources]),
            ('Applications' if en else '应用', app_entries),
        ])

    def check_markdown(self):
        missing = []
        for url in sorted(self.markdown_targets):
            path = self.site_dir / path_key(url).lstrip('/')
            if not path.is_file():
                missing.append(url)
        if missing:
            raise ValueError(f'{len(missing)} linked Markdown representations are missing; generate them first:\n' + '\n'.join(missing[:12]))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--site-dir', type=Path, default=ROOT / '_site', help='Built Jekyll destination (default: _site)')
    parser.add_argument('--check', action='store_true', help='Check generated files without writing; fail if any output is missing or stale')
    parser.add_argument('--check-markdown', action='store_true', help='Also require every linked page/index.md in the built destination')
    args = parser.parse_args()
    try:
        indexes = Indexes(args.site_dir.resolve())
        outputs = indexes.build()
        if args.check_markdown:
            indexes.check_markdown()
        stale = []
        for relative, content in outputs.items():
            destination = ROOT / relative
            if destination.exists() and destination.read_text(encoding='utf-8') == content:
                continue
            stale.append(relative)
            if not args.check:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(content, encoding='utf-8')
        if args.check and stale:
            raise ValueError('Missing or stale agent indexes:\n' + '\n'.join(str(p) for p in stale))
        action = 'Checked' if args.check else 'Generated'
        print(f'{action} {len(outputs)} llms.txt indexes; {len(indexes.markdown_targets)} unique direct Markdown targets; {len(stale)} changed files.')
        return 0
    except (ValueError, KeyError, OSError, json.JSONDecodeError, yaml.YAMLError) as error:
        print(f'Agent index error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
