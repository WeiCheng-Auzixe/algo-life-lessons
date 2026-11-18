/* =========================================================
   演算法生活課｜講義（簡報）共用程式
   講義頁只要：<main id="deck"> 裡放 <section class="slide">，
   最後依序載入 sources.js、wiki-titles.js（tools/build_wiki.py 產生）與 deck.js。其餘（縮放、翻頁、頁尾來源、
   測驗、勾選清單、資料來源頁、回首頁按鈕）都由這支程式處理。
   ========================================================= */
(function () {
  const ROOT = new URL('..', document.currentScript.src).href; // 專案根目錄
  const SOURCES = window.SOURCES || {};
  const deck = document.getElementById('deck');
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const anchorOf = p => p.replace(/\.md$/, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

  // 1) 舞台外框、進度條、導覽列
  const vp = document.createElement('div'); vp.id = 'viewport';
  deck.parentNode.insertBefore(vp, deck); vp.appendChild(deck);
  document.body.insertAdjacentHTML('afterbegin', '<div id="bar"></div>');
  document.body.insertAdjacentHTML('beforeend',
    `<nav id="nav" aria-label="翻頁"><a id="home" href="${ROOT}index.html" title="回講義庫" aria-label="回講義庫">⌂</a>` +
    '<span id="count"></span><button id="prev" aria-label="上一頁">←</button><button id="next" aria-label="下一頁">→</button></nav>');

  // 2) 頁尾「本頁根據」：<footer class="refs" data-wiki="a.md b.md" data-sources="S1 S4">
  const used = [];
  deck.querySelectorAll('footer.refs').forEach(f => {
    const wikis = (f.dataset.wiki || '').split(/\s+/).filter(Boolean);
    const srcs = (f.dataset.sources || '').split(/\s+/).filter(Boolean);
    srcs.forEach(s => { if (!used.includes(s)) used.push(s); });
    f.innerHTML = '<span class="refs-label">本頁根據</span>' +
      wikis.map(w => `<a class="chip wiki" href="${ROOT}wiki/index.html#${anchorOf(w)}">📘 ${esc(wikiTitle(w))}</a>`).join('') +
      '<span class="refs-sep"></span>' +
      srcs.map(s => SOURCES[s]
        ? `<a class="chip src" href="${esc(SOURCES[s].url)}" target="_blank" rel="noopener" title="${esc(SOURCES[s].title)}">${s} ${esc(SOURCES[s].short)}</a>`
        : `<span class="chip src" style="outline:2px solid var(--coral)">${s}？未登錄</span>`).join('');
  });
  function wikiTitle(p) { return (window.WIKI_TITLES && window.WIKI_TITLES[p]) || p.split('/').pop().replace('.md', ''); }

  // 3) 資料來源頁：<section class="slide sources" data-kind="sources"></section> 自動填入
  deck.querySelectorAll('.slide[data-kind="sources"]').forEach(s => {
    const list = used.sort((a, b) => +a.slice(1) - +b.slice(1))
      .map(k => `<li><b>${k}</b> ${esc(SOURCES[k] ? SOURCES[k].title : '（未登錄）')}　${SOURCES[k] ? `<a href="${esc(SOURCES[k].url)}" target="_blank" rel="noopener">連結</a>` : ''}</li>`).join('');
    s.innerHTML = `<div class="inner"><div class="text full"><p class="kicker">資料來源</p><h2>這份講義根據的 ${used.length} 篇資料</h2><ol class="srclist">${list}</ol>` +
      `<p class="cta">完整知識庫：<a href="${ROOT}wiki/index.html">演算法生活課 Wiki</a>　｜　<a href="${ROOT}index.html">回講義庫</a></p></div></div>`;
  });

  // 4) 小測驗
  deck.querySelectorAll('.q').forEach(q => {
    const fb = q.querySelector('.q-fb');
    q.querySelectorAll('.opt').forEach(b => b.onclick = () => {
      q.querySelectorAll('.opt').forEach(o => o.classList.remove('right', 'wrong'));
      const ok = b.dataset.ok === '1'; b.classList.add(ok ? 'right' : 'wrong');
      if (fb) fb.textContent = ok ? '答對了！' : '再想想看～';
    });
  });

  // 5) 勾選清單（只存在變數裡，不用 localStorage）
  deck.querySelectorAll('.checklist').forEach(cl => {
    const out = cl.parentNode.querySelector('.check-progress');
    const boxes = [...cl.querySelectorAll('input[type=checkbox]')];
    const upd = () => { if (out) { const n = boxes.filter(b => b.checked).length; out.innerHTML = n === boxes.length ? `<b>全部完成！</b>你的手機做完健檢了 🎉` : `已完成 <b>${n}</b> / ${boxes.length} 項`; } };
    boxes.forEach(b => b.addEventListener('change', upd)); upd();
  });

  // 6) 翻頁、縮放、網址 #s3 記住頁碼
  const slides = [...deck.querySelectorAll('.slide')]; let cur = 0;
  const count = document.getElementById('count'), bar = document.getElementById('bar');
  const prev = document.getElementById('prev'), next = document.getElementById('next');
  function fit() { const s = Math.min(innerWidth / 1300, innerHeight / 740); deck.style.transform = `scale(${s})`; }
  function show(i, push) {
    cur = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, k) => s.classList.toggle('active', k === cur));
    count.textContent = `${cur + 1} / ${slides.length}`; bar.style.width = `${(cur + 1) / slides.length * 100}%`;
    prev.disabled = cur === 0; next.disabled = cur === slides.length - 1;
    if (push !== false && location.hash !== `#s${cur + 1}`) { try { history.replaceState(null, '', `#s${cur + 1}`); } catch (e) { } }
  }
  function fromHash() { const m = /^#s(\d+)$/.exec(location.hash); show(m ? parseInt(m[1]) - 1 : 0, false); }
  addEventListener('keydown', e => {
    if (e.target.closest && e.target.closest('input,button')) { if (e.key === ' ') return; }
    if (['ArrowRight', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); show(cur + 1); }
    else if (['ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); show(cur - 1); }
    else if (e.key === 'Home') show(0); else if (e.key === 'End') show(slides.length - 1);
  });
  prev.onclick = () => show(cur - 1); next.onclick = () => show(cur + 1);
  let sx = null;
  addEventListener('touchstart', e => { sx = e.touches[0].clientX; }, { passive: true });
  addEventListener('touchend', e => { if (sx === null) return; const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); sx = null; });
  addEventListener('resize', fit); addEventListener('hashchange', fromHash); fit(); fromHash();
})();
