<?php
$current_page = basename(htmlspecialchars($_SERVER['PHP_SELF'])); //! Get the current page
?>

    <nav class="navbar navbar-expand-lg">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Logo</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <div class="mx-auto">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <a class="nav-link <?= ($current_page == 'index.php') ? 'active' : '' ?>" href="./index.php">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link <?= ($current_page == 'about.php') ? 'active' : '' ?>" href="./about.php">About us</a>
                        </li>
                    </ul>
                </div>
                <div class="d-flex" role="search">
                    <a href="../src/role_selection.php">
                        <button class="btn btn-signup text-light me-2">Sign up</button>
                    </a>
                    <a href="">
                        <button class="btn btn-login btn-outline-dark">Login</button>
                    </a>
                </div>
            </div>
        </div>
    </nav>

