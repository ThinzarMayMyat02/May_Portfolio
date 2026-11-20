(function initializeNavigation() {
  const navigation = document.querySelector('.app-tabs');
  const menuButton = document.querySelector('.menu-toggle');
  const mobileViewport = window.matchMedia('(max-width: 760px)');

  function setMenuOpen(open) {
    const expanded = mobileViewport.matches && open;

    navigation.hidden = mobileViewport.matches && !expanded;
    menuButton.setAttribute('aria-expanded', String(expanded));
    menuButton.textContent = expanded ? '✕ Close' : '☰ Menu';
  }

  menuButton.hidden = false;
  setMenuOpen(false);

  menuButton.addEventListener('click', function toggleMenu() {
    const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
    setMenuOpen(!isOpen);
  });

  mobileViewport.addEventListener('change', function resetMenu() {
    setMenuOpen(false);
  });

  document.addEventListener('keydown', function closeOnEscape(event) {
    const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
    if (event.key === 'Escape' && isOpen) {
      setMenuOpen(false);
      menuButton.focus();
    }
  });

  document.addEventListener('click', function closeOutsideMenu(event) {
    if (mobileViewport.matches && !event.target.closest('.site-header')) {
      setMenuOpen(false);
    }
  });
})();
