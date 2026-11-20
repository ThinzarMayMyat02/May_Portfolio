(function initializeTheme() {
  const storageKey = 'portfolio-theme';
  let currentTheme = 'dark';

  try {
    const savedTheme = localStorage.getItem(storageKey);
    if (savedTheme === 'light') {
      currentTheme = savedTheme;
    }
  } catch (error) {
    // The default theme also works when browser storage is unavailable.
  }

  // Apply the saved theme before the stylesheet loads to avoid a theme flash.
  document.documentElement.dataset.theme = currentTheme;

  document.addEventListener('DOMContentLoaded', function bindThemeToggle() {
    const button = document.querySelector('.theme-toggle');

    function updateButton() {
      const isLight = currentTheme === 'light';
      const nextTheme = isLight ? 'dark' : 'light';
      const icon = isLight ? '☾' : '☀';

      button.setAttribute('aria-pressed', String(isLight));
      button.setAttribute('aria-label', 'Switch to ' + nextTheme + ' mode');
      button.innerHTML = '<span aria-hidden="true">' + icon + '</span> ' +
        (isLight ? 'Dark mode' : 'Light mode');
    }

    button.addEventListener('click', function switchTheme() {
      currentTheme = currentTheme === 'light' ? 'dark' : 'light';
      document.documentElement.dataset.theme = currentTheme;

      try {
        localStorage.setItem(storageKey, currentTheme);
      } catch (error) {
        // Theme switching still works for the current page.
      }

      updateButton();
    });

    updateButton();
  });
})();
