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
        <div class="offcanvas-body border bg-light d-flex flex-column">
            <div class="flex-grow-1 overflow-auto mb-3">
                <ul class="list-group" id="contactList">
                    <li class="list-group-item d-flex align-items-center" onclick="showConversation('John Doe')">
                        <img alt="Profile picture of John Doe" class="rounded-circle me-3" height="50" src="https://storage.googleapis.com/a1aa/image/DcnuRmt96H7mGpxRQDCrNnBXYJqej7JpIBjcZXwd3UgHf97TA.jpg" width="50" />
                        <div>
                            <h6 class="mb-0">John Doe</h6>
                            <small class="text-muted">Online</small>
                        </div>
                    </li>
                    <li class="list-group-item d-flex align-items-center" onclick="showConversation('Jane Smith')">
                        <img alt="Profile picture of Jane Smith" class="rounded-circle me-3" height="50" src="https://storage.googleapis.com/a1aa/image/d21jL7y7Q74gA1LctixDVnjbM14lvfJEGhtlHjUqeSJUe73nA.jpg" width="50" />
                        <div>
                            <h6 class="mb-0">Jane Smith</h6>
                            <small class="text-muted">Offline</small>
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
            <div class="input-group">
                <input type="text" class="form-control" placeholder="Type a message...">
                <button class="btn btn-primary" type="button"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
    </div>

    <script>
        function showConversation(contactName) {
            const conversationBody = document.getElementById('conversationBody');
            conversationBody.innerHTML = ''; // Clear previous conversation

            if (contactName === 'John Doe') {
                conversationBody.innerHTML = `
                    <div class="d-flex justify-content-start mb-2">
                        <div class="p-2 bg-primary text-white rounded">Hello! How can I help you today?</div>
                    </div>
                    <div class="d-flex justify-content-end mb-2">
                        <div class="p-2 bg-secondary text-white rounded">I need some information about your services.</div>
                    </div>
                    <div class="d-flex justify-content-start mb-2">
                        <div class="p-2 bg-primary text-white rounded">Sure, what would you like to know?</div>
                    </div>
                    <div class="d-flex justify-content-end mb-2">
                        <div class="p-2 bg-secondary text-white rounded">Can you tell me more about your pricing?</div>
                    </div>
                    <div class="d-flex justify-content-start mb-2">
                        <div class="p-2 bg-primary text-white rounded">Our pricing varies depending on the service. Please visit our pricing page for more details.</div>
                    </div>
                `;
            } else if (contactName === 'Jane Smith') {
                conversationBody.innerHTML = `
                    <div class="d-flex justify-content-start mb-2">
                        <div class="p-2 bg-primary text-white rounded">Hi Jane! How are you?</div>
                    </div>
                    <div class="d-flex justify-content-end mb-2">
                        <div class="p-2 bg-secondary text-white rounded">I'm good, thanks! How about you?</div>
                    </div>
                    <div class="d-flex justify-content-start mb-2">
                        <div class="p-2 bg-primary text-white rounded">I'm doing well. Just wanted to catch up.</div>
                    </div>
                    <div class="d-flex justify-content-end mb-2">
                        <div class="p-2 bg-secondary text-white rounded">Sure, let's chat!</div>
                    </div>
                `;
            }

            const conversationCanvas = new bootstrap.Offcanvas(document.getElementById('conversationCanvas'));
            conversationCanvas.show();
        }
        </script>