// theme.js — toggles between light and dark themes via [data-theme] on <html>.
// Persists the choice in localStorage. The pre-paint script in base.html applies
// the saved theme before this file loads to avoid a flash of the wrong theme.
(function () {
    var STORAGE_KEY = 'aportfolio-theme';
    var root = document.documentElement;

    function setTheme(theme) {
        root.setAttribute('data-theme', theme);
        try {
            localStorage.setItem(STORAGE_KEY, theme);
        } catch (e) { /* localStorage might be unavailable; ignore */ }
        root.dispatchEvent(new CustomEvent('themechange', { detail: { theme: theme } }));
    }

    function currentTheme() {
        return root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    }

    var btn = document.getElementById('theme-toggle');
    if (btn) {
        btn.addEventListener('click', function () {
            setTheme(currentTheme() === 'dark' ? 'light' : 'dark');
        });
    }

    // Track OS-level changes only when the user hasn't expressed a preference.
    var media = window.matchMedia('(prefers-color-scheme: dark)');
    var handleSystemChange = function (event) {
        var stored = null;
        try { stored = localStorage.getItem(STORAGE_KEY); } catch (e) { /* ignore */ }
        if (!stored) {
            setTheme(event.matches ? 'dark' : 'light');
        }
    };
    if (typeof media.addEventListener === 'function') {
        media.addEventListener('change', handleSystemChange);
    } else if (typeof media.addListener === 'function') {
        media.addListener(handleSystemChange);
    }
})();
