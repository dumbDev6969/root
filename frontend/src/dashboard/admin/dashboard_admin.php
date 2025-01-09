<?php
// Prevent any output before headers
ini_set('display_errors', 0);
error_reporting(0);

// Start session
session_start();

// Check if user is logged in and is an admin
if (!isset($_SESSION['isLoggedIn']) || !$_SESSION['isLoggedIn'] || $_SESSION['userType'] !== 'admin') {
    header('Location: ../../auth/admin_login.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet" />

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <link href="../../../assets/links.css" rel="stylesheet" />
    <link rel="stylesheet" href="../../../assets/scroll-animation.css">
    <script src='../../../includes/scroll-animation.js'></script>
    
</head>

<body>
    <?php include '../../../includes/navigation_admin.php' ?>
    <div class="container">
        <div class="row mt-5 ">
            <div class="col-md-12 scroll-hidden">
                <div class="row gap-2">
                    <div class="col-md-3 " style="width: 18rem">
                        <div class="card" style="width: 18rem;">
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item text-secondary d-flex align-items-center justify-content-between">
                                    <h4>Tech graduates</h4>
                                    <i class="bi bi-person-square"></i>
                                </li>
                                <li class="list-group-item">
                                    <h1 class="tech-grad-count">0</h1>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-3" style="width: 18rem">
                        <div class="card" style="width: 18rem;">
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item text-secondary d-flex align-items-center justify-content-between">
                                    <h4>Employers</h4>
                                    <i class="bi bi-building-down"></i>
                                </li>
                                <li class="list-group-item">
                                    <h1 class="employer-count">0</h1>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-3" style="width: 18rem">
                        <div class="card" style="width: 18rem;">
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item text-secondary d-flex align-items-center justify-content-between">
                                    <h4>Job posted</h4>
                                    <i class="bi bi-pc-display"></i>
                                </li>
                                <li class="list-group-item">
                                    <h1 class="job-count">0</h1>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-3" style="width: 18rem">
                        <div>
                            <canvas id="myChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-12 scroll-hidden">
                <!-- main row for tech grad and empoyer -->
                <div class="row">
                    <div class="col-md-6 ">
                        <!-- row fo tech grad -->
                        <div class="row gap-2 mt-3 " style="overflow: auto">
                            <h4>Tech graduates</h4>
                            <div class="tech-grads-list row gap-2">
                                <!-- Tech grads will be loaded here dynamically -->
                            </div>

                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row gap-2 mt-3 " style="overflow: auto">
                            <h4>Employers</h4>
                            <div class="employers-list row gap-2">
                                <!-- Employers will be loaded here dynamically -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <script>
        const ctx = document.getElementById('myChart');

        // Function to update dashboard counts
        function updateCounts(users, employers, jobs) {
            document.querySelector('.tech-grad-count').textContent = users;
            document.querySelector('.employer-count').textContent = employers;
            document.querySelector('.job-count').textContent = jobs;
        }

        // Fetch dynamic data from API
        Promise.all([
            fetch('http://localhost:10000/api/get-table?table=users', { credentials: 'omit' }).then(r => r.json()),
            fetch('http://localhost:10000/api/get-table?table=employers', { credentials: 'omit' }).then(r => r.json()),
            fetch('http://localhost:10000/api/get-table?table=jobs', { credentials: 'omit' }).then(r => r.json())
        ])
        .then(([usersData, employersData, jobsData]) => {
            const techGradCount = usersData.data.length;
            const employerCount = employersData.data.length;
            const jobCount = jobsData.data.length;

            // Update the counts in the UI
            updateCounts(techGradCount, employerCount, jobCount);

            // Update tech grads list
            const techGradsList = document.querySelector('.tech-grads-list');
            techGradsList.innerHTML = usersData.data.map(user => `
                <div class="col-md-3" style="width: 15.5rem;">
                    <div class="card" style="width: 15rem;">
                        <div class="card-body">
                            <div class="card-title d-flex align-items-center flex-column">
                                <div class="profile border" style="height: 170px; width:170px; border-radius: 50%"></div>
                            </div>
                            <h5>${user.first_name} ${user.last_name}</h5>
                            <p class="card-text">
                                <span class="text-secondary">Started at</span><br>
                                ${new Date(user.created_at).toLocaleDateString()}
                            </p>
                            <a href="#" class="btn btn-outline-secondary btn-sm">View Profile</a>
                        </div>
                    </div>
                </div>
            `).join('');

            // Update employers list
            const employersList = document.querySelector('.employers-list');
            employersList.innerHTML = employersData.data.map(employer => `
                <div class="col-md-3" style="width: 15.5rem;">
                    <div class="card" style="width: 15rem;">
                        <div class="card-body">
                            <div class="card-title d-flex align-items-center flex-column">
                                <div class="profile border" style="height: 170px; width:170px; border-radius: 50%"></div>
                            </div>
                            <h5>${employer.company_name}</h5>
                            <p class="card-text">
                                <span class="text-secondary">Started at</span><br>
                                ${new Date(employer.created_at).toLocaleDateString()}
                            </p>
                            <a href="#" class="btn btn-outline-secondary btn-sm">View Profile</a>
                        </div>
                    </div>
                </div>
            `).join('');

            // Initialize the chart with dynamic data
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Tech Grads', 'Employers', 'Jobs'],
                    datasets: [{
                        label: '# of Registrations',
                        data: [techGradCount, employerCount, jobCount],
                        backgroundColor: [
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(153, 102, 255, 0.2)'
                        ],
                        borderColor: [
                            'rgba(75, 192, 192, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(153, 102, 255, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    </script>

</body>

</html>