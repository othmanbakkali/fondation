(function() {
  'use strict';
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const faqData = window.FTM_CONTACT_FAQ || [];

  function renderFaq() {
    document.getElementById('faqList').innerHTML = faqData.map(f => `
      <div class="faq-item"><button class="faq-question" aria-expanded="false">${f.q} <i class="fas fa-chevron-down"></i></button>
      <div class="faq-answer"><p>${f.r}</p></div></div>`).join('');
  }

  document.addEventListener('DOMContentLoaded', () => {
    renderFaq();

    // FAQ accordéon
    document.querySelectorAll('.faq-question').forEach(btn => {
      btn.addEventListener('click', () => {
        btn.parentElement.classList.toggle('active');
        btn.setAttribute('aria-expanded', btn.parentElement.classList.contains('active'));
      });
    });

    const lang = window.FTM_LANG && window.FTM_LANG.current_language || 'fr';

    // Compteur caractères
    const message = document.getElementById('message');
    const charCount = document.getElementById('charCount');
    if (message && charCount) {
      message.addEventListener('input', () => {
        charCount.textContent = message.value.length + (lang === 'ar' ? ' / 1000 حرف' : ' / 1000 caractères');
      });
    }

    // Pièce jointe
    document.getElementById('pj').addEventListener('change', function() {
      const file = this.files[0];
      if (file) {
        if (file.size > 5*1024*1024) { document.getElementById('pjInfo').textContent=lang === 'ar' ? 'الملف كبير جداً (>5 ميغا)' : (lang === 'en' ? 'File too large (>5 MB)' : 'Fichier trop volumineux (>5 Mo)'); this.value=''; }
        else { document.getElementById('pjInfo').textContent = file.name + ' (' + (file.size/1024).toFixed(1) + ' Ko)'; }
      }
    });

    // Ville autre
    const villeSelect = document.getElementById('ville');
    if (villeSelect) {
      villeSelect.addEventListener('change', function() {
        const otherGroup = document.getElementById('autreVilleGroup');
        if (otherGroup) otherGroup.style.display = this.value==='autre'?'block':'none';
      });
    }

    // Objet autre
    const objetSelect = document.getElementById('objet');
    if (objetSelect) {
      objetSelect.addEventListener('change', function() {
        const otherGroup = document.getElementById('autreObjetGroup');
        if (otherGroup) otherGroup.style.display = this.value==='autre'?'block':'none';
      });
    }

    // Formulaire
    document.getElementById('contactForm').addEventListener('submit', function(e) {
      e.preventDefault();
      const btn = document.getElementById('submitBtn');
      const nom = document.getElementById('nom').value.trim();
      const email = document.getElementById('email').value.trim();
      const objetVal = document.getElementById('objet').value;
      const sujet = document.getElementById('sujet').value.trim();
      const msg = document.getElementById('message').value.trim();
      const consent = document.getElementById('consentement').checked;
      let valid = true;

      // Reset erreurs
      document.querySelectorAll('.error-msg').forEach(el => el.style.display='none');
      document.querySelectorAll('.form-group input,.form-group select,.form-group textarea').forEach(el => el.style.borderColor='var(--bg-section)');

      if (!nom) { showError('nom', lang === 'ar' ? 'هذا الحقل إجباري' : (lang === 'en' ? 'This field is required' : 'Ce champ est obligatoire')); valid=false; }
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { showError('email', lang === 'ar' ? 'البريد الإلكتروني غير صالح' : (lang === 'en' ? 'Invalid email address' : 'Adresse email invalide')); valid=false; }
      if (!objetVal) { showError('objet', lang === 'ar' ? 'يرجى تحديد الموضوع' : (lang === 'en' ? 'Please select a subject' : 'Veuillez sélectionner un objet')); valid=false; }
      if (!sujet) { showError('sujet', lang === 'ar' ? 'هذا الحقل إجباري' : (lang === 'en' ? 'This field is required' : 'Ce champ est obligatoire')); valid=false; }
      if (!msg || msg.length < 10) { showError('message', lang === 'ar' ? 'الحد الأدنى 10 أحرف' : (lang === 'en' ? 'Minimum 10 characters' : 'Minimum 10 caractères')); valid=false; }
      if (!consent) { alert(lang === 'ar' ? 'يرجى قبول معالجة معلوماتكم الشخصية.' : (lang === 'en' ? 'Please accept the processing of your information.' : 'Veuillez accepter le traitement de vos informations.')); valid=false; }

      if (!valid) return;

      btn.textContent = lang === 'ar' ? 'جاري الإرسال...' : (lang === 'en' ? 'Sending...' : 'Envoi en cours...'); btn.disabled = true;

      const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
      
      const cityVal = document.getElementById('ville').value;
      const finalCity = cityVal === 'autre' ? document.getElementById('autreVille').value.trim() : cityVal;

      const finalObjet = objetVal === 'autre' ? document.getElementById('autreObjet').value.trim() : objetVal;

      const formData = new FormData();
      formData.append('nom', nom);
      formData.append('email', email);
      formData.append('telephone', document.getElementById('tel').value.trim());
      formData.append('ville', finalCity);
      formData.append('objet', finalObjet);
      formData.append('sujet', sujet);
      formData.append('message', msg);
      
      const pjFile = document.getElementById('pj').files[0];
      if (pjFile) {
        formData.append('pj', pjFile);
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
          document.getElementById('refMessage').textContent = data.reference;
          document.getElementById('contactForm').style.display = 'none';
          document.getElementById('formSuccess').style.display = 'block';
          document.getElementById('formSuccess').scrollIntoView({ behavior: 'smooth' });
        } else {
          alert(lang === 'ar' ? 'حدث خطأ، يرجى المحاولة مرة أخرى.' : 'Une erreur est survenue, veuillez réessayer.');
          btn.textContent = lang === 'ar' ? 'إرسال الرسالة' : (lang === 'en' ? 'Send message' : 'Envoyer le message');
          btn.disabled = false;
        }
      })
      .catch(err => {
        console.error(err);
        alert(lang === 'ar' ? 'حدث خطأ، يرجى المحاولة مرة أخرى.' : 'Une erreur est survenue, veuillez réessayer.');
        btn.textContent = lang === 'ar' ? 'إرسال الرسالة' : (lang === 'en' ? 'Send message' : 'Envoyer le message');
        btn.disabled = false;
      });
    });

    function showError(id, msg) {
      const el = document.getElementById(id);
      el.style.borderColor = '#EF4444';
      let err = el.parentElement.querySelector('.error-msg');
      if (!err) { err = document.createElement('small'); err.className='error-msg'; el.parentElement.appendChild(err); }
      err.textContent = msg; err.style.display = 'block';
    }
  });

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting && !prefersReducedMotion) e.target.classList.add('visible'); });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

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

  console.log('✅ Page Contact - Fondation Tanger Métropole');
})();