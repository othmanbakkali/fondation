(function() {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ========== DONNÉES DES ACTIVITÉS ==========
  const activities = window.FTM_ACTIVITIES_DATA || [];

  let filteredActivities = [...activities];

  // ========== TRI ==========
  function sortByDate(arr) {
    return arr.sort((a, b) => new Date(b.date) - new Date(a.date));
  }

  // ========== INIT FILTRE ANNÉES ==========
  function initYearFilter() {
    const years = [...new Set(activities.map(a => new Date(a.date).getFullYear()))].sort((a, b) => b - a);
    const yearSelect = document.getElementById('filterYear');
    years.forEach(y => {
      const opt = document.createElement('option');
      opt.value = y;
      opt.textContent = y;
      yearSelect.appendChild(opt);
    });
  }

  // ========== FILTRAGE ==========
  function filterActivities() {
    const cat = document.getElementById('filterCategory').value;
    const year = document.getElementById('filterYear').value;
    const month = document.getElementById('filterMonth').value;
    const search = document.getElementById('searchInput').value.toLowerCase().trim();

    filteredActivities = activities.filter(a => {
      const d = new Date(a.date);
      const matchCat = cat === 'all' || a.category === cat;
      const matchYear = year === 'all' || d.getFullYear().toString() === year;
      const matchMonth = month === 'all' || (d.getMonth() + 1).toString().padStart(2, '0') === month;
      const matchSearch = !search || a.title.toLowerCase().includes(search) || a.description.toLowerCase().includes(search) || a.category.toLowerCase().includes(search) || a.location.toLowerCase().includes(search);
      return matchCat && matchYear && matchMonth && matchSearch;
    });

    filteredActivities = sortByDate(filteredActivities);
    renderActivities();
  }

  // ========== HELPERS ==========
  function getCategoryIcon(cat) {
    const icons = { sport: 'fa-futbol', culture: 'fa-palette', education: 'fa-graduation-cap', social: 'fa-heart' };
    return icons[cat] || 'fa-star';
  }

  function getCategoryBadge(cat) {
    const badges = { sport: 'badge-sport', culture: 'badge-culture', education: 'badge-education', social: 'badge-social' };
    return badges[cat] || '';
  }

  function getCategoryLabel(cat) {
    const ui = window.FTM_LANG && window.FTM_LANG.ui;
    if (ui && ui[cat]) return ui[cat];
    const labels = { sport: 'Sport', culture: 'Culture', education: 'Éducation', social: 'Social' };
    return labels[cat] || cat;
  }

  function getReportsText(count) {
    const ui = window.FTM_LANG && window.FTM_LANG.ui;
    if (ui) {
      if (count === 0) return ui.no_report || 'Aucun rapport disponible';
      if (count === 1) return ui.one_report || '1 rapport disponible';
      return `${count} ${ui.reports_available || 'rapports disponibles'}`;
    }
    if (count === 0) return 'Aucun rapport disponible';
    return count === 1 ? '1 rapport disponible' : `${count} rapports disponibles`;
  }

  // ========== RENDU (TOUTES LES ACTIVITÉS) ==========
  function renderActivities() {
    const grid = document.getElementById('activitesGrid');
    const noResults = document.getElementById('noResults');
    const totalCount = document.getElementById('totalCount');

    totalCount.textContent = filteredActivities.length;

    if (filteredActivities.length === 0) {
      grid.innerHTML = '';
      noResults.style.display = 'block';
      return;
    }

    noResults.style.display = 'none';
    
    // Afficher TOUTES les activités filtrées
    grid.innerHTML = filteredActivities.map(a => `
      <div class="activite-card reveal">
        <div class="activite-card-image">
          <img src="${a.image || '/static/core/images/fonlogo.png'}" alt="${a.title}" loading="lazy" onerror="this.src='/static/core/images/fonlogo.png'; this.onerror=null;">
          <span class="activite-card-badge ${getCategoryBadge(a.category)}"><i class="fas ${getCategoryIcon(a.category)}"></i> ${getCategoryLabel(a.category)}</span>
        </div>
        <div class="activite-card-body">
          <h3 class="activite-card-title">${a.title}</h3>
          <p class="activite-card-desc">${a.description}</p>
          <div class="activite-card-meta">
            <span><i class="fas fa-users"></i> ${a.participants} ${window.FTM_LANG && window.FTM_LANG.ui.participants || 'participants'}</span>
            <span><i class="fas fa-file-alt"></i> ${getReportsText(a.reports)}</span>
            <span><i class="far fa-calendar-alt"></i> ${new Date(a.date).toLocaleDateString(window.FTM_LANG && window.FTM_LANG.current_language === 'ar' ? 'ar-MA' : 'fr-FR', {day:'numeric',month:'long',year:'numeric'})}</span>
          </div>
          <div class="activite-card-social">
            ${a.youtubeUrl ? `<a href="${a.youtubeUrl}" target="_blank" rel="noopener noreferrer" class="youtube" aria-label="Voir sur YouTube"><i class="fab fa-youtube"></i></a>` : ''}
            ${a.instagramUrl ? `<a href="${a.instagramUrl}" target="_blank" rel="noopener noreferrer" class="instagram" aria-label="Voir sur Instagram"><i class="fab fa-instagram"></i></a>` : ''}
            ${a.facebookUrl ? `<a href="${a.facebookUrl}" target="_blank" rel="noopener noreferrer" class="facebook" aria-label="Voir sur Facebook"><i class="fab fa-facebook-f"></i></a>` : ''}
          </div>
          <div class="formation-card-actions" style="display:flex; gap:10px; margin-top:auto;">
            <button class="btn btn-outline btn-sm" onclick="window._openModal(${a.id})" style="width: 100%; display: flex; justify-content: center; align-items: center;">${window.FTM_LANG && window.FTM_LANG.ui.read_more || "Lire la suite"}</button>
          </div>
        </div>
      </div>
    `).join('');

    // Réobserver les nouvelles cartes
    document.querySelectorAll('.activite-card.reveal').forEach(c => revealObserver.observe(c));
  }

  // ========== RÉINITIALISER ==========
  function resetFilters() {
    document.getElementById('filterCategory').value = 'all';
    document.getElementById('filterYear').value = 'all';
    document.getElementById('filterMonth').value = 'all';
    document.getElementById('searchInput').value = '';
    filterActivities();
  }

  // ========== MODALE ==========
  function openModal(activityId) {
    const activity = activities.find(a => a.id === activityId);
    if (!activity) return;

    const overlay = document.getElementById('modalOverlay');
    const body = document.getElementById('modalBody');

    body.innerHTML = `
      <img src="${activity.image}" alt="${activity.title}" onerror="this.style.display='none'">
      <span class="activite-card-badge ${getCategoryBadge(activity.category)}" style="position:static;display:inline-flex;margin-bottom:15px;"><i class="fas ${getCategoryIcon(activity.category)}"></i> ${getCategoryLabel(activity.category)}</span>
      <h2 id="modalTitle">${activity.title}</h2>
      <div class="modal-meta">
        <span><i class="far fa-calendar-alt"></i> ${new Date(activity.date).toLocaleDateString(window.FTM_LANG && window.FTM_LANG.current_language === 'ar' ? 'ar-MA' : 'fr-FR', {day:'numeric',month:'long',year:'numeric'})}</span>
        <span><i class="fas fa-map-marker-alt"></i> ${activity.location}</span>
        <span><i class="fas fa-users"></i> ${activity.participants} ${window.FTM_LANG && window.FTM_LANG.ui.participants || 'participants'}</span>
        <span><i class="fas fa-file-alt"></i> ${getReportsText(activity.reports)}</span>
      </div>
      <p class="modal-description">${activity.description}</p>
      ${activity.youtubeUrl ? `<div class="modal-video"><iframe src="${activity.youtubeUrl.replace('watch?v=', 'embed/')}" title="Vidéo de l'activité" loading="lazy" allowfullscreen></iframe></div>` : ''}
      <div class="modal-social">
        ${activity.youtubeUrl ? `<a href="${activity.youtubeUrl}" target="_blank" rel="noopener noreferrer" style="background:#FF0000;color:#fff;"><i class="fab fa-youtube"></i> YouTube</a>` : ''}
        ${activity.instagramUrl ? `<a href="${activity.instagramUrl}" target="_blank" rel="noopener noreferrer" style="background:#E4405F;color:#fff;"><i class="fab fa-instagram"></i> Instagram</a>` : ''}
        ${activity.facebookUrl ? `<a href="${activity.facebookUrl}" target="_blank" rel="noopener noreferrer" style="background:#1877F2;color:#fff;"><i class="fab fa-facebook-f"></i> Facebook</a>` : ''}
      </div>
    `;

    overlay.classList.add('active');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
    document.getElementById('modalClose').focus();
  }

  function openInscription(id) {
    const a = activities.find(x=>x.id===id); if (!a) return;
    const overlay = document.getElementById('inscriptionModal');
    document.getElementById('modalOverlay').classList.remove('active');
    
    const ui = window.FTM_LANG && window.FTM_LANG.ui || {};
    const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';
    
    document.getElementById('inscriptionModalBody').innerHTML = `
      <h2 id="inscriptionTitle">${ui.register || "Inscription"} : ${a.title}</h2>
      <form id="inscriptionForm" onsubmit="window._submitInscription(event,${a.id})">
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
    if (btn) { btn.disabled = true; btn.textContent = 'Envoi en cours...'; }

    fetch(`/activites/${id}/register/`, {
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
            <h2>Inscription reçue !</h2>
            <p>Votre demande d'inscription à l'activité a été transmise avec succès. Elle sera validée par l'administrateur sous peu.</p>
            <p style="font-weight:700;color:var(--primary)">N° de dossier : FTM-ACT-${id}-${data.registration_id}</p>
            <button class="btn btn-primary" onclick="document.getElementById('inscriptionModalClose').click()">Fermer</button>
          </div>`;
      } else {
        alert(data.error || 'Erreur lors de l\'inscription.');
        if (btn) { btn.disabled = false; btn.textContent = 'Confirmer mon inscription'; }
      }
    })
    .catch(err => {
      alert('Erreur de connexion. Veuillez réessayer.');
      if (btn) { btn.disabled = false; btn.textContent = 'Confirmer mon inscription'; }
    });
  }

  function closeModal() {
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.classList.remove('active');
      overlay.setAttribute('aria-hidden', 'true');
    });
    document.body.classList.remove('modal-open');
  }

  window._openModal = openModal;
  window._openInscription = openInscription;
  window._submitInscription = submitInscription;

  // ========== EVENT LISTENERS ==========
  document.addEventListener('DOMContentLoaded', () => {
    initYearFilter();
    filteredActivities = sortByDate([...activities]);
    renderActivities();

    document.getElementById('filterCategory').addEventListener('change', filterActivities);
    document.getElementById('filterYear').addEventListener('change', filterActivities);
    document.getElementById('filterMonth').addEventListener('change', filterActivities);
    document.getElementById('searchInput').addEventListener('input', filterActivities);
    document.getElementById('resetFilters').addEventListener('click', resetFilters);

    document.getElementById('modalClose').addEventListener('click', closeModal);
    document.getElementById('inscriptionModalClose').addEventListener('click', closeModal);
    document.querySelectorAll('.modal-overlay').forEach(m => m.addEventListener('click', e => {
      if (e.target === e.currentTarget) closeModal();
    }));

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeModal();
      }
    });
  });

  // ========== REVEAL OBSERVER ==========
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !prefersReducedMotion) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });

  // ========== BACK TO TOP ==========
  const btt = document.getElementById('backToTop');
  if (btt) {
    window.addEventListener('scroll', () => btt.classList.toggle('show', window.scrollY > 500));
    btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' }));
  }

  // ========== SIDEBAR ==========
  const fs = document.getElementById('floatingSidebar');
  if (fs) window.addEventListener('scroll', () => fs.classList.toggle('visible', window.scrollY > 300));

  // ========== HAMBURGER ==========
  const hamburger = document.getElementById('hamburger');
  const navMenu = document.getElementById('navMenu');
  if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('active'); navMenu.classList.toggle('active');
      hamburger.setAttribute('aria-expanded', navMenu.classList.contains('active'));
    });
    navMenu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
      hamburger.classList.remove('active'); navMenu.classList.remove('active');
    }));
  }

  // ========== DROPDOWN MOBILE ==========
  const dt = document.querySelector('.dropdown-toggle');
  const dp = document.querySelector('.nav-item.dropdown');
  if (dt && dp) {
    dt.addEventListener('click', function(e) {
      if (window.innerWidth <= 768) { e.preventDefault(); dp.classList.toggle('active'); }
    });
  }

  console.log('✅ Page Activités - Fondation Tanger Métropole - ' + activities.length + ' activités chargées');
})();
