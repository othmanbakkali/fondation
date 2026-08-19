(function() {
  'use strict';
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const formationsData = window.FTM_FORMATIONS_DATA || [];

  let filteredFormations = [...formationsData];

  function sortByDate(arr) { return arr.sort((a,b) => new Date(a.startDate) - new Date(b.startDate)); }

  function getRemaining(f) { return f.totalSeats - f.registeredSeats; }
  function getStatus(f) {
    const now = new Date();
    if (f.endDate) {
      const end = new Date(f.endDate + 'T' + (f.endTime || '23:59:59'));
      if (now > end) return 'finished';
    }
    if (f.registrationDeadline) {
      const deadline = new Date(f.registrationDeadline + 'T23:59:59');
      if (deadline < now && getRemaining(f) > 0) return 'closed';
    }
    if (getRemaining(f) <= 0) return 'full';
    if (getRemaining(f) <= 5) return 'limited';
    return 'open';
  }
  function getStatusLabel(s) {
    const isAr = window.FTM_LANG && window.FTM_LANG.current_language === 'ar';
    const isEn = window.FTM_LANG && window.FTM_LANG.current_language === 'en';
    const labels = { 
      open: isAr ? 'التسجيل مفتوح' : (isEn ? 'Registration open' : 'Inscriptions ouvertes'), 
      limited: isAr ? 'مقاعد محدودة' : (isEn ? 'Limited seats' : 'Places limitées'), 
      full: isAr ? 'ممتلئ' : (isEn ? 'Full' : 'Complet'), 
      closed: isAr ? 'التسجيل مغلق' : (isEn ? 'Registration closed' : 'Inscriptions fermées'), 
      finished: isAr ? 'منتهية' : (isEn ? 'Finished' : 'Formation terminée') 
    };
    return labels[s]||s;
  }
  function getStatusClass(s) {
    const classes = { open:'status-open', limited:'status-limited', full:'status-full', closed:'status-closed', finished:'status-finished' };
    return classes[s]||'';
  }
  function getCatLabel(c) {
    const ui = window.FTM_LANG && window.FTM_LANG.ui;
    if (ui && ui[c]) return ui[c];
    const l = { numerique:'Numérique', entrepreneuriat:'Entrepreneuriat', devperso:'Dév. personnel', communication:'Communication', gestion:'Gestion', langues:'Langues', culture:'Culture', social:'Social', sport:'Sport' };
    return l[c]||c;
  }
  function getSeatsColor(remaining, total) {
    const pct = (remaining/total)*100;
    if (pct <= 0) return '#EF4444';
    if (pct <= 15) return '#F59E0B';
    return '#10B981';
  }

  function initYears() {
    const years = [...new Set(formationsData.filter(f => f.startDate).map(f => new Date(f.startDate).getFullYear()))].sort((a,b) => b-a);
    const sel = document.getElementById('filterFormYear');
    years.forEach(y => { const o = document.createElement('option'); o.value=y; o.textContent=y; sel.appendChild(o); });
  }

  function updateStats() {
    const open = filteredFormations.filter(f => ['open','limited'].includes(getStatus(f))).length;
    const seats = filteredFormations.reduce((acc,f) => acc + Math.max(0, getRemaining(f)), 0);
    const reg = filteredFormations.reduce((acc,f) => acc + f.registeredSeats, 0);
    document.getElementById('statTotal').textContent = filteredFormations.length;
    document.getElementById('statOpen').textContent = open;
    document.getElementById('statSeats').textContent = seats;
    document.getElementById('statRegistered').textContent = reg;
  }

  function renderFormations() {
    const grid = document.getElementById('formationsGrid');
    const noRes = document.getElementById('noFormResults');
    if (filteredFormations.length === 0) { grid.innerHTML=''; noRes.style.display='block'; updateStats(); return; }
    noRes.style.display='none';
    grid.innerHTML = filteredFormations.map(f => {
      const status = getStatus(f); const rem = getRemaining(f); const pct = ((f.registeredSeats/f.totalSeats)*100).toFixed(0);
      return `
      <div class="formation-card reveal">
        <div class="formation-card-image">
          <img src="${f.image || '/static/core/images/fonlogo.png'}" alt="${f.title}" loading="lazy" onerror="this.src='/static/core/images/fonlogo.png'; this.onerror=null;">
          <span class="formation-card-badge" style="background:${getSeatsColor(rem,f.totalSeats)}">${getCatLabel(f.category)}</span>
        </div>
        <div class="formation-card-body">
          <span class="status-badge ${getStatusClass(status)}">${getStatusLabel(status)}</span>
          <h3>${f.title}</h3>
          <p class="formation-card-desc">${f.description}</p>
          <div class="formation-card-meta">
            <span><i class="fas fa-user"></i> ${f.instructor.name}</span>
            <span><i class="far fa-calendar-alt"></i> ${f.startDate ? new Date(f.startDate).toLocaleDateString(window.FTM_LANG && window.FTM_LANG.current_language === 'ar' ? 'ar-MA' : 'fr-FR',{day:'numeric',month:'short'}) : (window.FTM_LANG && window.FTM_LANG.current_language === 'ar' ? 'قريباً' : 'À venir')}</span>
            <span><i class="fas fa-map-marker-alt"></i> ${f.location ? f.location.split('–')[0] : ''}</span>
          </div>
          <div class="seats-bar"><div class="seats-fill" style="width:${pct}%;background:${getSeatsColor(rem,f.totalSeats)}"></div></div>
          <div class="seats-info">
            <span>${f.registeredSeats}/${f.totalSeats} ${window.FTM_LANG && window.FTM_LANG.ui.current_language === 'ar' ? 'مسجل' : 'inscrits'}</span>
            <span class="remaining ${rem<=5&&rem>0?'limited':''} ${rem<=0?'full':''}">${rem>0?rem+(window.FTM_LANG && window.FTM_LANG.current_language === 'ar' ? ' مقاعد متبقية' : ' places restantes'):(window.FTM_LANG && window.FTM_LANG.current_language === 'ar' ? 'ممتلئ' : 'Complet')}</span>
          </div>
          <div class="formation-card-actions">
            ${status==='open'||status==='limited' ? `<button class="btn btn-primary btn-sm" onclick="window._openInscription(${f.id})">${window.FTM_LANG && window.FTM_LANG.ui.register || "S'inscrire"}</button>` : `<button class="btn btn-sm" style="background:#ccc;color:#666;cursor:not-allowed" disabled>${status==='full'?(window.FTM_LANG && window.FTM_LANG.current_language === 'ar' ? 'ممتلئ' : 'Complet'):status==='closed'?(window.FTM_LANG && window.FTM_LANG.current_language === 'ar' ? 'التسجيل مغلق' : 'Inscriptions fermées'):(window.FTM_LANG && window.FTM_LANG.current_language === 'ar' ? 'منتهية' : 'Terminé')}</button>`}
            <button class="btn btn-outline btn-sm" onclick="window._openDetail(${f.id})">${window.FTM_LANG && window.FTM_LANG.current_language === 'ar' ? 'التفاصيل' : 'Détails'}</button>
            <button class="btn btn-sm" style="background:var(--bg-light);" onclick="window._shareFormation(${f.id})" title="Partager"><i class="fas fa-share-alt"></i></button>
          </div>
        </div>
      </div>`;
    }).join('');
    document.querySelectorAll('.formation-card.reveal').forEach(c => revealObserver.observe(c));
    updateStats();
  }

  function applyFilters() {
    const cat = document.getElementById('filterFormCat').value;
    const status = document.getElementById('filterStatus').value;
    const year = document.getElementById('filterFormYear').value;
    const search = document.getElementById('searchForm').value.toLowerCase().trim();
    filteredFormations = formationsData.filter(f => {
      const s = getStatus(f);
      return (cat==='all'||f.category===cat) && (status==='all'||s===status) && (year==='all'||(f.startDate && new Date(f.startDate).getFullYear().toString()===year)) && (!search||f.title.toLowerCase().includes(search)||f.description.toLowerCase().includes(search)||f.instructor.name.toLowerCase().includes(search)||f.location.toLowerCase().includes(search)||f.category.toLowerCase().includes(search));
    });
    filteredFormations = sortByDate(filteredFormations);
    renderFormations();
  }

  function resetFilters() {
    document.getElementById('filterFormCat').value='all'; document.getElementById('filterStatus').value='all';
    document.getElementById('filterFormYear').value='all'; document.getElementById('searchForm').value='';
    applyFilters();
  }

  // ========== MODALES ==========
  function openInscription(id) {
    const f = formationsData.find(x=>x.id===id); if (!f) return;
    const overlay = document.getElementById('inscriptionModal');
    
    const ui = window.FTM_LANG && window.FTM_LANG.ui || {};
    const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';

    document.getElementById('inscriptionModalBody').innerHTML = `
      <h2 id="inscriptionTitle">${ui.register || "Inscription"} : ${f.title}</h2>
      <form id="inscriptionForm" onsubmit="window._submitInscription(event,${f.id})">
        <div class="form-row">
          <div class="form-group"><label>${ui.full_name_label || "Nom complet *"}</label><input type="text" id="regName" required></div>
          <div class="form-group"><label>${ui.birth_date_label || "Date de naissance *"}</label><input type="date" id="regBirthDate" required></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label>${ui.email_label || "Email *"}</label><input type="email" id="regEmail" required></div>
          <div class="form-group"><label>${ui.phone_label || "Téléphone *"}</label><input type="tel" id="regPhone" required></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label>${ui.city_label || "Ville *"}</label><input type="text" id="regCity" required></div>
          <div class="form-group"><label>${ui.study_level_label || "Niveau d'études"}</label>
            <select id="regStudyLevel">
              <option>${lang === 'ar' ? 'بكالوريا' : 'Bac'}</option>
              <option>${lang === 'ar' ? 'بكالوريا + 2' : 'Bac+2'}</option>
              <option>${lang === 'ar' ? 'إجازة' : 'Licence'}</option>
              <option>${lang === 'ar' ? 'ماستر' : 'Master'}</option>
              <option>${lang === 'ar' ? 'دكتوراه' : 'Doctorat'}</option>
            </select>
          </div>
        </div>
        <div class="form-group"><label>${ui.motivation_label || "Motivation"}</label><textarea id="regMotivation" rows="3"></textarea></div>
        <label class="checkbox-label"><input type="checkbox" required> ${ui.accept_terms || "J'accepte les conditions d'inscription *"}</label>
        <button type="submit" class="btn btn-primary" style="width:100%">${ui.confirm_registration || "Confirmer mon inscription"}</button>
      </form>`;
    overlay.classList.add('active'); overlay.setAttribute('aria-hidden','false'); document.body.classList.add('modal-open');
  }

  function submitInscription(e, id) {
    e.preventDefault();
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    const name = document.getElementById('regName').value;
    const email = document.getElementById('regEmail').value;
    const phone = document.getElementById('regPhone').value;
    const city = document.getElementById('regCity').value;

    const formData = new FormData();
    formData.append('name', name);
    formData.append('email', email);
    formData.append('phone', phone);
    formData.append('city', city);
    if (csrfToken) {
      formData.append('csrfmiddlewaretoken', csrfToken);
    }

    const btn = e.target.querySelector('button[type="submit"]');
    const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';
    if (btn) { btn.disabled = true; btn.textContent = lang === 'ar' ? 'جاري الإرسال...' : (lang === 'en' ? 'Sending...' : 'Envoi en cours...'); }

    fetch(`/formations/${id}/register/`, {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': csrfToken || ''
      }
    })
    .then(response => {
      if (!response.ok) throw new Error('Network error');
      return response.json();
    })
    .then(data => {
      if (data.success) {
        document.getElementById('inscriptionModalBody').innerHTML = `
          <div class="inscription-success">
            <i class="fas fa-check-circle"></i>
            <h2>${lang === 'ar' ? 'تم استلام التسجيل !' : (lang === 'en' ? 'Registration received!' : 'Inscription reçue !')}</h2>
            <p>${lang === 'ar' ? 'تم إرسال طلب التسجيل الخاص بك بنجاح. سيتم التحقق منه من طرف المسؤول قريباً.' : (lang === 'en' ? 'Your registration request has been successfully transmitted. It will be validated by the administrator shortly.' : "Votre demande d'inscription a été transmise avec succès. Elle sera validée par l'administrateur sous peu.")}</p>
            <p style="font-weight:700;color:var(--primary)">${lang === 'ar' ? 'رقم الملف' : (lang === 'en' ? 'File No.' : 'N° de dossier')} : FTM-${id}-${data.registration_id}</p>
            <button class="btn btn-primary" onclick="document.getElementById('inscriptionModalClose').click()">${lang === 'ar' ? 'إغلاق' : (lang === 'en' ? 'Close' : 'Fermer')}</button>
          </div>`;
      } else {
        alert(data.error || 'Erreur.');
        if (btn) { btn.disabled = false; btn.textContent = window.FTM_LANG && window.FTM_LANG.ui.confirm_registration || "Confirmer mon inscription"; }
      }
    })
    .catch(err => {
      alert('Erreur.');
      if (btn) { btn.disabled = false; btn.textContent = window.FTM_LANG && window.FTM_LANG.ui.confirm_registration || "Confirmer mon inscription"; }
    });
  }

  function openDetail(id) {
    const f = formationsData.find(x=>x.id===id); if (!f) return;
    const overlay = document.getElementById('detailModal');
    const status = getStatus(f); const rem = getRemaining(f);
    const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';
    document.getElementById('detailModalBody').innerHTML = `
      <img src="${f.image}" alt="${f.title}" style="width:100%;border-radius:16px;margin-bottom:20px;max-height:350px;object-fit:cover" onerror="this.style.display='none'">
      <span class="status-badge ${getStatusClass(status)}">${getStatusLabel(status)}</span>
      <h2>${f.title}</h2>
      <div class="formation-card-meta" style="margin-bottom:15px">
        <span><i class="fas fa-user"></i> ${f.instructor.name}</span>
        <span><i class="far fa-calendar-alt"></i> ${f.startDate ? new Date(f.startDate).toLocaleDateString(lang === 'ar' ? 'ar-MA' : 'fr-FR',{day:'numeric',month:'long',year:'numeric'}) + (f.endDate ? ' → ' + new Date(f.endDate).toLocaleDateString(lang === 'ar' ? 'ar-MA' : 'fr-FR',{day:'numeric',month:'long',year:'numeric'}) : '') : (lang === 'ar' ? 'قريباً' : 'À venir')}</span>
        ${f.startTime ? `<span><i class="far fa-clock"></i> ${f.startTime} - ${f.endTime || ''}</span>` : ''}
        <span><i class="fas fa-map-marker-alt"></i> ${f.location || ''}</span>
      </div>
      ${f.fullDescription}
      <div style="margin-top:20px"><strong>${lang === 'ar' ? 'المقاعد' : 'Places'} :</strong> ${f.registeredSeats}/${f.totalSeats} (${rem > 0 ? rem + (lang === 'ar' ? ' متبقية' : ' restantes') : (lang === 'ar' ? 'ممتلئ' : 'Complet')})</div>
    `;
    overlay.classList.add('active'); overlay.setAttribute('aria-hidden','false'); document.body.classList.add('modal-open');
  }

  function shareFormation(id) {
    const f = formationsData.find(x=>x.id===id); if (!f) return;
    const url = `https://www.tangermetropole.ma/formations/${f.slug}/`;
    if (navigator.share) { navigator.share({title:f.title,text:f.description,url:url}).catch(()=>{}); }
    else { navigator.clipboard.writeText(url).then(()=>showToast(window.FTM_LANG && window.FTM_LANG.ui.link_copied || 'Lien copié avec succès !')); }
  }

  function showToast(msg) {
    const t = document.getElementById('toastNotification'); document.getElementById('toastMsg').textContent=msg;
    t.classList.add('show'); setTimeout(()=>t.classList.remove('show'), 3000);
  }

  function closeModals() {
    document.querySelectorAll('.modal-overlay').forEach(m=>{m.classList.remove('active');m.setAttribute('aria-hidden','true');});
    document.body.classList.remove('modal-open');
  }

  window._openInscription = openInscription;
  window._openDetail = openDetail;
  window._shareFormation = shareFormation;
  window._submitInscription = submitInscription;

  document.addEventListener('DOMContentLoaded', () => {
    initYears(); filteredFormations = sortByDate([...formationsData]); renderFormations();
    document.getElementById('filterFormCat').addEventListener('change', applyFilters);
    document.getElementById('filterStatus').addEventListener('change', applyFilters);
    document.getElementById('filterFormYear').addEventListener('change', applyFilters);
    document.getElementById('searchForm').addEventListener('input', applyFilters);
    document.getElementById('resetFormFilters').addEventListener('click', resetFilters);
    document.getElementById('inscriptionModalClose').addEventListener('click', closeModals);
    document.getElementById('detailModalClose').addEventListener('click', closeModals);
    document.querySelectorAll('.modal-overlay').forEach(m=>m.addEventListener('click',e=>{if(e.target===e.currentTarget)closeModals();}));
    document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModals();});
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

  console.log('✅ Page Formations - Fondation Tanger Métropole');
})();
