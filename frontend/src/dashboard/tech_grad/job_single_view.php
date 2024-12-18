<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
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
    <!-- <script>
        document.addEventListener('DOMContentLoaded', function () {
            const employerData = JSON.parse(localStorage.getItem('employerData'));
            if (employerData) {
                document.getElementById('company-name').textContent = employerData.company_name || 'Company Name';
                document.getElementById('industry-description').textContent = 'Tech Industry Job Experts';
                document.getElementById('career-building').textContent = 'Building Careers in Technology';
                document.getElementById('date-started').textContent = new Date(employerData.created_at).toLocaleDateString();
            }
        });
    </script> -->
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
    <div class="container  mt-5 p-5 d-flex align-items-center justify-content-center">
        <div class="card w-50 shadow-lg scroll-hidden">
            <h5 class="card-header bg-secondary text-white">Company Name</h5>
            <div class="card-body">
                <h5 class="card-title">Job Name</h5>
                <button class="btn btn-sm btn-outline-secondary mb-3" disabled>Job Type (Full-time)</button>
                <p class="card-text">
                    <i class="bi bi-geo-alt"></i>
                    Location
                </p>
                <p class="card-text">Job Description: Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit at inventore, aliquam vero doloremque unde minus. Eius atque dignissimos harum.</p>
                <h5 class="card-text text-success">Salary: 500 - 1000</h5>
                <p class="card-text">
                    <strong>Requirements:</strong>
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quos, laboriosam.
                </p>
                <form action="#">
                    <div class="row">
                        <div class="col-md-12">
                        <button type="button" class="btn btn-lg btn-dark w-100" data-bs-toggle="modal" data-bs-target="#applyModal">Apply Now!</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
<!--  -->
    <div class="modal fade" id="applyModal" tabindex="-1" aria-labelledby="applyModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="applyModalLabel">Submit Your Resume</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="resumeForm">
                        <div class="mb-3">
                            <label for="resume" class="form-label">Upload Resume</label>
                            <input type="file" class="form-control" id="resume" required>
                        </div>
                        <div class="mb-3">
                            <label for="message" class="form-label">Message (Optional)</label>
                            <textarea class="form-control" id="message" rows="3"></textarea>
                        </div>
                        <button type="submit" class="btn btn-dark w-100">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </div>


</html>