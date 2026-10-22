document.querySelectorAll('[data-filter-group]').forEach(group => {
  const controls = group.querySelector('.filters');
  const cards = [...group.querySelectorAll('[data-filter-item]')];
  controls.hidden = false;
  controls.addEventListener('click', event => {
    const button = event.target.closest('button[data-filter]');
    if (!button) return;
    controls.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    let count = 0;
    cards.forEach(card => { card.hidden = button.dataset.filter !== 'all' && card.dataset.filterItem !== button.dataset.filter; if (!card.hidden) count++; });
    group.querySelector('.filter-status').textContent = `显示 ${count} 篇教程`;
  });
});
const toc = document.querySelector('[data-toc]');
if (toc) {
  document.querySelectorAll('[data-article-body] h2').forEach((heading, index) => {
    if (!heading.id) heading.id = `section-${index + 1}`;
    const item = document.createElement('li'); const link = document.createElement('a');
    link.href = `#${heading.id}`; link.textContent = heading.textContent;
    item.append(link); toc.querySelector('ol').append(item);
  });
  toc.hidden = !toc.querySelector('li');
}
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
