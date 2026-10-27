(() => {
  'use strict';

  const settings = document.getElementById('site-analytics-config');
  if (!settings) return;
  let config;
  try {
    config = JSON.parse(settings.textContent);
    if (!/^G-[A-Z0-9]+$/.test(config.measurementId) ||
        location.origin !== new URL(config.origin).origin) return;
  } catch {
    return;
  }

  // Only this site's configured App Store products count as product interest.
  const productId = value => {
    try {
      const url = new URL(value, location.origin);
      if (url.protocol !== 'https:' || url.hostname !== 'apps.apple.com') return '';
      return url.pathname.match(/\/id(\d+)\/?$/)?.[1] || '';
    } catch {
      return '';
    }
  };
  const apps = new Map();
  for (const app of config.apps || []) {
    const id = productId(app.url);
    if (id) apps.set(id, app.id);
  }
  const cleanUrl = value => {
    try {
      const url = new URL(value);
      return /^https?:$/.test(url.protocol) ? url.origin + url.pathname : '';
    } catch {
      return '';
    }
  };

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', config.measurementId, {
    page_location: location.origin + location.pathname,
    page_referrer: cleanUrl(document.referrer),
    allow_google_signals: false,
    allow_ad_personalization_signals: false,
  });
  const tag = document.createElement('script');
  tag.async = true;
  tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(config.measurementId);
  document.head.appendChild(tag);

  const trackStoreClick = event => {
    if (event.defaultPrevented || (event.type === 'auxclick' && event.button !== 1)) return;
    const link = event.target?.closest?.('a[href]');
    if (!link) return;
    const appId = apps.get(productId(link.href));
    if (!appId) return;
    window.gtag('event', 'app_store_click', {
      send_to: config.measurementId,
      app_id: appId,
      content_language: document.documentElement.lang || 'zh-CN',
      page_path: location.pathname,
      link_url: cleanUrl(link.href),
      link_domain: 'apps.apple.com',
    });
  };
  // Let the browser follow links normally, including keyboard and new-tab clicks.
  document.addEventListener('click', trackStoreClick);
  document.addEventListener('auxclick', trackStoreClick);
})();
