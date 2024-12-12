<?php 
include '../includes/latest_trends.php';

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <title>
        Find jobs!
    </title>
    <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&amp;display=swap" rel="stylesheet" />
    <link href="../assets/general.css" rel="stylesheet" />
    <link href="../assets/links.css" rel="stylesheet" />
    <style>
    
    </style>
</head>

<body>
    <?php include '../includes/navigationV1.php' ?>
    <div class="container-fluid vh-100 d-flex flex-column align-items-center scroll-hidden">
        <div class="container mt-5 d-flex flex-column align-items-center">
            <h2 class="text-center">
                Empowering tech graduates to connect with top employers.
            </h2>
            <p class="text-center">
                Explore thousands of job opportunities and take the next step in your tech career.
            </p>
            <a class="text-light mt-5" href="role_selection.php">
                <button class="btn btn-lg btn-color">
                    Get started today—it's free!
                </button>
            </a>
        </div>
        <div class="container d-flex justify-content-evenly mt-5 p-3 align-items-center scroll-hidden">
            <div class="card text-bg-light mb-3 box-start">
                <div class="card-header">
                    <h5 class="card-title">
                        <i class="fas fa-file-alt">
                        </i>
                        Personalized Job Matches
                    </h5>
                </div>
                <div class="card-body">
                    <p class="card-text">
                        Get job recommendations tailored to your skills and preferences. Save time and find the right opportunities for you.
                    </p>
                </div>
            </div>
            <div class="card text-bg-light mb-3 box-mid">
                <div class="card-header">
                    <h5 class="card-title">
                        <i class="fas fa-search">
                        </i>
                        Hassle-free Finding jobs
                    </h5>
                </div>
                <div class="card-body">
                    <p class="card-text">
                        Apply to jobs with just one click. Upload your resume, fill out your profile, and let the platform do the rest.
                    </p>
                </div>
            </div>
            <div class="card text-bg-light mb-3 box-end">
                <div class="card-header">
                    <h5 class="card-title">
                        <i class="fas fa-chart-line">
                        </i>
                        Powerful Employer Insights
                    </h5>
                </div>
                <div class="card-body">
                    <p class="card-text">
                        Gain valuable insights on job postings and applicant performance. Track applications, view analytics, and hire top tech talent faster.
                    </p>
                </div>
            </div>
        </div>
    </div>
    <div class="container-fluid vh-100 d-flex flex-column align-items-center scroll-hidden">
        <h1>Latest trends!</h1>
        <marquee behavior="scroll" direction="left" style="height: 400px;">
            <div class="container d-flex align-items-center justify-content-evenly">
            
                <?php echo $store_data;?>
            
        </div>
        </marquee>
    <div class="container-fluid vh-100 d-flex align-items-center justify-content-center scroll-hidden">
        <h1>
            And me!
        </h1>
    </div>
    <?php include '../includes/footer.php'?>
    <script src="../includes/scroll-animation.js"></script>
</body>

</html>