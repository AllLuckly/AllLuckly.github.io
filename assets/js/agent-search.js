(() => {
  'use strict';

  // WebMCP draft (2026-10-20): https://webmachinelearning.github.io/webmcp/
  // Unsupported browsers retain their existing navigation and search behavior.
  let modelContext;
  try {
    const current = document.modelContext;
    modelContext = typeof current?.registerTool === 'function' ? current :
      (typeof navigator === 'undefined' ? undefined : navigator.modelContext);
    if (typeof modelContext?.registerTool !== 'function') return;
  } catch {
    return;
  }

  const pageLanguage = /^en(?:-|$)/i.test(document.documentElement.lang) ? 'en' : 'zh-CN';
  const indexCache = new Map();
  const normalize = value => value.normalize('NFKC').toLowerCase().replace(/\s+/gu, ' ').trim();
  const text = value => typeof value === 'string' ? value : '';
  const searchable = value => Array.isArray(value) ? value.map(text).join(' ') : text(value);
  const checkAbort = signal => {
    if (!signal?.aborted) return;
    if (typeof signal.throwIfAborted === 'function') signal.throwIfAborted();
    throw new DOMException('Blog search was cancelled.', 'AbortError');
  };

  const validateInput = input => {
    if (!input || typeof input !== 'object' || Array.isArray(input) ||
        Object.keys(input).some(key => !['query', 'language', 'limit'].includes(key))) {
      throw new TypeError('Expected query and optional language and limit only.');
    }
    if (typeof input.query !== 'string' || input.query.length > 200 ||
        !input.query.trim() || /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/u.test(input.query)) {
      throw new TypeError('query must be a nonempty string of at most 200 characters without control characters.');
    }
    const language = input.language === undefined ? pageLanguage : input.language;
    if (language !== 'zh-CN' && language !== 'en') {
      throw new TypeError('language must be zh-CN or en.');
    }
    const limit = input.limit === undefined ? 5 : input.limit;
    if (!Number.isInteger(limit) || limit < 1 || limit > 10) {
      throw new TypeError('limit must be an integer from 1 to 10.');
    }
    return {query: input.query.trim(), language, limit};
  };

  const loadIndex = async (language, signal) => {
    checkAbort(signal);
    if (indexCache.has(language)) return indexCache.get(language);
    const path = language === 'en' ? '/en/search.json' : '/search.json';
    // Queries stay local: only fixed same-origin index paths are requested.
    const response = await fetch(path, {
      method: 'GET',
      mode: 'same-origin',
      credentials: 'omit',
      redirect: 'error',
      headers: {Accept: 'application/json'},
      signal,
    });
    if (!response.ok) throw new Error(`Blog search index could not be loaded (HTTP ${response.status}).`);
    const entries = await response.json();
    checkAbort(signal);
    if (!Array.isArray(entries) || entries.some(entry => !entry || typeof entry !== 'object' ||
        Array.isArray(entry) || typeof entry.title !== 'string' || typeof entry.url !== 'string')) {
      throw new Error('Blog search index has an invalid format.');
    }
    // Only completed, successful reads are cached. Failures and cancellation can retry.
    // Each in-flight execution owns its signal, so cancelling one cannot cancel another.
    indexCache.set(language, entries);
    return entries;
  };

  const sameOriginUrl = value => {
    if (typeof value !== 'string' || !value.trim()) return '';
    try {
      const url = new URL(value, location.origin);
      return url.origin === location.origin && /^https?:$/.test(url.protocol) &&
        !url.username && !url.password ? url.href : '';
    } catch {
      return '';
    }
  };

  const tool = {
    name: 'search_blog_articles',
    title: pageLanguage === 'en' ? 'Search blog articles' : '搜索博客文章',
    description: 'Search this blog’s published Chinese or English article index using normalized keywords. All whitespace-separated keywords must occur in the title, description, category, app name, or keywords. Returns matching article metadata and reading URLs without navigating. This is keyword matching, not semantic search.',
    inputSchema: {
      type: 'object',
      properties: {
        query: {type: 'string', minLength: 1, maxLength: 200, description: 'One or more keywords separated by whitespace.'},
        language: {type: 'string', enum: ['zh-CN', 'en'], default: pageLanguage, description: 'Index language; defaults to this page’s language.'},
        limit: {type: 'integer', minimum: 1, maximum: 10, default: 5},
      },
      required: ['query'],
      additionalProperties: false,
    },
    annotations: {readOnlyHint: true, untrustedContentHint: true, consequentialHint: false},
    async execute(input, options = {}) {
      const {query, language, limit} = validateInput(input);
      const signal = options.signal;
      checkAbort(signal);
      const terms = [...new Set(normalize(query).split(' '))];
      const entries = await loadIndex(language, signal);
      checkAbort(signal);
      const matches = [];
      entries.forEach((entry, index) => {
        if (entry.lang && entry.lang !== language) return;
        const url = sameOriginUrl(entry.url);
        if (!url) return;
        const fields = [entry.title, entry.description, entry.category, entry.app_name, entry.keywords]
          .map(value => normalize(searchable(value)));
        if (!terms.every(term => fields.some(field => field.includes(term)))) return;
        const weights = [8, 2, 4, 5, 6];
        const score = terms.reduce((total, term) => total + fields.reduce((sum, field, fieldIndex) =>
          sum + (field.includes(term) ? weights[fieldIndex] : 0), 0), 0);
        matches.push({score, index, article: {
          title: entry.title,
          url,
          markdown_url: sameOriginUrl(entry.markdown_url),
          description: text(entry.description),
          date: text(entry.date),
          author: text(entry.author),
          version_note: text(entry.version_note),
          app_name: text(entry.app_name),
          lang: language,
        }});
      });
      matches.sort((left, right) => right.score - left.score || left.index - right.index);
      checkAbort(signal);
      const results = matches.slice(0, limit).map(match => match.article);
      // The current WebMCP callback returns Promise<any>; the browser serializes this JSON-safe object.
      return {query, language, match_type: 'normalized-keywords', total_matches: matches.length,
        returned_count: results.length, results};
    },
  };

  try {
    // The current API is async; older implementations may return undefined.
    Promise.resolve(modelContext.registerTool(tool)).catch(() => {});
  } catch {
    // A disabled or unavailable experimental API must not break the ordinary page.
  }
})();
