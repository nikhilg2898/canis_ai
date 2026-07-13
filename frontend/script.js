// ==========================================
// CANIS AI Frontend Script v2.0
// ==========================================

// Backend API Configuration
const API_URL = "https://canis-ai-frs2.onrender.com/chat";

// Elements
const chatContainer = document.getElementById('chat-container');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const typingIndicator = document.getElementById('typing-indicator');
const newChatBtn = document.getElementById('new-chat-btn');
const sendBtn = document.getElementById('send-btn');

// ==========================================
// Escape HTML
// ==========================================

function escapeHTML(text) {
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

// ==========================================
// Current Time
// ==========================================

function getTime() {
    return new Date().toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// ==========================================
// Add Message
// ==========================================

function addMessage(text, sender) {
    const safeText = escapeHTML(text).replace(/\n/g, '<br>');

    const message = document.createElement('div');
    message.className = sender === 'user' ? 'message user' : 'message ai';

    if (sender === 'user') {
        message.innerHTML = '<div class="bubble">' + safeText + '<div class="time">' + getTime() + '</div></div>';
    } else {
        message.innerHTML = '<div class="avatar">🐺</div><div class="bubble">' + safeText + '<div class="time">' + getTime() + '</div></div>';
    }

    chatContainer.appendChild(message);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// ==========================================
// Typing Indicator
// ==========================================

function showTyping() {
    typingIndicator.classList.remove('hidden');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function hideTyping() {
    typingIndicator.classList.add('hidden');
}

// ==========================================
// Auto Resize Textarea
// ==========================================

userInput.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 160) + 'px';
});

// ==========================================
// Send Message
// ==========================================

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    userInput.value = '';
    userInput.style.height = 'auto';

    sendBtn.disabled = true;
    userInput.disabled = true;

    showTyping();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error('Backend Error (' + response.status + ')');
        }

        const data = await response.json();
        const responseText = data.response;

        hideTyping();
        addMessage(responseText, 'ai');
    } catch (error) {
        hideTyping();
        addMessage(
            '⚠️ Connection Failed\n\nPlease check:\n• FastAPI server is running\n• Backend URL is correct\n• Internet connection\n• Groq API key is valid\n\nError: ' + error.message,
            'ai'
        );
        console.error(error);
    } finally {
        sendBtn.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

// ==========================================
// Form Submit
// ==========================================

chatForm.addEventListener('submit', function (e) {
    e.preventDefault();
    sendMessage();
});

// ==========================================
// Enter Key
// ==========================================

userInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// ==========================================
// New Chat
// ==========================================

newChatBtn.addEventListener('click', function () {
    chatContainer.innerHTML = '';
    welcomeMessage();
});

// ==========================================
// Welcome Message
// ==========================================

function welcomeMessage() {
    const hour = new Date().getHours();
    let greeting = 'Hello';

    if (hour < 12) greeting = 'Good Morning';
    else if (hour < 17) greeting = 'Good Afternoon';
    else greeting = 'Good Evening';

    addMessage(
        greeting + '! 👋\n\n🐺 Woof! I\'m Canis.\nConversational Assistant for Natural Intelligence & Support.\n\nYour loyal AI crony 🐕\n\nHow can I help you today?',
        'ai'
    );
}

// ==========================================
// Initialize
// ==========================================

welcomeMessage();
userInput.focus();

// ==========================================
// Lucide Icons
// ==========================================

lucide.createIcons();
