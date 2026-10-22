#!/usr/bin/env python3
"""Check built metadata and internal links for the new app/tutorial experience."""
import json
import re
from collections import Counter
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote, urljoin
from xml.etree import ElementTree
import yaml

ROOT = Path(__file__).resolve().parents[1] / '_site'
SITE_URL = 'https://allluckly.cn/'
SITEMAP_NS = {'sm':'http://www.sitemaps.org/schemas/sitemap/0.9','video':'http://www.google.com/schemas/sitemap-video/1.1'}
class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.links=[]; self.graphs=[]; self.canonical=[]; self.h1=0; self.ld=False; self.buf=''; self.ids=set(); self.filter_items=[]; self.work_items=[]; self.videos=[]; self.sources=[]; self.tracks=[]; self.robots=[]
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if attrs.get('id'): self.ids.add(attrs['id'])
        if attrs.get('data-filter-item'): self.filter_items.append(attrs['data-filter-item'])
        if attrs.get('data-work-item'): self.work_items.append(attrs['data-work-item'])
        if tag=='video': self.videos.append(attrs)
        if tag=='source': self.sources.append(attrs)
        if tag=='track': self.tracks.append(attrs)
        if tag=='h1': self.h1+=1
        if tag=='script' and attrs.get('type')=='application/ld+json': self.ld=True; self.buf=''
        if tag=='link' and attrs.get('rel')=='canonical': self.canonical.append(attrs['href'])
        if tag=='meta' and attrs.get('name')=='robots': self.robots.append(attrs.get('content',''))
        if tag in ['a','img','script','link','video','source','track']:
            value=attrs.get('href') or attrs.get('src')
            if value: self.links.append(value)
        if tag=='video' and attrs.get('poster'): self.links.append(attrs['poster'])
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
video_sitemap=ElementTree.parse(ROOT/'video-sitemap.xml')
video_sitemap_entries=video_sitemap.findall('sm:url',SITEMAP_NS)
robot_sitemaps=re.findall(r'^Sitemap:\s*(\S+)',(ROOT/'robots.txt').read_text(),re.M)
new=[ROOT/'index.html',ROOT/'about/index.html',ROOT/'journal/index.html']+list((ROOT/'apps').rglob('*.html'))+list((ROOT/'guides').rglob('*.html'))+list((ROOT/'works').rglob('*.html'))
for file in new:
    page=pages[file]; assert page.h1==1, f'expected one h1: {file}'
    for url in page.links:
        parsed=urlparse(url)
        if parsed.netloc and parsed.netloc!='allluckly.cn': continue
        if parsed.scheme in ['mailto','tel'] or not parsed.path: continue
        assert target(url), f'broken internal link in {file}: {url}'
        if parsed.fragment and target(url) in pages:
            assert unquote(parsed.fragment) in pages[target(url)].ids, f'broken fragment in {file}: {url}'
apps=[]; articles=[]; videos=[]
for file,page in pages.items():
    for graph in page.graphs:
        for entity in graph['@graph']:
            if entity['@type']=='SoftwareApplication': apps.append(entity)
            if entity['@type']=='BlogPosting' and 'about' in entity: articles.append(entity)
            if entity['@type']=='VideoObject': videos.append(entity)
assert len(apps)==3
app_ids={app['@id'] for app in apps}
articles=[article for article in articles if article['about'].get('@id') in app_ids]
for article in articles:
    assert article['about']['@id'] in app_ids
    assert article['author']['name']=='Bison'
for app in apps:
    assert 'aggregateRating' not in app and 'offers' not in app
    assert app['downloadUrl'].startswith('https://apps.apple.com/cn/app/id')
source_guides=[]; source_works=[]
for source in (ROOT.parent/'_posts').glob('*.md'):
    text=source.read_text()
    if not re.search(r'^layout:\s*[\'\"]?(guide|work)[\'\"]?\s*$',text,re.M): continue
    front,body=text.split('---',2)[1:]
    fields=yaml.safe_load(front)
    if fields.get('published') is False: continue
    if fields['layout']=='work':
        for key in ['title','description','permalink','app_id','image','video']:
            assert fields.get(key), f'missing {key}: {source}'
        assert fields['permalink'].startswith('/works/'), f'work must have its own route: {source}'
        assert 'series_order' not in fields, f'work must not enter tutorial numbering: {source}'
        assert body.strip(), f'work needs a visible text account: {source}'
        source_works.append(fields)
        continue
    for key in ['title','description','permalink','app_id','series_order','topic','reading_time']:
        assert fields.get(key), f'missing {key}: {source}'
    assert isinstance(fields['reading_time'],int) and fields['reading_time']>0, f'invalid reading time: {source}'
    assert len(re.findall(r'[\u4e00-\u9fff]',body))>=1500, f'tutorial needs more detail: {source.name}'
    assert len(re.findall(r'^## ',body,re.M))>=5, f'tutorial needs task sections: {source.name}'
    assert len(re.findall(r'/guides/[a-z0-9-]+/',body))>=2, f'tutorial needs related reading: {source.name}'
    source_guides.append(fields)
guide_urls={urljoin(SITE_URL,g['permalink']) for g in source_guides}
guide_articles=[article for article in articles if article['url'] in guide_urls]
assert Counter(article['url'] for article in guide_articles)==Counter(guide_urls), 'published guide URLs differ from source'
article_counts=Counter(article['about']['@id'] for article in guide_articles)
assert set(article_counts)==app_ids and min(article_counts.values())>=20, f'expected at least 20 tutorials per app: {article_counts}'
assert len({g['permalink'] for g in source_guides})==len(source_guides), 'duplicate tutorial URL'
assert len({g['title'] for g in source_guides})==len(source_guides), 'duplicate tutorial title'
for app in ['pastel','man_yue','draw_illustration']:
    orders=sorted(int(g['series_order']) for g in source_guides if g['app_id']==app)
    assert orders==list(range(1,len(orders)+1)), f'nonsequential learning route: {app}'
assert Counter(pages[ROOT/'index.html'].filter_items)==Counter({'pastel':2,'man_yue':2,'draw_illustration':2}), 'homepage must introduce all apps'
assert len(pages[ROOT/'guides/index.html'].filter_items)==len(guide_articles), 'directory must link every tutorial'
for slug,app in [('aquarell','pastel'),('manyue','man_yue'),('vectorpaint','draw_illustration')]:
    assert pages[ROOT/f'guides/{slug}/index.html'].filter_items==[app]*sum(g['app_id']==app for g in source_guides)
work_urls={urljoin(SITE_URL,work['permalink']) for work in source_works}
assert len(work_urls)==len(source_works), 'duplicate work URL'
work_articles=[article for article in articles if article['url'] in work_urls]
assert Counter(article['url'] for article in work_articles)==Counter(work_urls), 'published works differ from source'
assert len(videos)==len(source_works), 'each published work must describe one video'
assert Counter(entry.findtext('sm:loc',namespaces=SITEMAP_NS) for entry in video_sitemap_entries)==Counter(work_urls), 'video sitemap differs from published works'
assert (urljoin(SITE_URL,'video-sitemap.xml') in robot_sitemaps)==bool(videos), 'robots must advertise video sitemap only when videos exist'
assert (urljoin(SITE_URL,'works/') in urls)==bool(source_works), 'empty works directory must stay out of sitemap'
assert any('noindex' in value for value in pages[ROOT/'works/index.html'].robots)==(not source_works), 'works directory indexing must follow published content'
assert Counter(pages[ROOT/'works/index.html'].work_items)==Counter(work['permalink'] for work in source_works), 'works directory must link every work'
assert len(pages[ROOT/'index.html'].work_items)==min(2,len(source_works)), 'homepage must show up to two works'

def duration_seconds(value):
    match=re.fullmatch(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?',value)
    assert match and any(match.groups()), f'invalid video duration: {value}'
    hours,minutes,seconds=(float(part or 0) for part in match.groups())
    total=hours*3600+minutes*60+seconds
    assert total>0, f'empty video duration: {value}'
    return total

def caption_seconds(value):
    parts=value.split(':')
    assert len(parts) in [2,3], f'invalid caption time: {value}'
    return sum(float(part)*60**power for power,part in enumerate(reversed(parts)))

for work in source_works:
    video=work['video']; canonical=urljoin(SITE_URL,work['permalink'])
    for key in ['src','poster','name','description','upload_date','duration']:
        assert video.get(key), f'missing video.{key}: {canonical}'
    assert urlparse(video['src']).path.lower().endswith('.mp4'), f'expected MP4 recording: {canonical}'
    seconds=duration_seconds(video['duration'])
    upload=datetime.fromisoformat(str(video['upload_date']).replace('Z','+00:00'))
    assert upload.tzinfo is not None, f'video upload date needs timezone: {canonical}'
    page=pages[target(canonical)]
    assert len(page.videos)==1, f'expected one visible player: {canonical}'
    player=page.videos[0]
    assert 'controls' in player and 'playsinline' in player and 'autoplay' not in player, f'expected user-controlled player: {canonical}'
    assert urljoin(SITE_URL,player.get('poster',''))==urljoin(SITE_URL,video['poster']), f'poster differs: {canonical}'
    assert any(urljoin(SITE_URL,source.get('src',''))==urljoin(SITE_URL,video['src']) and source.get('type')=='video/mp4' for source in page.sources), f'video source differs: {canonical}'
    entities=[entity for entity in videos if entity['@id']==canonical+'#video']
    assert len(entities)==1, f'missing unique VideoObject: {canonical}'
    entity=entities[0]
    for key in ['name','duration']:
        assert entity[key]==video[key], f'VideoObject {key} differs: {canonical}'
    description=' '.join(re.sub(r'<[^>]+>','',video['description']).split())
    assert entity['description']==description, f'VideoObject description differs: {canonical}'
    assert entity['contentUrl']==urljoin(SITE_URL,video['src']), f'VideoObject source differs: {canonical}'
    assert entity['thumbnailUrl']==urljoin(SITE_URL,video['poster']), f'VideoObject poster differs: {canonical}'
    assert datetime.fromisoformat(entity['uploadDate'].replace('Z','+00:00'))==upload, f'VideoObject date differs: {canonical}'
    article=next(article for article in work_articles if article['url']==canonical)
    assert article['video']['@id']==entity['@id'] and article['about']==entity['about'], f'work/video/app relation differs: {canonical}'
    assert entity['mainEntityOfPage']['@id']==canonical, f'video watch page differs: {canonical}'
    assert canonical in urls, f'work missing from sitemap: {canonical}'
    sitemap_entry=next(entry for entry in video_sitemap_entries if entry.findtext('sm:loc',namespaces=SITEMAP_NS)==canonical)
    sitemap_videos=sitemap_entry.findall('video:video',SITEMAP_NS)
    assert len(sitemap_videos)==1, f'expected one sitemap video: {canonical}'
    sitemap_video=sitemap_videos[0]
    for tag,key in [('title','name'),('description','description'),('thumbnail_loc','thumbnailUrl'),('content_loc','contentUrl')]:
        assert sitemap_video.findtext('video:'+tag,namespaces=SITEMAP_NS)==entity[key], f'video sitemap {tag} differs from VideoObject: {canonical}'
    sitemap_date=sitemap_video.findtext('video:publication_date',namespaces=SITEMAP_NS)
    assert datetime.fromisoformat(sitemap_date.replace('Z','+00:00'))==upload, f'video sitemap date differs: {canonical}'
    assert len(description)<=2048, f'video sitemap description is too long: {canonical}'
    if video.get('captions'):
        caption_url=urljoin(SITE_URL,video['captions'])
        assert any(urljoin(SITE_URL,track.get('src',''))==caption_url and track.get('srclang')=='zh-CN' and track.get('kind')=='subtitles' for track in page.tracks), f'caption track differs: {canonical}'
        assert entity['caption']['contentUrl']==caption_url, f'VideoObject captions differ: {canonical}'
        if urlparse(caption_url).netloc=='allluckly.cn':
            caption_file=target(caption_url); assert caption_file, f'missing captions: {canonical}'
            caption_text=caption_file.read_text(encoding='utf-8-sig')
            assert caption_text.startswith('WEBVTT'), f'invalid WebVTT header: {caption_url}'
            cues=re.findall(r'^((?:\d{2}:)?\d{2}:\d{2}\.\d{3}) --> ((?:\d{2}:)?\d{2}:\d{2}\.\d{3})(?:[^\n]*)$',caption_text,re.M)
            assert cues, f'no timed captions: {caption_url}'
            for start,end in cues:
                assert 0<=caption_seconds(start)<caption_seconds(end)<=seconds+1, f'caption outside recording: {caption_url}'
    for asset in [video['src'],video['poster']]:
        absolute=urljoin(SITE_URL,asset)
        if urlparse(absolute).netloc=='allluckly.cn':
            file=target(absolute); assert file and file.stat().st_size>0, f'missing media: {absolute}'
            if asset==video['src']: assert file.stat().st_size<100*1024*1024, f'video exceeds GitHub file limit: {asset}'
for slug,app in [('aquarell','pastel'),('manyue','man_yue'),('vectorpaint','draw_illustration')]:
    expected=Counter(work['permalink'] for work in source_works if work['app_id']==app)
    assert Counter(pages[ROOT/f'apps/{slug}/index.html'].work_items)==expected, f'app work links differ: {app}'
print(f'PASS: {graph_count} JSON-LD graphs, {len(urls)} sitemap URLs, Atom feed, {len(new)} new/updated pages, {len(guide_articles)} detailed tutorials, 3 complete learning routes and {len(videos)} work videos')
