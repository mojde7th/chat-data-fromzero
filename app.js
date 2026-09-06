(function () {
  const KEY = 'chat-data-fromzero-read-v1';
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  let onlyUnread = false;

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; }
  }
  function save(m) { localStorage.setItem(KEY, JSON.stringify(m)); }
  function pages() { return $$('.page'); }
  function links() { return $$('.grp a[href^="#"]'); }
  function unreadLinks() {
    const m = load();
    return links().filter((a) => !m[a.getAttribute('href').slice(1)]);
  }
  function paintRead() {
    const m = load();
    const all = links();
    let n = 0;
    all.forEach((a) => {
      const id = a.getAttribute('href').slice(1);
      const on = !!m[id];
      a.classList.toggle('read', on);
      if (on) n++;
    });
    const bar = $('.prog>i');
    if (bar && all.length) bar.style.width = Math.round((n / all.length) * 100) + '%';
    const lab = $('#readCount');
    if (lab) lab.textContent = n + ' / ' + all.length;
    $$('#unreadBox').forEach((box) => {
      if (!box) return;
      const u = unreadLinks();
      box.innerHTML = u.length
        ? ('<b>نخوانده</b>' + u.slice(0, 8).map((a) => '<a href="' + a.getAttribute('href') + '" data-go="' + a.getAttribute('href').slice(1) + '">' + a.textContent.trim() + '</a>').join(''))
        : '<span class="dim">همه خوانده شد</span>';
    });
    const side = document.querySelector('.side');
    if (side) side.classList.toggle('only-unread', onlyUnread);
    const bu = $('#btnOnlyUnread');
    if (bu) bu.classList.toggle('on', onlyUnread);
  }
  function show(id) {
    const page = document.getElementById(id) || document.getElementById('start');
    pages().forEach((p) => p.classList.toggle('on', p === page));
    links().forEach((a) => a.classList.toggle('on', a.getAttribute('href') === '#' + page.id));
    const grp = document.querySelector('.grp a.on');
    if (grp) {
      const box = grp.closest('.grp');
      if (box) box.classList.add('open');
    }
    $$('#btnRead, #btnReadTop').forEach((mark) => {
      if (!mark) return;
      const m = load();
      mark.textContent = m[page.id] ? 'خوانده شد — برداشتن تیک' : 'این صفحه را خواندم';
      mark.classList.toggle('mark', !!m[page.id]);
      mark.dataset.id = page.id;
    });
    window.scrollTo(0, 0);
  }
  function go(id) {
    location.hash = id;
    show(id);
  }
  function current() {
    return (location.hash || '#start').replace(/^#/, '') || 'start';
  }
  function filterTab(tab) {
    $$('.tabs button').forEach((b) => b.classList.toggle('on', b.dataset.tab === tab));
    $$('.grp').forEach((g) => {
      const t = g.dataset.tab;
      g.style.display = !tab || tab === 'all' || t === tab || t === 'all' ? '' : 'none';
    });
  }
  function toggleRead(id) {
    const m = load();
    m[id] = !m[id];
    save(m);
    paintRead();
    $$('#btnRead, #btnReadTop').forEach((mark) => {
      if (!mark) return;
      mark.textContent = m[id] ? 'خوانده شد — برداشتن تیک' : 'این صفحه را خواندم';
      mark.classList.toggle('mark', !!m[id]);
    });
  }
  document.addEventListener('click', (ev) => {
    const t = ev.target.closest('[data-go]');
    if (t) { ev.preventDefault(); go(t.getAttribute('data-go')); return; }
    const a = ev.target.closest('.grp a[href^="#"]');
    if (a) { ev.preventDefault(); go(a.getAttribute('href').slice(1)); return; }
    const g = ev.target.closest('.grp>button');
    if (g) { g.parentElement.classList.toggle('open'); return; }
    const tb = ev.target.closest('.tabs button');
    if (tb) { filterTab(tb.dataset.tab); return; }
    if (ev.target.id === 'btnRead' || ev.target.id === 'btnReadTop') toggleRead(ev.target.dataset.id);
    if (ev.target.id === 'btnReset') {
      if (confirm('همه تیک‌های خوانده‌شده پاک شود؟')) { save({}); paintRead(); show(current()); }
    }
    if (ev.target.id === 'btnOnlyUnread') { onlyUnread = !onlyUnread; paintRead(); }
    if (ev.target.id === 'btnNextUnread' || ev.target.id === 'btnNextTop') {
      const u = unreadLinks();
      if (!u.length) { alert('نخوانده نماند'); return; }
      const cur = current();
      const i = u.findIndex((x) => x.getAttribute('href').slice(1) === cur);
      go((u[i + 1] || u[0]).getAttribute('href').slice(1));
    }
  });
  window.addEventListener('hashchange', () => show(current()));
  show(current());
  paintRead();
})();
