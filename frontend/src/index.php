<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bootstrap Scroll Animation</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>

    <link rel="stylesheet" href="../assets/general.css">
    <link rel="stylesheet" href="../assets/links.css">
</head>

<body>
    <?php include '../includes/navigationV1.php' ?>
    <div class="container-fluid vh-100 d-flex flex-column  align-items-center scroll-hidden">
        <div class="container mt-5 d-flex flex-column align-items-center ">
            <h2 class="text-center">Empowering tech graduates to connect with top employers. </h2>
            <p class="text-center">Explore thousands of job opportunities and take the next step in your tech career.</p>

            <a href="role_selection.php" class="text-light mt-5">
                <button class="btn btn-lg btn-color">Get started today—it's free!</button>
            </a>

        </div>
        <div class="container d-flex justify-content-evenly mt-5 p-3 align-items-center scroll-hidden">
            <div class="card text-bg-light mb-3 box-start ">
                <div class="card-header ">
                    <h5 class="card-title"><i class="bi bi-file-earmark-check-fill"></i>
                </div>
                <div class="card-body">
                    <div class="text ">
                        <h4>Personalized Job Matches</h4>
                        </h5>
                        <p class="card-text">Get job recommendations tailored to your skills and preferences. Save time and find the right opportunities for you.</p>
                    </div>
                </div>
            </div>

            <div class="card text-bg-light mb-3 box-mid rounded-start-2">
                <div class="card-header">
                    <h5 class="card-title"><i class="bi bi-search"></i>
                </div>
                <div class="card-body">
                    <h4>Hassle-free Finding jobs</h4>
                    </h5>
                    <p class="card-text">Apply to jobs with just one click. Upload your resume, fill out your profile, and let the platform do the rest.</p>
                </div>
            </div>
            <div class="card text-bg-light mb-3 box-end rounded-start-2">
                <div class="card-header">
                    <h5 class="card-title"><i class="bi bi-file-earmark-check-fill"></i>
                </div>
                <div class="card-body">
                    <h4>Powerful Employer Insights</h4>
                    </h5>
                    <p class="card-text">Gain valuable insights on job postings and applicant performance. Track applications, view analytics, and hire top tech talent faster.</p>
                </div>
            </div>
        </div>
    </div>
    <div class="container-fluid vh-100 d-flex align-items-center justify-content-center scroll-hidden">
        <h1>I appear smoothly!</h1>
    </div>
    <div class="container-fluid vh-100  d-flex align-items-center justify-content-center scroll-hidden">
        <h1>Me too!</h1>
    </div>
    <div class="container-fluid vh-100  d-flex align-items-center justify-content-center scroll-hidden">
        <h1>And me!</h1>
    </div>
    <script src='../includes/scroll-animation.js'></script>
</body>

</html>