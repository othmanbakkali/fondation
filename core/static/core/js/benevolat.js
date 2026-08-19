(function() {
  'use strict';
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ========== DONNÉES ==========
  const actionsData = window.FTM_VOLUNTEER_ACTIONS || [];

  const galeriePhotos = window.FTM_VOLUNTEER_PHOTOS || actionsData.map(a => ({src:a.image, title:a.title, legend:a.description, date:a.date}));

  const videosData = window.FTM_VOLUNTEER_VIDEOS || [];

  const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';

  const domaines = lang === 'ar' ? [
    { icon:"fa-calendar-check", nom:"تنظيم الفعاليات" },{ icon:"fa-directions", nom:"الاستقبال والتوجيه" },
    { icon:"fa-bullhorn", nom:"التواصل" },{ icon:"fa-camera", nom:"التصوير والفيديو" },
    { icon:"fa-paint-brush", nom:"التصميم الغرافيكي" },{ icon:"fa-code", nom:"تطوير الويب" },
    { icon:"fa-hashtag", nom:"شبكات التواصل الاجتماعي" },{ icon:"fa-chalkboard-teacher", nom:"التنشيط والتأطير" },
    { icon:"fa-truck", nom:"اللوجيستيك" },{ icon:"fa-heart", nom:"الأعمال الاجتماعية" },
    { icon:"fa-futbol", nom:"الأنشطة الرياضية" },{ icon:"fa-palette", nom:"الأنشطة الثقافية" },
    { icon:"fa-graduation-cap", nom:"التكوين والمواكبة" }
  ] : (lang === 'en' ? [
    { icon:"fa-calendar-check", nom:"Event organization" },{ icon:"fa-directions", nom:"Reception and orientation" },
    { icon:"fa-bullhorn", nom:"Communication" },{ icon:"fa-camera", nom:"Photography & Video" },
    { icon:"fa-paint-brush", nom:"Graphic design" },{ icon:"fa-code", nom:"Web development" },
    { icon:"fa-hashtag", nom:"Social media" },{ icon:"fa-chalkboard-teacher", nom:"Animation & Supervision" },
    { icon:"fa-truck", nom:"Logistics" },{ icon:"fa-heart", nom:"Social actions" },
    { icon:"fa-futbol", nom:"Sports activities" },{ icon:"fa-palette", nom:"Cultural activities" },
    { icon:"fa-graduation-cap", nom:"Training & Mentoring" }
  ] : [
    { icon:"fa-calendar-check", nom:"Organisation d'événements" },{ icon:"fa-directions", nom:"Accueil et orientation" },
    { icon:"fa-bullhorn", nom:"Communication" },{ icon:"fa-camera", nom:"Photographie et vidéo" },
    { icon:"fa-paint-brush", nom:"Design graphique" },{ icon:"fa-code", nom:"Développement web" },
    { icon:"fa-hashtag", nom:"Réseaux sociaux" },{ icon:"fa-chalkboard-teacher", nom:"Animation et encadrement" },
    { icon:"fa-truck", nom:"Logistique" },{ icon:"fa-heart", nom:"Actions sociales" },
    { icon:"fa-futbol", nom:"Activités sportives" },{ icon:"fa-palette", nom:"Activités culturelles" },
    { icon:"fa-graduation-cap", nom:"Formation et accompagnement" }
  ]);

  const competences = lang === 'ar' ? [
    "التنظيم","التواصل","التصوير الفوتوغرافي","الفيديو","مونتاج الفيديو","التصميم الغرافيكي","تطوير الويب","شبكات التواصل الاجتماعي","التنشيط","التأطير","اللوجيستيك","الإسعافات الأولية","اللغات","الرياضة","الثقافة","التدريب"
  ] : (lang === 'en' ? [
    "Organization","Communication","Photography","Video","Video Editing","Graphic Design","Web Development","Social Media","Animation","Supervision","Logistics","First Aid","Languages","Sports","Culture","Training"
  ] : [
    "Organisation","Communication","Photographie","Vidéo","Montage vidéo","Design graphique","Développement web","Réseaux sociaux","Animation","Encadrement","Logistique","Premiers secours","Langues","Sport","Culture","Formation"
  ]);

  const dispoOptions = lang === 'ar' ? [
    "خلال الأسبوع","في عطلة نهاية الأسبوع","صباحاً","بعد الزوال","مساءً","حسب الحاجة"
  ] : (lang === 'en' ? [
    "Weekdays","Weekends","Morning","Afternoon","Evening","As needed"
  ] : [
    "En semaine","Le week-end","Le matin","L'après-midi","Le soir","Selon les besoins"
  ]);

  const temoignages = window.FTM_TESTIMONIALS || [];

  const faqData = window.FTM_VOLUNTEER_FAQ || [];

  // ========== RENDU ==========
  function renderActions() {
    document.getElementById('actionsGrid').innerHTML = actionsData.sort((a,b)=>new Date(b.date)-new Date(a.date)).map(a => `
      <div class="action-card reveal">
        <img src="${a.image}" alt="${a.title}" loading="lazy" onerror="this.closest('article,.action-card')?.remove()">
        <div class="action-card-body">
          <h4>${a.title}</h4><p>${a.description}</p>
          <div class="action-meta">
            <span><i class="far fa-calendar-alt"></i> ${new Date(a.date).toLocaleDateString(lang === 'ar' ? 'ar-MA' : 'fr-FR')}</span>
            <span><i class="fas fa-map-marker-alt"></i> ${a.location}</span>
            <span><i class="fas fa-users"></i> ${a.volunteers} ${lang === 'ar' ? 'متطوعين' : (lang === 'en' ? 'volunteers' : 'bénévoles')}</span>
          </div>
          <div class="action-social">
            ${a.youtubeUrl?`<a href="${a.youtubeUrl}" target="_blank" class="youtube" aria-label="YouTube"><i class="fab fa-youtube"></i></a>`:''}
            ${a.instagramUrl?`<a href="${a.instagramUrl}" target="_blank" class="instagram" aria-label="Instagram"><i class="fab fa-instagram"></i></a>`:''}
            ${a.facebookUrl?`<a href="${a.facebookUrl}" target="_blank" class="facebook" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>`:''}
          </div>
          <button class="btn btn-primary btn-sm">${lang === 'ar' ? 'اكتشف النشاط' : (lang === 'en' ? 'Discover activity' : "Découvrir l'activité")}</button>
        </div>
      </div>`).join('');
  }

  function renderGalerie() {
    const grid = document.getElementById('galerieGrid');
    if (!grid) return;
    grid.innerHTML = galeriePhotos.map((p,i) => `
      <div class="galerie-item reveal" onclick="window._openLightbox(${i})">
        <img src="${p.src}" alt="${p.title}" loading="lazy" onerror="this.closest('.photo-card,.gallery-item')?.remove()">
      </div>`).join('');
  }

  function renderVideos() {
    const grid = document.getElementById('videosBenevolesGrid');
    if (!grid) return;
    grid.innerHTML = videosData.map(v => `
      <div class="video-card reveal">
        <div class="video-thumb" onclick="window._openVideo('${v.url}','${v.platform}')">
          <img src="${v.thumb}" alt="${v.title}" loading="lazy"><div class="play-icon"><i class="fas fa-play"></i></div>
        </div>
        <div class="video-info"><h4>${v.title}</h4><p style="font-size:.85rem;color:var(--text-secondary)">${v.desc}</p></div>
      </div>`).join('');
  }

  function renderDomaines() {
    document.getElementById('domainesGrid').innerHTML = domaines.map(d => `
      <div class="domaine-card reveal"><i class="fas ${d.icon}"></i><h4>${d.nom}</h4></div>`).join('');
    document.getElementById('domainesCheckGrid').innerHTML = domaines.map((d, i) => `
      <input type="checkbox" id="dom_${i}" class="domaine-check"><label for="dom_${i}">${d.nom}</label>`).join('');
  }

  function renderTemoignages() {
    const grid = document.getElementById('temoignagesGrid');
    if (!grid) return;
    grid.innerHTML = temoignages.map(t => `
      <div class="temoignage-card reveal">
        <img src="${t.photo}" alt="${t.name}" loading="lazy"><p class="quote">« ${t.quote} »</p>
        <p class="name">${t.name}</p><p class="role">${t.role}</p>
      </div>`).join('');
  }

  function renderFaq() {
    document.getElementById('faqList').innerHTML = faqData.map((f,i) => `
      <div class="faq-item"><button class="faq-question" aria-expanded="false">${f.q} <i class="fas fa-chevron-down"></i></button>
      <div class="faq-answer"><p>${f.r}</p></div></div>`).join('');
  }

  function renderCompetences() {
    document.getElementById('competencesGrid').innerHTML = competences.map((c, i) => `
      <input type="checkbox" id="comp_${i}" class="comp-check"><label for="comp_${i}">${c}</label>`).join('');
  }

  function renderDispo() {
    document.getElementById('dispoGrid').innerHTML = dispoOptions.map((d, i) => `
      <input type="checkbox" id="dispo_${i}" class="dispo-check"><label for="dispo_${i}">${d}</label>`).join('');
  }

  // ========== LIGHTBOX ==========
  let lbIndex = 0;
  function openLightbox(i) { lbIndex = i; showLb(); document.getElementById('lightbox').classList.add('active'); document.body.classList.add('lightbox-open'); }
  function showLb() {
    const p = galeriePhotos[lbIndex];
    document.getElementById('lightboxContent').innerHTML = `<img src="${p.src}" alt="${p.title}"><h4 style="color:#fff;margin-top:10px">${p.title}</h4><p style="color:#aaa">${p.legend} · ${p.date}</p>`;
  }
  function closeLb() { document.getElementById('lightbox').classList.remove('active'); document.body.classList.remove('lightbox-open'); }
  window._openLightbox = openLightbox;

  // ========== VIDÉO ==========
  function openVideo(url, platform) {
    const overlay = document.getElementById('videoModal');
    const vidId = platform==='youtube' ? url.split('v=')[1]?.split('&')[0] : '';
    document.getElementById('videoModalContent').innerHTML = vidId ? `<iframe src="https://www.youtube.com/embed/${vidId}" title="Vidéo" allowfullscreen></iframe>` : `<p style="padding:40px;text-align:center">${lang === 'ar' ? 'فيديو على' : (lang === 'en' ? 'Video on' : 'Vidéo sur')} <a href="${url}" target="_blank">${platform}</a></p>`;
    overlay.classList.add('active'); document.body.classList.add('modal-open');
  }
  function closeVideo() { document.getElementById('videoModal').classList.remove('active'); document.getElementById('videoModalContent').innerHTML=''; document.body.classList.remove('modal-open'); }
  window._openVideo = openVideo;

  // ========== CHIFFRES ANIMÉS ==========
  const chiffresObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting && !e.target.dataset.animated) {
        e.target.dataset.animated = '1';
        const target = +e.target.dataset.target, duration = 2000, step = target/(duration/16);
        let current = 0;
        const update = () => { current+=step; if(current<target){ e.target.textContent=Math.floor(current); requestAnimationFrame(update); } else e.target.textContent=target; };
        update();
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.chiffre-num').forEach(el => chiffresObserver.observe(el));

  // ========== INIT ==========
  document.addEventListener('DOMContentLoaded', () => {
    renderActions(); renderGalerie(); renderVideos(); renderDomaines(); renderTemoignages(); renderFaq(); renderCompetences(); renderDispo();
    if (window.FTM_TRANSLATE_UI) window.FTM_TRANSLATE_UI();
    document.querySelectorAll('.reveal').forEach(el => {
      revealObserver.observe(el);
      el.classList.add('visible');
    });

    // FAQ
    document.querySelectorAll('.faq-question').forEach(btn => {
      btn.addEventListener('click', () => { btn.parentElement.classList.toggle('active'); btn.setAttribute('aria-expanded', btn.parentElement.classList.contains('active')); });
    });

    // Ville autre
    document.getElementById('ville').addEventListener('change', function() {
      document.getElementById('autreVilleGroup').style.display = this.value==='autre'?'block':'none';
    });

    // CV
    document.getElementById('cv').addEventListener('change', function() {
      const file = this.files[0];
      if (file) {
        if (file.size > 5*1024*1024) { document.getElementById('cvInfo').textContent=lang === 'ar' ? 'الملف كبير جداً (>5 ميغا)' : (lang === 'en' ? 'File too large (>5 MB)' : 'Fichier trop volumineux (>5 Mo)'); this.value=''; }
        else { document.getElementById('cvInfo').textContent = file.name + ' (' + (file.size/1024).toFixed(1) + ' Ko)'; }
      }
    });

    // Formulaire
    document.getElementById('candidatureForm').addEventListener('submit', function(e) {
      e.preventDefault();
      const btn = document.getElementById('submitBtn');
      btn.textContent = lang === 'ar' ? 'جاري الإرسال...' : (lang === 'en' ? 'Sending...' : 'Envoi en cours...'); btn.disabled = true;

      const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
      const checkedComps = Array.from(document.querySelectorAll('.comp-check:checked'))
                                .map(cb => cb.nextElementSibling.textContent);
      const competencesStr = checkedComps.join(', ');
      
      const cityVal = document.getElementById('ville').value;
      const finalCity = cityVal === 'autre' ? document.getElementById('autreVille').value.trim() : cityVal;

      const checkedDispos = Array.from(document.querySelectorAll('.dispo-check:checked'))
                                 .map(cb => cb.nextElementSibling.textContent);
      const dispoStr = checkedDispos.join(', ');

      const checkedDomaines = Array.from(document.querySelectorAll('.domaine-check:checked'))
                                    .map(cb => cb.nextElementSibling.textContent);
      const domainesStr = checkedDomaines.join(', ');

      const formData = new FormData();
      formData.append('nom', document.getElementById('nom').value.trim());
      formData.append('email', document.getElementById('email').value.trim());
      formData.append('telephone', document.getElementById('tel').value.trim());
      formData.append('ville', finalCity);
      formData.append('competences', competencesStr);
      formData.append('skills_description', document.getElementById('descComp').value.trim());
      formData.append('availability', dispoStr);
      formData.append('desired_fields', domainesStr);
      formData.append('motivation', document.getElementById('motivation').value.trim());
      formData.append('experience', document.getElementById('experience').value.trim());
      
      const cvFile = document.getElementById('cv').files[0];
      if (cvFile) {
        formData.append('cv', cvFile);
      }

      fetch(window.location.pathname, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrf,
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          document.getElementById('refCandidature').textContent = data.reference;
          document.getElementById('candidatureForm').style.display = 'none';
          document.getElementById('candidatureSuccess').style.display = 'block';
          document.getElementById('candidatureSuccess').scrollIntoView({ behavior: 'smooth' });
        } else {
          alert(lang === 'ar' ? 'حدث خطأ، يرجى المحاولة مرة أخرى.' : 'Une erreur est survenue, veuillez réessayer.');
          btn.textContent = lang === 'ar' ? 'إرسال الطلب' : (lang === 'en' ? 'Submit my candidacy' : 'Envoyer ma candidature');
          btn.disabled = false;
        }
      })
      .catch(err => {
        console.error(err);
        alert(lang === 'ar' ? 'حدث خطأ، يرجى المحاولة مرة أخرى.' : 'Une erreur est survenue, veuillez réessayer.');
        btn.textContent = lang === 'ar' ? 'إرسال الطلب' : (lang === 'en' ? 'Submit my candidacy' : 'Envoyer ma candidature');
        btn.disabled = false;
      });
    });

    // Lightbox
    const lightbox = document.getElementById('lightbox');
    const lightboxClose = document.getElementById('lightboxClose');
    const lightboxPrev = document.getElementById('lightboxPrev');
    const lightboxNext = document.getElementById('lightboxNext');
    const videoModal = document.getElementById('videoModal');
    const videoModalClose = document.getElementById('videoModalClose');
    if (lightboxClose) lightboxClose.addEventListener('click', closeLb);
    if (lightboxPrev) lightboxPrev.addEventListener('click', () => { lbIndex = (lbIndex-1+galeriePhotos.length)%galeriePhotos.length; showLb(); });
    if (lightboxNext) lightboxNext.addEventListener('click', () => { lbIndex = (lbIndex+1)%galeriePhotos.length; showLb(); });
    document.addEventListener('keydown', e => {
      if (lightbox && lightbox.classList.contains('active')) {
        if (e.key==='Escape') closeLb(); if (e.key==='ArrowLeft' && lightboxPrev) lightboxPrev.click(); if (e.key==='ArrowRight' && lightboxNext) lightboxNext.click();
      }
      if (e.key==='Escape') closeVideo();
    });
    if (videoModalClose) videoModalClose.addEventListener('click', closeVideo);
    if (videoModal) videoModal.addEventListener('click', e => { if (e.target===e.currentTarget) closeVideo(); });
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

  console.log('Page Benevolat - Fondation Tanger Metropole');
})();

