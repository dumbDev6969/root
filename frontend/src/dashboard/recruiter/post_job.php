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
    <script src="../../../assets/js/remove-tokens.js"></script>
    <script src="../../../assets/js/post_job.js"></script>

    <link rel="stylesheet" href="../../../assets/scroll-animation.css">
    <script src='../../../includes/scroll-animation.js'></script>
</head>

<body>
    <?php include '../../../includes/navigation_recruiter.php' ?>
    <div class="container p-5 mt-5 scroll-hidden">
        <form id="postJobForm" action="submit_job.php" method="POST">
            <div class="container">
                <div class="row">
                    <!-- Job Title -->
                    <div class="col-md-8 mb-3">
                        <div class="form-floating">
                            <input type="text" class="form-control" id="job-title" name="job_title" placeholder="Job Title" required>
                            <label for="job-title">Job Title</label>
                        </div>
                    </div>

                    <!-- Job Type -->
                    <div class="col-md-4 mb-3">
                        <div class="form-floating">
                            <select class="form-select" id="job-type" name="job_type" required>
                                <option value="Full-time">Full-time</option>
                                <option value="Part-time">Part-time</option>
                                <option value="Freelance">Freelance</option>
                                <option value="Internship">Internship</option>
                            </select>
                            <label for="job-type">Job Type</label>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <!-- Location -->
                    <div class="col-md-6 mb-3">
                        <div class="form-floating">
                            <input type="text" class="form-control" id="location" name="location" placeholder="Location" required>
                            <label for="location">Location</label>
                        </div>
                    </div>

                    <!-- Salary Range -->
                    <div class="col-md-6 mb-3">
                        <div class="form-floating">
                            <input type="text" class="form-control" id="salary-range" name="salary_range" required>
                            <label for="salary-range"> Salary range E.g 500 - 1000</label>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <!-- Job Description -->
                    <div class="col-md-12 mb-3">
                        <div class="form-floating">
                            <textarea class="form-control" id="job-description" name="job_description" placeholder="Job Description" style="height: 100px" required></textarea>
                            <label for="job-description">Job Description</label>
                        </div>
                    </div>

                    <!-- Requirements -->
                    <div class="col-md-12 mb-3">
                        <div class="form-floating">
                            <textarea class="form-control" id="requirements" name="requirements" placeholder="Requirements" style="height: 100px" required></textarea>
                            <label for="requirements">Requirements</label>
                        </div>
                    </div>
                </div>

                <!-- Submit Button -->
                <div class="row">
                    <div class="col-md-12">
                        <button type="button" class="btn btn-dark w-100" style="height: 60px" onclick="postJob()">Post</button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</body>
</html>
