(function() {
  'use strict';
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const mediaData = window.FTM_MEDIA_DATA || [];

  let currentTab = 'all';
  let filteredMedia = [...mediaData];
  let lightboxIndex = 0;
  let lightboxItems = [];

  function sortByDate(arr) { return arr.sort((a,b) => new Date(b.date) - new Date(a.date)); }

  function initYears() {
    const years = [...new Set(mediaData.map(m => new Date(m.date).getFullYear()))].sort((a,b) => b-a);
    const sel = document.getElementById('filterMediaYear');
    years.forEach(y => { const o = document.createElement('option'); o.value=y; o.textContent=y; sel.appendChild(o); });
  }

  function getCatLabel(c) {
    const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';
    const l = {
      activites: lang === 'ar' ? 'أنشطة' : (lang === 'en' ? 'Activities' : 'Activités'),
      formations: lang === 'ar' ? 'تكوينات' : (lang === 'en' ? 'Formations' : 'Formations'),
      evenements: lang === 'ar' ? 'فعاليات' : (lang === 'en' ? 'Events' : 'Événements'),
      culture: lang === 'ar' ? 'ثقافة' : (lang === 'en' ? 'Culture' : 'Culture'),
      sport: lang === 'ar' ? 'رياضة' : (lang === 'en' ? 'Sport' : 'Sport'),
      social: lang === 'ar' ? 'تضامن' : (lang === 'en' ? 'Social' : 'Social'),
      rapports: lang === 'ar' ? 'تقارير' : (lang === 'en' ? 'Reports' : 'Rapports')
    };
    return l[c]||c;
  }

  function updateCounts() {
    const photos = mediaData.filter(m=>m.type==='photo').length;
    const videos = mediaData.filter(m=>m.type==='video').length;
    const pdfs = mediaData.filter(m=>m.type==='pdf').length;
    document.getElementById('statPhotos').textContent = photos;
    document.getElementById('statVideos').textContent = videos;
    document.getElementById('statPdfs').textContent = pdfs;
    document.getElementById('countAll').textContent = mediaData.length;
    document.getElementById('countPhotos').textContent = photos;
    document.getElementById('countVideos').textContent = videos;
    document.getElementById('countPdfs').textContent = pdfs;
  }

  function renderAll() {
    const photos = filteredMedia.filter(m=>m.type==='photo');
    const videos = filteredMedia.filter(m=>m.type==='video');
    const pdfs = filteredMedia.filter(m=>m.type==='pdf');
    const showAll = currentTab === 'all';
    const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';

    document.getElementById('photosGrid').innerHTML = (showAll||currentTab==='photo') ? photos.map((p,i) => `
      <div class="photo-item reveal" onclick="window._openLightbox('${currentTab==='all'?'photo':'current'}','${currentTab==='all'?p.id:i}')">
        <img src="${p.thumbnail || '/static/core/images/fonlogo.png'}" alt="${p.title}" loading="lazy" onerror="this.src='/static/core/images/fonlogo.png'; this.onerror=null;">
        <div class="photo-overlay"><h4>${p.title}</h4><span>${getCatLabel(p.category)} · ${new Date(p.date).toLocaleDateString(lang === 'ar' ? 'ar-MA' : 'fr-FR')}</span></div>
      </div>
    `).join('') : '';

    document.getElementById('videosGrid').innerHTML = (showAll||currentTab==='video') ? videos.map(v => `
      <div class="video-card reveal">
        <div class="video-thumb" onclick="window._openVideo('${v.videoUrl}','${v.videoPlatform}','${v.title}','${v.description}')">
          <img src="${v.thumbnail || '/static/core/images/fonlogo.png'}" alt="${v.title}" loading="lazy" onerror="this.src='/static/core/images/fonlogo.png'; this.onerror=null;">
          <div class="play-btn"><i class="fas fa-play"></i></div>
          <span class="video-platform-badge">${v.videoPlatform}</span>
        </div>
        <div class="video-info">
          <h4>${v.title}</h4>
          <p>${v.description}</p>
          <div class="video-meta">
            <span><i class="far fa-clock"></i> ${v.duration}</span>
            <span><i class="far fa-calendar-alt"></i> ${new Date(v.date).toLocaleDateString(lang === 'ar' ? 'ar-MA' : 'fr-FR')}</span>
          </div>
        </div>
      </div>
    `).join('') : '';

    document.getElementById('pdfsGrid').innerHTML = (showAll||currentTab==='pdf') ? pdfs.map(d => `
      <div class="pdf-card reveal">
        <div class="pdf-card-header"><i class="fas fa-file-pdf"></i> PDF</div>
        <div class="pdf-card-body">
          <h4>${d.title}</h4>
          <p>${d.description}</p>
          <div class="pdf-meta">
            <span><i class="fas fa-file"></i> ${d.pages} ${lang === 'ar' ? 'صفحة' : 'pages'}</span>
            <span><i class="fas fa-weight"></i> ${d.fileSize}</span>
            <span><i class="fas fa-globe"></i> ${d.language}</span>
          </div>
          <div class="pdf-actions">
            <a href="${d.fileUrl}" target="_blank" class="btn btn-primary btn-sm"><i class="fas fa-eye"></i> ${lang === 'ar' ? 'عرض' : (lang === 'en' ? 'View' : 'Consulter')}</a>
            <a href="${d.fileUrl}" download class="btn btn-outline btn-sm"><i class="fas fa-download"></i></a>
            <button class="btn btn-sm" style="background:var(--bg-light)" onclick="window._shareMedia('${d.title}')"><i class="fas fa-share-alt"></i></button>
          </div>
        </div>
      </div>
    `).join('') : '';

    document.getElementById('noMediaResults').style.display = filteredMedia.length===0 ? 'block' : 'none';
    document.querySelectorAll('.reveal').forEach(c => revealObserver.observe(c));
  }

  function applyFilters() {
    const cat = document.getElementById('filterMediaCat').value;
    const year = document.getElementById('filterMediaYear').value;
    const search = document.getElementById('searchMedia').value.toLowerCase().trim();
    filteredMedia = mediaData.filter(m => {
      return (cat==='all'||m.category===cat) && (year==='all'||new Date(m.date).getFullYear().toString()===year) && (!search||m.title.toLowerCase().includes(search)||m.description.toLowerCase().includes(search)||m.category.toLowerCase().includes(search));
    });
    filteredMedia = sortByDate(filteredMedia);
    renderAll();
  }

  function resetFilters() {
    document.getElementById('filterMediaCat').value='all'; document.getElementById('filterMediaYear').value='all';
    document.getElementById('searchMedia').value=''; applyFilters();
  }

  // ========== LIGHTBOX ==========
  function openLightbox(type, identifier) {
    let photos;
    if (type === 'photo') {
      photos = mediaData.filter(m => m.type === 'photo');
      lightboxIndex = photos.findIndex(m => m.id === identifier);
    } else {
      photos = filteredMedia.filter(m => m.type === 'photo');
      lightboxIndex = parseInt(identifier);
    }
    if (photos.length === 0) return;
    lightboxItems = photos;
    if (lightboxIndex < 0) lightboxIndex = 0;
    showLightboxImage();
    document.getElementById('lightbox').classList.add('active');
    document.getElementById('lightbox').setAttribute('aria-hidden','false');
    document.body.classList.add('lightbox-open');
  }

  function showLightboxImage() {
    const item = lightboxItems[lightboxIndex];
    const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';
    document.getElementById('lightboxContent').innerHTML = `<img src="${item.source}" alt="${item.title}" onerror="this.src='${item.thumbnail}'"><h4>${item.title}</h4><p>${getCatLabel(item.category)} · ${new Date(item.date).toLocaleDateString(lang === 'ar' ? 'ar-MA' : 'fr-FR')}</p>`;
    document.getElementById('lightboxCounter').textContent = `${lightboxIndex+1} / ${lightboxItems.length}`;
  }

  function closeLightbox() {
    document.getElementById('lightbox').classList.remove('active');
    document.getElementById('lightbox').setAttribute('aria-hidden','true');
    document.body.classList.remove('lightbox-open');
  }

  function lightboxPrev() { if (lightboxItems.length>1) { lightboxIndex = (lightboxIndex-1+lightboxItems.length)%lightboxItems.length; showLightboxImage(); } }
  function lightboxNext() { if (lightboxItems.length>1) { lightboxIndex = (lightboxIndex+1)%lightboxItems.length; showLightboxImage(); } }

  // ========== VIDÉO MODALE ==========
  function openVideo(url, platform, title, desc) {
    const overlay = document.getElementById('videoModal');
    const vidId = platform==='youtube' ? url.split('v=')[1]?.split('&')[0] : '';
    const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';
    document.getElementById('videoModalContent').innerHTML = vidId ? `<iframe src="https://www.youtube.com/embed/${vidId}" title="${title}" allowfullscreen></iframe>` : `<p style="padding:40px;text-align:center">${lang === 'ar' ? 'الفيديو متاح على' : 'Vidéo disponible sur'} <a href="${url}" target="_blank">${platform}</a></p>`;
    document.getElementById('videoModalTitle').textContent = title;
    document.getElementById('videoModalDesc').textContent = desc;
    overlay.classList.add('active'); overlay.setAttribute('aria-hidden','false'); document.body.classList.add('modal-open');
  }

  function closeVideoModal() {
    const overlay = document.getElementById('videoModal');
    overlay.classList.remove('active'); overlay.setAttribute('aria-hidden','true');
    document.getElementById('videoModalContent').innerHTML = '';
    document.body.classList.remove('modal-open');
  }

  // ========== SHARE ==========
  function shareMedia(title) {
    const url = window.location.href;
    if (navigator.share) { navigator.share({title,url}).catch(()=>{}); }
    else { navigator.clipboard.writeText(url).then(()=>showToast(window.FTM_LANG && window.FTM_LANG.ui.link_copied || 'Lien copié !')); }
  }

  function showToast(msg) {
    const t = document.getElementById('toast'); document.getElementById('toastMsg').textContent=msg;
    t.classList.add('show'); setTimeout(()=>t.classList.remove('show'), 3000);
  }

  window._openLightbox = openLightbox;
  window._openVideo = openVideo;
  window._shareMedia = shareMedia;

  document.addEventListener('DOMContentLoaded', () => {
    initYears(); filteredMedia = sortByDate([...mediaData]); updateCounts(); renderAll();
    document.getElementById('filterMediaCat').addEventListener('change', applyFilters);
    document.getElementById('filterMediaYear').addEventListener('change', applyFilters);
    document.getElementById('searchMedia').addEventListener('input', applyFilters);
    document.getElementById('resetMediaFilters').addEventListener('click', resetFilters);

    // Onglets
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentTab = btn.dataset.tab;
        renderAll();
      });
    });

    // Lightbox
    document.getElementById('lightboxClose').addEventListener('click', closeLightbox);
    document.getElementById('lightboxPrev').addEventListener('click', lightboxPrev);
    document.getElementById('lightboxNext').addEventListener('click', lightboxNext);
    document.addEventListener('keydown', e => {
      if (document.getElementById('lightbox').classList.contains('active')) {
        if (e.key==='Escape') closeLightbox();
        if (e.key==='ArrowLeft') lightboxPrev();
        if (e.key==='ArrowRight') lightboxNext();
      }
      if (e.key==='Escape') closeVideoModal();
    });

    document.getElementById('videoModalClose').addEventListener('click', closeVideoModal);
    document.getElementById('videoModal').addEventListener('click', e => { if (e.target===e.currentTarget) closeVideoModal(); });
  });

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

  console.log('✅ Médiathèque - Fondation Tanger Métropole');
})();