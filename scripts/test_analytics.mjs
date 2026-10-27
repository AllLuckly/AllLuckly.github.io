import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const source = readFileSync(new URL('../assets/js/analytics.js', import.meta.url), 'utf8');
const validConfig = {
  measurementId: 'G-TEST12345',
  origin: 'https://allluckly.cn',
  apps: [{id: 'pastel', url: 'https://apps.apple.com/cn/app/id1591340577'}],
};

function run(config = validConfig, origin = validConfig.origin) {
  const listeners = new Map();
  const scripts = [];
  const document = {
    getElementById: () => config === null ? null : {textContent: JSON.stringify(config)},
    referrer: 'https://example.com/search?q=private#fragment',
    documentElement: {lang: 'en'},
    createElement: () => ({}),
    head: {appendChild: script => scripts.push(script)},
    addEventListener: (name, handler) => listeners.set(name, handler),
  };
  const window = {};
  vm.runInNewContext(source, {
    window, document, URL, Map, Date,
    location: {origin, pathname: '/en/apps/aquarell/', search: '?token=private'},
  });
  const events = () => (window.dataLayer || []).map(args => Array.from(args));
  const click = (url, overrides = {}) => {
    const event = {type: 'click', button: 0, target: {closest: () => ({href: url})}, ...overrides};
    listeners.get(event.type)?.(event);
  };
  return {scripts, listeners, events, click};
}

for (const config of [null, {}, {...validConfig, measurementId: ''}, {...validConfig, measurementId: 'UA-123'}]) {
  const result = run(config);
  assert.equal(result.scripts.length, 0, 'Disabled or invalid settings must not request Google');
  assert.equal(result.listeners.size, 0);
}
for (const origin of ['http://127.0.0.1:4173', 'https://preview.example.com']) {
  assert.equal(run(validConfig, origin).scripts.length, 0, 'Previews must not send production traffic');
}

const active = run();
assert.equal(active.scripts.length, 1);
assert.equal(active.scripts[0].src, 'https://www.googletagmanager.com/gtag/js?id=G-TEST12345');
assert.equal(active.scripts[0].async, true);
const pageview = active.events().find(event => event[0] === 'config');
assert.equal(pageview[2].page_location, 'https://allluckly.cn/en/apps/aquarell/');
assert.equal(pageview[2].page_referrer, 'https://example.com/search');
assert.equal(pageview[2].allow_google_signals, false);

active.click('https://apps.apple.com/us/app/aquarell/id1591340577?ct=private#fragment');
const interest = active.events().at(-1);
assert.equal(interest[0], 'event');
assert.equal(interest[1], 'app_store_click');
assert.equal(interest[2].app_id, 'pastel');
assert.equal(interest[2].content_language, 'en');
assert.equal(interest[2].link_url, 'https://apps.apple.com/us/app/aquarell/id1591340577');
assert.equal(interest[2].page_path, '/en/apps/aquarell/');

const before = active.events().length;
for (const url of [
  '/guides/aquarell/',
  'https://apps.apple.com/cn/app/id999999999',
  'https://apps.apple.com.example.com/cn/app/id1591340577',
  'http://apps.apple.com/cn/app/id1591340577',
]) active.click(url);
active.click(validConfig.apps[0].url, {defaultPrevented: true});
active.click(validConfig.apps[0].url, {type: 'auxclick', button: 2});
assert.equal(active.events().length, before, 'Only intentional clicks on configured products count');
active.click(validConfig.apps[0].url, {type: 'auxclick', button: 1});
assert.equal(active.events().length, before + 1, 'Middle-click product links count without changing navigation');

console.log('Analytics gating, preview isolation, product clicks and URL sanitization passed.');
