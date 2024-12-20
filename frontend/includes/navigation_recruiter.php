<?php
$current_page = basename(htmlspecialchars($_SERVER['PHP_SELF'])); //! Get the current page
?>
<style>
    .navbar {
        position: sticky;
        top: 0;
        z-index: 99;
    }
    .offcanvas{
        z-index: 999;
    }
</style>
<nav class="navbar navbar-expand-lg bg-light p-3">
    <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <div class="mx-auto">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link <?= ($current_page == 'dashboard_recruiter.php') ? 'active' : '' ?>" href="./dashboard_recruiter.php">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link <?= ($current_page == 'manage_job.php') ? 'active' : '' ?>" href="./manage_job.php">Manage Job</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link <?= ($current_page == 'post_job.php') ? 'active' : '' ?>" href="./post_job.php">Post a Job</a>
                    </li>
                    <li class="nav-item">
                        <button class="btn" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasScrolling" aria-controls="offcanvasScrolling">Messages</button>
                    </li>
                    <li>
                        <button id="logout-button" type="button" class="btn btn-small btn-outline-secondary ms-2" onclick="logout()">Logout</button>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</nav>

<!-- Offcanvas Structures (Messages and Conversation) -->
<div class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1" id="offcanvasScrolling" aria-labelledby="offcanvasScrollingLabel">
    <!-- Offcanvas Header and Body -->
    <!-- ... (No changes needed here) ... -->
</div>

<div class="offcanvas offcanvas-end" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1" id="conversationCanvas" aria-labelledby="conversationCanvasLabel">
    <!-- Offcanvas Header and Body -->
    <!-- ... (No changes needed here) ... -->
</div>

<!-- Load FontAwesome for icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
<!-- Load chat.js with cache busting -->
<script src="/frontend/assets/js/chat.js?v=<?= time(); ?>"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Debug session data
    console.log('Session data:', <?= json_encode($_SESSION) ?>);

    // Define sessionData as a global JavaScript variable
    var sessionData = <?= json_encode($_SESSION) ?>;

    <?php
    if (isset($_SESSION['employerData']) && isset($_SESSION['employerData']['employer_uuid'])) {
        $employer_uuid = $_SESSION['employerData']['employer_uuid'];
        echo "console.log('Employer UUID:', '" . $employer_uuid . "');";

        // Initialize chat directly without setTimeout
        echo "
        if (typeof connectWebSocket === 'function') {
            connectWebSocket('" . $employer_uuid . "', '" . getWebSocketURL() . "');
        } else {
            console.error('Chat functionality not loaded properly');
            alert('Chat functionality not loaded properly. Please refresh the page.');
        }
        ";
    } else {
        echo "console.error('Session data:', " . json_encode($_SESSION) . ");";
        echo "alert('Error: No employer UUID found in session. Please check if you are properly logged in.');";
    }
    
    /**
     * Function to dynamically get the WebSocket URL based on the current protocol and host.
     * This ensures that WebSockets work correctly in both development and production environments.
     */
    function getWebSocketURL() {
        $protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off' ||
                     $_SERVER['SERVER_PORT'] == 443) ? "wss" : "ws";
        $host = $_SERVER['HTTP_HOST'];
        return "$protocol://$host/ws/chat";
    }
    ?>
});
</script>

<div class="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1" id="offcanvasScrolling" aria-labelledby="offcanvasScrollingLabel">
    <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasScrollingLabel">Messages</h5>
        <div class="d-flex align-items-center">
            <span id="connectionStatus" class="me-2 small">
                <span class="text-warning"><i class="fas fa-circle me-1"></i>Connecting...</span>
            </span>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
    </div>
    <div class="offcanvas-body border bg-light d-flex flex-column">
        <div class="mb-3">
            <input type="text" id="searchInput" class="form-control" placeholder="Search users..." data-bs-toggle="dropdown" aria-expanded="false">
            <ul class="dropdown-menu w-100" id="searchResults">
                <!-- Search results will appear here -->
            </ul>
        </div>
        <div class="flex-grow-1 overflow-auto mb-3">
            <ul class="list-group" id="contactList">
                <!-- Contact list will be populated dynamically based on chat history -->
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
        <div class="input-group">
            <input type="text" class="form-control" placeholder="Type a message...">
            <button class="btn btn-primary" type="button"><i class="fas fa-paper-plane"></i></button>
        </div>
    </div>
</div>

<!-- Load FontAwesome for icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
<!-- Load chat.js with absolute path -->
<script src="/frontend/assets/js/chat.js?v=<?php echo time(); ?>"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    <?php
    // Start session if not already started
    if (session_status() === PHP_SESSION_NONE) {
        session_start();
    }

    // Debug session data
    echo "console.log('Session data:', " . json_encode($_SESSION) . ");";

    // Define sessionData as a global JavaScript variable
    echo "var sessionData = " . json_encode($_SESSION) . ";";

    if (isset($_SESSION['employerData']) && isset($_SESSION['employerData']['employer_uuid'])) {
        $employer_uuid = $_SESSION['employerData']['employer_uuid'];
        echo "console.log('Employer UUID:', '" . $employer_uuid . "');";
        
        // Initialize chat directly without setTimeout
        echo "
        if (typeof connectWebSocket === 'function') {
            connectWebSocket('" . $employer_uuid . "');
        } else {
            console.error('Chat functionality not loaded properly');
            alert('Chat functionality not loaded properly. Please refresh the page.');
        }
        ";
    } else {
        echo "console.error('Session data:', " . json_encode($_SESSION) . ");";
        echo "alert('Error: No employer UUID found in session. Please check if you are properly logged in.');";
    }
    ?>
});
</script>
