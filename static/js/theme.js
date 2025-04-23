const themeToggle = document.getElementById('theme-switcher');
const body = document.body;

function setTheme(isDark) {
    body.classList.toggle('dark-theme', isDark);
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

themeToggle.addEventListener('click', () => {
    const isDark = !body.classList.contains('dark-theme');
    setTheme(isDark);
});

// Initialize theme
const savedTheme = localStorage.getItem('theme') || 'light';
setTheme(savedTheme === 'dark');

