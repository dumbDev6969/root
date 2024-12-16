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
    <script src="../../../assets/js/dashboard_recruiter.js"></script>

    <link rel="stylesheet" href="../../../assets/scroll-animation.css">
    <script src='../../../includes/scroll-animation.js'></script>
    <style>
        .col-lg-3 {
            width: 15rem
        }
    </style>
</head>

<body>
    <?php include '../../../includes/navigation_recruiter.php' ?>
    <div class="container-fluid">
        <div class="container d-flex align-items-center justify-content-between scroll-hidden">
            <div class="row">
                <div class="col-md-12">
                    <div class="container d-flex align-items-center ">
                        <div class="border border-dark" style="height: 100px; width:100px; border-radius: 50%;" onclick="document.getElementById('profile-input').click()">
                            <input type="file" class="form-control border mb-4 d-none" id="profile-input">
                        </div>
                        <h4 id="company-name" class="mt-4 mb-3 me-3 ms-4">Company Name</h4>
                    </div>
                </div>
                <div class="col-md-12">
                    <div class="d-flex justify-content-between mt-3" style="width: 350px; line-height: 1.2;">
                        <div class="description">
                            <p>
                                <p id="industry-description" class="text-secondary mb-1">Tech Industry Job Experts</p>
                                <h5 id="career-building" class="fw-bold">Building Careers in Technology</h5>
                            </p>
                        </div>
                        <div>
                            <p>
                                <p class="text-secondary mb-1">Date Started</p>
                                <h5 id="date-started" class="fw-bold">dd/mm/yy</h5>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="edit">
                <a href="./edit_profile.php">
                    <button type="button" class="btn btn-small btn-secondary">Edit profile</button>
                </a>
                <button id="logout-button" type="button" class="btn btn-small btn-danger ms-2" onclick="remove()">Logout</button>
            </div>
        </div>
        <div class="row mt-3 scroll-hidden">
            <div class="col-4">
                <div id="simple-list-example" class="d-flex flex-column gap-2 simple-list-example-scrollspy text-center">
                    <a class="p-1 rounded" href="#simple-list-item-1">
                        <button type="button" class="btn btn-sm btn-secondary" style="width: 100px">Applicants</button>
                    </a>
                    <a class="p-1 rounded" href="#simple-list-item-2">
                        <button type="button" class="btn btn-sm btn-secondary" style="width: 100px">Jobs</button>
                    </a>
                </div>
            </div>
            <div class="col-8">
                <div data-bs-spy="scroll" data-bs-target="#simple-list-example" data-bs-offset="0" data-bs-smooth-scroll="true" class="scrollspy-example " tabindex="0" style="height: 91vh; overflow: auto">
                    <h4 id="simple-list-item-1" class="mt-4 mb-3">Applicants</h4>
                    <div class="row gap-2">
                        <div class="col-lg-3 col-md-12">
                            <div class="card" style="width: 15rem;">
                                <div class="card-body">
                                    <div class="card-title d-flex align-items-center flex-column">
                                        <!-- img -->
                                        <div class="profile border" style="height: 170px; width:170px; border-radius: 50%">

                                        </div>
                                    </div>
                                    <h5 class="mt-3">Johua Cabuang</h5>
                                    <h6 class="card-subtitle mb-3 text-body-secondary">Job Title Applied</h6>
                                    <p class="card-text">
                                        <span class="text-secondary">Applied at</span> <br>
                                        dd/mm/yyyy
                                    </p>
                                    <a href="#" class="card-link">Card link</a>
                                    <a href="#" class="card-link">Another link</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-3 col-md-12">
                            <div class="card" style="width: 15rem;">
                                <div class="card-body">
                                    <div class="card-title d-flex align-items-center flex-column">
                                        <!-- img -->
                                        <div class="profile border" style="height: 170px; width:170px; border-radius: 50%">

                                        </div>
                                    </div>
                                    <h5>Johua Cabuang</h5>
                                    <h6 class="card-subtitle mb-2 text-body-secondary">Job title applied</h6>
                                    <p class="card-text">
                                        <span class="text-secondary">Applied at</span> <br>
                                        dd/mm/yyyy
                                    </p>
                                    <a href="#" class="card-link">Card link</a>
                                    <a href="#" class="card-link">Another link</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <h4 id="simple-list-item-2" class="mt-5 mb-3">Jobs</h4>
                    <div class="row gap-3" id="job-container">
                        <div class="col-lg-3 col-md-12 ">
                            <div class="card" style="width: 15.5rem;">
                                <div class="card-body">
                                    <div class="d-flex  justify-content-between align-items-center">
                                        <div>
                                            <h5 class="card-title fw-bold">Jr. Software Dev</h5>

                                        </div>
                                        <div class="company-profile border" style="height: 50px; width: 50px; border-radius: 50px">
                                            img
                                        </div>
                                    </div>
                                    <h6 class="card-subtitle mb-2 text-body-secondary">Company name</h6>
                                    <p class="text-secondary">Pangasinan SCCP</p>
                                    <p class="card-text">
                                        <button type="button" disabled class="btn btn-outline-secondary btn-sm">Part time</button>
                                        <h6 class="fw-bold mt-2">$100 - $120</h6>
                                    </p>
                                    <form action="#">
                                        <div class="row">
                                            <div class="col-md-8 p-1">
                                                <button type="button" class="btn btn-sm btn-dark w-100">More details</button>
                                            </div>
                                            <div class="col-md-4 p-1">
                                                <button type="button" class="btn btn-sm btn-secondary w-100">Save</button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-3 col-md-12">
                            <div class="card" style="width: 15.5rem;">
                                <div class="card-body">
                                    <div class="d-flex  justify-content-between align-items-center">
                                        <div>
                                            <h5 class="card-title">Jr. Sofware dev</h5>

                                        </div>
                                        <div class="company-profile border" style="height: 50px; width: 50px; border-radius: 50px">
                                            img
                                        </div>
                                    </div>
                                    <h6 class="card-subtitle mb-2 text-body-secondary">Company name</h6>
                                    <p class="text-secondary">Pangasinan SCCP</p>
                                    <p class="card-text">
                                        <button type="button" disabled class="btn btn-outline-secondary btn-sm">Part time</button>
                                        <h6>$100 - $120</h6>
                                    </p>
                                    <form action="#">
                                        <div class="row">
                                            <div class="col-md-8 p-1">
                                                <button type="button" class="btn btn-sm btn-dark w-100">More details</button>
                                            </div>
                                            <div class="col-md-4 p-1">
                                                <button type="button" class="btn btn-sm btn-secondary w-100">Save</button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-3 col-md-12">

                        </div>
                    </div>

                </div>
            </div>
        </div>

    </div>

    <script>

        function remove(){
            localStorage.removeItem("employerData")
            window.location.href = "../../../src/auth/login.php";
        }
    </script>
</body>
</html>
