/**
 * chat.js
 * Handles real-time chat functionalities using WebSockets.
 */

let socket; // Declare socket in a broader scope for better management

document.addEventListener('DOMContentLoaded', () => {
    if (!sessionData) {
        console.error('Session data is not available.');
        alert('Error: Session data not found. Please log in again.');
        return;
    }

    const userUuid = getUserUUIDFromSession();
    if (!userUuid) {
        console.error('User UUID not found in session data.');
        alert('Error: User UUID not found. Please log in again.');
        return;
    }

    const webSocketURL = getWebSocketURL(); // Retrieve the WebSocket URL from PHP

    connectWebSocket(userUuid, webSocketURL);

    // Event listeners
    document.getElementById('logout-button').addEventListener('click', logout);
});

/**
 * Establishes a WebSocket connection.
 * @param {string} userUuid - The UUID of the current user.
 * @param {string} url - The WebSocket URL.
 */
function connectWebSocket(userUuid, url) {
    socket = new WebSocket(`${url}?uuid=${userUuid}`);

    const connectionStatus = document.getElementById('connectionStatus');
    const contactList = document.getElementById('contactList');
    const conversationBody = document.getElementById('conversationBody');
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');

    socket.onopen = () => {
        console.log('WebSocket connection established.');
        connectionStatus.innerHTML = '<span class="text-success"><i class="fas fa-circle me-1"></i>Online</span>';
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        switch (data.type) {
            case 'status':
                updateOnlineStatus(data.user_uuid, data.status);
                break;
            case 'message':
                displayMessage(data.message);
                break;
            case 'history':
                loadChatHistory(data.messages);
                break;
            case 'search_results':
                displaySearchResults(data.results);
                break;
            case 'error':
                console.error('Error from server:', data.message);
                alert(`Error: ${data.message}`);
                break;
            default:
                console.warn('Unknown message type:', data.type);
        }
    };

    socket.onclose = (event) => {
        console.log('WebSocket connection closed:', event);
        connectionStatus.innerHTML = '<span class="text-danger"><i class="fas fa-circle me-1"></i>Offline</span>';
    };

    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    // Handle sending messages via Enter key
    const messageInput = document.querySelector('.input-group input');
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const content = messageInput.value.trim();
            if (content) {
                const receiverUuid = getSelectedReceiverUUID(); // Implement a method to get the selected receiver's UUID
                if (receiverUuid) {
                    sendMessage(receiverUuid, content);
                    messageInput.value = '';
                } else {
                    alert('Please select a user to send the message.');
                }
            }
        }
    });

    // Handle sending messages via send button
    document.querySelector('.input-group button').addEventListener('click', () => {
        const content = messageInput.value.trim();
        if (content) {
            const receiverUuid = getSelectedReceiverUUID(); // Implement a method to get the selected receiver's UUID
            if (receiverUuid) {
                sendMessage(receiverUuid, content);
                messageInput.value = '';
            } else {
                alert('Please select a user to send the message.');
            }
        }
    });

    // Handle searching users
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.trim();
        if (query.length > 0) {
            const searchMessage = {
                type: 'search',
                query: query
            };
            socket.send(JSON.stringify(searchMessage));
        } else {
            searchResults.innerHTML = '';
        }
    });
}

/**
 * Retrieves the WebSocket URL from a PHP-generated global variable.
 * This function must be defined in your PHP navigation includes.
 * @returns {string} - The WebSocket URL.
 */
function getWebSocketURL() {
    // Assuming the WebSocket URL is passed from PHP as a global variable
    // You can set it in your PHP script and retrieve it here
    return window.webSocketURL || 'ws://localhost:8000/ws/chat'; // Fallback URL
}

/**
 * Retrieves the user's UUID from the sessionData.
 * @returns {string|null} - The user's UUID or null if not found.
 */
function getUserUUIDFromSession() {
    return sessionData?.userData?.user_uuid || sessionData?.employerData?.employer_uuid || null;
}

/**
 * Sends a message to the specified receiver via WebSocket.
 * @param {string} receiverUuid - The UUID of the message receiver.
 * @param {string} content - The message content.
 */
function sendMessage(receiverUuid, content) {
    const timestamp = new Date().toISOString();
    const message = {
        type: 'message',
        receiver_uuid: receiverUuid,
        content: content,
        timestamp: timestamp
    };
    socket.send(JSON.stringify(message));
    // Optionally, display the sent message in the UI
    displayMessage({ ...message, sender_uuid: getUserUUIDFromSession() });
}

/**
 * Logs out the user by clearing session data and redirecting to the login page.
 */
function logout() {
    // Implement your logout logic here, e.g., making an AJAX call to the server to destroy the session
    // For simplicity, we'll just redirect to the login page
    window.location.href = '/logout.php'; // Ensure this route handles session destruction
}

/**
 * Updates the online status of a user in the contact list.
 * @param {string} userUuid - The UUID of the user.
 * @param {string} status - The status ('online' or 'offline').
 */
function updateOnlineStatus(userUuid, status) {
    const userElement = document.getElementById(`user-${userUuid}`);
    if (userElement) {
        const statusElem = userElement.querySelector('.status');
        if (statusElem) {
            statusElem.innerText = status === 'online' ? 'Online' : 'Offline';
            statusElem.className = status === 'online' ? 'text-success status' : 'text-danger status';
        }
    }
}

/**
 * Displays a message in the conversation body.
 * @param {Object} message - The message object containing sender_uuid, content, and timestamp.
 */
function displayMessage(message) {
    const isSentByUser = message.sender_uuid === getUserUUIDFromSession();
    const messageClass = isSentByUser ? 'sent-message' : 'received-message';
    const alignmentClass = isSentByUser ? 'text-end' : 'text-start';
    const messageHtml = `
        <div class="${messageClass} ${alignmentClass}">
            <span>${escapeHTML(message.content)}</span>
            <br/>
            <small>${new Date(message.timestamp).toLocaleTimeString()}</small>
        </div>
    `;
    const conversationBody = document.getElementById('conversationBody');
    conversationBody.innerHTML += messageHtml;
    conversationBody.scrollTop = conversationBody.scrollHeight;
}

/**
 * Loads chat history into the conversation body.
 * @param {Array} messages - An array of message objects.
 */
function loadChatHistory(messages) {
    const conversationBody = document.getElementById('conversationBody');
    conversationBody.innerHTML = ''; // Clear existing messages
    messages.forEach(message => {
        displayMessage(message);
    });
}

/**
 * Displays search results in the dropdown.
 * @param {Array} results - An array of search result objects.
 */
function displaySearchResults(results) {
    const searchResults = document.getElementById('searchResults');
    searchResults.innerHTML = ''; // Clear existing results
    results.forEach(result => {
        const listItem = document.createElement('li');
        listItem.classList.add('dropdown-item', 'cursor-pointer');
        listItem.innerText = result.content; // Adjust based on your data structure
        listItem.addEventListener('click', () => {
            selectUser(result.user_uuid); // Implement user selection logic
        });
        searchResults.appendChild(listItem);
    });
}

/**
 * Escapes HTML to prevent XSS attacks.
 * @param {string} unsafe - The unsafe string containing HTML.
 * @returns {string} - The escaped string.
 */
function escapeHTML(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}

/**
 * Selects a user to start a conversation.
 * @param {string} userUuid - The UUID of the selected user.
 */
function selectUser(userUuid) {
    // Implement your logic to select a user, load conversation, etc.
    console.log(`Selected user UUID: ${userUuid}`);
    // Load the conversation with the selected user
    // This might involve setting a current receiver UUID and loading chat history
}