// Interface simulations only. Native WebMCP still requires a supporting browser.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import vm from 'node:vm';

const source = await fs.readFile(new URL('../assets/js/agent-search.js', import.meta.url), 'utf8');
const origin = 'https://allluckly.cn';
const article = (title, extra = {}) => ({
  title, description: 'Connect your NAS and read offline.', category: 'Tutorials', app_name: 'ManYue',
  keywords: ['SMB', 'library'], url: '/guides/example/', markdown_url: '/guides/example/index.md',
  date: '2026-10-23', author: 'Bison', version_note: 'Check your app version.', lang: 'en', ...extra,
});
const english = [
  article('SMB setup', {url: '/en/guides/smb/', markdown_url: '/en/guides/smb/index.md'}),
  article('Offline reading', {url: '/en/guides/offline/', keywords: ['NAS', 'download']}),
  article('Reader settings', {description: 'Tune font size.', keywords: ['fonts'], app_name: 'Book Isle'}),
];
const chinese = [article('漫阅 SMB 连接教程', {description: '连接 NAS，离线阅读漫画。', category: '教程',
  url: '/guides/manyue-smb/', markdown_url: '/guides/manyue-smb/index.md', app_name: '漫阅+', lang: 'zh-CN'})];
const jsonResponse = data => ({ok: true, status: 200, json: async () => data});
const flush = () => new Promise(resolve => setImmediate(resolve));

function setup({api = 'document', lang = 'en', fetchImpl, documentContext, navigatorContext} = {}) {
  const registrations = [];
  const calls = [];
  const contextApi = {registerTool(tool) { registrations.push(tool); return Promise.resolve(); }};
  const document = {documentElement: {lang}};
  const navigator = {};
  if (api === 'document') document.modelContext = contextApi;
  if (api === 'navigator') navigator.modelContext = contextApi;
  if (documentContext) document.modelContext = documentContext;
  if (navigatorContext) navigator.modelContext = navigatorContext;
  const context = vm.createContext({
    document, navigator, location: {origin}, URL, Map, Set, DOMException, Promise,
    fetch: async (path, options) => {
      calls.push({path, options});
      return fetchImpl ? fetchImpl(path, options) : jsonResponse(path.startsWith('/en/') ? english : chinese);
    },
  });
  vm.runInContext(source, context, {filename: 'agent-search.js'});
  return {registrations, calls, context, tool: registrations[0]};
}

const unsupported = setup({api: 'none'});
assert.equal(unsupported.registrations.length, 0);
assert.equal(unsupported.calls.length, 0);
assert.equal(unsupported.context.document.modelContext, undefined);
assert.equal(unsupported.context.navigator.modelContext, undefined);

// Registration respects receiver binding and document API precedence.
let documentCalls = 0;
let navigatorCalls = 0;
const current = {registerTool(tool) { assert.equal(this, current); documentCalls++; assert.equal(tool.name, 'search_blog_articles'); }};
const legacy = {registerTool() { navigatorCalls++; }};
setup({documentContext: current, navigatorContext: legacy});
assert.equal(documentCalls, 1);
assert.equal(navigatorCalls, 0);
const brokenLegacy = {};
Object.defineProperty(brokenLegacy, 'registerTool', {get() { throw new Error('Legacy API unavailable'); }});
setup({documentContext: current, navigatorContext: brokenLegacy});
assert.equal(documentCalls, 2); // A working current API never inspects the old registration API.
setup({api: 'none', documentContext: {}, navigatorContext: legacy});
assert.equal(navigatorCalls, 1);
setup({documentContext: {registerTool() { throw new Error('Disabled by browser'); }}});
setup({documentContext: {registerTool() { return Promise.reject(new Error('Disabled by policy')); }}});
await flush(); // Rejected registration is handled, not an unhandled rejection.

const primary = setup();
assert.equal(primary.tool.name, 'search_blog_articles');
assert.equal(primary.tool.inputSchema.additionalProperties, false);
assert.equal(primary.tool.annotations.readOnlyHint, true);
assert.equal(primary.calls.length, 0); // Index fetch is lazy.
const first = await primary.tool.execute({query: '  ＳＭＢ   NAS  ', limit: 10});
assert.equal(first.language, 'en');
assert.equal(first.match_type, 'normalized-keywords');
assert.equal(first.total_matches, 1);
assert.equal(first.returned_count, 1); // No padding to requested limit.
assert.equal(first.results[0].title, 'SMB setup');
assert.equal(first.results[0].url, origin + '/en/guides/smb/');
assert.equal(first.results[0].markdown_url, origin + '/en/guides/smb/index.md');
assert.deepEqual(Object.keys(first.results[0]).sort(),
  ['title', 'url', 'markdown_url', 'description', 'date', 'author', 'version_note', 'app_name', 'lang'].sort());
assert.equal(first.results[0].author, 'Bison');
assert.equal(first.results[0].version_note, 'Check your app version.');
assert.doesNotThrow(() => JSON.stringify(first));
const request = primary.calls[0];
assert.equal(request.path, '/en/search.json');
assert.equal(request.options.credentials, 'omit');
assert.equal(request.options.mode, 'same-origin');
assert.equal(request.options.redirect, 'error');
assert.equal(request.options.method, 'GET');
assert.equal(request.options.body, undefined);
assert.equal(request.options.headers.Accept, 'application/json');
assert.doesNotMatch(JSON.stringify(primary.calls), /SMB|ＳＭＢ|NAS/);
await primary.tool.execute({query: 'font'});
assert.equal(primary.calls.length, 1); // Successful index cache reused.
const empty = await primary.tool.execute({query: 'nonexistent phrase'});
assert.equal(empty.returned_count, 0);
assert.equal(empty.total_matches, 0);
assert.equal(empty.results.length, 0);
const zh = await primary.tool.execute({query: '漫阅 NAS', language: 'zh-CN'});
assert.equal(zh.results[0].title, '漫阅 SMB 连接教程');
assert.equal(zh.results[0].lang, 'zh-CN');
assert.equal(primary.calls.at(-1).path, '/search.json');
assert.equal(zh.results[0].date, '2026-10-23');

const compatible = setup({api: 'navigator', lang: 'zh-CN'});
assert.equal(compatible.registrations.length, 1);
assert.equal(compatible.tool.inputSchema.properties.language.default, 'zh-CN');
assert.equal((await compatible.tool.execute({query: '漫画'})).returned_count, 1);
assert.equal(compatible.calls[0].path, '/search.json');
const englishPage = setup({lang: 'en-GB'});
assert.equal(englishPage.tool.inputSchema.properties.language.default, 'en');

// Every keyword must match, but it may match a different metadata field.
const ranked = setup({fetchImpl: async () => jsonResponse([
  article('Reference', {description: 'camera manual', category: ['Design', 'Photography'], keywords: ['lighting']}),
  article('Camera manual', {description: 'Basics', keywords: ['lighting']}),
  article('Camera only', {description: 'No other matching term', keywords: []}),
  article('Camera manual external', {url: 'https://example.net/article/'}),
])});
const ranking = await ranked.tool.execute({query: 'camera manual', limit: 1});
assert.equal(ranking.total_matches, 2);
assert.equal(ranking.returned_count, 1);
assert.equal(ranking.results[0].title, 'Camera manual');
assert.equal((await ranked.tool.execute({query: 'Photography lighting'})).returned_count, 1);
assert.equal((await ranked.tool.execute({query: 'ManYue lighting'})).returned_count, 2);
const many = setup({fetchImpl: async () => jsonResponse(Array.from({length: 12}, (_, index) =>
  article(`Camera ${index}`, {url: `/en/guides/camera-${index}/`})))});
assert.equal((await many.tool.execute({query: 'camera'})).returned_count, 5);
assert.equal((await many.tool.execute({query: 'camera', limit: 10})).returned_count, 10);

const beforeInvalid = primary.calls.length;
for (const input of [null, [], 'SMB', {}, {query: ''}, {query: '   '}, {query: 7}, {query: 'x'.repeat(201)},
  {query: 'x\0'}, {query: 'SMB', language: 'fr'}, {query: 'SMB', language: null},
  {query: 'SMB', limit: 0}, {query: 'SMB', limit: 11}, {query: 'SMB', limit: 1.5},
  {query: 'SMB', limit: '2'}, {query: 'SMB', limit: Infinity}, {query: 'SMB', extra: true}]) {
  await assert.rejects(primary.tool.execute(input), error => error.name === 'TypeError');
}
assert.equal(primary.calls.length, beforeInvalid);

// A failed request or malformed payload must never poison the successful cache.
for (const failure of ['network', 'http', 'json', 'format']) {
  let attempts = 0;
  const retry = setup({fetchImpl: async () => {
    attempts++;
    if (attempts > 1) return jsonResponse(english);
    if (failure === 'network') throw new Error('Temporary network failure');
    if (failure === 'http') return {ok: false, status: 503};
    if (failure === 'json') return {ok: true, status: 200, json: async () => { throw new SyntaxError('Malformed JSON'); }};
    return jsonResponse({unexpected: true});
  }});
  await assert.rejects(retry.tool.execute({query: 'SMB'}));
  assert.equal((await retry.tool.execute({query: 'SMB'})).returned_count, 1);
  assert.equal(attempts, 2);
}

const cancelled = new AbortController();
cancelled.abort();
const preAbort = setup();
await assert.rejects(preAbort.tool.execute({query: 'SMB'}, {signal: cancelled.signal}), error => error.name === 'AbortError');
assert.equal(preAbort.calls.length, 0);
await assert.rejects(primary.tool.execute({query: 'SMB'}, {signal: cancelled.signal}), error => error.name === 'AbortError');

let started;
const inFlight = new Promise(resolve => { started = resolve; });
let abortAttempts = 0;
const abortable = setup({fetchImpl: async (_path, {signal}) => {
  abortAttempts++;
  if (abortAttempts > 1) return jsonResponse(english);
  started();
  return new Promise((_resolve, reject) => {
    signal.addEventListener('abort', () => reject(signal.reason), {once: true});
  });
}});
const abort = new AbortController();
const pending = abortable.tool.execute({query: 'SMB'}, {signal: abort.signal});
await inFlight;
abort.abort();
await assert.rejects(pending, error => error.name === 'AbortError');
assert.equal((await abortable.tool.execute({query: 'SMB'})).returned_count, 1);
assert.equal(abortAttempts, 2);

// Cancellation while parsing also prevents caching, and does not affect another caller.
const parsingAbort = new AbortController();
let parseAttempts = 0;
const parsing = setup({fetchImpl: async () => {
  parseAttempts++;
  return {ok: true, status: 200, json: async () => {
    if (parseAttempts === 1) parsingAbort.abort();
    return english;
  }};
}});
await assert.rejects(parsing.tool.execute({query: 'SMB'}, {signal: parsingAbort.signal}), error => error.name === 'AbortError');
assert.equal((await parsing.tool.execute({query: 'SMB'})).returned_count, 1);
assert.equal(parseAttempts, 2);

let releaseFirst;
let concurrencyAttempts = 0;
const concurrent = setup({fetchImpl: async (_path, {signal}) => {
  concurrencyAttempts++;
  if (concurrencyAttempts === 2) return jsonResponse(english);
  return new Promise((resolve, reject) => {
    releaseFirst = resolve;
    signal.addEventListener('abort', () => reject(signal.reason), {once: true});
  });
}});
const firstAbort = new AbortController();
const cancelledSearch = concurrent.tool.execute({query: 'SMB'}, {signal: firstAbort.signal});
const successfulSearch = concurrent.tool.execute({query: 'font'});
firstAbort.abort();
await assert.rejects(cancelledSearch, error => error.name === 'AbortError');
assert.equal((await successfulSearch).returned_count, 1);
assert.equal(typeof releaseFirst, 'function');

console.log('PASS: WebMCP interface simulations — absent/current/legacy API, keyword search and ranking, both languages, actual result counts, input limits, same-origin credential-free fetch, cache retry, and AbortSignal cancellation.');
console.log('Native browser support and any scanner result are not established by these simulations.');
