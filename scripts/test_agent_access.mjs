import assert from 'node:assert/strict';
import {handle, wantsMarkdown, markdownPath} from '../cloudflare/agent-access.mjs';

assert.equal(wantsMarkdown('text/markdown'), true);
assert.equal(wantsMarkdown('text/html, text/markdown;q=0.2'), false);
assert.equal(wantsMarkdown('text/markdown;q=0, */*'), false);
assert.equal(wantsMarkdown('*/*'), false);
assert.equal(wantsMarkdown('text/markdown;q=broken'), false);
assert.equal(wantsMarkdown('text/markdown;q=0.2, text/*;q=1'), false);
assert.equal(wantsMarkdown('text/markdown;q=0.2, */*;q=1'), false);
assert.equal(wantsMarkdown('text/markdown;q=0.2, text/html;q=0, text/*;q=1'), true);
assert.equal(markdownPath('/'), '/index.md');
assert.equal(markdownPath('/en/index.html'), '/en/index.md');
assert.equal(markdownPath('/legacy/article.a文件'), '/legacy/article.a文件/index.md');

const requests = [];
let missing = false;
const mockFetch = async request => {
  requests.push(request);
  if (new URL(request.url).pathname.endsWith('/index.md')) return new Response(missing ? '<h1>Not found</h1>' : '# A real article\n\nFull text.', {status: missing ? 404 : 200, headers: {'Content-Type': missing ? 'text/html' : 'text/plain', 'Vary': 'Accept-Encoding', ETag: '"markdown-v1"'}});
  return new Response('<h1>A real article</h1>', {headers: {'Content-Type': 'text/html', 'Vary': 'Accept-Encoding', 'Link': '</feed.xml>; rel="alternate"; type="application/atom+xml"', 'X-Frame-Options': 'DENY'}});
};
const req = (path, headers = {}, method = 'GET') => new Request('https://allluckly.cn' + path, {headers, method});

const article = '/en/guides/vectorpaint-getting-started/';
let result = await handle(req(article + '?utm_source=reader', {Accept: 'text/markdown'}), mockFetch);
assert.match(result.headers.get('Content-Type'), /^text\/markdown/);
assert.match(result.headers.get('Vary'), /Accept-Encoding, Accept/);
assert.match(result.headers.get('Link'), /en\/guides\/vectorpaint-getting-started\/index.md/);
assert.match(result.headers.get('Content-Signal'), /ai-input=yes/);
assert.match(await result.text(), /^# A real article/);
assert.equal(requests.at(-1).url, 'https://allluckly.cn/en/guides/vectorpaint-getting-started/index.md');
assert.equal(requests.at(-1).headers.has('Cookie'), false);

result = await handle(req(article, {Accept: 'text/html'}), mockFetch);
assert.match(await result.text(), /^<h1>/);
assert.match(result.headers.get('Link'), /feed.xml/);
assert.equal(result.headers.get('X-Frame-Options'), 'DENY');

missing = true;
result = await handle(req(article, {Accept: 'text/markdown'}), mockFetch);
assert.match(result.headers.get('Content-Type'), /^text\/html/);
assert.match(await result.text(), /^<h1>/);
missing = false;

result = await handle(req('/en/', {Accept: 'text/markdown'}, 'HEAD'), mockFetch);
assert.match(result.headers.get('Content-Type'), /^text\/markdown/);
assert.equal(await result.text(), '');

for (const headers of [{Accept:'text/markdown', Cookie:'session=private'}, {Accept:'text/markdown', Authorization:'Bearer private'}]) {
  const before = requests.length;
  await handle(req('/en/', headers), mockFetch);
  assert.equal(requests.length, before + 1);
  assert.equal(requests.at(-1).url, 'https://allluckly.cn/en/');
}
for (const headers of [{Accept:'text/markdown', Range:'bytes=0-10'}, {Accept:'text/markdown', 'If-None-Match':'"markdown-v1"'}]) {
  const before = requests.length;
  const value = await handle(req('/en/', headers), mockFetch);
  assert.equal(requests.length, before + 1);
  assert.equal(requests.at(-1).url, 'https://allluckly.cn/en/index.md');
  for (const name of ['Range', 'If-None-Match']) if (headers[name]) assert.equal(requests.at(-1).headers.get(name), headers[name]);
  assert.match(value.headers.get('Content-Type'), /^text\/markdown/);
}
// Route membership keeps nonexistent Markdown URLs out of discovery headers.
result = await handle(req('/not-generated/', {Accept:'text/markdown'}), mockFetch);
assert.doesNotMatch(result.headers.get('Link'), /rel="alternate"; type="text\/markdown"/);
// Direct Markdown access links to the precise canonical, including old URLs
// without a trailing slash; the old article is not silently renamed.
const old = '/cocoapods/CocoaPods%E5%AE%89%E8%A3%85%E5%8F%8A%E4%BD%BF%E7%94%A8';
result = await handle(req(old + '/index.md'), mockFetch);
assert.ok(result.headers.get('Link').includes(`<https://allluckly.cn${old}>; rel="canonical"`));
const before = requests.length;
await handle(req('/en/', {}, 'POST'), mockFetch);
assert.equal(requests.length, before + 1);
assert.equal(requests.at(-1).method, 'POST');
console.log('PASS: Markdown negotiation, HTML preference, q=0, missing-page fallback, headers, HEAD, private/conditional/range requests and non-GET passthrough');
