// tech-background.js
const canvas = document.getElementById('tech-background-canvas');
const ctx = canvas.getContext('2d');

// Resize canvas to fit the window
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// Node class for dots
class Node {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.radius = Math.random() * 2 + 1; // Random size for dots
        this.speedX = Math.random() * 2 - 1; // Random horizontal speed
        this.speedY = Math.random() * 2 - 1; // Random vertical speed
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
        ctx.fillStyle = 'rgba(66, 135, 245, 0.8)'; // Blue dots
        ctx.fill();
    }
}

// Line class for connections
class Connection {
    constructor(nodeA, nodeB) {
        this.nodeA = nodeA;
        this.nodeB = nodeB;
        this.opacity = 0;
    }

    update() {
        const dx = this.nodeB.x - this.nodeA.x;
        const dy = this.nodeB.y - this.nodeA.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        // Fade out connections over distance
        this.opacity = 1 - distance / 200;
        if (this.opacity < 0) this.opacity = 0;
    }

    draw() {
        if (this.opacity > 0) {
            ctx.strokeStyle = `rgba(34, 197, 94, ${this.opacity})`; // Green lines
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(this.nodeA.x, this.nodeA.y);
            ctx.lineTo(this.nodeB.x, this.nodeB.y);
            ctx.stroke();
        }
    }
}

// Create nodes and connections
const nodes = [];
const connections = [];
const nodeCount = 50;

for (let i = 0; i < nodeCount; i++) {
    const x = Math.random() * canvas.width;
    const y = Math.random() * canvas.height;
    nodes.push(new Node(x, y));
}

for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
        connections.push(new Connection(nodes[i], nodes[j]));
    }
}

// Animation loop
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Update and draw nodes
    nodes.forEach(node => {
        node.update();
        node.draw();
    });

    // Update and draw connections
    connections.forEach(connection => {
        connection.update();
        connection.draw();
    });

    requestAnimationFrame(animate);
}
animate();