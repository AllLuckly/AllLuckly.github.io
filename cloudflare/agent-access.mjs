/** Serve the same public content as HTML or its committed Markdown representation.
 * Deploy on allluckly.cn/* as a Cloudflare Worker route in front of GitHub Pages.
 * No user-agent detection, crawler exemptions, external requests or AI conversion.
 */
import manifest from '../agent-markdown/manifest.json' with {type: 'json'};

const POLICY = 'search=yes, ai-input=yes, ai-train=no';
const ORIGIN = 'https://allluckly.cn';
const pages = new Map();
for (const [canonical, markdown] of Object.entries(manifest.routes)) {
  const page = {canonical: new URL(canonical, ORIGIN).href, markdown: new URL(markdown, ORIGIN).href};
  pages.set(new URL(canonical, ORIGIN).pathname, page);
  pages.set(new URL(markdown, ORIGIN).pathname, page);
}

export function wantsMarkdown(accept = '') {
  const ranges = accept.toLowerCase().split(',').map(part => {
    const [type, ...params] = part.trim().split(';');
    const quality = params.find(value => value.trim().startsWith('q='));
    const q = quality ? Number(quality.trim().slice(2)) : 1;
    return {type: type.trim(), q: Number.isFinite(q) && q >= 0 && q <= 1 ? q : 0};
  });
  const markdown = Math.max(0, ...ranges.filter(r => r.type === 'text/markdown').map(r => r.q));
  // The most specific range sets HTML quality, including an explicit q=0.
  // A broad text/* or */* preference must not lose to a lower-q Markdown range.
  const htmlRanges = ['text/html', 'text/*', '*/*'].map(type => ranges.filter(r => r.type === type));
  const matchingHtml = htmlRanges.find(group => group.length) || [];
  const html = Math.max(0, ...matchingHtml.map(r => r.q));
  return markdown > 0 && markdown >= html;
}

export function markdownPath(path) {
  if (path.endsWith('/index.html')) path = path.slice(0, -10);
  return path.replace(/\/$/, '') + '/index.md';
}

function addVary(headers, name) {
  const values = (headers.get('Vary') || '').split(',').map(x => x.trim()).filter(Boolean);
  if (!values.some(value => value.toLowerCase() === name.toLowerCase()) && !values.includes('*')) values.push(name);
  headers.set('Vary', values.join(', '));
}

function decorate(response, url, markdown, head, page) {
  const headers = new Headers(response.headers);
  // The site's declared policy also prevents the converter's permissive default
  // from accidentally granting training permission for attributed guest posts.
  headers.set('Content-Signal', POLICY);
  if (markdown) {
    headers.set('Content-Type', 'text/markdown; charset=utf-8');
    headers.set('X-Robots-Tag', 'noindex, follow');
  }
  if (/text\/html|text\/markdown/i.test(headers.get('Content-Type') || '')) {
    addVary(headers, 'Accept');
    const links = ['</sitemap.xml>; rel="sitemap"; type="application/xml"', '</llms.txt>; rel="describedby"; type="text/plain"', '</.well-known/agent-skills/index.json>; rel="describedby"; type="application/json"'];
    if (page && response.status < 400) {
      links.unshift(`<${page.canonical}>; rel="canonical"`);
      if (!url.pathname.endsWith('/index.md')) links.push(`<${page.markdown}>; rel="alternate"; type="text/markdown"`);
    }
    const prior = headers.get('Link');
    headers.set('Link', [prior, ...links].filter(Boolean).join(', '));
  }
  return new Response(head ? null : response.body, {status: response.status, statusText: response.statusText, headers});
}

export async function handle(request, originFetch = fetch) {
  const url = new URL(request.url);
  if (url.origin !== ORIGIN || !['GET', 'HEAD'].includes(request.method)) return originFetch(request);
  const head = request.method === 'HEAD';
  const page = pages.get(url.pathname.replace(/\/index\.html$/, '/'));
  // Preserve assets, feeds, private resources and conditional/range semantics.
  // Generated Markdown is public; never forward cookies or authorization to a
  // different resource, and never convert personalized or partial responses.
  const asset = /\.(?:xml|json|txt|md|vtt|mp4|webm|png|jpe?g|gif|webp|avif|svg|ico|css|js|mjs|woff2?|ttf|pdf|zip)$/i.test(url.pathname);
  const personal = request.headers.has('Authorization') || request.headers.has('Cookie');
  if (personal) return originFetch(request);
  if (page && !asset && wantsMarkdown(request.headers.get('Accept') || '')) {
    const headers = new Headers(request.headers);
    headers.set('Accept', 'text/plain');
    let converted;
    try {
      converted = await originFetch(new Request(page.markdown, {method: request.method, headers, redirect: 'manual'}));
    } catch {
      // Markdown is an optional representation: a transient mirror fetch failure
      // must not prevent a reader from receiving the original HTML page.
    }
    const type = converted?.headers.get('Content-Type') || '';
    // A missing resource or an HTML error fallback must never be advertised as Markdown.
    if (converted && ((converted.status === 304) || ([200, 206].includes(converted.status) && /^(text\/(plain|markdown)|application\/octet-stream)(;|$)/i.test(type)))) {
      // Bytes are the stored Markdown resource itself, so its own ETag,
      // Last-Modified and range headers remain valid (unlike HTML conversion).
      return decorate(converted, url, true, head, page);
    }
  }
  const response = await originFetch(request);
  const directMarkdown = page && asset && url.pathname.endsWith('/index.md') && response.status < 400 && /^(text\/(plain|markdown)|application\/octet-stream)(;|$)/i.test(response.headers.get('Content-Type') || '');
  return decorate(response, url, directMarkdown, head, page);
}

export default {fetch(request) {return handle(request);}};
