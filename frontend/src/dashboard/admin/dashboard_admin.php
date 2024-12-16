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
                                    <h1>69</h1>
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
                                    <h1>69</h1>
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
                                    <h1>69k</h1>
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
                            <div class="col-md-3 " style="width: 15.5rem; ">
                                <div class="card" style="width: 15rem;">
                                    <div class="card-body">
                                        <div class="card-title d-flex align-items-center flex-column">
                                            <!-- img -->
                                            <div class="profile border" style="height: 170px; width:170px; border-radius: 50%">

                                            </div>
                                        </div>
                                        <h5>Johua Cabuang</h5>

                                        <p class="card-text">
                                            <span class="text-secondary">Started at</span> <br>
                                            dd/mm/yyyy
                                        </p>
                                        <a href="#" class="card-link">Card link</a>
                                        <a href="#" class="card-link">Another link</a>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row gap-2 mt-3 " style="overflow: auto">
                            <h4>Employers</h4>
                            <div class="col-md-3 " style="width: 15.5rem; ">
                                <div class="card" style="width: 15rem;">
                                    <div class="card-body">
                                        <div class="card-title d-flex align-items-center flex-column">
                                            <!-- img -->
                                            <div class="profile border" style="height: 170px; width:170px; border-radius: 50%">

                                            </div>
                                        </div>
                                        <h5>Company name</h5>

                                        <p class="card-text">
                                            <span class="text-secondary">Started at</span> <br>
                                            dd/mm/yyyy
                                        </p>
                                        <a href="#" class="card-link">Card link</a>
                                        <a href="#" class="card-link">Another link</a>
                                    </div>
                                </div>
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

        // Fetch dynamic data from your backend
        fetch('http://localhost/php/root/frontend/src/dashboard/admin/get_data.php') 
            .then(response => response.json())
            .then(data => {
                // Data from the server
                const techGradCount = data.tech_grad || 0; // Replace with the correct data field
                const employerCount = data.employers || 0; // Replace with the correct data field

                // Initialize the chart with dynamic data
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['Tech Grads', 'Employers'], // Dynamic labels
                        datasets: [{
                            label: '# of Registrations',
                            data: [techGradCount, employerCount], // Dynamic data
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
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