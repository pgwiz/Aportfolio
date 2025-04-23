// main.js
const API_BASE = '/api/portfolio/';
const WS_URL = `wss://${window.location.host}/ws/stats/`;

// WebSocket Connection
function initializeWebSocket() {
    const socket = new WebSocket(WS_URL);
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        updateLiveStats(data);
    };
}

// static/js/main.js
async function fetchProfileData() {
    try {
        const response = await fetch('/api/profile/update/', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        const data = await response.json();
        populateProfile(data);
    } catch (error) {
        console.error('Failed to load profile:', error);
    }
}

function populateProfile(data) {
    document.getElementById('profile-name').value = data.name;
    document.getElementById('profile-bio').value = data.bio;
    document.getElementById('profile-tagline').value = data.tagline;
}

document.getElementById('update-profile-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    try {
        const response = await fetch('/api/profile/update/', {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
            body: formData
        });

        if (response.ok) {
            alert('Profile updated successfully!');
        } else {
            alert('Failed to update profile.');
        }
    } catch (error) {
        console.error('Error updating profile:', error);
    }
});

// Fetch Portfolio Data
async function fetchPortfolioData(endpoint) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`);
        if (!response.ok) throw new Error('Failed to load data');
        return await response.json();
    } catch (error) {
        showError(`Failed to load ${endpoint} data`);
        return [];
    }
}

async function loadPortfolioData() {
    const [projects, skills] = await Promise.all([
        fetchPortfolioData('projects/'),
        fetchPortfolioData('skills/')
    ]);
    renderProjects(projects);
    renderSkills(skills);
}

// Contact Form Handler
document.getElementById('contact-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    try {
        const response = await fetch('/api/chat/contact/', {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(formData)),
            headers: { 'Content-Type': 'application/json' }
        });
        if (response.ok) {
            showSuccess('Message sent successfully!');
            e.target.reset();
        } else {
            throw new Error('Failed to send message');
        }
    } catch (error) {
        showError(error.message || 'An error occurred');
    }
});

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initializeWebSocket();
    loadPortfolioData();
});

function showError(message) {
    const errorBox = document.getElementById('error-box');
    errorBox.textContent = message;
    errorBox.style.display = 'block';
    setTimeout(() => errorBox.style.display = 'none', 3000);
}

function showLiveUpdateIndicator() {
    const indicator = document.querySelector('.live-update-indicator');
    indicator.style.display = 'flex';
    setTimeout(() => indicator.style.display = 'none', 3000);
}