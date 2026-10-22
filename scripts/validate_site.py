#!/usr/bin/env python3
"""Check built metadata and internal links for the new app/tutorial experience."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1] / '_site'
class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.links=[]; self.graphs=[]; self.canonical=[]; self.h1=0; self.ld=False; self.buf=''
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='h1': self.h1+=1
        if tag=='script' and attrs.get('type')=='application/ld+json': self.ld=True; self.buf=''
        if tag=='link' and attrs.get('rel')=='canonical': self.canonical.append(attrs['href'])
        if tag in ['a','img','script','link']:
            value=attrs.get('href') or attrs.get('src')
            if value: self.links.append(value)
    def handle_data(self, data):
        if self.ld: self.buf+=data
    def handle_endtag(self, tag):
        if tag=='script' and self.ld:
            self.graphs.append(json.loads(self.buf)); self.ld=False

def target(url):
    route=unquote(urlparse(url).path).lstrip('/')
    path=ROOT/route
    return next((x for x in [path,path/'index.html',Path(str(path)+'.html')] if x.is_file()),None)

pages={p:Page(p.read_text()) for p in ROOT.rglob('*.html')}
graph_count=sum(len(p.graphs) for p in pages.values())
assert graph_count>0
sitemap=ElementTree.parse(ROOT/'sitemap.xml')
urls=[n.text for n in sitemap.findall('.//{*}loc')]
assert len(urls)==len(set(urls)), 'duplicate sitemap entries'
for url in urls:
    assert url.startswith('https://allluckly.cn/') and ' ' not in url, url
    file=target(url); assert file, f'sitemap target missing: {url}'
    assert pages[file].canonical==[url], f'canonical differs: {url}'
ElementTree.parse(ROOT/'feed.xml')
new=[ROOT/'index.html',ROOT/'about/index.html',ROOT/'journal/index.html']+list((ROOT/'apps').rglob('*.html'))+list((ROOT/'guides').rglob('*.html'))
for file in new:
    page=pages[file]; assert page.h1==1, f'expected one h1: {file}'
    for url in page.links:
        parsed=urlparse(url)
        if parsed.netloc and parsed.netloc!='allluckly.cn': continue
        if parsed.scheme in ['mailto','tel'] or not parsed.path: continue
        assert target(url), f'broken internal link in {file}: {url}'
apps=[]; articles=[]
for file,page in pages.items():
    for graph in page.graphs:
        for entity in graph['@graph']:
            if entity['@type']=='SoftwareApplication': apps.append(entity)
            if entity['@type']=='BlogPosting' and 'about' in entity: articles.append(entity)
assert len(apps)==3 and len(articles)==3
app_ids={app['@id'] for app in apps}
for article in articles:
    assert article['about']['@id'] in app_ids
    assert article['author']['name']=='Bison'
for app in apps:
    assert 'aggregateRating' not in app and 'offers' not in app
    assert app['downloadUrl'].startswith('https://apps.apple.com/cn/app/id')
print(f'PASS: {graph_count} JSON-LD graphs, {len(urls)} sitemap URLs, Atom feed, {len(new)} new/updated pages and 3 app/tutorial relationships')
