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

// Fetch Portfolio Data
async function fetchPortfolioData(endpoint) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`);
        if (!response.ok) throw new Error(`Failed to load ${endpoint} data`);
        return await response.json();
    } catch (error) {
        showError(error.message || `Failed to load ${endpoint} data`);
        return [];
    }
}

// Load All Portfolio Data
async function loadPortfolioData() {
    try {
        // Fetch all portfolio data in parallel
        const [projects, skills, experiences, socialLinks, content, interactive] = await Promise.all([
            fetchPortfolioData('projects/'),
            fetchPortfolioData('skills/'),
            fetchPortfolioData('experiences/'),
            fetchPortfolioData('social-links/'),
            fetchPortfolioData('content/'),
            fetchPortfolioData('interactive/')
        ]);

        // Render each section
        renderProjects(projects);
        renderSkills(skills);
        renderExperiences(experiences);
        renderSocialLinks(socialLinks);
        renderContent(content);
        renderInteractive(interactive);

        // Show success message
        showSuccess('Portfolio data loaded successfully!');
    } catch (error) {
        showError('Failed to load portfolio data');
    }
}

// Render Functions for Each Section
function renderProjects(projects) {
    const projectGrid = document.getElementById('project-grid');
    projectGrid.innerHTML = ''; // Clear existing content

    if (projects.length === 0) {
        projectGrid.innerHTML = '<p>No projects added yet.</p>';
    } else {
        projects.forEach(project => {
            const card = document.createElement('div');
            card.className = 'project-card';
            card.innerHTML = `
                <h4>${project.title}</h4>
                <p><strong>Type:</strong> ${project.project_type_display}</p>
                <p><strong>Tech Stack:</strong> ${project.tech_stack.join(', ')}</p>
                <a href="${project.deploy_url}" target="_blank">View Project</a>
            `;
            projectGrid.appendChild(card);
        });
    }
}

function renderSkills(skills) {
    const skillGrid = document.getElementById('skill-grid');
    skillGrid.innerHTML = ''; // Clear existing content

    if (skills.length === 0) {
        skillGrid.innerHTML = '<p>No skills added yet.</p>';
    } else {
        skills.forEach(skill => {
            const card = document.createElement('div');
            card.className = 'skill-card';
            card.innerHTML = `
                <h4>${skill.name}</h4>
                <div class="skill-bar">
                    <div class="skill-progress" style="width: ${skill.proficiency}%"></div>
                </div>
                <p><strong>Type:</strong> ${skill.skill_type_display}</p>
                <p><strong>Category:</strong> ${skill.category}</p>
            `;
            skillGrid.appendChild(card);
        });
    }
}

function renderExperiences(experiences) {
    const experienceGrid = document.getElementById('experience-grid');
    experienceGrid.innerHTML = ''; // Clear existing content

    if (experiences.length === 0) {
        experienceGrid.innerHTML = '<p>No experiences added yet.</p>';
    } else {
        experiences.forEach(experience => {
            const card = document.createElement('div');
            card.className = 'experience-card';
            card.innerHTML = `
                <h4>${experience.title}</h4>
                <p><strong>Organization:</strong> ${experience.organization}</p>
                <p><strong>Type:</strong> ${experience.exp_type_display}</p>
                <p><strong>Dates:</strong> ${experience.start_date} to ${experience.end_date || 'Present'}</p>
                <p><strong>Description:</strong> ${experience.description}</p>
            `;
            experienceGrid.appendChild(card);
        });
    }
}

function renderSocialLinks(socialLinks) {
    const socialGrid = document.getElementById('social-grid');
    socialGrid.innerHTML = ''; // Clear existing content

    if (socialLinks.length === 0) {
        socialGrid.innerHTML = '<p>No social links added yet.</p>';
    } else {
        socialLinks.forEach(link => {
            const card = document.createElement('div');
            card.className = 'social-link-card';
            card.innerHTML = `
                <h4>${link.platform_display}</h4>
                <a href="${link.url}" target="_blank">${link.url}</a>
            `;
            socialGrid.appendChild(card);
        });
    }
}

function renderContent(content) {
    const contentGrid = document.getElementById('content-grid');
    contentGrid.innerHTML = ''; // Clear existing content

    if (content.length === 0) {
        contentGrid.innerHTML = '<p>No content added yet.</p>';
    } else {
        content.forEach(item => {
            const card = document.createElement('div');
            card.className = 'content-card';
            card.innerHTML = `
                <h4>${item.title}</h4>
                <p><strong>Type:</strong> ${item.content_type_display}</p>
                <p><strong>Published Date:</strong> ${item.published_date}</p>
                <p><strong>Description:</strong> ${item.description}</p>
                <a href="${item.url}" target="_blank">View Content</a>
            `;
            contentGrid.appendChild(card);
        });
    }
}

function renderInteractive(interactive) {
    const interactiveSection = document.getElementById('interactive-section');
    interactiveSection.innerHTML = ''; // Clear existing content

    if (!interactive) {
        interactiveSection.innerHTML = '<p>No interactive features configured yet.</p>';
    } else {
        interactiveSection.innerHTML = `
            <p><strong>Code Playground:</strong> ${interactive.code_playground_enabled ? 'Enabled' : 'Disabled'}</p>
            <p><strong>Live Streaming:</strong> ${interactive.live_streaming ? 'Enabled' : 'Disabled'}</p>
            <p><strong>Last Stream Start:</strong> ${interactive.last_stream_start || 'Not available'}</p>
            <p><strong>Active Challenges:</strong> ${interactive.active_challenges.join(', ') || 'None'}</p>
        `;
    }
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

// Helper Functions
function showError(message) {
    const errorBox = document.getElementById('error-box');
    errorBox.textContent = message;
    errorBox.style.display = 'block';
    setTimeout(() => errorBox.style.display = 'none', 3000);
}

function showSuccess(message) {
    const successBox = document.getElementById('success-box');
    successBox.textContent = message;
    successBox.style.display = 'block';
    setTimeout(() => successBox.style.display = 'none', 3000);
}

function showLiveUpdateIndicator() {
    const indicator = document.querySelector('.live-update-indicator');
    indicator.style.display = 'flex';
    setTimeout(() => indicator.style.display = 'none', 3000);
}