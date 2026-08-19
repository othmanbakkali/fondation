(() => {
  const __ = window.gettext || ((message) => message);
  const root = document.documentElement;
  const body = document.body;
  const sidebar = document.getElementById('adminSidebar');
  const overlay = document.getElementById('sidebarOverlay');
  const themeToggle = document.getElementById('themeToggle');
  const modal = document.getElementById('confirmationModal');
  const mediaModal = document.getElementById('mediaModal');
  const modalMessage = document.getElementById('modalMessage');
  const toastBox = document.getElementById('toastContainer');

  const savedTheme = localStorage.getItem('dashboard-theme');
  if (savedTheme === 'dark') {
    root.dataset.theme = 'dark';
    if (themeToggle) themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
  }
  localStorage.setItem('dashboard-sidebar-collapsed', 'false');
  sidebar?.classList.remove('collapsed');

  function toast(message, type = 'success') {
    const item = document.createElement('div');
    item.className = `toast ${type}`;
    item.textContent = message;
    toastBox?.appendChild(item);
    setTimeout(() => item.remove(), 3200);
  }
  window.dashboardToast = toast;

  document.getElementById('hamburgerAdmin')?.addEventListener('click', () => {
    sidebar?.classList.add('open');
    overlay?.classList.add('active');
  });
  document.getElementById('sidebarClose')?.addEventListener('click', closeSidebar);
  overlay?.addEventListener('click', closeSidebar);
  function closeSidebar(){ sidebar?.classList.remove('open'); overlay?.classList.remove('active'); }

  document.getElementById('sidebarCollapse')?.addEventListener('click', () => {
    sidebar?.classList.toggle('collapsed');
    localStorage.setItem('dashboard-sidebar-collapsed', sidebar?.classList.contains('collapsed') ? 'true' : 'false');
  });

  document.querySelectorAll('.sidebar-toggle').forEach(btn => {
    btn.addEventListener('click', () => btn.closest('.sidebar-group')?.classList.toggle('open'));
  });

  themeToggle?.addEventListener('click', () => {
    const dark = root.dataset.theme !== 'dark';
    root.dataset.theme = dark ? 'dark' : '';
    localStorage.setItem('dashboard-theme', dark ? 'dark' : 'light');
    themeToggle.innerHTML = dark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
  });

  document.querySelectorAll('.notification-menu .icon-btn, .user-chip').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      btn.closest('.notification-menu, .admin-user-menu')?.classList.toggle('open');
    });
  });
  document.addEventListener('click', () => document.querySelectorAll('.notification-menu.open,.admin-user-menu.open').forEach(el => el.classList.remove('open')));
  async function refreshNotifications() {
    try {
      const response = await fetch('/dashboard/notification-counts/', {headers: {'X-Requested-With': 'XMLHttpRequest'}});
      if (!response.ok) return;
      const data = await response.json();
      document.querySelectorAll('[data-notification-count]').forEach(el => {
        el.textContent = data.total;
        el.style.display = data.total > 0 ? '' : 'none';
      });
      document.querySelectorAll('[data-notification-messages]').forEach(el => el.textContent = data.messages);
      document.querySelectorAll('[data-notification-volunteers]').forEach(el => el.textContent = data.volunteers);
      document.querySelectorAll('[data-notification-content]').forEach(el => el.textContent = data.content);
      document.querySelectorAll('[data-notification-formations-registrations]').forEach(el => el.textContent = data.formations_registrations);
      document.querySelectorAll('[data-notification-activities-registrations]').forEach(el => el.textContent = data.activities_registrations);
    } catch (error) {
      console.warn('Notifications refresh failed', error);
    }
  }
  document.querySelector('[data-refresh-notifications]')?.addEventListener('click', e => {
    e.preventDefault();
    refreshNotifications();
    toast(__('notifications_refreshed'));
  });
  refreshNotifications();
  setInterval(refreshNotifications, 20000);

  document.querySelector('[data-dismiss-alert]')?.addEventListener('click', e => e.currentTarget.closest('.inline-alert')?.remove());

  document.querySelectorAll('[data-toast]').forEach(el => el.addEventListener('click', e => {
    if (el.tagName === 'BUTTON') e.preventDefault();
    toast(el.dataset.toast ? __(el.dataset.toast) : __('Action simulée.'));
  }));

  document.querySelectorAll('[data-confirm-submit]').forEach(el => el.addEventListener('click', e => { if (!confirm(el.dataset.confirmSubmit || __('Confirmer cette action ?'))) e.preventDefault(); }));

  document.querySelectorAll('[data-confirm]').forEach(el => el.addEventListener('click', e => {
    e.preventDefault();
    if (modalMessage) modalMessage.textContent = el.dataset.confirm || __('Confirmer cette action ?');
    modal?.classList.add('open');
  }));
  document.querySelectorAll('[data-close-modal]').forEach(el => el.addEventListener('click', () => modal?.classList.remove('open')));
  document.querySelector('[data-confirm-action]')?.addEventListener('click', () => { modal?.classList.remove('open'); toast(__('Action confirmée visuellement.')); });
  document.querySelector('[data-open-media]')?.addEventListener('click', () => mediaModal?.classList.add('open'));
  document.querySelectorAll('[data-close-media]').forEach(el => el.addEventListener('click', () => mediaModal?.classList.remove('open')));

  document.querySelectorAll('[data-tabs]').forEach(tabbar => {
    tabbar.querySelectorAll('[data-tab-button]').forEach(btn => {
      btn.addEventListener('click', () => {
        const name = btn.dataset.tabButton;
        tabbar.querySelectorAll('button').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const scope = tabbar.closest('.page-editor-panel, .admin-main') || document;
        scope.querySelectorAll('[data-tab-panel]').forEach(panel => panel.classList.toggle('hidden', panel.dataset.tabPanel !== name));
      });
    });
  });

  document.querySelectorAll('[data-admin-table]').forEach(table => {
    const panel = table.closest('.panel, .span-2') || document;
    const search = panel.querySelector('[data-table-search]');
    const filter = panel.querySelector('[data-table-filter]');
    function applyFilter() {
      const q = (search?.value || '').toLowerCase();
      const f = (filter?.value || '').toLowerCase();
      table.querySelectorAll('tbody tr').forEach(row => {
        const txt = row.textContent.toLowerCase();
        row.style.display = txt.includes(q) && (!f || txt.includes(f)) ? '' : 'none';
      });
    }
    search?.addEventListener('input', applyFilter);
    filter?.addEventListener('change', applyFilter);
    panel.querySelector('[data-select-all]')?.addEventListener('change', e => {
      table.querySelectorAll('.row-check').forEach(cb => cb.checked = e.target.checked);
    });
    table.querySelectorAll('th[data-sort]').forEach((th, index) => {
      th.addEventListener('click', () => {
        const rows = [...table.tBodies[0].rows];
        rows.sort((a,b) => a.cells[index + 2].textContent.localeCompare(b.cells[index + 2].textContent));
        rows.forEach(r => table.tBodies[0].appendChild(r));
      });
    });
  });

  document.querySelectorAll('[data-bulk-action]').forEach(btn => btn.addEventListener('click', () => toast('Action groupee simulee sur les elements selectionnes.')));
  document.querySelectorAll('[data-detail]').forEach(btn => btn.addEventListener('click', () => toast(__('Ouverture du détail simulée.'), 'success')));

  document.querySelectorAll('[data-upload-zone]').forEach(zone => {
    const input = zone.querySelector('[data-file-input]');
    ['dragenter','dragover'].forEach(evt => zone.addEventListener(evt, e => { e.preventDefault(); zone.classList.add('dragover'); }));
    ['dragleave','drop'].forEach(evt => zone.addEventListener(evt, e => { e.preventDefault(); zone.classList.remove('dragover'); }));
    zone.addEventListener('drop', e => toast(`${e.dataTransfer.files.length} ${__('fichier(s) prêt(s) pour upload simulé.')}`));
    input?.addEventListener('change', () => toast(`${input.files.length} ${__('fichier(s) sélectionné(s).')}`));
  });

  document.querySelectorAll('[data-toggle-password]').forEach(btn => btn.addEventListener('click', () => {
    const input = btn.parentElement.querySelector('input');
    input.type = input.type === 'password' ? 'text' : 'password';
    btn.innerHTML = input.type === 'password' ? '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
  }));
const globalSearch = document.getElementById('globalSearch');
  const globalResults = document.getElementById('globalResults');
  const links = [
    [__('Tableau de bord'),'/dashboard/'],[__('Accueil'),'/dashboard/home-page/'],[__('Activités'),'/dashboard/activities/'],
    [__('Actualités'),'/dashboard/news/'],[__('Formations'),'/dashboard/formations/'],[__('Bénévolat'),'/dashboard/volunteers/'],
    [__('Messages'),'/dashboard/contacts/'],[__('Paramètres'),'/dashboard/settings/']
  ];
  globalSearch?.addEventListener('input', () => {
    const q = globalSearch.value.toLowerCase();
    if (!q) { globalResults.style.display = 'none'; return; }
    globalResults.innerHTML = links.filter(([label]) => label.toLowerCase().includes(q)).map(([label,url]) => `<a href="${url}"><i class="fas fa-search"></i> ${label}</a>`).join('') || `<a>${__('Aucun résultat')}</a>`;
    globalResults.style.display = 'block';
  });
})();

