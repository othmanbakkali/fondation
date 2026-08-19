(function() {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    });
  }, { threshold: 0.14, rootMargin: '0px 0px -24px 0px' });

  $$('.reveal').forEach((el, index) => {
    if (prefersReducedMotion) {
      el.classList.add('visible');
      el.style.transition = 'none';
      return;
    }
    el.style.transitionDelay = `${Math.min(index * 0.04, 0.28)}s`;
    revealObserver.observe(el);
  });

  document.addEventListener('DOMContentLoaded', () => {
    const searchInput = $('#searchMembre');
    const searchClear = $('#searchClear');
    const filterSelect = $('#filterFonction');
    const tableRows = $$('#membresTable tbody tr');
    const noResults = $('#noResults');
    const memberCount = $('#memberCount');
    const tableWrapper = $('.table-wrapper');
    const totalMembers = tableRows.length;

    const updateCount = count => {
      if (memberCount) memberCount.innerHTML = `<span>${count}</span> membres affichés sur <span>${totalMembers}</span>`;
    };

    const filterMembers = () => {
      const searchTerm = (searchInput?.value || '').toLowerCase().trim();
      const filterValue = filterSelect?.value || 'all';
      let visibleCount = 0;
      if (searchClear) searchClear.style.display = searchTerm.length ? 'flex' : 'none';
      tableRows.forEach(row => {
        const name = (row.getAttribute('data-nom') || row.textContent || '').toLowerCase();
        const functionName = row.getAttribute('data-fonction') || 'all';
        const visible = name.includes(searchTerm) && (filterValue === 'all' || functionName === filterValue);
        row.style.display = visible ? '' : 'none';
        if (visible) visibleCount += 1;
      });
      if (noResults) noResults.style.display = visibleCount === 0 ? 'block' : 'none';
      if (tableWrapper) tableWrapper.style.display = visibleCount === 0 ? 'none' : 'block';
      updateCount(visibleCount);
    };

    searchInput?.addEventListener('input', filterMembers);
    searchClear?.addEventListener('click', () => {
      if (!searchInput) return;
      searchInput.value = '';
      filterMembers();
      searchInput.focus();
    });
    filterSelect?.addEventListener('change', filterMembers);
    updateCount(totalMembers);

    $$('.action-btn').forEach(btn => {
      btn.addEventListener('click', event => {
        event.preventDefault();
        const row = btn.closest('tr');
        const name = row?.querySelector('.col-nom strong')?.textContent || 'Membre';
        showToast(`${btn.getAttribute('title') || 'Action'} : ${name}`);
      });
    });

    $('#exportBtn')?.addEventListener('click', () => {
      const rows = [];
      tableRows.forEach(row => {
        if (row.style.display === 'none') return;
        const cells = row.querySelectorAll('td');
        rows.push({
          num: cells[0]?.textContent.trim() || '',
          nom: cells[2]?.querySelector('strong')?.textContent.trim() || '',
          fonc: cells[3]?.textContent.trim() || '',
          stat: cells[4]?.textContent.trim() || ''
        });
      });
      if (!rows.length) { showToast('Aucun membre à exporter.'); return; }
      let csv = 'N°,Nom complet,Fonction,Statut\n';
      rows.forEach(row => { csv += `"${row.num}","${row.nom}","${row.fonc}","${row.stat}"\n`; });
      const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'membres-bureau-tanger-metropole.csv';
      link.click();
      URL.revokeObjectURL(link.href);
      showToast(`${rows.length} membre(s) exporté(s) !`);
    });
  });

  function showToast(message) {
    $('.toast-notification')?.remove();
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.innerHTML = `<i class="fas fa-check-circle"></i><span>${message}</span>`;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add('show'), 80);
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }
})();
