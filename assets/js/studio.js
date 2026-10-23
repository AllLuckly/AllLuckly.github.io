const studioEnglish = document.documentElement.lang.toLowerCase().startsWith('en');
document.querySelectorAll('[data-filter-group]').forEach(group => {
  const controls = group.querySelector('.filters');
  if (!controls) return;
  const cards = [...group.querySelectorAll('[data-filter-item]')];
  const search = group.querySelector('[data-guide-search]');
  const libraryControls = group.querySelector('[data-library-controls]');
  const status = group.querySelector('.filter-status');
  const empty = group.querySelector('[data-guide-empty]');
  const resetButtons = [...group.querySelectorAll('[data-guide-reset]')];
  let selectedApp = 'all';
  const normalize = value => value.normalize('NFKC').toLocaleLowerCase();
  controls.hidden = false;
  if (libraryControls) {
    libraryControls.hidden = false;
    group.setAttribute('data-library-ready', '');
  }
  const updateResults = () => {
    const terms = normalize(search?.value || '').trim().split(/\s+/).filter(Boolean);
    let count = 0;
    cards.forEach(card => {
      const text = normalize(card.dataset.searchText || card.textContent);
      card.hidden = (selectedApp !== 'all' && card.dataset.filterItem !== selectedApp) || !terms.every(term => text.includes(term));
      if (!card.hidden) count++;
    });
    group.querySelectorAll('[data-library-section]').forEach(section => {
      section.hidden = ![...section.querySelectorAll('[data-filter-item]')].some(card => !card.hidden);
    });
    controls.querySelectorAll('button[data-filter]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.filter === selectedApp));
    });
    if (status) status.textContent = studioEnglish ? (count ? `${count} tutorial${count === 1 ? '' : 's'} shown` : 'No matching tutorials') : (count ? `显示 ${count} 篇教程` : '没有匹配的教程');
    if (empty) empty.hidden = count !== 0;
    resetButtons.forEach(button => {
      if (!empty?.contains(button)) button.hidden = selectedApp === 'all' && terms.length === 0;
    });
  };
  controls.addEventListener('click', event => {
    const button = event.target.closest('button[data-filter]');
    if (!button || !controls.contains(button)) return;
    selectedApp = button.dataset.filter;
    updateResults();
  });
  resetButtons.forEach(button => button.addEventListener('click', () => {
    selectedApp = 'all';
    if (search) search.value = '';
    updateResults();
    if (search) search.focus();
  }));
  if (search) search.addEventListener('input', updateResults);
  updateResults();
  window.addEventListener('pageshow', updateResults);
});
let articleHeadings = [...document.querySelectorAll('[data-article-body] h2')];
if (!articleHeadings.length && document.querySelector('.technical-article')) {
  articleHeadings = [...document.querySelectorAll('[data-article-body] h3')];
}
const articleTocs = [...document.querySelectorAll('[data-toc]')];
articleTocs.forEach(toc => {
  const list = toc.querySelector('ol');
  if (!list) return;
  articleHeadings.forEach((heading, index) => {
    if (!heading.id) heading.id = `section-${index + 1}`;
    heading.tabIndex = -1;
    const item = document.createElement('li');
    const link = document.createElement('a');
    link.href = `#${heading.id}`;
    link.textContent = heading.textContent;
    item.append(link);
    list.append(item);
  });
  toc.hidden = articleHeadings.length === 0;
});
if (articleHeadings.length && articleTocs.length) {
  let scheduled = false;
  let activeId = null;
  const updateCurrentSection = () => {
    scheduled = false;
    let current = articleHeadings[0];
    const readingLine = Math.min(120, window.innerHeight / 4);
    for (const heading of articleHeadings) {
      if (heading.getBoundingClientRect().top > readingLine) break;
      current = heading;
    }
    if (activeId === current.id) return;
    activeId = current.id;
    articleTocs.forEach(toc => toc.querySelectorAll('a').forEach(link => {
      if (link.getAttribute('href') === `#${activeId}`) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }));
  };
  const scheduleCurrentSection = () => {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(updateCurrentSection);
  };
  window.addEventListener('scroll', scheduleCurrentSection, { passive: true });
  window.addEventListener('resize', scheduleCurrentSection);
  window.addEventListener('hashchange', scheduleCurrentSection);
  window.addEventListener('pageshow', scheduleCurrentSection);
  updateCurrentSection();
}
const search = document.querySelector('[data-journal-search]');
if (search) {
  search.hidden = false;
  const items = [...document.querySelectorAll('[data-journal-item]')];
  search.querySelector('input').addEventListener('input', event => {
    const query = event.target.value.trim().toLocaleLowerCase(); let count = 0;
    items.forEach(item => { item.hidden = !item.textContent.toLocaleLowerCase().includes(query); if (!item.hidden) count++; });
    search.querySelector('[data-search-status]').textContent = studioEnglish ? (count ? `${count} article${count === 1 ? '' : 's'} found` : 'No matching articles. Try another keyword.') : (count ? `找到 ${count} 篇文章` : '没有找到匹配文章，试试其他关键词。');
  });
}

const workVideo = document.querySelector('#work-video');
const videoChapters = document.querySelector('[data-video-chapters]');
if (workVideo && videoChapters) {
  const links = [...videoChapters.querySelectorAll('[data-video-chapter]')];
  const status = videoChapters.querySelector('[data-video-chapter-status]');
  const parseSeconds = value => {
    if (!/^\d+(?:\.\d+)?$/.test(value)) return null;
    const seconds = Number(value);
    return Number.isFinite(seconds) ? seconds : null;
  };
  const chapters = links.map(link => ({ link, start: parseSeconds(link.dataset.videoChapter) }));
  let pendingSeek = null;
  const showStatus = message => {
    if (!status) return;
    status.textContent = message;
    status.hidden = !message;
  };
  const updateChapter = () => {
    let current = null;
    chapters.forEach(chapter => {
      if (chapter.start !== null && chapter.start <= workVideo.currentTime) current = chapter.link;
    });
    links.forEach(link => {
      if (link === current) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });
  };
  const applyPendingSeek = () => {
    if (pendingSeek === null || workVideo.readyState < 1) return;
    const duration = workVideo.duration;
    if (Number.isFinite(duration) && pendingSeek >= duration) {
      pendingSeek = null;
      return;
    }
    try {
      workVideo.currentTime = pendingSeek;
      pendingSeek = null;
      updateChapter();
    } catch {
      showStatus(studioEnglish ? 'This chapter could not be loaded. Use the player timeline.' : '暂时无法定位章节，请使用播放器进度条。');
    }
  };
  const seekTo = (seconds, play) => {
    pendingSeek = seconds;
    showStatus('');
    applyPendingSeek();
    workVideo.scrollIntoView({ block: 'center', behavior: 'auto' });
    // Call play during the click/keyboard event, preserving browser user activation.
    if (play) {
      const playback = workVideo.play();
      if (playback && typeof playback.catch === 'function') {
        playback.catch(() => showStatus(studioEnglish ? 'Press Play in the player to watch the selected chapter.' : '请点击播放器的播放按钮，继续观看所选章节。'));
      }
    }
  };
  const seekFromLocation = () => {
    const match = window.location.hash.match(/^#t=(\d+(?:\.\d+)?)$/);
    if (!match && window.location.hash && window.location.hash !== '#work-video') return;
    const value = match ? match[1] : new URLSearchParams(window.location.search).get('t');
    const seconds = parseSeconds(value);
    if (seconds !== null) seekTo(seconds, false);
  };
  videoChapters.addEventListener('click', event => {
    const link = event.target.closest('[data-video-chapter]');
    if (!link || !videoChapters.contains(link) || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const seconds = parseSeconds(link.dataset.videoChapter);
    if (seconds === null) return;
    event.preventDefault();
    const destination = new URL(window.location.href);
    destination.searchParams.delete('t');
    destination.hash = link.hash;
    if (destination.href !== window.location.href) window.history.pushState(null, '', destination.href);
    seekTo(seconds, true);
  });
  workVideo.addEventListener('loadedmetadata', applyPendingSeek);
  workVideo.addEventListener('timeupdate', updateChapter);
  window.addEventListener('hashchange', seekFromLocation);
  window.addEventListener('popstate', seekFromLocation);
  seekFromLocation();
  updateChapter();
}
