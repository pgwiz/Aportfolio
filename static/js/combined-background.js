// combined-background.js
const canvas = document.getElementById('combined-background-canvas');
const ctx = canvas.getContext('2d');

// Resize canvas to fit the window
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// Particle Class
class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.radius = Math.random() * 2 + 1;
        this.speedX = Math.random() * 2 - 1;
        this.speedY = Math.random() * 2 - 1;
        this.color = color;
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;

        // Bounce off edges
        if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
        if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
    }
}

// Tech Fiber Class
class TechFiber {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.length = Math.random() * 50 + 20;
        this.angle = Math.random() * Math.PI * 2;
        this.speed = Math.random() * 0.05 + 0.01;
    }

    update() {
        this.angle += this.speed;
        this.x += Math.cos(this.angle) * 2;
        this.y += Math.sin(this.angle) * 2;

        // Reset position if out of bounds
        if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
        }
    }

    draw() {
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(
            this.x + Math.cos(this.angle) * this.length,
            this.y + Math.sin(this.angle) * this.length
        );
        ctx.strokeStyle = 'rgba(66, 135, 245, 0.3)';
        ctx.lineWidth = 1;
        ctx.stroke();
    }
}

// Create particles and fibers
const particles = [];
const fibers = [];
const particleCount = 50;
const fiberCount = 20;

for (let i = 0; i < particleCount; i++) {
    const x = Math.random() * canvas.width;
    const y = Math.random() * canvas.height;
    const color = body.classList.contains('dark-mode') ? '#ecf0f1' : '#2ecc71';
    particles.push(new Particle(x, y, color));
}

for (let i = 0; i < fiberCount; i++) {
    const x = Math.random() * canvas.width;
    const y = Math.random() * canvas.height;
    fibers.push(new TechFiber(x, y));
}

// Animation loop
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Update and draw particles
    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });

    // Update and draw fibers
    fibers.forEach(fiber => {
        fiber.update();
        fiber.draw();
    });

    requestAnimationFrame(animate);
}
animate();

// Update particle colors on theme change
const themeToggleb = document.getElementById('theme-toggle');
themeToggleb.addEventListener('click', () => {
    particles.forEach(particle => {
        particle.color = body.classList.contains('dark-mode') ? '#ecf0f1' : '#2ecc71';
    });
});