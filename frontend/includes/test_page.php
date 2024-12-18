<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bootstrap Offcanvas</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="../../../assets/links.css" rel="stylesheet">
</head>

<body>
    <?php include './test.php'; ?>

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

    <!-- Bootstrap JS (includes Popper.js) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
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
</body>

</html>