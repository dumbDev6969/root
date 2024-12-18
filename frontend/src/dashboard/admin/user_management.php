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
</head>

<body>
    <?php include '../../../includes/navigation_admin.php' ?>
    <div class="container mt-5 d-flex align-items-center justify-content-center scroll-hidden">
        <div class="col-md-9 " style="height: 90vh; overflow: auto">
            <div class="row gap-2">
                <div class="col-md-12">
                    <form action="#">
                        <div class="row g-1  p-1">
                            <div class="col-md-9">
                                <input type="search" class="form-control" name="job" id="job-search" placeholder="E.g Web developer">
                            </div>
                            <div class="col-md-3">
                                <button type="submit" class="btn btn-dark"><i class="bi bi-search"></i></button>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="col-md-12 ">
                    <div class="row gap-2">
                        <div class="col-md-3 " style="width: 15.5rem;">
                        <div class="card" style="width: 15rem;">
                                <div class="card-body">
                                    <div class="card-title d-flex align-items-center flex-column">
                                        <!-- img -->
                                        <div class="profile border" style="height: 170px; width:170px; border-radius: 50%">

                                        </div>
                                    </div>
                                    <h5 class="mt-3">Johua Cabuang</h5>
                                    <h6 class="card-subtitle mb-3 text-body-secondary">Job Interest</h6>
                                    <p class="card-text">
                                        <span class="text-secondary">Started at</span> <br>
                                        dd/mm/yyyy
                                    </p>
                                    <div class="row g-1">
                                        <div class="col-md-6">
                                            <button type="submit" class="btn btn-sm btn-dark w-100">Delete</button>
                                        </div>
                                        <div class="col-md-6">
                                            <button type="submit" class="btn btn-sm btn-secondary w-100">Deactivate</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                       
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>

</html>