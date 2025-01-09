<?php
$current_page = basename(htmlspecialchars($_SERVER['PHP_SELF'])); //! Get the current page
//echo $current_page;
?>
<style>
        .navbar {
            position: sticky;
            top: 0;
            z-index: 99;
        }
        .offcanvas {
            z-index: 999;
        }
        .chat-message {
            max-width: 80%;
            word-wrap: break-word;
            margin-bottom: 0.5rem;
        }
        .chat-message.sent {
            background-color: #6c757d;
            border-radius: 1rem 1rem 0.3rem 1rem;
        }
        .chat-message.received {
            background-color: #007bff;
            border-radius: 1rem 1rem 1rem 0.3rem;
        }
        .chat-timestamp {
            font-size: 0.75em;
            opacity: 0.8;
            margin-top: 0.25rem;
        }
        .chat-status {
            font-size: 0.75em;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }
        .chat-status i {
            font-size: 0.875em;
        }
        #conversationBody {
            padding: 1rem;
            background-color: #f8f9fa;
            border-radius: 0.5rem;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }
        .message-input-container {
            background-color: white;
            border-top: 1px solid #dee2e6;
            padding: 1rem;
            margin: -1rem;
            margin-top: 0;
            box-shadow: 0 -4px 12px rgba(0,0,0,0.05);
        }
        .offcanvas-header {
            background-color: white;
            border-bottom: 1px solid #dee2e6;
            box-shadow: 0 2px 12px rgba(0,0,0,0.05);
            padding: 1rem;
            z-index: 1;
        }
        .chat-message {
            max-width: 80%;
            word-wrap: break-word;
            margin-bottom: 0.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
            animation: messageAppear 0.3s ease-out;
        }
        @keyframes messageAppear {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .chat-message:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .chat-message.sent {
            background-color: #6c757d;
            border-radius: 1.2rem 1.2rem 0.3rem 1.2rem;
            margin-left: auto;
        }
        .chat-message.received {
            background-color: #007bff;
            border-radius: 1.2rem 1.2rem 1.2rem 0.3rem;
            margin-right: auto;
        }
        .chat-status {
            font-size: 0.75em;
            display: flex;
            align-items: center;
            gap: 0.25rem;
            transition: color 0.2s ease;
        }
        .chat-status i {
            font-size: 0.875em;
            transition: transform 0.2s ease;
        }
        .chat-status:hover i {
            transform: scale(1.1);
        }
        .websocket-error {
            position: fixed;
            top: 1rem;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
            padding: 0.75rem 1.25rem;
            border-radius: 0.25rem;
            text-align: center;
            max-width: 90%;
            animation: fadeIn 0.3s ease-in;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .websocket-error.error {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .websocket-error.success {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .websocket-error.warning {
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            color: #856404;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translate(-50%, -20px); }
            to { opacity: 1; transform: translate(-50%, 0); }
        }
        @keyframes fadeOut {
            from { opacity: 1; transform: translate(-50%, 0); }
            to { opacity: 0; transform: translate(-50%, -20px); }
        }
        .websocket-error.fade-out {
            animation: fadeOut 0.3s ease-out forwards;
        }
</style>
<script>
    <?php
    if (session_status() === PHP_SESSION_NONE) {
        session_start();
    }
    // Ensure sessionData is always defined with at least empty values
    $defaultSession = [
        'user_uuid' => null,
        'employerData' => ['employer_uuid' => null]
    ];
    $sessionData = array_merge($defaultSession, $_SESSION);
    echo "var sessionData = " . json_encode($sessionData) . ";";
    ?>
    <?php
    $sender_uuid = $_SESSION['userData']['user_uuid'] ?? 'unknown_sender';
    ?>
    let socket = null;

    function showConnectionError(message, type = 'error', autoHide = false) {
        // Remove any existing error banner
        const existingError = document.getElementById('websocket-error');
        if (existingError) {
            existingError.remove();
        }

        // Create and show new error banner
        const errorDiv = document.createElement('div');
        errorDiv.id = 'websocket-error';
        errorDiv.className = `websocket-error ${type}`;

        // Add icon based on type
        const icon = document.createElement('i');
        switch (type) {
            case 'success':
                icon.className = 'fas fa-check-circle';
                break;
            case 'warning':
                icon.className = 'fas fa-exclamation-triangle';
                break;
            default:
                icon.className = 'fas fa-times-circle';
        }
        
        // Add close button
        const closeButton = document.createElement('button');
        closeButton.innerHTML = '×';
        closeButton.style.cssText = 'background: none; border: none; margin-left: auto; font-size: 1.5em; cursor: pointer; padding: 0 0.5rem;';
        closeButton.onclick = () => {
            errorDiv.classList.add('fade-out');
            setTimeout(() => errorDiv.remove(), 300);
        };
        
        const messageSpan = document.createElement('span');
        messageSpan.textContent = message;
        
        errorDiv.appendChild(icon);
        errorDiv.appendChild(messageSpan);
        errorDiv.appendChild(closeButton);
        document.body.appendChild(errorDiv);

        // Auto-hide based on message type or parameter
        if (autoHide || type === 'success' || message.includes('reconnect')) {
            setTimeout(() => {
                if (document.getElementById('websocket-error')) {
                    errorDiv.classList.add('fade-out');
                    setTimeout(() => errorDiv.remove(), 300);
                }
            }, 5000);
        }
    }

    // Add Font Awesome for icons
    const fontAwesome = document.createElement('link');
    fontAwesome.rel = 'stylesheet';
    fontAwesome.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css';
    document.head.appendChild(fontAwesome);

    function connectWebSocket() {
        const userUuid = '<?php echo $sender_uuid; ?>';
        if (socket && socket.readyState === WebSocket.OPEN) {
            console.log('WebSocket is already connected. Skipping reconnection.');
            return;
        }
        try {
            socket = new WebSocket(`wss://root-4ytd.onrender.com/ws/chat?uuid=${userUuid}`);
            
            socket.onopen = () => {
                console.log('WebSocket connected');
                // Clear any error messages when connection is successful
                const errorBanner = document.getElementById('websocket-error');
                if (errorBanner) {
                    errorBanner.remove();
                }
            };

            socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                console.log('Received WebSocket message:', data);

                if (data.type === 'message') {
                    // Handle received message
                    const message = data.message;
                    const conversationBody = document.getElementById('conversationBody');
                    if (conversationBody && message.sender_uuid !== userUuid) {
                        const receivedMessage = `
                            <div class="d-flex justify-content-start">
                                <div class="chat-message received p-3 text-white">
                                    <div>${message.content}</div>
                                    <div class="chat-timestamp text-white-50">
                                        ${new Date(message.timestamp).toLocaleTimeString()}
                                    </div>
                                </div>
                            </div>
                        `;
                        conversationBody.innerHTML += receivedMessage;
                        // Auto-scroll to latest message
                        conversationBody.scrollTop = conversationBody.scrollHeight;
                    }
                } else if (data.type === 'history') {
                    // Handle chat history
                    console.log('Received chat history:', data.messages);
                    const conversationBody = document.getElementById('conversationBody');
                    if (!conversationBody) {
                        console.error('Conversation body element not found');
                        return;
                    }

                    // Clear the loading indicator
                    conversationBody.innerHTML = '';

                    // Check if we have messages
                    if (!Array.isArray(data.messages) || data.messages.length === 0) {
                        conversationBody.innerHTML = `
                            <div class="text-center p-3 text-muted">
                                <div>No messages yet</div>
                                <small>Start a conversation!</small>
                            </div>
                        `;
                        return;
                    }

                    // Sort messages by timestamp
                    const sortedMessages = [...data.messages].sort((a, b) => 
                        new Date(a.timestamp) - new Date(b.timestamp)
                    );

                    // Render each message
                    sortedMessages.forEach(message => {
                        const isSender = message.sender_uuid === userUuid;
                        const messageHtml = `
                            <div class="d-flex justify-content-${isSender ? 'end' : 'start'}">
                                <div class="chat-message ${isSender ? 'sent' : 'received'} p-3 text-white">
                                    <div>${message.content}</div>
                                    <div class="d-flex align-items-center justify-content-between mt-1">
                                        <div class="chat-timestamp text-white-50">
                                            ${new Date(message.timestamp).toLocaleTimeString()}
                                        </div>
                                        ${isSender ? `
                                            <div class="chat-status text-success">
                                                <i class="fas fa-check"></i>
                                                <span>Saved</span>
                                            </div>
                                        ` : ''}
                                    </div>
                                </div>
                            </div>
                        `;
                        conversationBody.insertAdjacentHTML('beforeend', messageHtml);
                    });

                    // Scroll to the latest message
                    conversationBody.scrollTop = conversationBody.scrollHeight;
                } else if (data.type === 'response') {
                    // Handle server response
                    if (data.status === 'success') {
                        console.log('Message saved:', data.message);
                        if (data.data?.delivery_status === 'pending') {
                            showConnectionError('Message saved and will be delivered when recipient connects', 'success', true);
                        } else {
                            showConnectionError('Message delivered successfully', 'success', true);
                        }
                    } else {
                        console.error('Error with message:', data.message);
                        showConnectionError(data.message || 'Error processing message', 'error');
                    }
                } else if (data.type === 'error') {
                    // Handle error messages
                    console.error('Server error:', data.message, data.details);
                    showConnectionError(data.message, 'error');
                } else if (data.type === 'status') {
                    // Handle status updates
                    if (data.status === 'online') {
                        showConnectionError(`${data.user_uuid} is now online`, 'success', true);
                    } else if (data.status === 'offline') {
                        showConnectionError(`${data.user_uuid} is now offline`, 'warning', true);
                    }
                }
            };

            socket.onclose = () => {
                console.log('WebSocket disconnected');
                showConnectionError('Chat connection lost. Attempting to reconnect...', 'warning', true);
                setTimeout(connectWebSocket, 3000);
            };

            socket.onerror = (error) => {
                console.error('WebSocket error:', error);
                showConnectionError('Unable to connect to chat server. Please check if the server is running.', 'error');
            };
        } catch (error) {
            console.error('Failed to create WebSocket connection:', error);
            showConnectionError('Failed to establish chat connection. Please try again later.', 'error');
        }
    }

    // Connect WebSocket when the page loads
    connectWebSocket();

    function logMessage(uuid, message) {
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            console.error('WebSocket is not connected');
            showConnectionError('Cannot send message: Chat connection is not available');
            return false;
        }

        try {
            const messageData = {
                type: "message",
                sender_uuid: '<?php echo $sender_uuid; ?>',
                data: {
                    receiver_uuid: uuid,
                    msg: message,
                    date: new Date().toISOString(),
                    attachments: {
                        images: [],
                        videos: [],
                        voice_message: []
                    }
                }
            };

            socket.send(JSON.stringify(messageData));
            console.log('Sent message:', messageData);
            return true;
        } catch (error) {
            console.error('Failed to send message:', error);
            showConnectionError('Failed to send message. Please try again.');
            return false;
        }
    }
</script>
<nav class="navbar navbar-expand-lg bg-light p-3">
    <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <div class="mx-auto">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                        <a class="nav-link <?= ($current_page == 'dashboard_tech_grad.php') ? 'active' : '' ?>" href="./dashboard_tech_grad.php">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link <?= ($current_page == 'job_search.php') ? 'active' : '' ?>" href="./job_search.php">Search jobs</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link <?= ($current_page == 'manage_profile.php') ? 'active' : '' ?>" href="./manage_profile.php">Manage profile</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link <?= ($current_page == 'saved_jobs.php') ? 'active' : '' ?>" href="./saved_jobs.php">Saved jobs</a>
                    </li>
                    <li class="nav-item">
                        <button class="btn " type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasScrolling" aria-controls="offcanvasScrolling">Messages</button>
                    </li>
                    <li>
            
<button id="logout-button" type="button" class="btn btn-small btn-outline-secondary ms-2" onclick="window.location.href='../src/auth/logout.php'">Logout</button>
        
                    </li>
                </ul>
            </div>
        </div>
    </div>
</nav>

<div class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1" id="offcanvasScrolling" aria-labelledby="offcanvasScrollingLabel">
    <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasScrollingLabel">Messages</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="p-3">
        <input type="text" id="searchInput" class="form-control mb-3" placeholder="Search users or employers...">
        <ul class="list-group" id="searchResults"></ul>
    </div>
    <script>
        document.getElementById('searchInput').addEventListener('input', async function () {
            const query = this.value.trim();
            const resultsContainer = document.getElementById('searchResults');
            resultsContainer.innerHTML = '';

            if (query.length > 2) {
                try {
                    const userResponse = await fetch(`https://root-4ytd.onrender.com/api/get-table?table=users&query=${encodeURIComponent(query)}`);
                    const employerResponse = await fetch(`https://root-4ytd.onrender.com/api/get-table?table=employers&query=${encodeURIComponent(query)}`);
                    const userData = userResponse.ok ? await userResponse.json() : { data: [] };
                    const employerData = employerResponse.ok ? await employerResponse.json() : { data: [] };

                    const combinedData = [...userData.data, ...employerData.data].filter(item => {
                        const queryLower = query.toLowerCase();
                        return (
                            (item.first_name && item.first_name.toLowerCase().includes(queryLower)) ||
                            (item.last_name && item.last_name.toLowerCase().includes(queryLower)) ||
                            (item.company_name && item.company_name.toLowerCase().includes(queryLower))
                        );
                    });

                    if (combinedData.length === 0) {
                        resultsContainer.innerHTML = '<li class="list-group-item text-warning">No results found</li>';
                        return;
                }

                    combinedData.forEach(item => {
                        const li = document.createElement('li');
                        li.className = 'list-group-item border-0 rounded mb-2';
                        li.style.cssText = 'cursor: pointer; transition: all 0.2s ease; background-color: #f8f9fa;';
                        const name = item.first_name && item.last_name ? `${item.first_name} ${item.last_name}` : item.company_name || 'Unknown';
                        const avatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random`;
                        const uuid = item.user_uuid || item.employer_uuid || 'Unknown';
                        li.setAttribute('onclick', `showConversation('${name}', '${uuid}')`);
                        li.innerHTML = `
                            <div class="d-flex align-items-center p-2">
                                <div class="position-relative">
                                    <img src="${avatarUrl}" alt="${name}" class="rounded-circle me-3" width="48" height="48" style="box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                                    <span class="position-absolute bottom-0 end-0 transform translate-middle p-1 bg-success border border-light rounded-circle" style="width: 12px; height: 12px;"></span>
                                </div>
                                <div>
                                    <div class="fw-semibold">${name}</div>
                                    <small class="text-muted">Click to start chatting</small>
                                </div>
                                <i class="fas fa-chevron-right ms-auto text-muted"></i>
                            </div>
                        `;
                        li.addEventListener('mouseenter', () => {
                            li.style.backgroundColor = '#e9ecef';
                            li.style.transform = 'translateX(4px)';
                            li.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
                        });
                        li.addEventListener('mouseleave', () => {
                            li.style.backgroundColor = '#f8f9fa';
                            li.style.transform = 'none';
                            li.style.boxShadow = 'none';
                        });
                        resultsContainer.appendChild(li);
                    });
                } catch (error) {
                    resultsContainer.innerHTML = '<li class="list-group-item text-danger">Error fetching results</li>';
                }
            }
        });
    </script>
    <div class="offcanvas-body border bg-light d-flex flex-column">
        <div class="flex-grow-1 overflow-auto mb-3">
            <ul class="list-group" id="contactList">
                <li class="list-group-item border-0 rounded mb-2" style="cursor: pointer; transition: all 0.2s ease; background-color: #f8f9fa;" onclick="showConversation('John Doe', 'example_uuid')">
                    <div class="d-flex align-items-center p-2">
                        <div class="position-relative">
                            <img alt="Profile picture of John Doe" class="rounded-circle me-3" height="48" width="48" src="https://storage.googleapis.com/a1aa/image/DcnuRmt96H7mGpxRQDCrNnBXYJqej7JpIBjcZXwd3UgHf97TA.jpg" style="box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
                            <span class="position-absolute bottom-0 end-0 transform translate-middle p-1 bg-success border border-light rounded-circle" style="width: 12px; height: 12px;"></span>
                        </div>
                        <div>
                            <div class="fw-semibold">John Doe</div>
                            <small class="text-muted">Online</small>
                        </div>
                        <i class="fas fa-chevron-right ms-auto text-muted"></i>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</div>


<div class="offcanvas offcanvas-end" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1" id="conversationCanvas" aria-labelledby="conversationCanvasLabel">
    <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="conversationCanvasLabel">Conversation</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body border bg-light d-flex flex-column">
        <div class="flex-grow-1 overflow-auto mb-3" id="conversationBody">
            <!-- Conversation messages will be dynamically inserted here -->
        </div>
<div class="message-input-container">
            <div class="input-group">
                <input 
                    type="text" 
                    id="messageInput" 
                    class="form-control border-0 shadow-none" 
                    placeholder="Type a message..." 
                    onkeypress="if(event.key === 'Enter') { event.preventDefault(); sendMessage(); }"
                    autocomplete="off"
                    style="background-color: #f8f9fa; border-radius: 1.5rem;"
                >
                <button 
                    class="btn btn-primary rounded-circle d-flex align-items-center justify-content-center ms-2" 
                    style="width: 40px; height: 40px; padding: 0;"
                    type="button" 
                    onclick="sendMessage()"
                >
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
        <script>
            function sendMessage() {
                const messageInput = document.getElementById('messageInput');
                const message = messageInput.value.trim();
                if (message) {
                    const conversationBody = document.getElementById('conversationBody');
                    const messageId = Date.now(); // Unique ID for the message
                    const timestamp = new Date().toLocaleTimeString();
                    const sentMessage = `
                        <div class="d-flex justify-content-end" id="msg-${messageId}">
                            <div class="chat-message sent p-3 text-white">
                                <div>${message}</div>
                                <div class="d-flex align-items-center justify-content-between mt-1">
                                    <div class="chat-timestamp text-white-50">${timestamp}</div>
                                    <div class="chat-status text-white-50">
                                        <i class="fas fa-clock"></i>
                                        <span>Sending...</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    conversationBody.innerHTML += sentMessage;
                    messageInput.value = ''; // Clear the input field after sending
                    
                    // Send message and handle immediate errors
                    const sent = logMessage(uuid_target, message);
                    if (!sent) {
                        const messageElement = document.getElementById(`msg-${messageId}`);
                        if (messageElement) {
                            const statusElement = messageElement.querySelector('.chat-status');
                            statusElement.innerHTML = '<i class="fas fa-times"></i> Failed';
                            statusElement.className = 'chat-status text-danger';
                        }
                        return;
                    }
                    
                    // Listen for server response
                    const messageStatusHandler = (event) => {
                        const data = JSON.parse(event.data);
                        if (data.type === 'response') {
                            const messageElement = document.getElementById(`msg-${messageId}`);
                            if (messageElement) {
                                const statusElement = messageElement.querySelector('.chat-status');
                                if (data.status === 'success') {
                                    if (data.data?.delivery_status === 'pending') {
                                        statusElement.innerHTML = '<i class="fas fa-check"></i> Saved';
                                        statusElement.className = 'chat-status text-success';
                                        statusElement.title = 'Message will be delivered when recipient connects';
                                    } else {
                                        statusElement.innerHTML = '<i class="fas fa-check-double"></i> Delivered';
                                        statusElement.className = 'chat-status text-success';
                                    }
                                } else {
                                    statusElement.innerHTML = '<i class="fas fa-times"></i> Failed';
                                    statusElement.className = 'chat-status text-danger';
                                    console.error('Message failed:', data.message);
                                }
                            }
                            socket.removeEventListener('message', messageStatusHandler);
                        }
                    };
                    socket.addEventListener('message', messageStatusHandler);

                    // Auto-scroll to the latest message
                    conversationBody.scrollTop = conversationBody.scrollHeight;
                }
            }

            // Remove unused function
        </script>
    </div>
</div>

<script>
    let uuid_target;
    function showConversation(contactName, uuid) {
        uuid_target = uuid;
        
        // Update conversation title
        const conversationTitle = document.getElementById('conversationCanvasLabel');
        conversationTitle.textContent = contactName;
        
        // Clear previous messages
        const conversationBody = document.getElementById('conversationBody');
        conversationBody.innerHTML = '';
        
        // Show loading indicator
        conversationBody.innerHTML = `
            <div class="text-center p-3">
                <i class="fas fa-spinner fa-spin"></i>
                <div class="mt-2 text-muted">Loading messages...</div>
            </div>
        `;

        // Show conversation panel
        const conversationCanvas = bootstrap.Offcanvas.getOrCreateInstance(document.getElementById('conversationCanvas'));
        conversationCanvas.show();

        // Show connection status and request chat history
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            showConnectionError('Connecting to chat server...', 'warning', true);
            connectWebSocket();
            // Add event listener for when connection is established
            const checkConnection = setInterval(() => {
                if (socket && socket.readyState === WebSocket.OPEN) {
                    requestChatHistory(uuid);
                    clearInterval(checkConnection);
                }
            }, 1000);
        } else {
            requestChatHistory(uuid);
        }
    }

    function requestChatHistory(targetUuid) {
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            console.error('Cannot request chat history: WebSocket not connected');
            return;
        }

        try {
            const request = {
                type: "history_request",
                data: {
                    target_uuid: targetUuid
                }
            };
            socket.send(JSON.stringify(request));
            console.log('Requested chat history for:', targetUuid);
        } catch (error) {
            console.error('Failed to request chat history:', error);
            showConnectionError('Failed to load chat history. Please try again.');
        }
    }
</script>
