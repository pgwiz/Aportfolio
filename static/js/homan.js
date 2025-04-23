// Select the canvas element
const canvas = document.getElementById('background-canvas');
const ctx = canvas.getContext('2d');

// Set canvas dimensions to cover the entire window
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Update canvas size on window resize
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

// Particle class for creating floating dots
class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.radius = Math.random() * 3 + 1; // Random size between 1px and 4px
        this.speedX = Math.random() * 2 - 1; // Horizontal speed
        this.speedY = Math.random() * 2 - 1; // Vertical speed
        this.color = Math.random() > 0.5 ? 'rgba(26, 115, 232, 0.8)' : 'rgba(52, 168, 83, 0.8)'; // Blue or Green
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;

        // Wrap around the screen edges
        if (this.x < 0) this.x = canvas.width;
        if (this.x > canvas.width) this.x = 0;
        if (this.y < 0) this.y = canvas.height;
        if (this.y > canvas.height) this.y = 0;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
    }
}

// Create an array of particles
const particles = Array.from({ length: 100 }, () => new Particle());

// Animation loop
function animate() {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Update and draw each particle
    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });

    // Loop the animation
    requestAnimationFrame(animate);
}

// Start the animation
animate();