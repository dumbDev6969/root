<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>What's your interests?</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>

    <link rel="stylesheet" href="../assets/general.css">
    <link rel="stylesheet" href="../assets/links.css">
    <script src="../assets/js/geo.js"></script>
</head>



<body>
    <?php include '../includes/navigationV1.php' ?>
    <div class="container mt-5 p-5 scroll-hidden">
        <h4>What's you interests?</h4>
        <form class="row g-3 mt-3">

            <div class="col-md-6">
                <div class="form-floating">
                    <input type="text" name="job-interest" class="form-control" id="job-interest-input" placeholder="Job interest E.g Developer, Designer" required>
                    <label for="job-interest-input">Developer, Designer</label>
                </div>
            </div>

            <div class="col-md-6">
                <div class="form-floating">
                    <select name="job-type" class="form-select" id="job-type-input" required>
                        <option value="">Select Employment Type</option>
                        <option value="Full-time">Full Time</option>
                        <option value="Part-time">Part Time</option>
                        <option value="Freelance">Freelance</option>
                        <option value="Internship">Internship</option>
                    </select>
                    <label for="employment-type-input">Employment Type</label>
                </div>
            </div>

            <div class="col-md-6">
                <div class="form-floating">
                    <input type="text" name="prefered-location" class="form-control" id="prefered-location-input" placeholder="Prefered location" required>
                    <label for="prefered-location-input">Prefered location</label>
                </div>
            </div>

            <div class="col-md-6">
                <div class="form-floating">
                    <input type="text" name="excpected-salary" class="form-control" id="excpected-salary-input" placeholder="Expected salary" required>
                    <label for="excpected-salary-input">Expected salary</label>
                </div>
            </div>

            <div class="col-12">
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="terms-check" required>
                    <label class="form-check-label" for="terms-check">
                        Agree to terms and conditions
                    </label>
                </div>
            </div>

            <div class="col-12">
                <button type="submit" class="btn btn-dark">Create Account</button>
            </div>
        </form>
    </div>
    <script src='../includes/scroll-animation.js'></script>
    <script src="../assets/js/jobseeker.js"></script>
</body>

</html>