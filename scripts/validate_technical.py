#!/usr/bin/env python3
"""Validate legacy article attribution, dates, navigation and topic discovery."""
import json
import re
from collections import Counter
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse, urljoin
from xml.etree import ElementTree
import yaml

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / '_site'
ORIGIN = 'https://allluckly.cn/'
metadata = yaml.safe_load((REPO / '_data/technical_articles.yml').read_text())
updates = yaml.safe_load((REPO / '_data/technical_updates.yml').read_text())
topics = yaml.safe_load((REPO / '_data/technical_topics.yml').read_text())
topic_by_id = {topic['id']: topic for topic in topics}

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ld = False; self.buffer = ''; self.entities = []; self.h1 = 0
        self.descriptions = []; self.canonicals = []; self.text = []; self.links = []; self.images = []
        self.feed(text)
    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if tag == 'h1': self.h1 += 1
        if tag == 'meta' and a.get('name') == 'description': self.descriptions.append(a['content'])
        if tag == 'link' and a.get('rel') == 'canonical': self.canonicals.append(a['href'])
        if tag == 'a': self.links.append(a.get('href', ''))
        if tag == 'img': self.images.append(a.get('src', ''))
        if tag == 'script' and a.get('type') == 'application/ld+json': self.ld = True; self.buffer = ''
    def handle_data(self, value):
        if self.ld: self.buffer += value
        else: self.text.append(value)
    def handle_endtag(self, tag):
        if tag == 'script' and self.ld:
            self.entities.extend(json.loads(self.buffer)['@graph']); self.ld = False

def target(url):
    path = ROOT / unquote(urlparse(url).path).lstrip('/')
    return next((p for p in [path, path / 'index.html', Path(str(path) + '.html')] if p.is_file()), None)

pages = {path: Page(path.read_text()) for path in ROOT.rglob('*.html')}
articles = {}
for path, page in pages.items():
    for entity in page.entities:
        if entity['@type'] == 'BlogPosting': articles[entity['headline']] = (path, page, entity)
sources = {}
for source in (REPO / '_posts').glob('*.md'):
    fields = yaml.safe_load(source.read_text().split('---', 2)[1])
    if fields.get('layout') == 'post': sources[str(source.relative_to(REPO))] = fields
assert set(sources) == set(metadata), 'legacy metadata must cover exactly the legacy sources'
assert len({m['summary'] for m in metadata.values()}) == len(metadata), 'duplicate summaries'
sitemap = ElementTree.parse(ROOT / 'sitemap.xml')
lastmods = {n.findtext('{*}loc'): n.findtext('{*}lastmod') for n in sitemap.findall('{*}url')}
expected_topics = {topic['id']: [] for topic in topics}

for source, fields in sources.items():
    m = metadata[source]; topic = topic_by_id[m['topic']]
    assert len(m['summary']) >= 30 and m['summary'] != m.get('author_name'), source
    assert 3 <= len(m['keywords']) <= 6 and len(set(m['keywords'])) == len(m['keywords']), source
    assert m['credit'] and m['provenance'] in ['original', 'contribution', 'translation', 'collection', 'archive'], source
    path, page, article = articles[fields['title']]
    visible = ' '.join(' '.join(page.text).split())
    assert page.h1 == 1, f'multiple article headings: {source}'
    assert page.descriptions == [m['summary']] and article['description'] == m['summary'], source
    assert m['summary'] in visible and m['credit'] in visible, f'hidden metadata: {source}'
    assert page.canonicals == [article['url']] and article['url'] in lastmods, source
    assert article['keywords'] == m['keywords'] and article['articleSection'] == topic['name'], source
    assert article['about']['@id'] == urljoin(ORIGIN, topic['url']) + '#topic', source
    assert 'image' not in article, f'theme banner used as article image: {source}'
    if m.get('author_name'):
        assert article['author']['name'] == m['author_name'], source
        assert article['author']['@type'] == m.get('author_type', 'Person'), source
    else:
        assert 'author' not in article, f'guessed author: {source}'
    if m.get('source_url'):
        assert article['citation'] == m['source_url'] and m['source_url'] in page.links, source
    match = re.match(r'_posts/(\d{4})-(\d{1,2})-(\d{1,2})-', source)
    original_date = '-'.join([match[1], match[2].zfill(2), match[3].zfill(2)])
    assert article['datePublished'][:10] == original_date, f'publication date changed: {source}'
    expected_modified = str(updates[source]['updated']) if source in updates else original_date
    assert article['dateModified'][:10] == expected_modified and lastmods[article['url']] == article['dateModified'], source
    if source in updates:
        assert updates[source]['note'] in visible and '阅读说明补充于' in visible, source
        for ref in updates[source]['references']: assert ref['url'] in page.links, source
    crumbs = next(e for e in page.entities if e['@type'] == 'BreadcrumbList')['itemListElement']
    assert [c['name'] for c in crumbs] == ['首页', '开发笔记', topic['name'], fields['title']], source
    assert [c['position'] for c in crumbs] == [1, 2, 3, 4], source
    for crumb in crumbs:
        assert target(crumb['item']), f'broken breadcrumb: {source}'
    assert urljoin(ORIGIN, topic['url']) in [urljoin(ORIGIN, u) for u in page.links], source
    assert all('/_posts/' not in u for u in page.images), f'legacy page.path image error: {source}'
    for link in page.links + page.images:
        parsed = urlparse(urljoin(article['url'], link))
        if parsed.scheme in ['http', 'https'] and parsed.netloc == 'allluckly.cn' and parsed.path:
            assert target(parsed.geturl()), f'broken local reference in {source}: {link}'
    expected_topics[m['topic']].append(article['url'])

all_urls = [url for urls in expected_topics.values() for url in urls]
for url, expected in [('/journal/', all_urls)] + [(t['url'], expected_topics[t['id']]) for t in topics]:
    page = pages[target(url)]
    assert page.h1 == 1, url
    collection = next(e for e in page.entities if e['@type'] == 'CollectionPage')
    listed = collection['mainEntity']['itemListElement']
    assert Counter(e['url'] for e in listed) == Counter(expected), f'topic schema mismatch: {url}'
    assert [e['position'] for e in listed] == list(range(1, len(listed)+1)), url
    links = {urljoin(ORIGIN, u) for u in page.links}
    assert set(expected) <= links, f'topic articles must be static links: {url}'
    for link in page.links:
        parsed = urlparse(link)
        if parsed.scheme in ['', 'http', 'https'] and parsed.netloc in ['', 'allluckly.cn'] and parsed.path:
            assert target(link), f'broken topic link: {link}'

print(f'PASS: {len(sources)} legacy articles, {len(topics)} topic collections, exact author/source attribution, unchanged publication dates, {len(updates)} visible reading updates and static discovery links')
