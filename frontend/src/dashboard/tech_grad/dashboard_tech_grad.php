<?php
// Prevent any output before headers
ini_set('display_errors', 0);
error_reporting(0);

// Start session
session_start();

// Check if user is logged in and is a tech grad user
if (!isset($_SESSION['isLoggedIn']) || !$_SESSION['isLoggedIn'] || $_SESSION['userType'] !== 'user') {
    header('Location: ../../auth/login.php');
    exit;
}

// Get user data
$userData = $_SESSION['userData'];
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tech Grad Dashboard</title>
    <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="../../../assets/scroll-animation.css">
    <script src='../../../includes/scroll-animation.js'></script>
    <style>
        .col-lg-3 {
            width: 15rem
        }
    </style>
</head>

<body>
    <?php include '../../../includes/navigation_users.php' ?>

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

    <div class="container-fluid">
        <div class="container d-flex align-items-center justify-content-between scroll-hidden">
            <div class="row">
                <div class="col-md-6">
                    <div class="container d-flex align-items-center ">
                        <div class="border border-dark" style="height: 100px; width:100px; border-radius: 50%;" onclick="document.getElementById('profile-input').click()">
                            <input type="file" class="form-control border mb-4 d-none" id="profile-input">
                        </div>
                        <h4 id="company-name" class="mt-4 mb-3 me-3 ms-4"><?php echo htmlspecialchars($userData['first_name'] . ' ' . $userData['last_name']); ?></h4>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="d-flex justify-content-between mt-3" style="width: 350px; line-height: 1.2;">
                        <div class="description">
                            <p>
                            <p id="industry-description" class="text-secondary mb-1">Tech Industry Job Experts</p>
                            <h5 id="career-building" class="fw-bold">Building Careers in Technology</h5>
                            </p>
                        </div>
                        <div>
                            <p>
                            <p class="text-secondary mb-1">Date Started</p>
                            <h5 id="date-started" class="fw-bold"><?php echo date('d/m/Y', strtotime($userData['created_at'])); ?></h5>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row scroll-hidden">
            <div class="col-md-6 ">
                <div class="mt-3 p-3 d-flex algin-items-center justify-content-center">
                    <div class="resume w-100">
                        <img src="https://tse4.mm.bing.net/th?id=OIP.zLTJn9vwvvV_XBwoTEbJ5gHaKe&pid=Api&P=0&h=180" alt="" style="width: 100%; object-fit: contain">
                    </div>
                </div>
            </div>
            <div class="col-md-6 ">
                <div class="container mt-3 p-3 ">
                    <h4 class="text-secondary">Information</h4>
                    <div class="ms-3 row" style="line-height: 40px">
                        <div class="col-md-12">
                            <i class="bi bi-envelope-at"></i>
                            <span class="ms-3">Email</span>
                            <strong class="ms-5"><?php echo htmlspecialchars($userData['email']); ?></strong>
                        </div>
                        <div class="col-md-12">
                            <i class="bi bi-telephone"></i>
                            <span class="ms-3">Phone</span>
                            <strong class="ms-5"><?php echo htmlspecialchars($userData['phone_number']); ?></strong>
                        </div>
                        <div class="col-md-12">
                            <i class="bi bi-geo-alt"></i>
                            <span class="ms-3">State</span>
                            <strong class="ms-5"><?php echo htmlspecialchars($userData['state']); ?></strong>
                        </div>
                        <div class="col-md-12">
                            <hr>
                            <h4 class="text-secondary">Qualifications</h4>
                            <i class="bi bi-person-check"></i>
                            <span class="ms-3">Degree</span>
                            <strong class="ms-5"><?php echo htmlspecialchars($userData['degree'] ?? 'BSIT'); ?></strong>
                        </div>
                        <div class="col-md-12">
                            <i class="bi bi-building-check"></i>
                            <span class="ms-3">Graduated at</span>
                            <strong class="ms-5"><?php echo htmlspecialchars($userData['graduated_at'] ?? 'Not specified'); ?></strong>
                        </div>
                        <div class="col-md-12">
                            <i class="bi bi-patch-check"></i>
                            <span class="ms-3">Certification</span>
                            <strong class="ms-5"><?php echo htmlspecialchars($userData['certification'] ?? 'Not specified'); ?></strong>
                        </div>
                        <div class="col-md-12">
                            <i class="bi bi-pc-display"></i>
                            <span class="ms-3">Specialized training</span>
                            <strong class="ms-5"><?php echo htmlspecialchars($userData['specialized_training'] ?? 'Not specified'); ?></strong>
                        </div>
                        <div class="col-md-12">
                            <hr>
                            <h4 class="text-secondary">Interests</h4>
                        </div>
                        <div class="col-md-12">
                            <i class="bi bi-person-workspace"></i>
                            <span class="ms-3">Job interest</span>
                            <strong class="ms-5"><?php echo htmlspecialchars($userData['job_interest'] ?? 'Not specified'); ?></strong>
                        </div>
                        <div class="col-md-12">
                            <i class="bi bi-calendar3-week"></i>
                            <span class="ms-3">Job type</span>
                            <strong class="ms-5"><?php echo htmlspecialchars($userData['job_type'] ?? 'Not specified'); ?></strong>
                        </div>
                        <div class="col-md-12">
                            <i class="bi bi-pin-map"></i>
                            <span class="ms-3">Preferred location</span>
                            <strong class="ms-5"><?php echo htmlspecialchars($userData['preferred_location'] ?? 'Not specified'); ?></strong>
                        </div>
                        <div class="col-md-12">
                            <i class="bi bi-cash"></i>
                            <span class="ms-3">Salary range</span>
                            <strong class="ms-5"><?php echo htmlspecialchars($userData['salary_range'] ?? 'Not specified'); ?></strong>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
