// ========== MAIN.JS - FONDATION TANGER METROPOLE ==========
(function() {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

  const navbar = $('#navbar');
  if (navbar) {
    const updateNavbar = () => navbar.classList.toggle('scrolled', window.scrollY > 50);
    updateNavbar();
    window.addEventListener('scroll', updateNavbar, { passive: true });
  }

  const hamburger = $('#hamburger');
  const navMenu = $('#navMenu');
  const closeMenu = () => {
    if (!hamburger || !navMenu) return;
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
    hamburger.setAttribute('aria-expanded', 'false');
  };
  if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('active');
      navMenu.classList.toggle('active');
      hamburger.setAttribute('aria-expanded', navMenu.classList.contains('active') ? 'true' : 'false');
    });
    $$('#navMenu a').forEach(link => link.addEventListener('click', () => {
      if (!link.classList.contains('dropdown-toggle') || window.innerWidth > 768) closeMenu();
    }));
    document.addEventListener('click', e => {
      if (navMenu.classList.contains('active') && !navMenu.contains(e.target) && !hamburger.contains(e.target)) closeMenu();
    });
  }

  const dropdownToggle = $('.dropdown-toggle');
  const dropdownParent = $('.nav-item.dropdown');
  if (dropdownToggle && dropdownParent) {
    dropdownToggle.addEventListener('click', e => {
      if (window.innerWidth <= 768) {
        e.preventDefault();
        dropdownParent.classList.toggle('active');
        dropdownToggle.setAttribute('aria-expanded', dropdownParent.classList.contains('active') ? 'true' : 'false');
      }
    });
    document.addEventListener('click', e => {
      if (!dropdownParent.contains(e.target)) {
        dropdownParent.classList.remove('active');
        dropdownToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  const sections = $$('section[id]');
  const navLinks = $$('.nav-link:not(.dropdown-toggle)');
  if (sections.length && navLinks.length) {
    window.addEventListener('scroll', () => {
      let current = '';
      sections.forEach(section => {
        if (window.scrollY >= section.offsetTop - 120) current = section.getAttribute('id') || '';
      });
      navLinks.forEach(link => {
        link.classList.toggle('active', current && (link.getAttribute('href') || '').includes(current));
      });
    }, { passive: true });
  }

  const slidesTrack = $('#slidesTrack');
  const sliderDots = $('#sliderDots');
  if (slidesTrack && sliderDots) {
    const slides = $$('.slide', slidesTrack);
    let currentSlide = 0;
    let slideInterval = null;

    slides.forEach((_, i) => {
      const dot = document.createElement('span');
      dot.className = `dot${i === 0 ? ' active' : ''}`;
      dot.addEventListener('click', () => goToSlide(i));
      sliderDots.appendChild(dot);
    });

    const updateSlider = () => {
      if (!slides.length) return;
      slidesTrack.style.transform = `translateX(-${currentSlide * 100}%)`;
      $$('.dot', sliderDots).forEach((dot, i) => dot.classList.toggle('active', i === currentSlide));
    };
    const nextSlide = () => { currentSlide = (currentSlide + 1) % Math.max(slides.length, 1); updateSlider(); };
    const prevSlide = () => { currentSlide = (currentSlide - 1 + Math.max(slides.length, 1)) % Math.max(slides.length, 1); updateSlider(); };
    function goToSlide(i) { currentSlide = i; updateSlider(); resetInterval(); }
    function startInterval() { if (slides.length > 1 && !prefersReducedMotion) slideInterval = setInterval(nextSlide, 4000); }
    function resetInterval() { clearInterval(slideInterval); startInterval(); }

    $('#prevSlide')?.addEventListener('click', () => { prevSlide(); resetInterval(); });
    $('#nextSlide')?.addEventListener('click', () => { nextSlide(); resetInterval(); });
    $('#annonceSlider')?.addEventListener('mouseenter', () => clearInterval(slideInterval));
    $('#annonceSlider')?.addEventListener('mouseleave', startInterval);
    startInterval();
  }

  const statsSection = $('#stats');
  if (statsSection) {
    let statsAnimated = false;
    const statsObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting || statsAnimated) return;
        statsAnimated = true;
        $$('.stat-number').forEach(stat => {
          const target = Number(stat.getAttribute('data-target') || stat.textContent || 0);
          const duration = prefersReducedMotion ? 1 : 1800;
          const step = Math.max(target / (duration / 16), 1);
          let current = 0;
          const update = () => {
            current += step;
            if (current < target) { stat.textContent = Math.floor(current); requestAnimationFrame(update); }
            else stat.textContent = target;
          };
          update();
        });
      });
    }, { threshold: 0.3 });
    statsObserver.observe(statsSection);
  }

  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -20px 0px' });
  $$('.reveal').forEach(el => {
    if (prefersReducedMotion) {
      el.classList.add('visible');
      el.style.transition = 'none';
    } else {
      revealObserver.observe(el);
    }
  });

  const activitesData = window.FTM_HOME_ACTIVITIES || [];
  const grid = $('#activitesGrid');
  if (grid && activitesData.length) {
    grid.innerHTML = activitesData.map(a => `
      <div class="activite-card reveal">
        <div class="activite-img"><img src="${a.img}" alt="${a.titre}" loading="lazy"></div>
        <div class="activite-body">
          <span class="categorie">${a.cat}</span>
          <h3>${a.titre}</h3>
          <p class="date"><i class="far fa-calendar-alt"></i> ${a.date}</p>
          <p>${a.desc}</p>
          <a href="${a.url || '#'}" class="btn btn-sm btn-outline">${a.readMoreText || 'Lire la suite'}</a>
        </div>
      </div>
    `).join('');
    $$('.activite-card.reveal').forEach(card => revealObserver.observe(card));
  }

  const carouselTrack = $('#carouselTrack');
  if (carouselTrack) {
    carouselTrack.addEventListener('mouseenter', () => carouselTrack.style.animationPlayState = 'paused');
    carouselTrack.addEventListener('mouseleave', () => carouselTrack.style.animationPlayState = 'running');
  }

  const btt = $('#backToTop');
  if (btt) {
    window.addEventListener('scroll', () => btt.classList.toggle('show', window.scrollY > 500), { passive: true });
    btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' }));
  }

  const floatingSidebar = $('#floatingSidebar');
  if (floatingSidebar) {
    window.addEventListener('scroll', () => floatingSidebar.classList.toggle('visible', window.scrollY > 300), { passive: true });
  }
})();