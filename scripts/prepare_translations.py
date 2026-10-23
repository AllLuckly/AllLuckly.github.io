#!/usr/bin/env python3
"""Extract/cache/render complete static translations; publishing needs no translator.

Use `extract` after export_i18n_sources.rb; fill the reviewed cache before `render`.
Missing strings are errors, never a reason to copy Chinese prose to an English URL.
The rendering stage does not make network requests or overwrite editorial work.
"""
import argparse
import hashlib
import html as html_lib
import json
import re
import unicodedata
from copy import deepcopy
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

import yaml
from bs4 import BeautifulSoup, Comment, NavigableString

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/bilingual'
CACHE = ROOT / '_i18n/zh-en.json'
OVERRIDES = ROOT / '_i18n/editorial-overrides.json'
HAN = re.compile(r'[\u3400-\u9fff]')
SKIP_TAGS = ('pre', 'code', 'script', 'style')
BLOCK_TAGS = ('p', 'li', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'figcaption')
METADATA_FIELDS = ('title', 'description', 'topic', 'level', 'keywords', 'image_alt', 'recording_note')
IGNORED_FIELDS = ('excerpt', 'slug', 'ext', 'path', 'draft', 'headline', 'featured', 'comments', 'mathjax', 'tags', 'categories')


def read_json(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default


def read_yaml(path, default=None):
    return yaml.safe_load(path.read_text()) if path.exists() else default


def frontmatter(path):
    parts = re.split(r'^---\s*$', path.read_text(), maxsplit=2, flags=re.M)
    if len(parts) != 3:
        return {}, ''
    return yaml.safe_load(parts[1]) or {}, parts[2]


def source_rows():
    rows = read_json(OUT / 'posts-source.json')
    if not rows:
        raise SystemExit('Run bundle exec ruby scripts/export_i18n_sources.rb after building the originals.')
    for row in rows:
        actual = hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest()
        if row.get('source_sha256') != actual:
            raise SystemExit(f"Source changed; rebuild Jekyll and re-export originals: {row['path']}")
    return sorted(rows, key=lambda r: ({'guide': 0, 'post': 1, 'work': 2}[r['data']['layout']], r['path']))


def translation_cache():
    """Editorial metadata also supplies exact translations for article link labels."""
    result = {**read_json(CACHE, {}), **read_json(ROOT / '_i18n/glossary.json', {})}
    for part in sorted((ROOT / '_i18n/segments').glob('*.json')):
        for key, value in read_json(part, {}).items():
            if key in result and result[key] != value:
                raise ValueError(f'Conflicting translation segment {key} in {part}')
            result[key] = value
    result.update(read_json(OVERRIDES, {}))
    guides = read_yaml(ROOT / '_data/guide_metadata_en.yml', {})
    legacy = read_yaml(ROOT / '_data/technical_articles_en.yml', {})
    for row in source_rows():
        reviewed = guides.get(row['path'], legacy.get(row['path'], {}))
        if reviewed and reviewed.get('source_sha256') != row['source_sha256']:
            raise SystemExit(f"English metadata needs review after original changed: {row['path']}")
        for field in METADATA_FIELDS:
            source, translated = row['data'].get(field), reviewed.get(field)
            if isinstance(source, str) and isinstance(translated, str):
                result[source.strip()] = translated.strip()
    return result


def source_body(row):
    snapshot = OUT / 'source-html' / (Path(row['path']).stem + '.html')
    html = BeautifulSoup(Path(row['destination']).read_text(), 'html.parser')
    article = html.select_one('[data-article-body]')
    if article is None:
        raise ValueError(f"Missing rendered body: {row['path']}")
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    snapshot.write_text(article.decode_contents())
    return BeautifulSoup(article.decode_contents(), 'html.parser')


def text_nodes(soup):
    for node in soup.find_all(string=True):
        if isinstance(node, Comment) or node.find_parent(SKIP_TAGS):
            continue
        if HAN.search(str(node)):
            yield node


def english_word_boundaries(soup, preserved_nodes=None):
    """Chinese needs no spaces around inline tags; English does. Never edit code."""
    nodes = [n for n in soup.find_all(string=True) if not isinstance(n, Comment)]
    preserved_nodes = preserved_nodes or set()
    for index in range(len(nodes) - 1):
        left, right = nodes[index:index + 2]
        if not str(left) or not str(right): continue
        block = left.find_parent(BLOCK_TAGS)
        if block is None or block is not right.find_parent(BLOCK_TAGS): continue
        if not ((str(left)[-1].isalnum() or str(left)[-1] in ':;!?)]') and str(right)[0].isalnum()): continue
        if not left.find_parent(SKIP_TAGS) and id(left) not in preserved_nodes:
            replacement = NavigableString(str(left) + ' ')
            left.replace_with(replacement)
            nodes[index] = replacement
        elif not right.find_parent(SKIP_TAGS) and id(right) not in preserved_nodes:
            replacement = NavigableString(' ' + str(right))
            right.replace_with(replacement)
            nodes[index + 1] = replacement


def contextual_paragraphs(body, source_path):
    """Reviewed whole sentences handle old prose split across inline code tags."""
    entries = read_json(ROOT / '_i18n/paragraph-overrides.json', {}).get(source_path, {})
    for path in sorted((ROOT / '_i18n/paragraph-overrides').glob('*.json')):
        for key, value in read_json(path, {}).get(source_path, {}).items():
            if key in entries and entries[key] != value:
                raise ValueError(f'Conflicting paragraph override in {source_path}: {key}')
            entries[key] = value
    found = set()
    for element in body.find_all(BLOCK_TAGS):
        key = hashlib.sha256(str(element).encode()).hexdigest()[:16]
        if key not in entries: continue
        found.add(key)
        codes = element.find_all('code')
        for tag in element.find_all(True):
            if tag.name not in ('code', 'br') and not tag.find_parent('code'):
                raise ValueError(f'Whole-paragraph override would drop markup in {source_path}: {key}')
        text = entries[key]
        if re.findall(r'\[\[CODE(\d+)\]\]', text) != [str(i) for i in range(len(codes))]:
            raise ValueError(f'Code markers changed in {source_path}: {key}')
        replacement = html_lib.escape(text)
        for i, code in enumerate(codes): replacement = replacement.replace(f'[[CODE{i}]]', str(code))
        content = BeautifulSoup(replacement, 'html.parser')
        element.clear()
        for node in list(content.contents): element.append(node)
    if found != set(entries): raise ValueError(f'Stale paragraph overrides in {source_path}: {set(entries) - found}')


def metadata_strings(data):
    for key in METADATA_FIELDS:
        value = data.get(key)
        if isinstance(value, str) and HAN.search(value):
            yield value
        elif isinstance(value, list):
            yield from (x for x in value if isinstance(x, str) and HAN.search(x))
    video = data.get('video', {})
    for key in ('name', 'description'):
        if HAN.search(video.get(key, '')):
            yield video[key]
    yield from (c['title'] for c in video.get('chapters', []) if HAN.search(c['title']))


def normalize_date(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def english_routes(rows):
    """Lock readable English routes separately from completion status.

    A trailing slash also avoids Jekyll collection extension inference for old
    titles containing a period, e.g. the Chinese article about .a static files.
    """
    path = ROOT / '_data/translation_routes.yml'
    routes = read_yaml(path, {})
    legacy = read_yaml(ROOT / '_data/technical_articles_en.yml', {})
    for row in rows:
        if row['url'] in routes: continue
        if row['data']['layout'] == 'post':
            title = legacy[row['path']]['title']
            ascii_title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode()
            slug = re.sub(r'[^a-z0-9]+', '-', ascii_title.lower()).strip('-')[:110].rstrip('-')
            routes[row['url']] = '/en/journal/' + str(row['data']['date'])[:10] + '-' + slug + '/'
        else:
            routes[row['url']] = '/en' + row['url'].replace('/index.html', '/')
    if len(set(routes.values())) != len(routes):
        raise ValueError('English route collision; resolve explicitly in translation_routes.yml')
    path.write_text(yaml.safe_dump(routes, allow_unicode=True, sort_keys=False, width=160))
    return routes


def editorial_sources():
    result = {}
    for path in (ROOT / '_translations').glob('*'):
        if path.suffix not in ('.html', '.md', '.markdown'):
            continue
        fields, _ = frontmatter(path)
        if fields.get('translation_method') == 'editorial':
            original = ROOT / fields['source_path']
            current = hashlib.sha256(original.read_bytes()).hexdigest()
            if fields.get('translation_source_sha256') != current:
                raise SystemExit(f'Editorial article needs review after original changed: {path}')
            result[fields['source_path']] = (fields, path)
    return result


def extract():
    strings = {}
    editorial = editorial_sources()
    legacy_en = read_yaml(ROOT / '_data/technical_articles_en.yml', {})
    for row in source_rows():
        if row['path'] in editorial or row['data']['layout'] == 'work':
            continue
        fields = row['data']
        # Legacy titles and metadata are edited independently, with attribution.
        if fields['layout'] != 'post':
            for text in metadata_strings(fields):
                strings.setdefault(text.strip(), {'kind': 'metadata', 'source': row['path']})
        elif row['path'] not in legacy_en:
            strings.setdefault(fields['title'].strip(), {'kind': 'title', 'source': row['path']})
        body = source_body(row)
        for node in text_nodes(body):
            strings.setdefault(str(node).strip(), {'kind': 'body', 'source': row['path']})
        for element in body.find_all(True):
            for attr in ('alt', 'title', 'aria-label'):
                value = element.get(attr, '')
                if HAN.search(value):
                    strings.setdefault(value.strip(), {'kind': 'attribute', 'source': row['path']})
    cache = translation_cache()
    queue = [{'id': hashlib.sha256(text.encode()).hexdigest()[:16], 'text': text, **context}
             for text, context in strings.items() if text not in cache and hashlib.sha256(text.encode()).hexdigest()[:16] not in cache]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'translation-queue.json').write_text(json.dumps(queue, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(strings)} unique strings, {len(queue)} uncached, {sum(len(q["text"]) for q in queue)} characters.')


def translation_manifest():
    pairs = {}
    for path in sorted((ROOT / 'en').rglob('*')):
        if not path.is_file():
            continue
        fields, _ = frontmatter(path)
        if fields.get('lang') == 'en' and fields.get('source_url') and fields.get('permalink'):
            zh_url = fields['source_url'].replace('/index.html', '/')
            pairs[zh_url] = {'zh_url': zh_url, 'en_url': fields['permalink'], 'status': 'complete', 'title_en': fields['title']}
    for path in sorted((ROOT / '_translations').glob('*')):
        if path.suffix not in ('.html', '.md', '.markdown'):
            continue
        fields, _ = frontmatter(path)
        if fields.get('lang') == 'en' and fields.get('source_url'):
            zh_url = fields['source_url']
            pairs[zh_url] = {'zh_url': zh_url, 'en_url': fields['permalink'], 'source_path': fields['source_path'],
                             'status': 'complete', 'title_en': fields['title']}
    (ROOT / '_data/translations.yml').write_text(yaml.safe_dump(pairs, allow_unicode=True, sort_keys=False, width=110))
    print(f'{len(pairs)} complete reciprocal pairs in manifest.')
    return pairs


def render(allow_partial=False):
    cache = translation_cache()
    legacy = read_yaml(ROOT / '_data/technical_articles_en.yml', {})
    updates = read_yaml(ROOT / '_data/technical_updates_en.yml', {})
    glossary = read_json(ROOT / '_i18n/glossary.json', {})
    preserved = {}
    for path in sorted((ROOT / '_i18n/preserved').glob('*.json')):
        preserved.update(read_json(path, {}))
    editorial = editorial_sources()
    rows = source_rows()
    routes = english_routes(rows)
    route_map = {unquote(row['url']): routes[row['url']] for row in rows}
    for path in (ROOT / 'en').rglob('*'):
        if path.is_file():
            f, _ = frontmatter(path)
            if f.get('source_url'): route_map[unquote(f['source_url']).replace('/index.html', '/')] = f['permalink']

    def translate(text):
        if not isinstance(text, str) or not HAN.search(text):
            return text
        trimmed = text.strip()
        segment_id = hashlib.sha256(trimmed.encode()).hexdigest()[:16]
        result = cache.get(trimmed, cache.get(segment_id))
        if not result or not isinstance(result, str) or (result.strip() == trimmed and glossary.get(trimmed) != trimmed and segment_id not in preserved):
            raise KeyError(trimmed)
        if segment_id in preserved:
            rule = preserved[segment_id]
            if isinstance(rule, dict):
                if not rule.get('reason') or not rule.get('verbatim'): raise ValueError(f'Incomplete code-preservation rule: {segment_id}')
                for snippet in rule['verbatim']:
                    if not snippet or snippet not in text or snippet not in result:
                        raise ValueError(f'Literal code snippet was modified: {segment_id}')
            else:
                if result.strip() != trimmed: raise ValueError(f'Preserved source segment was modified: {segment_id}')
                return text
        return text[:len(text)-len(text.lstrip())] + result + text[len(text.rstrip()):]

    def localized_link(href):
        parts = urlsplit(href)
        if parts.netloc and parts.netloc not in ('allluckly.cn', 'www.allluckly.cn'):
            return href
        destination = route_map.get(unquote(parts.path).replace('/index.html', '/'))
        if destination:
            return urlunsplit(('', '', destination, parts.query, parts.fragment))
        return href

    dest = ROOT / '_translations'
    dest.mkdir(exist_ok=True)
    written, pending = 0, []
    for row in rows:
        if row['path'] in editorial:
            written += 1
            continue
        fields = {k: deepcopy(v) for k, v in row['data'].items() if k not in IGNORED_FIELDS}
        if fields['layout'] == 'work':
            pending.append(row['path'])
            continue
        try:
            if fields['layout'] == 'post':
                if row['path'] not in legacy: raise KeyError('reviewed legacy metadata')
                fields['technical_translation'] = legacy[row['path']]
                fields['title'] = legacy[row['path']]['title']
                fields['description'] = legacy[row['path']]['summary']
                fields['category'] = 'Development notes'
                if row['path'] in updates: fields['technical_update_translation'] = updates[row['path']]
            else:
                for key in METADATA_FIELDS:
                    if key in fields:
                        fields[key] = [translate(t) for t in fields[key]] if isinstance(fields[key], list) else translate(fields[key])
                fields['category'] = 'Tutorials'
            body = source_body(row)
            contextual_paragraphs(body, row['path'])
            preserved_nodes = set()
            for node in list(text_nodes(body)):
                segment_id = hashlib.sha256(str(node).strip().encode()).hexdigest()[:16]
                replacement = NavigableString(translate(str(node)))
                node.replace_with(replacement)
                if segment_id in preserved: preserved_nodes.add(id(replacement))
            for node in list(body.find_all(string=True)):
                if not isinstance(node, Comment) and not node.find_parent(SKIP_TAGS) and id(node) not in preserved_nodes and not HAN.search(str(node)):
                    localized = str(node).translate(str.maketrans({'，': ', ', '。': '.', '；': '; ', '：': ': ', '？': '?', '！': '!', '、': ', ', '（': '(', '）': ')'}))
                    if localized != str(node): node.replace_with(NavigableString(localized))
            english_word_boundaries(body, preserved_nodes)
            for element in body.find_all(True):
                for attr in ('alt', 'title', 'aria-label'):
                    if attr in element.attrs: element[attr] = translate(element[attr])
                if element.name == 'a' and element.get('href'):
                    element['href'] = localized_link(element['href'])
        except KeyError as missing:
            pending.append(row['path'])
            stale = dest / (Path(row['path']).stem + '.html')
            if stale.exists():
                archive = OUT / 'stale-translations'
                archive.mkdir(exist_ok=True)
                stale.replace(archive / stale.name)
            if not allow_partial: raise SystemExit(f'Missing translation for {row["path"]}: {str(missing)[:160]}')
            continue
        fields.update(lang='en', source_path=row['path'], source_url=row['url'], permalink=routes[row['url']],
                      translation_method='machine-assisted',
                      translation_source_sha256=hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest())
        fields['excerpt'] = fields.get('description', fields['title'])
        for key in ('date', 'modified'): fields[key] = normalize_date(fields.get(key))
        if fields.get('modified') is None: fields.pop('modified', None)
        html = str(body).replace('{% endraw %}', '&#123;% endraw %}')
        body_output = '\n{% raw %}\n' + html + '\n{% endraw %}\n'
        translated_path = dest / (Path(row['path']).stem + '.html')
        previous_fields, previous_body = frontmatter(translated_path) if translated_path.exists() else ({}, '')
        previous_date = previous_fields.pop('translation_date', '')
        unchanged = previous_fields == fields and previous_body == body_output and 'T' in str(previous_date)
        fields['translation_date'] = previous_date if unchanged else datetime.now(timezone.utc).isoformat(timespec='seconds')
        output = '---\n' + yaml.safe_dump(fields, allow_unicode=True, sort_keys=False, width=110) + '---' + body_output
        translated_path.write_text(output)
        written += 1
    translation_manifest()
    print(f'{written}/{len(rows)} full English articles; {len(pending)} pending.')
    if pending and not allow_partial: raise SystemExit('Incomplete English article coverage.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('extract', 'render', 'manifest'))
    parser.add_argument('--allow-partial', action='store_true', help='Development only: keep incomplete articles unpublished.')
    args = parser.parse_args()
    if args.action == 'extract': extract()
    elif args.action == 'manifest': translation_manifest()
    else: render(args.allow_partial)
