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

// Get job ID from query parameter
$jobId = isset($_GET['id']) ? $_GET['id'] : null;
if (!$jobId) {
    header('Location: job_search.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Details</title>
    <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="../../../assets/links.css">
    <link rel="stylesheet" href="../../../assets/scroll-animation.css">
    <script src='../../../includes/scroll-animation.js'></script>
    <style>
        .col-lg-3 {
            width: 15rem
        }
    </style>
</head>

<body>
    <div class="container scroll-hidden" style="position: sticky; top:0">
        <nav style="--bs-breadcrumb-divider: '/';" aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="./job_search.php">Home</a></li>
                <li class="breadcrumb-item active" aria-current="page">Job</li>
            </ol>
        </nav>
    </div>
    <div class="container mt-5 p-5 d-flex align-items-center justify-content-center">
        <div class="card w-50 shadow-lg scroll-hidden">
            <h5 class="card-header bg-secondary text-white" id="company-name">Loading...</h5>
            <div class="card-body">
                <h5 class="card-title" id="job-title">Loading...</h5>
                <button class="btn btn-sm btn-outline-secondary mb-3" disabled id="job-type">Loading...</button>
                <p class="card-text">
                    <i class="bi bi-geo-alt"></i>
                    <span id="job-location">Loading...</span>
                </p>
                <p class="card-text" id="job-description">Loading...</p>
                <h5 class="card-text text-success" id="job-salary">Loading...</h5>
                <p class="card-text">
                    <strong>Requirements:</strong>
                    <span id="job-requirements">Loading...</span>
                </p>
                <form id="apply-form">
                    <div class="row">
                        <div class="col-md-12">
                            <button type="button" class="btn btn-lg btn-dark w-100" data-bs-toggle="modal" data-bs-target="#applyModal">Apply Now!</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <div class="modal fade" id="applyModal" tabindex="-1" aria-labelledby="applyModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="applyModalLabel">Submit Your Resume</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="resumeForm">
                        <input type="hidden" name="user_id" value="<?php echo htmlspecialchars($userData['user_id']); ?>">
                        <input type="hidden" name="job_id" value="<?php echo htmlspecialchars($jobId); ?>">
                        <div class="mb-3">
                            <label for="resume" class="form-label">Upload Resume</label>
                            <input type="file" class="form-control" id="resume" name="resume" required>
                        </div>
                        <div class="mb-3">
                            <label for="message" class="form-label">Message (Optional)</label>
                            <textarea class="form-control" id="message" name="message" rows="3"></textarea>
                        </div>
                        <button type="submit" class="btn btn-dark w-100">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script>
    // Add user data and job ID for application handling
    const userData = <?php echo json_encode($userData); ?>;
    const jobId = <?php echo json_encode($jobId); ?>;
    
    // Fetch job details when page loads
    document.addEventListener('DOMContentLoaded', function() {
        fetch(`https://root-4ytd.onrender.com/jobs/${jobId}`)
            .then(response => response.json())
            .then(job => {
                document.getElementById('company-name').textContent = job.company_name;
                document.getElementById('job-title').textContent = job.title;
                document.getElementById('job-type').textContent = job.type;
                document.getElementById('job-location').textContent = job.location;
                document.getElementById('job-description').textContent = job.description;
                document.getElementById('job-salary').textContent = `Salary: $${job.salary_min} - $${job.salary_max}`;
                document.getElementById('job-requirements').textContent = job.requirements;
            })
            .catch(error => {
                console.error('Error fetching job details:', error);
                alert('Error loading job details. Please try again later.');
            });

        // Handle resume submission
        document.getElementById('resumeForm').addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);
            
            fetch('https://root-4ytd.onrender.com/applications/submit', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    alert('Application submitted successfully!');
                    window.location.href = 'job_search.php';
                } else {
                    alert(result.message || 'Failed to submit application. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error submitting application:', error);
                alert('Error submitting application. Please try again later.');
            });
        });
    });
    </script>
</body>
</html>