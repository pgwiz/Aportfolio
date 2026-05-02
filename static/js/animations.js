// animations.js — reveals elements with .animate-on-scroll as they enter the viewport,
// and animates skill bar fills to their target percentage.
(function () {
    var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function fillSkillBars(scope) {
        var bars = (scope || document).querySelectorAll('[data-skill-fill]');
        bars.forEach(function (bar) {
            var target = parseFloat(bar.getAttribute('data-target')) || 0;
            target = Math.max(0, Math.min(100, target));
            bar.style.width = target + '%';
        });
    }

    function reveal(el) {
        el.classList.add('is-visible');
        fillSkillBars(el);
    }

    var revealTargets = document.querySelectorAll('.animate-on-scroll');

    if (prefersReducedMotion || !('IntersectionObserver' in window)) {
        revealTargets.forEach(reveal);
        return;
    }

    var observer = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                reveal(entry.target);
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -10% 0px' });

    revealTargets.forEach(function (el) { observer.observe(el); });
})();
