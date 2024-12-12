<?php //echo $_SERVER['PHP_SELF']?>
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
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&amp;display=swap" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="../assets/general.css">
    <link href="../assets/links.css" rel="stylesheet" />
    <style>
        #navbar-example2 {
            position: sticky;
            top: 0;
            z-index: 999;
        }
    </style>
</head>

<body>
    <?php include '../includes/navigationV1.php' ?>
    <nav id="navbar-example2" class="navbar  px-3 mb-3 team-navigation bg-light">
        <ul class="nav nav-pills">
            <li class="nav-item">
                <a class="nav-link" href="#scrollspyHeading1">Designer</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#scrollspyHeading2">Backend</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#scrollspyHeading3">Docs</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#scrollspyHeading4">Frontend</a>
            </li>
        </ul>
    </nav>
    <div data-bs-spy="scroll" data-bs-target="#navbar-example2" data-bs-root-margin="0px 0px -40%" data-bs-smooth-scroll="true" class="scrollspy-example  p-3 rounded-2" tabindex="0">
        <h4 id="scrollspyHeading1">First heading</h4>
        <div class="card text-bg-dark">
            <img src="https://tse4.mm.bing.net/th?id=OIP.f0XXmgpwVqRYWFpzB-DpkQHaE8&pid=Api&P=0&h=220" class="card-img" alt="...">
            <div class="card-img-overlay">
                <h5 class="card-title">Card title</h5>
                <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                <p class="card-text"><small>Last updated 3 mins ago</small></p>
            </div>
        </div>
        <h4 id="scrollspyHeading2">Second heading</h4>
        <div class="card text-bg-dark">
            <img src="https://tse4.mm.bing.net/th?id=OIP.f0XXmgpwVqRYWFpzB-DpkQHaE8&pid=Api&P=0&h=220" class="card-img" alt="...">
            <div class="card-img-overlay">
                <h5 class="card-title">Card title</h5>
                <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                <p class="card-text"><small>Last updated 3 mins ago</small></p>
            </div>
        </div>
        <h4 id="scrollspyHeading3">Third heading</h4>
        <div class="card text-bg-dark">
            <img src="https://tse4.mm.bing.net/th?id=OIP.f0XXmgpwVqRYWFpzB-DpkQHaE8&pid=Api&P=0&h=220" class="card-img" alt="...">
            <div class="card-img-overlay">
                <h5 class="card-title">Card title</h5>
                <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                <p class="card-text"><small>Last updated 3 mins ago</small></p>
            </div>
        </div>
        <h4 id="scrollspyHeading4">Fourth heading</h4>
        <div class="card text-bg-dark">
            <img src="https://tse4.mm.bing.net/th?id=OIP.f0XXmgpwVqRYWFpzB-DpkQHaE8&pid=Api&P=0&h=220" class="card-img" alt="...">
            <div class="card-img-overlay">
                <h5 class="card-title">Card title</h5>
                <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                <p class="card-text"><small>Last updated 3 mins ago</small></p>
            </div>
        </div>
    </div>

    <script src="../includes/scroll-animation.js"></script>
    
</body>

</html>