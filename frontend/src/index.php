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
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <link href="../assets/general.css" rel="stylesheet" />
    <link href="../assets/links.css" rel="stylesheet" />
    <style>
    
    </style>
</head>

<body>
<?php include '../includes/navigationV1.php' ?>
    <div class="container-fluid  mt-5 d-flex flex-column align-items-center scroll-hidden" role="main" 
        <div class="container mt-3 d-flex flex-column align-items-center">
            <h2 class="text-center">
                Empowering tech graduates to connect with top employers.
            </h2>
            <p class="text-center">
                Explore thousands of job opportunities and take the next step in your tech career.
            </p>
            <a class="text-light mt-5" href="role_selection.php">
                <button class="btn btn-lg " aria-label="Get started today—it's free!">
                    Get started today—it's free!
                </button>
            </a>
        </div>

        <div class="row d-flex justify-content-evenly mt-5 p-5 align-items-center flex-wrap scroll-hidden " aria-label="Features">
            <div class="col-md-4 d-flex align-items-center justify-content-center flex-column ">
                <i class="fas fa-file-alt" style="font-size: 64px" aria-hidden="true"></i>
                <h3>Personalized Job Matches</h3>
                <p class="text-center">Get job recommendations tailored to your skills and preferences.</p>
            </div>
            <div class="col-md-4 d-flex align-items-center justify-content-center flex-column ">
                <i class="fas fa-search" style="font-size: 64px" aria-hidden="true"></i>
                <h3>Hassle-free Job Search</h3>
                <p class="text-center">Apply to jobs with just one click. Upload your resume, fill out your profile, and let the platform do the rest.</p>
            </div>
            <div class="col-md-4 d-flex align-items-center justify-content-center flex-column">
                <i class="fas fa-file-alt" style="font-size: 64px" aria-hidden="true"></i>
                <h3>Employer Insights</h3>
                <p class="text-center">Gain valuable insights on job postings and applicant performance.</p>
            </div>
        </div>
    </div>
    <div class="container mt-5 p-5  d-flex flex-column align-items-center scroll-hidden" role="complementary">
        <h1>Latest trends!</h1>
        <marquee behavior="scroll" direction="left" style="height: 400px;" aria-label="Latest trends">
            <div class="row d-flex align-items-center justify-content-evenly">
                <?php echo $store_data; ?>
            </div>
        </marquee>
    </div>
    <div class="container-fluid vh-100 d-flex align-items-center justify-content-center scroll-hidden" style="padding: 40px; background-color: #f3f4f6; border-radius: 10px; text-align: center;" role="contentinfo">
        <div>
            <h1>And me!</h1>
            <p style="font-size: 1.2rem; color: #555;">Discover exclusive career resources and advice tailored to help you stand out in the tech industry.</p>
            <button class="btn btn-lg btn-primary" style="margin-top: 20px;" aria-label="Learn More">Learn More</button>
        </div>
    </div>
    <?php include '../includes/footer.php'?>
    <script src="../includes/scroll-animation.js"></script>
</body>

</html>
