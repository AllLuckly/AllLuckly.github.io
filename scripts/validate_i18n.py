#!/usr/bin/env python3
"""Check built bilingual pages against complete translation pairs, never mirrored prose."""
import argparse
import json
import hashlib
import re
from collections import Counter
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse
from xml.etree import ElementTree as ET
import yaml

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / '_site'
ORIGIN = 'https://allluckly.cn/'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--allow-partial', action='store_true', help='Validate completed pairs while translations are still being prepared.')
args = parser.parse_args()


def frontmatter(path):
    parts = re.split(r'^---\s*$', path.read_text(), maxsplit=2, flags=re.M)
    assert len(parts) == 3, f'missing front matter: {path}'
    return yaml.safe_load(parts[1]) or {}, parts[2]


def absolute(url):
    return urljoin(ORIGIN, url)


def route(url):
    return unquote(urlparse(absolute(url)).path).replace('/index.html', '/')


def target(url):
    path = ROOT / route(url).lstrip('/')
    return next((p for p in (path, path / 'index.html', Path(str(path) + '.html')) if p.is_file()), None)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.lang = None
        self.canonical = []
        self.alternates = {}
        self.entities = []
        self.links = []
        self.collection_links = None
        self._collection_depth = 0
        self.tracks = []
        self.ids = set()
        self.body_text = []
        self.body_tags = Counter()
        self.code = []
        self._body_depth = 0
        self._code_depth = 0
        self._code_buffer = []
        self._ld = False
        self._buffer = ''
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if tag == 'html': self.lang = a.get('lang')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical.append(a['href'])
        if tag == 'link' and a.get('rel') == 'alternate' and a.get('hreflang'):
            assert a['hreflang'] not in self.alternates, f'duplicate hreflang: {a}'
            self.alternates[a['hreflang']] = a['href']
        # Learning paths include task shortcuts before the ordered directory.
        # Compare ItemList order with that directory, not navigation shortcuts.
        if 'series-lessons' in a.get('class', '').split():
            assert self.collection_links is None, 'duplicate lesson directory'
            self.collection_links = []
            self._collection_depth = 1
        elif self._collection_depth and tag not in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'):
            self._collection_depth += 1
        if tag == 'a':
            self.links.append(a.get('href', ''))
            if self._collection_depth: self.collection_links.append(a.get('href', ''))
        if tag == 'track': self.tracks.append(a)
        if a.get('id'): self.ids.add(a['id'])
        if tag == 'script' and a.get('type') == 'application/ld+json': self._ld = True; self._buffer = ''
        if 'data-article-body' in a:
            assert not self._body_depth, 'nested article body'
            self._body_depth = 1
        elif self._body_depth:
            if tag not in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'):
                self._body_depth += 1
            self.body_tags[tag] += 1
        if self._body_depth and tag == 'code':
            self._code_depth += 1
            if self._code_depth == 1: self._code_buffer = []

    def handle_data(self, text):
        if self._ld: self._buffer += text
        if self._body_depth:
            if self._code_depth: self._code_buffer.append(text)
            else: self.body_text.append(text)

    def handle_endtag(self, tag):
        if tag in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'): return
        if self._collection_depth: self._collection_depth -= 1
        if tag == 'script' and self._ld:
            self.entities.extend(json.loads(self._buffer)['@graph']); self._ld = False
        if tag == 'code' and self._code_depth:
            self._code_depth -= 1
            if not self._code_depth: self.code.append(''.join(self._code_buffer))
        if self._body_depth: self._body_depth -= 1

    def entity(self, kind):
        found = [e for e in self.entities if e['@type'] == kind]
        assert len(found) == 1, f'expected one {kind}, got {len(found)}'
        return found[0]


pages = {p: Page(p.read_text()) for p in ROOT.rglob('*.html')}
mapping_path = REPO / '_data/translations.yml'
assert mapping_path.is_file(), 'translation manifest is missing'
mapping = yaml.safe_load(mapping_path.read_text()) or {}
complete = {key: pair for key, pair in mapping.items() if pair.get('status') == 'complete'}
technical_metadata_en = yaml.safe_load((REPO / '_data/technical_articles_en.yml').read_text()) or {}
assert complete, 'no complete translation pairs'
english_urls = [absolute(pair['en_url']) for pair in complete.values()]
assert len(set(map(route, english_urls))) == len(english_urls), 'duplicate English destination'
assert len(set(route(pair['zh_url']) for pair in complete.values())) == len(complete), 'duplicate original destination'
sitemap = {n.text for n in ET.parse(ROOT / 'sitemap.xml').findall('./{*}url/{*}loc')}

for key, pair in complete.items():
    zh_url, en_url = absolute(pair['zh_url']), absolute(pair['en_url'])
    assert route(key) == route(zh_url), f'manifest key differs from original: {key}'
    assert not route(zh_url).startswith('/en/') and route(en_url).startswith('/en/'), key
    zh_file, en_file = target(zh_url), target(en_url)
    assert zh_file in pages and en_file in pages, f'complete pair must exist: {key}'
    zh, en = pages[zh_file], pages[en_file]
    assert zh.lang == 'zh-CN' and en.lang == 'en', f'HTML language differs: {key}'
    expected_alternates = {'zh-CN': zh_url, 'en': en_url}
    assert zh.alternates == en.alternates == expected_alternates, f'hreflang must be self-inclusive and reciprocal: {key}'
    assert zh.canonical == [zh_url] and en.canonical == [en_url], f'self canonical differs: {key}'
    assert zh_url in sitemap and en_url in sitemap, f'published pair absent from sitemap: {key}'
    assert route(en_url) in {route(x) for x in zh.links}, f'Chinese page needs a visible English switch: {key}'
    assert route(zh_url) in {route(x) for x in en.links}, f'English page needs its original: {key}'

sources = {}
for path in (REPO / '_posts').glob('*.md'):
    fields, _ = frontmatter(path)
    if fields.get('published') is not False and fields.get('layout') in ('guide', 'post', 'work'):
        sources[str(path.relative_to(REPO))] = fields
translations = {}
for path in (REPO / '_translations').rglob('*'):
    if not path.is_file() or path.suffix not in ('.html', '.md', '.markdown'): continue
    fields, body = frontmatter(path)
    if fields.get('published') is False: continue
    source_path = fields.get('source_path')
    assert source_path in sources, f'unknown original: {path}'
    assert source_path not in translations, f'duplicate translation: {source_path}'
    translations[source_path] = fields
    assert fields.get('lang') == 'en' and fields.get('translation_date'), f'language/date missing: {path}'
    assert fields.get('translation_source_sha256') == hashlib.sha256((REPO / source_path).read_bytes()).hexdigest(), f'English edition predates an original-source change: {path}'
    assert fields['layout'] == sources[source_path]['layout'], f'translation changed article type: {path}'
    pair = next((p for p in complete.values() if p.get('source_path') == source_path), None)
    assert pair and route(fields['permalink']) == route(pair['en_url']), f'unlisted or incomplete translation: {path}'
    assert route(fields['source_url']) == route(pair['zh_url']), f'wrong original URL: {path}'
    zh, en = pages[target(pair['zh_url'])], pages[target(pair['en_url'])]
    original, translated = zh.entity('BlogPosting'), en.entity('BlogPosting')
    assert translated['inLanguage'] == 'en' and translated['headline'] == fields['title'], path
    assert translated['translationOfWork']['@id'] == absolute(pair['zh_url']) + '#article', path
    assert translated['datePublished'] == original['datePublished'], f'original date changed: {path}'
    assert datetime.fromisoformat(translated['dateModified']) >= datetime.fromisoformat(translated['datePublished']), f'translation update predates original publication: {path}'
    assert translated.get('author') == original.get('author'), f'original attribution changed: {path}'
    assert translated.get('citation') == original.get('citation'), f'original source changed: {path}'
    assert translated.get('about', {}).get('@id') == original.get('about', {}).get('@id'), f'entity association changed: {path}'
    assert zh.code == en.code, f'code spans/blocks changed: {path}'
    for tag in ('h2', 'h3', 'h4', 'p', 'li', 'td', 'th', 'blockquote', 'table', 'img', 'pre'):
        assert zh.body_tags[tag] == en.body_tags[tag], f'body structure changed ({tag}): {path}'
    source_text, english_text = ''.join(zh.body_text).strip(), ''.join(en.body_text).strip()
    assert english_text and english_text != source_text, f'English page mirrors original prose: {path}'
    assert len(re.findall(r'[A-Za-z]', english_text)) >= min(80, len(source_text)), f'English prose missing: {path}'
    if fields['layout'] == 'guide':
        for field in ('app_id', 'series_order'):
            assert fields[field] == sources[source_path][field], f'learning route changed: {path}'
    if fields['layout'] == 'post':
        metadata = fields.get('technical_translation') or technical_metadata_en.get(source_path, {})
        assert metadata.get('summary') and metadata.get('credit') and metadata.get('keywords'), f'English technical metadata missing: {path}'
        assert translated['description'] == metadata['summary'] and translated['keywords'] == metadata['keywords'], path
    if fields['layout'] == 'work':
        video, original_video = en.entity('VideoObject'), zh.entity('VideoObject')
        for field in ('contentUrl', 'thumbnailUrl', 'uploadDate', 'duration', 'inLanguage'):
            assert video[field] == original_video[field], f'underlying recording changed ({field}): {path}'
        chapters = fields['video'].get('chapters', [])
        assert [c['start'] for c in chapters] == [c['startOffset'] for c in original_video.get('hasPart', [])], path
        assert [c['name'] for c in video.get('hasPart', [])] == [c['title'] for c in chapters], path
        for chapter, clip in zip(chapters, video.get('hasPart', [])):
            assert clip['url'] == absolute(pair['en_url']) + '?t=' + str(chapter['start']) + '#work-video', path
        captions = fields['video'].get('captions')
        assert captions and fields['video'].get('captions_lang') == 'en', f'English subtitles missing: {path}'
        assert video['caption']['inLanguage'] == 'en' and video['caption']['contentUrl'] == absolute(captions), path
        assert any(t.get('srclang') == 'en' and absolute(t.get('src', '')) == absolute(captions) for t in en.tracks), path
        caption_file = target(captions)
        assert caption_file and caption_file.read_text(encoding='utf-8-sig').startswith('WEBVTT'), f'invalid captions: {path}'
        original_caption_file = target(original_video['caption']['contentUrl'])
        timing = r'^((?:\d{2}:)?\d{2}:\d{2}\.\d{3}) --> ((?:\d{2}:)?\d{2}:\d{2}\.\d{3})'
        english_cues = re.findall(timing, caption_file.read_text(), re.M)
        assert english_cues == re.findall(timing, original_caption_file.read_text(), re.M), f'subtitle timing changed: {path}'

if not args.allow_partial:
    assert set(translations) == set(sources), f'full translation coverage missing: {set(sources) - set(translations)}'

# Both languages describe the same six products; each directory lists only its own language.
apps = yaml.safe_load((REPO / '_data/apps.yml').read_text())
product_ids = {absolute(a['url']) + '#app' for a in apps}
for path, page in pages.items():
    if page.lang != 'en': continue
    for entity in page.entities:
        if entity['@type'] == 'SoftwareApplication': assert entity['@id'] in product_ids, path
        if entity['@type'] == 'CollectionPage':
            items = entity['mainEntity']['itemListElement']
            assert [i['position'] for i in items] == list(range(1, len(items) + 1)), path
            expected_routes = [route(item['url']) for item in items]
            directory_links = page.collection_links if page.collection_links is not None else page.links
            actual_routes = list(dict.fromkeys(route(link) for link in directory_links if route(link) in set(expected_routes)))
            assert actual_routes == expected_routes, f'collection order differs from visible links: {path}'
            for item in items:
                assert route(item['url']).startswith('/en/') and target(item['url']), f'cross-language collection: {path}'
                assert route(item['url']) in {route(link) for link in page.links}, f'nonvisible collection item: {path}'
        if entity['@type'] == 'BreadcrumbList':
            assert all(route(c['item']).startswith('/en/') and target(c['item']) for c in entity['itemListElement']), path

video_entries = ET.parse(ROOT / 'video-sitemap.xml').findall('./{*}url')
expected_watch_pages = {absolute(f['permalink']) for f in sources.values() if f['layout'] == 'work'}
expected_watch_pages |= {absolute(f['permalink']) for f in translations.values() if f['layout'] == 'work'}
assert Counter(e.findtext('{*}loc') for e in video_entries) == Counter(expected_watch_pages), 'video sitemap must cover both watch-page languages'
for entry in ET.parse(ROOT / 'en/feed.xml').findall('./{*}entry'):
    assert route(entry.findtext('{*}id')).startswith('/en/'), 'English feed contains a Chinese article'
for entry in ET.parse(ROOT / 'feed.xml').findall('./{*}entry'):
    assert not route(entry.findtext('{*}id')).startswith('/en/'), 'Chinese feed contains a translated article'
print(f'PASS: {len(complete)} reciprocal language pairs, {len(translations)}/{len(sources)} complete English articles, preserved code/attribution/dates, localized collections and captions')
