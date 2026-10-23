(() => {
  const english = document.documentElement.lang.toLowerCase().startsWith('en');
  const normalize = value => String(value).normalize('NFKC').toLocaleLowerCase();

  document.querySelectorAll('[data-technical-library]').forEach(library => {
    const form = library.querySelector('[data-technical-controls]');
    const input = library.querySelector('[data-technical-query]');
    if (!form || !input) return;

    const rows = Array.from(library.querySelectorAll('[data-technical-item]'), element => ({
      element,
      text: normalize(element.dataset.searchText || element.textContent)
    }));
    const sections = Array.from(library.querySelectorAll('[data-technical-section]'));
    const status = library.querySelector('[data-technical-status]');
    const empty = library.querySelector('[data-technical-empty]');
    const resets = Array.from(library.querySelectorAll('[data-technical-reset]'));

    const update = () => {
      const terms = normalize(input.value).trim().split(/\s+/).filter(Boolean);
      let count = 0;
      rows.forEach(({ element, text }) => {
        element.hidden = !terms.every(term => text.includes(term));
        if (!element.hidden) count += 1;
      });
      sections.forEach(section => {
        section.hidden = !Array.from(section.querySelectorAll('[data-technical-item]')).some(row => !row.hidden);
      });
      if (status) status.textContent = english ? (terms.length ? `${count} of ${rows.length} articles found` : `All ${rows.length} articles shown`) : (terms.length ? `找到 ${count} 篇文章，共 ${rows.length} 篇` : `显示全部 ${rows.length} 篇文章`);
      if (empty) empty.hidden = count !== 0;
      resets.forEach(button => {
        if (form.contains(button)) button.hidden = input.value.length === 0;
      });
    };

    const reset = () => {
      input.value = '';
      update();
      input.focus();
    };

    form.addEventListener('submit', event => event.preventDefault());
    form.addEventListener('reset', event => {
      event.preventDefault();
      reset();
    });
    resets.filter(button => !form.contains(button)).forEach(button => button.addEventListener('click', reset));
    input.addEventListener('input', update);
    input.addEventListener('search', update);
    window.addEventListener('pageshow', update);
    form.hidden = false;
    update();
  });
})();
