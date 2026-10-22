document.querySelectorAll('[data-filter-group]').forEach(group => {
  const controls = group.querySelector('.filters');
  const cards = [...group.querySelectorAll('[data-filter-item]')];
  const search = group.querySelector('[data-guide-search]');
  const libraryControls = group.querySelector('[data-library-controls]');
  let selectedApp = 'all';
  controls.hidden = false;
  if (libraryControls) libraryControls.hidden = false;
  const updateResults = () => {
    const terms = (search?.value || '').trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    cards.forEach(card => {
      const text = (card.dataset.searchText || card.textContent).toLocaleLowerCase();
      card.hidden = (selectedApp !== 'all' && card.dataset.filterItem !== selectedApp) || !terms.every(term => text.includes(term));
      if (!card.hidden) count++;
    });
    group.querySelectorAll('[data-library-section]').forEach(section => {
      section.hidden = ![...section.querySelectorAll('[data-filter-item]')].some(card => !card.hidden);
    });
    group.querySelector('.filter-status').textContent = count ? `显示 ${count} 篇教程` : '没有找到匹配教程，请调整关键词或切换应用。';
  };
  controls.addEventListener('click', event => {
    const button = event.target.closest('button[data-filter]');
    if (!button) return;
    selectedApp = button.dataset.filter;
    controls.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    updateResults();
  });
  if (search) search.addEventListener('input', updateResults);
  updateResults();
  window.addEventListener('pageshow', updateResults);
});
document.querySelectorAll('[data-toc]').forEach(toc => {
  document.querySelectorAll('[data-article-body] h2').forEach((heading, index) => {
    if (!heading.id) heading.id = `section-${index + 1}`;
    const item = document.createElement('li'); const link = document.createElement('a');
    link.href = `#${heading.id}`; link.textContent = heading.textContent;
    item.append(link); toc.querySelector('ol').append(item);
  });
  toc.hidden = !toc.querySelector('li');
});
const search = document.querySelector('[data-journal-search]');
if (search) {
  search.hidden = false;
  const items = [...document.querySelectorAll('[data-journal-item]')];
  search.querySelector('input').addEventListener('input', event => {
    const query = event.target.value.trim().toLocaleLowerCase(); let count = 0;
    items.forEach(item => { item.hidden = !item.textContent.toLocaleLowerCase().includes(query); if (!item.hidden) count++; });
    search.querySelector('[data-search-status]').textContent = count ? `找到 ${count} 篇文章` : '没有找到匹配文章，试试其他关键词。';
  });
}
