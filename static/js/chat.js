/*class ChatInterface {
    constructor() {
        this.ws = null;
        this.initializeWebSocket();
        this.setupEventListeners();
    }

    initializeWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        this.ws = new WebSocket(`${protocol}//${window.location.host}/ws/chat/`);
        
        this.ws.onmessage = (e) => {
            const data = JSON.parse(e.data);
            this.handleMessage(data);
        };

        this.ws.onclose = () => {
            setTimeout(() => this.initializeWebSocket(), 5000);
        };
    }

    handleMessage(data) {
        switch(data.type) {
            case 'chat.message':
                this.appendMessage(data);
                break;
            case 'typing.indicator':
                this.showTypingIndicator(data);
                break;
        }
    }

    appendMessage(data) {
        const messagesDiv = document.getElementById('messages');
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.innerHTML = `
            <div class="message-header">
                <span class="sender">${data.sender}</span>
                <span class="timestamp">${data.timestamp}</span>
            </div>
            <div class="message-content">${this.sanitize(data.message)}</div>
        `;
        messagesDiv.appendChild(messageElement);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    sanitize(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}*/
// chat.js
const chatButton = document.getElementById('chat-button');
const chatWindow = document.querySelector('.chat-window');
const closeChat = document.querySelector('.close-chat');
const messageInput = document.querySelector('.chat-input input');
const sendButton = document.querySelector('.send-message');
const chatMessages = document.querySelector('.chat-messages');
const notificationBadge = document.querySelector('.notification-badge');

// Chat WebSocket Connection
const chatSocket = new WebSocket(`wss://${window.location.host}/ws/chat/`);

// Toggle Chat Window
chatButton.addEventListener('click', () => {
    chatWindow.classList.toggle('active');
    notificationBadge.style.display = 'none';
});

closeChat.addEventListener('click', () => {
    chatWindow.classList.remove('active');
});

// Handle incoming messages
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    appendMessage(data);
    if (!chatWindow.classList.contains('active')) {
        updateNotificationBadge();
    }
};

function appendMessage(data) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${data.sender === 'user' ? 'sent' : 'received'}`;
    messageDiv.innerHTML = `
        <div class="message-content">${data.message}</div>
        <div class="message-time">${new Date().toLocaleTimeString()}</div>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function updateNotificationBadge() {
    const currentCount = parseInt(notificationBadge.textContent) || 0;
    notificationBadge.textContent = currentCount + 1;
    notificationBadge.style.display = 'flex';
}

// Send Message
sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
        chatSocket.send(JSON.stringify({
            message: message,
            receiver_id: 'ADMIN_ID'  // Replace with actual admin ID
        }));
        appendMessage({ message, sender: 'user' });
        messageInput.value = '';
    }
}

function toggleChatLoading(isLoading) {
    const loader = document.querySelector('.chat-loader');
    loader.style.display = isLoading ? 'block' : 'none';
}

function initializeChatWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws/chat/`);

    ws.onopen = () => console.log('Chat WebSocket connected');
    ws.onclose = () => {
        console.log('Chat WebSocket disconnected. Reconnecting...');
        setTimeout(initializeChatWebSocket, 5000);
    };

    ws.onmessage = (e) => {
        const data = JSON.parse(e.data);
        appendMessage(data);
        if (!chatWindow.classList.contains('active')) {
            updateNotificationBadge();
        }
    };
}

function sanitize(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}