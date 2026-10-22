#!/usr/bin/env python3
"""Check built metadata and internal links for the new app/tutorial experience."""
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
from xml.etree import ElementTree
import yaml

ROOT = Path(__file__).resolve().parents[1] / '_site'
class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.links=[]; self.graphs=[]; self.canonical=[]; self.h1=0; self.ld=False; self.buf=''; self.ids=set(); self.filter_items=[]
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if attrs.get('id'): self.ids.add(attrs['id'])
        if attrs.get('data-filter-item'): self.filter_items.append(attrs['data-filter-item'])
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
        if parsed.fragment and target(url) in pages:
            assert unquote(parsed.fragment) in pages[target(url)].ids, f'broken fragment in {file}: {url}'
apps=[]; articles=[]
for file,page in pages.items():
    for graph in page.graphs:
        for entity in graph['@graph']:
            if entity['@type']=='SoftwareApplication': apps.append(entity)
            if entity['@type']=='BlogPosting' and 'about' in entity: articles.append(entity)
assert len(apps)==3
app_ids={app['@id'] for app in apps}
article_counts=Counter(article['about']['@id'] for article in articles)
assert set(article_counts)==app_ids and min(article_counts.values())>=20, f'expected at least 20 tutorials per app: {article_counts}'
for article in articles:
    assert article['about']['@id'] in app_ids
    assert article['author']['name']=='Bison'
for app in apps:
    assert 'aggregateRating' not in app and 'offers' not in app
    assert app['downloadUrl'].startswith('https://apps.apple.com/cn/app/id')
source_guides=[]
for source in (ROOT.parent/'_posts').glob('*.md'):
    text=source.read_text()
    if not re.search(r'^layout:\s*[\'\"]?guide[\'\"]?\s*$',text,re.M): continue
    front,body=text.split('---',2)[1:]
    fields=yaml.safe_load(front)
    for key in ['title','description','permalink','app_id','series_order','topic','reading_time']:
        assert fields.get(key), f'missing {key}: {source}'
    assert isinstance(fields['reading_time'],int) and fields['reading_time']>0, f'invalid reading time: {source}'
    assert len(re.findall(r'[\u4e00-\u9fff]',body))>=1500, f'tutorial needs more detail: {source.name}'
    assert len(re.findall(r'^## ',body,re.M))>=5, f'tutorial needs task sections: {source.name}'
    assert len(re.findall(r'/guides/[a-z0-9-]+/',body))>=2, f'tutorial needs related reading: {source.name}'
    source_guides.append(fields)
assert len(source_guides)==len(articles), 'published guide count differs from source'
assert len({g['permalink'] for g in source_guides})==len(source_guides), 'duplicate tutorial URL'
assert len({g['title'] for g in source_guides})==len(source_guides), 'duplicate tutorial title'
for app in ['pastel','man_yue','draw_illustration']:
    orders=sorted(int(g['series_order']) for g in source_guides if g['app_id']==app)
    assert orders==list(range(1,len(orders)+1)), f'nonsequential learning route: {app}'
assert Counter(pages[ROOT/'index.html'].filter_items)==Counter({'pastel':2,'man_yue':2,'draw_illustration':2}), 'homepage must introduce all apps'
assert len(pages[ROOT/'guides/index.html'].filter_items)==len(articles), 'directory must link every tutorial'
for slug,app in [('aquarell','pastel'),('manyue','man_yue'),('vectorpaint','draw_illustration')]:
    assert pages[ROOT/f'guides/{slug}/index.html'].filter_items==[app]*sum(g['app_id']==app for g in source_guides)
print(f'PASS: {graph_count} JSON-LD graphs, {len(urls)} sitemap URLs, Atom feed, {len(new)} new/updated pages, {len(articles)} detailed tutorials and 3 complete learning routes')
