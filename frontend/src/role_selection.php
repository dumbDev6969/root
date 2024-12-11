<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Select Your Role</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>

    <link rel="stylesheet" href="../assets/general.css">
    <link rel="stylesheet" href="../assets/links.css">
</head>

<body>
    <?php include '../includes/navigationV1.php' ?>
    <div class="container vh-100 d-flex flex-column align-items-center justify-content-center scroll-hidden">
        <h1 class="mb-4">What’s Your Role?</h1>
        <p class="text-center mb-5">Choose your role to get started with the platform.</p>
        <div class="d-flex gap-3 scroll-hidden">
            <a href="signup_tech_grad.php" class="btn btn-grad btn-lg">I’m a Tech Graduate</a>
            <a href="signup_recruiter.php" class="btn btn-recruite btn-lg">I’m a Recruiter</a>
        </div>
    </div>
    <script src='../includes/scroll-animation.js'></script>
</body>

</html>
