import assert from 'node:assert/strict';
import {handle} from '../cloudflare/agent-access.mjs';

// Repair only origin-404 trailing-slash aliases of explicit manifest HTML pages.
// The old Search Console URL ends in /, while its existing canonical does not.
const origin = 'https://allluckly.cn';
const legacy = new URL('/ios支付/iOS开发2015年最新内购教程', origin).pathname;
const query = '?ref=a%2Fb&x=1&x=2';
const notFound = () => new Response('Origin not found', {
  status: 404, headers: {'Content-Type': 'text/html'},
});
const request = (path, options) => new Request(origin + path, options);

for (const [alias, canonical] of [[legacy + '/', legacy], ['/guides', '/guides/']]) {
  for (const method of ['GET', 'HEAD']) {
    for (const accept of ['text/html', 'text/markdown']) {
      const original = request(alias + query, {method, headers: {Accept: accept}});
      let calls = 0;
      const result = await handle(original, async received => {
        calls++;
        assert.equal(received, original);
        return notFound();
      });
      assert.equal(calls, 1);
      assert.equal(result.status, 301);
      assert.equal(result.headers.get('Location'), origin + canonical + query);
      assert.equal(await result.text(), '');
    }
  }
}

// Known aliases do not replace successful pages, errors other than 404, or
// existing origin redirects. HTTPS upgrading still applies to origin Location.
for (const status of [200, 206, 301, 302, 303, 307, 308, 403, 404, 500]) {
  const result = await handle(request(legacy + '/'), async () => new Response('Origin body', {
    status, headers: {'Content-Type': 'text/html', Location: 'http://allluckly.cn/guides/?ref=a%2Fb'},
  }));
  assert.equal(result.status, status);
  assert.equal(await result.text(), 'Origin body');
  assert.equal(result.headers.get('Location'), [301, 302, 303, 307, 308].includes(status)
    ? origin + '/guides/?ref=a%2Fb' : 'http://allluckly.cn/guides/?ref=a%2Fb');
}

// Never guess a homepage or parent destination. Canonicals, unknown URLs,
// asset paths and Markdown representations keep their real origin 404.
for (const path of [
  '/', legacy, '/guides/', '/ios', '/ios/', '/unknown/', '/guides/no-such-tutorial/',
  legacy + '//', legacy + '/index.md', legacy + '/index.md/',
  '/assets/images/apps/icouldplay.png', '/assets/images/apps/icouldplay.png/',
  '/robots.txt', '/sitemap.xml', '/auth.md',
]) {
  const result = await handle(request(path, {headers: {Accept: 'text/html'}}), async () => notFound());
  assert.equal(result.status, 404, path);
  assert.equal(result.headers.has('Location'), false, path);
  assert.equal(await result.text(), 'Origin not found', path);
}

// Personalized requests and writes keep their existing passthrough behavior.
for (const headers of [{Cookie: 'session=private'}, {Authorization: 'Bearer private'}]) {
  const original = request(legacy + '/' + query, {headers});
  const response = notFound();
  const result = await handle(original, async received => {
    assert.equal(received, original);
    return response;
  });
  assert.equal(result, response);
}
for (const method of ['POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']) {
  const original = request(legacy + '/', {method});
  const response = notFound();
  const result = await handle(original, async received => {
    assert.equal(received, original);
    return response;
  });
  assert.equal(result, response);
}

// Preserve the pre-existing HTTP-to-HTTPS upgrade, with path and query intact.
const result = await handle(new Request('http://allluckly.cn' + legacy + '/' + query), () => {
  assert.fail('The HTTP upgrade must not fetch the origin');
});
assert.equal(result.status, 301);
assert.equal(result.headers.get('Location'), origin + legacy + '/' + query);

console.log('PASS: only manifest HTML trailing-slash aliases with origin 404 redirect; queries, canonical URLs, true 404s, assets, Markdown, private requests, writes and existing HTTPS upgrades are preserved');
