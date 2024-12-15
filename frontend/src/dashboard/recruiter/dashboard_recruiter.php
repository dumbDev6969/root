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
</head>

<body>
    <?php include '../../../includes/navigation_recruiter.php' ?>
    <div class="container-fluid">
        <div class="container d-flex align-items-center justify-content-between">
            <div class="row">
                <div class="col-md-12">
                    <div class="container d-flex align-items-center ">
                        <input type="file" class="form-control border" style="height: 100px; width:100px; border-radius: 50%;">
                        <h4>Company name</h4>
                    </div>
                </div>
                <div class="col-md-12">
                    <div class="d-flex  justify-content-between" style="width: 350px; line-height: 0px">
                        <div class="">
                            <p>
                                <p class="text-secondary">Tech Industry Job Experts</p>
                                <h5>Building Careers in Technology</h5>
                            </p>
                        </div>
                        <div >
                            <p>
                                <p class="text-secondary">Date started</p>
                                <h5>dd/mm/yy</h5>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="edit">
                <a href="./edit_profile.php">
                    <button type="button"  class="btn btn-small btn-secondary">Edit profile</button>
                </a>
            </div>
        </div>
        <div class="row mt-3">
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
                    <h4 id="simple-list-item-1">Applicants</h4>
                    <div class="row gap-2">
                        <div class="col-lg-3 col-md-12">
                            <div class="card" style="width: 15rem;">
                                <div class="card-body">
                                    <h5 class="card-title">Card title</h5>
                                    <h6 class="card-subtitle mb-2 text-body-secondary">Card subtitle</h6>
                                    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                                    <a href="#" class="card-link">Card link</a>
                                    <a href="#" class="card-link">Another link</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-3 col-md-12">
                            <div class="card" style="width: 15rem;">
                                <div class="card-body">
                                    <h5 class="card-title">Card title</h5>
                                    <h6 class="card-subtitle mb-2 text-body-secondary">Card subtitle</h6>
                                    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                                    <a href="#" class="card-link">Card link</a>
                                    <a href="#" class="card-link">Another link</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-3 col-md-12">
                            <div class="card" style="width: 15rem;">
                                <div class="card-body">
                                    <h5 class="card-title">Card title</h5>
                                    <h6 class="card-subtitle mb-2 text-body-secondary">Card subtitle</h6>
                                    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                                    <a href="#" class="card-link">Card link</a>
                                    <a href="#" class="card-link">Another link</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-3 col-md-12">
                            <div class="card" style="width: 15rem;">
                                <div class="card-body">
                                    <h5 class="card-title">Card title</h5>
                                    <h6 class="card-subtitle mb-2 text-body-secondary">Card subtitle</h6>
                                    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                                    <a href="#" class="card-link">Card link</a>
                                    <a href="#" class="card-link">Another link</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-3 col-md-12">
                            <div class="card" style="width: 15rem;">
                                <div class="card-body">
                                    <h5 class="card-title">Card title</h5>
                                    <h6 class="card-subtitle mb-2 text-body-secondary">Card subtitle</h6>
                                    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                                    <a href="#" class="card-link">Card link</a>
                                    <a href="#" class="card-link">Another link</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <h4 id="simple-list-item-2">Jobs</h4>
                    
                    
                </div>
            </div>
        </div>

    </div>
</body>

</html>