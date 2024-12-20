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
    <title>Saved Jobs</title>
    <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <link href="../../../assets/links.css" rel="stylesheet" />
    <link rel="stylesheet" href="../../../assets/scroll-animation.css">
    <script src='../../../includes/scroll-animation.js'></script>
</head>

<body>
    <?php include '../../../includes/navigation_users.php' ?>
    <div class="container-fluid d-flex justify-content-center scroll-hidden">
        <!-- jobs -->
        <div class="col-md-9 m-5" style="height: 90vh; overflow: hidden">
            <div class="row gap-2">
                <div class="col-md-12">
                    <form id="search-form">
                        <div class="row">
                            <div class="col-md-12">
                                <div class="input-group">
                                    <input type="search" class="form-control" name="saved-job" id="saved-job-search" placeholder="E.g Web developer">
                                    <button type="submit" class="btn btn-dark"><i class="bi bi-search"></i></button>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="col-md-12">
                    <div class="row gap-2" id="saved-jobs-container">
                        <!-- Saved jobs will be dynamically loaded here -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
    // Add user data for saved jobs handling
    const userData = <?php echo json_encode($userData); ?>;
    
    // Load saved jobs when page loads
    document.addEventListener('DOMContentLoaded', function() {
        loadSavedJobs();

        // Handle search form submission
        document.getElementById('search-form').addEventListener('submit', function(event) {
            event.preventDefault();
            const searchTerm = document.getElementById('saved-job-search').value;
            loadSavedJobs(searchTerm);
        });
    });

    function loadSavedJobs(searchTerm = '') {
        const userId = userData.user_id;
        fetch(`http://localhost:10000/saved-jobs/${userId}?search=${searchTerm}`)
            .then(response => response.json())
            .then(jobs => {
                const container = document.getElementById('saved-jobs-container');
                container.innerHTML = ''; // Clear existing jobs

                jobs.forEach(job => {
                    const jobCard = createJobCard(job);
                    container.appendChild(jobCard);
                });

                if (jobs.length === 0) {
                    container.innerHTML = '<div class="col-12 text-center"><h4>No saved jobs found</h4></div>';
                }
            })
            .catch(error => {
                console.error('Error loading saved jobs:', error);
                alert('Error loading saved jobs. Please try again later.');
            });
    }

    function createJobCard(job) {
        const col = document.createElement('div');
        col.className = 'col-md-3';
        col.style.width = '15.5rem';

        col.innerHTML = `
            <div class="card" style="width: 15.5rem;">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h5 class="card-title">${job.title}</h5>
                        </div>
                        <div class="company-profile border" style="height: 50px; width: 50px; border-radius: 50px">
                            ${job.company_logo || 'img'}
                        </div>
                    </div>
                    <h6 class="card-subtitle mb-2 text-body-secondary">${job.company_name}</h6>
                    <p class="text-secondary">${job.location}</p>
                    <p class="card-text">
                        <button type="button" disabled class="btn btn-outline-secondary btn-sm">${job.type}</button>
                        <h6>$${job.salary_min} - $${job.salary_max}</h6>
                    </p>
                    <form>
                        <div class="row">
                            <div class="col-md-8 p-1">
                                <a href="job_single_view.php?id=${job.job_id}" class="btn btn-sm btn-dark w-100">More details</a>
                            </div>
                            <div class="col-md-4 p-1">
                                <button type="button" class="btn btn-sm btn-secondary w-100" onclick="removeJob('${job.job_id}')">Remove</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        `;

        return col;
    }

    function removeJob(jobId) {
        if (!confirm('Are you sure you want to remove this job from your saved list?')) {
            return;
        }

        const userId = userData.user_id;
        fetch(`http://localhost:10000/saved-jobs/remove`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: userId,
                job_id: jobId
            })
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                loadSavedJobs(); // Reload the saved jobs list
            } else {
                alert(result.message || 'Failed to remove job. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error removing job:', error);
            alert('Error removing job. Please try again later.');
        });
    }
    </script>
</body>

</html>