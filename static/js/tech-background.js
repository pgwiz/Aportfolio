// tech-background.js — subtle node/connection background animation.
// Adapts to the current theme via the [data-theme] attribute and respects
// reduced-motion preferences. Pauses when the page is not visible.
(function () {
    var canvas = document.getElementById('tech-background-canvas');
    if (!canvas || !canvas.getContext) return;

    var ctx = canvas.getContext('2d');
    var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var dpr = Math.max(1, Math.min(2, window.devicePixelRatio || 1));
    var width = 0;
    var height = 0;
    var rafId = null;
    var running = true;

    function resize() {
        width = canvas.clientWidth || window.innerWidth;
        height = canvas.clientHeight || window.innerHeight;
        canvas.width = Math.round(width * dpr);
        canvas.height = Math.round(height * dpr);
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function colors() {
        var dark = document.documentElement.getAttribute('data-theme') === 'dark';
        return dark
            ? { node: 'rgba(165, 180, 252, 0.85)', line: 'rgba(99, 102, 241, ' }
            : { node: 'rgba(79, 70, 229, 0.55)',  line: 'rgba(99, 102, 241, ' };
    }

    function makeNodes(count) {
        var arr = [];
        for (var i = 0; i < count; i++) {
            arr.push({
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * 0.3,
                vy: (Math.random() - 0.5) * 0.3,
                r: Math.random() * 1.5 + 0.6
            });
        }
        return arr;
    }

    var NODE_COUNT = window.innerWidth < 700 ? 28 : 55;
    var LINK_DISTANCE = 140;
    var nodes = [];

    function frame() {
        if (!running) return;
        var c = colors();
        ctx.clearRect(0, 0, width, height);

        for (var i = 0; i < nodes.length; i++) {
            var n = nodes[i];
            n.x += n.vx;
            n.y += n.vy;
            if (n.x < 0 || n.x > width)  n.vx *= -1;
            if (n.y < 0 || n.y > height) n.vy *= -1;

            ctx.beginPath();
            ctx.fillStyle = c.node;
            ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
            ctx.fill();

            for (var j = i + 1; j < nodes.length; j++) {
                var m = nodes[j];
                var dx = n.x - m.x;
                var dy = n.y - m.y;
                var dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < LINK_DISTANCE) {
                    var alpha = (1 - dist / LINK_DISTANCE) * 0.5;
                    ctx.strokeStyle = c.line + alpha + ')';
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(n.x, n.y);
                    ctx.lineTo(m.x, m.y);
                    ctx.stroke();
                }
            }
        }
        rafId = requestAnimationFrame(frame);
    }

    function start() {
        if (rafId) return;
        running = true;
        rafId = requestAnimationFrame(frame);
    }

    function stop() {
        running = false;
        if (rafId) {
            cancelAnimationFrame(rafId);
            rafId = null;
        }
    }

    resize();
    nodes = makeNodes(NODE_COUNT);

    if (prefersReducedMotion) {
        // Render a single static frame, then stop.
        frame();
        stop();
    } else {
        start();
    }

    window.addEventListener('resize', function () {
        resize();
        nodes = makeNodes(NODE_COUNT);
    });

    document.addEventListener('visibilitychange', function () {
        if (document.hidden) stop(); else if (!prefersReducedMotion) start();
    });
})();
