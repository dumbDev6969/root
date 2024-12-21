// WebSocket connection
let ws = null;
let currentUserUUID = null;

// Initialize chat functionality
function initChat(userUUID) {
    currentUserUUID = userUUID;
    connectWebSocket();
}

// Connect to WebSocket server
function connectWebSocket() {
    if (!currentUserUUID) {
        console.error('User UUID not provided');
        return;
    }

    const wsUrl = `ws://localhost:8000/ws/chat?uuid=${currentUserUUID}`;
    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        console.log('WebSocket connection established');
        updateConnectionStatus('Connected');
    };

    ws.onclose = () => {
        console.log('WebSocket connection closed');
        updateConnectionStatus('Disconnected');
        // Attempt to reconnect after 5 seconds
        setTimeout(connectWebSocket, 5000);
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        updateConnectionStatus('Error connecting');
    };

    ws.onmessage = handleWebSocketMessage;
}

// Handle incoming WebSocket messages
function handleWebSocketMessage(event) {
    const data = JSON.parse(event.data);
    console.log('Received message:', data);

    switch (data.type) {
        case 'message':
            displayMessage(data.message);
            break;
        case 'response':
            handleMessageResponse(data);
            break;
        case 'status':
            updateUserStatus(data);
            break;
        case 'online_users':
            updateOnlineUsers(data.users);
            break;
        case 'history':
            loadChatHistory(data.messages);
            break;
        case 'error':
            handleError(data);
            break;
        default:
            console.warn('Unknown message type:', data.type);
    }
}

// Send a message
function sendMessage(receiverUUID, content, attachments = {}) {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        showNotification('Connection lost. Reconnecting...', 'error');
        return false;
    }

    const message = {
        type: 'message',
        sender_uuid: currentUserUUID,
        data: {
            receiver_uuid: receiverUUID,
            msg: content,
            date: new Date().toISOString(),
            attachments: attachments
        }
    };

    ws.send(JSON.stringify(message));
    return true;
}

// Handle message response from server
function handleMessageResponse(response) {
    const messageElement = document.querySelector(`[data-timestamp="${response.data.timestamp}"]`);
    if (!messageElement) return;

    const statusElement = messageElement.querySelector('.message-status');
    if (!statusElement) return;

    if (response.status === 'success') {
        if (response.data.delivery_status === 'pending') {
            // Message saved but recipient is offline
            statusElement.textContent = '✓ Saved';
            statusElement.title = 'Message will be delivered when recipient connects';
            statusElement.classList.add('pending');
        } else {
            // Message delivered successfully
            statusElement.textContent = '✓✓';
            statusElement.title = 'Delivered';
            statusElement.classList.add('delivered');
        }
    } else {
        // Handle other error cases
        statusElement.textContent = '!';
        statusElement.title = 'Error: ' + response.message;
        statusElement.classList.add('error');
    }
}

// Display a message in the chat window
function displayMessage(message) {
    const chatContainer = document.getElementById('chat-messages');
    if (!chatContainer) return;

    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(message.sender_uuid === currentUserUUID ? 'sent' : 'received');
    messageElement.dataset.timestamp = message.timestamp;

    const contentElement = document.createElement('div');
    contentElement.classList.add('message-content');
    contentElement.textContent = message.content;

    const statusElement = document.createElement('span');
    statusElement.classList.add('message-status');
    statusElement.textContent = '✓'; // Initial status
    
    messageElement.appendChild(contentElement);
    messageElement.appendChild(statusElement);
    
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Update user online status
function updateUserStatus(data) {
    const userElement = document.querySelector(`[data-user-uuid="${data.user_uuid}"]`);
    if (!userElement) return;

    const statusIndicator = userElement.querySelector('.status-indicator');
    if (statusIndicator) {
        statusIndicator.classList.toggle('online', data.status === 'online');
        statusIndicator.classList.toggle('offline', data.status === 'offline');
    }
}

// Update list of online users
function updateOnlineUsers(users) {
    const usersList = document.getElementById('online-users');
    if (!usersList) return;

    usersList.innerHTML = '';
    users.forEach(user => {
        const userElement = document.createElement('div');
        userElement.classList.add('user');
        userElement.dataset.userUuid = user.user_uuid;

        const statusIndicator = document.createElement('span');
        statusIndicator.classList.add('status-indicator');
        statusIndicator.classList.add(user.status);

        const userName = document.createElement('span');
        userName.textContent = user.user_uuid;

        userElement.appendChild(statusIndicator);
        userElement.appendChild(userName);
        usersList.appendChild(userElement);
    });
}

// Load chat history
function loadChatHistory(messages) {
    const chatContainer = document.getElementById('chat-messages');
    if (!chatContainer) return;

    chatContainer.innerHTML = '';
    messages.forEach(message => {
        displayMessage(message);
    });
}

// Update connection status
function updateConnectionStatus(status) {
    const statusElement = document.getElementById('connection-status');
    if (statusElement) {
        statusElement.textContent = status;
        statusElement.className = `status-${status.toLowerCase()}`;
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notificationElement = document.getElementById('notification');
    if (!notificationElement) return;

    notificationElement.textContent = message;
    notificationElement.className = `notification ${type}`;
    notificationElement.style.display = 'block';

    setTimeout(() => {
        notificationElement.style.display = 'none';
    }, 3000);
}

// Handle errors
function handleError(error) {
    console.error('Error:', error);
    showNotification(error.message, 'error');
}

// Export functions for use in other modules
window.ChatModule = {
    init: initChat,
    sendMessage: sendMessage,
    disconnect: () => {
        if (ws) {
            ws.close();
        }
    }
};
