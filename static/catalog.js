(() => {
  const form = document.querySelector('#catalog-filters');
  if (!form) return;
  const search = form.querySelector('#search');
  const category = form.querySelector('#category');
  const cards = [...document.querySelectorAll('[data-project]')];
  const count = document.querySelector('#result-count');
  const empty = document.querySelector('#empty-state');
  const params = new URLSearchParams(location.search);
  search.value = params.get('q') || '';
  if ([...category.options].some(option => option.value === params.get('category'))) category.value = params.get('category');
  function update() {
    const terms = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    cards.forEach(card => {
      const match = (category.value === 'all' || card.dataset.category === category.value) && terms.every(term => card.dataset.search.toLowerCase().includes(term));
      card.hidden = !match;
      if (match) visible++;
    });
    count.textContent = `Showing ${visible} of ${cards.length} projects`;
    empty.hidden = visible !== 0;
    const query = new URLSearchParams();
    if (search.value.trim()) query.set('q', search.value.trim());
    if (category.value !== 'all') query.set('category', category.value);
    history.replaceState(null, '', location.pathname + (query.size ? '?' + query : '') + location.hash);
  }
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('input', update);
  form.addEventListener('change', update);
  form.addEventListener('reset', () => { search.value = ''; category.value = 'all'; queueMicrotask(update); });
  document.querySelector('#empty-reset').addEventListener('click', () => { form.reset(); search.focus(); });
  form.hidden = false;
  update();
})();
