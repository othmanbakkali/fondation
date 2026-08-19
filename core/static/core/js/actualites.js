(function() {
  'use strict';
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const newsData = window.FTM_NEWS_DATA || [];

  let filteredNews = [...newsData];

  function sortByDate(arr) { return arr.sort((a,b) => new Date(b.date) - new Date(a.date)); }

  function normalizeCategory(c) {
    if (!c) return 'actualites';
    let norm = c.toLowerCase().trim().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    if (norm.includes('actualite') || norm.includes('news')) return 'actualites';
    if (norm.includes('communique') || norm.includes('annonc')) return 'communiques';
    if (norm.includes('formation')) return 'formations';
    if (norm.includes('concour')) return 'concours';
    return norm;
  }

  function initYears() {
    const years = [...new Set(newsData.map(n => new Date(n.date).getFullYear()))].sort((a,b) => b-a);
    const sel = document.getElementById('filterYearNews');
    years.forEach(y => { const o = document.createElement('option'); o.value=y; o.textContent=y; sel.appendChild(o); });
  }

  function getCatIcon(c) {
    const norm = normalizeCategory(c);
    const icons = { actualites:'fa-newspaper', communiques:'fa-bullhorn', formations:'fa-graduation-cap', concours:'fa-trophy' };
    return icons[norm]||'fa-star';
  }
  function getCatBadge(c) {
    const norm = normalizeCategory(c);
    const b = { actualites:'badge-actualites', communiques:'badge-communiques', formations:'badge-formations', concours:'badge-concours' };
    return b[norm]||'';
  }
  function getCatLabel(c) {
    const norm = normalizeCategory(c);
    const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';
    const l = {
      actualites: lang === 'ar' ? 'المستجدات' : (lang === 'en' ? 'News' : 'Actualités'),
      communiques: lang === 'ar' ? 'البلاغات' : (lang === 'en' ? 'Announcements' : 'Communiqués'),
      formations: lang === 'ar' ? 'التكوينات' : (lang === 'en' ? 'Formations' : 'Formations'),
      concours: lang === 'ar' ? 'المباريات' : (lang === 'en' ? 'Contests' : 'Concours')
    };
    return l[norm]||c;
  }

  function renderFeatured() {
    const featured = sortByDate([...newsData]).find(n => n.featured) || sortByDate([...newsData])[0];
    const card = document.getElementById('featuredCard');
    if (!card) return;
    const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';
    if (!featured) { card.innerHTML = `<div class="empty-state"><p>${lang === 'ar' ? 'لا توجد مستجدات منشورة.' : (lang === 'en' ? 'No news published yet.' : 'Aucune actualité publiée depuis le dashboard.')}</p></div>`; return; }
    card.innerHTML = `
      <div class="featured-image">
        <img src="${featured.image || '/static/core/images/fonlogo.png'}" alt="${featured.title}" loading="lazy" onerror="this.src='/static/core/images/fonlogo.png'; this.onerror=null;">
        <span class="featured-badge">⭐ ${window.FTM_LANG && window.FTM_LANG.ui.featured || 'À la une'}</span>
      </div>
      <div class="featured-content">
        <span class="featured-category ${getCatBadge(featured.category)}" style="color:#fff;"><i class="fas ${getCatIcon(featured.category)}"></i> ${getCatLabel(featured.category)}</span>
        <h2>${featured.title}</h2>
        <p>${featured.excerpt}</p>
        <div class="featured-meta">
          <span><i class="far fa-calendar-alt"></i> ${new Date(featured.date).toLocaleDateString(lang === 'ar' ? 'ar-MA' : 'fr-FR',{day:'numeric',month:'long',year:'numeric'})}</span>
          <span><i class="far fa-user"></i> ${featured.author}</span>
          <span><i class="far fa-clock"></i> ${featured.readingTime} ${lang === 'ar' ? 'دقائق قراءة' : (lang === 'en' ? 'min read' : 'min de lecture')}</span>
        </div>
        <button class="btn btn-primary" onclick="window._openNewsModal(${featured.id})">${lang === 'ar' ? 'اقرأ المقال' : (lang === 'en' ? 'Read article' : "Lire l'article")}</button>
      </div>`;
  }

  function renderCategories() {
    const cats = ['actualites','communiques','formations','concours'];
    const wrapper = document.getElementById('categoriesWrapper');
    const counts = {};
    const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';
    cats.forEach(c => { counts[c] = newsData.filter(n => normalizeCategory(n.category) === c).length; });
    wrapper.innerHTML = `
      <button class="cat-btn active" data-cat="all"><i class="fas fa-list"></i> ${lang === 'ar' ? 'الكل' : (lang === 'en' ? 'All' : 'Toutes')} <span class="count">${newsData.length}</span></button>
      ${cats.map(c => `<button class="cat-btn" data-cat="${c}"><i class="fas ${getCatIcon(c)}"></i> ${getCatLabel(c)} <span class="count">${counts[c]}</span></button>`).join('')}`;
    wrapper.querySelectorAll('.cat-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        wrapper.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById('filterCat').value = btn.dataset.cat;
        applyFilters();
      });
    });
  }

  function renderNews() {
    const grid = document.getElementById('publicationsGrid');
    const noRes = document.getElementById('noNewsResults');
    if (filteredNews.length === 0) { grid.innerHTML=''; noRes.style.display='block'; return; }
    noRes.style.display='none';
    const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';
    // Afficher TOUTES les publications filtrées
    grid.innerHTML = filteredNews.map(n => `
      <div class="news-card reveal">
        <div class="news-card-image">
          <img src="${n.image || '/static/core/images/fonlogo.png'}" alt="${n.title}" loading="lazy" onerror="this.src='/static/core/images/fonlogo.png'; this.onerror=null;">
          ${n.mediaType==='video' ? `<div class="play-icon" onclick="window._openVideo('${n.videoUrl||n.youtubeUrl}')"><i class="fas fa-play"></i></div><span class="video-duration">${lang === 'ar' ? 'فيديو' : 'Vidéo'}</span>` : ''}
          <span class="news-card-badge ${getCatBadge(n.category)}"><i class="fas ${getCatIcon(n.category)}"></i> ${getCatLabel(n.category)}</span>
        </div>
        <div class="news-card-body">
          <h3>${n.title}</h3>
          <p class="news-card-excerpt">${n.excerpt}</p>
          <div class="news-card-meta">
            <span><i class="far fa-calendar-alt"></i> ${new Date(n.date).toLocaleDateString(lang === 'ar' ? 'ar-MA' : 'fr-FR',{day:'numeric',month:'long',year:'numeric'})}</span>
            <span><i class="far fa-clock"></i> ${n.readingTime} ${lang === 'ar' ? 'دقائق' : 'min'}</span>
          </div>
          <div class="news-card-social">
            ${n.instagramUrl?`<a href="${n.instagramUrl}" target="_blank" rel="noopener noreferrer" class="instagram" aria-label="Instagram"><i class="fab fa-instagram"></i></a>`:''}
            ${n.facebookUrl?`<a href="${n.facebookUrl}" target="_blank" rel="noopener noreferrer" class="facebook" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>`:''}
            ${n.youtubeUrl?`<a href="${n.youtubeUrl}" target="_blank" rel="noopener noreferrer" class="youtube" aria-label="YouTube"><i class="fab fa-youtube"></i></a>`:''}
          </div>
          <button class="btn btn-primary btn-sm news-card-btn" onclick="window._openNewsModal(${n.id})">${window.FTM_LANG && window.FTM_LANG.ui.read_more || 'Lire la suite'}</button>
        </div>
      </div>`).join('');
    document.querySelectorAll('.news-card.reveal').forEach(c => revealObserver.observe(c));
  }

  function applyFilters() {
    const cat = document.getElementById('filterCat').value;
    const year = document.getElementById('filterYearNews').value;
    const month = document.getElementById('filterMonthNews').value;
    const search = document.getElementById('searchNews').value.toLowerCase().trim();
    filteredNews = newsData.filter(n => {
      const d = new Date(n.date);
      return (cat==='all'||normalizeCategory(n.category)===cat) && (year==='all'||d.getFullYear().toString()===year) && (month==='all'||(d.getMonth()+1).toString().padStart(2,'0')===month) && (!search||n.title.toLowerCase().includes(search)||n.excerpt.toLowerCase().includes(search)||normalizeCategory(n.category).includes(search));
    });
    filteredNews = sortByDate(filteredNews);
    renderNews();
  }

  function resetFilters() {
    document.getElementById('filterCat').value='all'; document.getElementById('filterYearNews').value='all';
    document.getElementById('filterMonthNews').value='all'; document.getElementById('searchNews').value='';
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.toggle('active', b.dataset.cat==='all'));
    applyFilters();
  }

  function openNewsModal(id) {
    const n = newsData.find(x => x.id===id); if (!n) return;
    const overlay = document.getElementById('articleModal');
    const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';
    document.getElementById('articleModalBody').innerHTML = `
      <img src="${n.image}" alt="${n.title}" onerror="this.style.display='none'">
      <span class="news-card-badge ${getCatBadge(n.category)}" style="position:static;display:inline-flex;margin-bottom:15px;"><i class="fas ${getCatIcon(n.category)}"></i> ${getCatLabel(n.category)}</span>
      <h2>${n.title}</h2>
      <div class="modal-meta">
        <span><i class="far fa-calendar-alt"></i> ${new Date(n.date).toLocaleDateString(lang === 'ar' ? 'ar-MA' : 'fr-FR',{day:'numeric',month:'long',year:'numeric'})}</span>
        <span><i class="far fa-user"></i> ${n.author}</span>
        <span><i class="far fa-clock"></i> ${n.readingTime} ${lang === 'ar' ? 'دقائق قراءة' : (lang === 'en' ? 'min read' : 'min de lecture')}</span>
      </div>
      <div class="modal-content">${n.content}</div>
      ${n.youtubeUrl?`<div class="modal-video-wrapper" style="margin-top:20px;"><iframe src="${n.youtubeUrl.replace('watch?v=','embed/')}" title="Vidéo" allowfullscreen></iframe></div>`:''}
    `;
    overlay.classList.add('active'); overlay.setAttribute('aria-hidden','false'); document.body.classList.add('modal-open');
  }

  function openVideo(url) {
    if (!url) return;
    const overlay = document.getElementById('videoModal');
    const vidId = url.includes('youtube') ? url.split('v=')[1]?.split('&')[0] : '';
    document.getElementById('videoModalContent').innerHTML = vidId ? `<iframe src="https://www.youtube.com/embed/${vidId}" title="Vidéo" allowfullscreen></iframe>` : `<video src="${url}" controls autoplay style="width:100%;height:100%;"></video>`;
    overlay.classList.add('active'); overlay.setAttribute('aria-hidden','false'); document.body.classList.add('modal-open');
  }

  function closeModals() {
    document.querySelectorAll('.modal-overlay').forEach(m => { m.classList.remove('active'); m.setAttribute('aria-hidden','true'); });
    document.body.classList.remove('modal-open');
  }

  window._openNewsModal = openNewsModal;
  window._openVideo = openVideo;

  document.addEventListener('DOMContentLoaded', () => {
    initYears(); renderFeatured(); renderCategories();
    filteredNews = sortByDate([...newsData]); renderNews();
    document.getElementById('filterCat').addEventListener('change', () => { applyFilters(); updateCatBtns(); });
    document.getElementById('filterYearNews').addEventListener('change', applyFilters);
    document.getElementById('filterMonthNews').addEventListener('change', applyFilters);
    document.getElementById('searchNews').addEventListener('input', applyFilters);
    document.getElementById('resetNewsFilters').addEventListener('click', resetFilters);
    document.getElementById('articleModalClose').addEventListener('click', closeModals);
    document.getElementById('videoModalClose').addEventListener('click', closeModals);
    document.querySelectorAll('.modal-overlay').forEach(m => m.addEventListener('click', e => { if (e.target===e.currentTarget) closeModals(); }));
    document.addEventListener('keydown', e => { if (e.key==='Escape') closeModals(); });
    document.getElementById('newsletterForm').addEventListener('submit', function(e) {
      e.preventDefault();
      document.getElementById('newsletterSuccess').style.display='block';
      this.reset();
      setTimeout(() => { document.getElementById('newsletterSuccess').style.display='none'; }, 4000);
    });
  });

  function updateCatBtns() {
    const val = document.getElementById('filterCat').value;
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.toggle('active', b.dataset.cat===val));
  }

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting && !prefersReducedMotion) e.target.classList.add('visible'); });
  }, { threshold: 0.1 });

  const btt = document.getElementById('backToTop');
  if (btt) { window.addEventListener('scroll', () => btt.classList.toggle('show', window.scrollY > 500)); btt.addEventListener('click', () => window.scrollTo({top:0,behavior:prefersReducedMotion?'auto':'smooth'})); }

  const fs = document.getElementById('floatingSidebar');
  if (fs) window.addEventListener('scroll', () => fs.classList.toggle('visible', window.scrollY > 300));

  const hamburger = document.getElementById('hamburger'), navMenu = document.getElementById('navMenu');
  if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => { hamburger.classList.toggle('active'); navMenu.classList.toggle('active'); });
    navMenu.querySelectorAll('a').forEach(l => l.addEventListener('click', () => { hamburger.classList.remove('active'); navMenu.classList.remove('active'); }));
  }
  const dt = document.querySelector('.dropdown-toggle'), dp = document.querySelector('.nav-item.dropdown');
  if (dt && dp) dt.addEventListener('click', function(e) { if (window.innerWidth <= 768) { e.preventDefault(); dp.classList.toggle('active'); } });

  console.log('✅ Page Actualités - Fondation Tanger Métropole - ' + newsData.length + ' publications');
})();
