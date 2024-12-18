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
    <style>
        a{
            text-decoration: none;
        }
    </style>
</head>

<body>
    <?php include '../../../includes/navigation_users.php' ?>
    <div class="container-fluid scroll-hidden">
        <div class="row mt-2">
            <!-- filters -->
            <div class="col-md-3">
                <h4>Employment type</h4>
                <hr>
                <div class="container">
                    <form action="#">
                        <div class="form-check mt-3">
                            <input class="form-check-input" type="checkbox" value="Full-time" id="full-time">
                            <label class="form-check-label text-secondary" for="defaultCheck1">Full time</label>
                        </div>
                        <div class="form-check mt-3">
                            <input class="form-check-input" type="checkbox" value="Part-time" id="part-time">
                            <label class="form-check-label text-secondary" for="defaultCheck2">Part time</label>
                        </div>
                        <div class="form-check mt-3">
                            <input class="form-check-input" type="checkbox" value="Freelance" id="freelance">
                            <label class="form-check-label text-secondary" for="defaultCheck1">Freelance</label>
                        </div>
                        <div class="form-check mt-3">
                            <input class="form-check-input" type="checkbox" value="Internship" id="Intership">
                            <label class="form-check-label text-secondary" for="defaultCheck2">Internship</label>
                        </div>

                        <hr>
                        <h4>Expected salary</h4>
                        <hr>
                        <div class="mt-2">
                            <input type="searh" class="form-control" placeholder="Salary" name="salary" id="salary-input">
                            <div class="mt-2">
                                <button type="submit" class="btn btn-sm btn-dark w-100">Save</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <!-- jobs -->
            <div class="col-md-9 " style="height: 90vh; overflow: auto">
                <div class="row gap-2">
                    <div class="col-md-12">
                        <form action="#">
                            <div class="row">
                               <div class="col-md-7">
                                    <input type="search" class="form-control" name="job" id="job-search" placeholder="E.g Web developer">
                                </div>
                                <div class="col-md-3">
                                <input type="search" class="form-control" name="company" id="company-search" placeholder="E.g Tech solutions">
                                </div>
                                <div class="col-md-2">
                                <button type="submit" class="btn btn-dark"><i class="bi bi-search"></i></button>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="col-md-12 ">
                        <div class="row gap-2">
                        <a href="./job_single_view.php" style="width: 15.5rem;">
                            <div class="col-md-3 " style="width: 15.5rem;">
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
                            </a>
                            
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>

</html>