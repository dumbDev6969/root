<?php
$current_page = basename(htmlspecialchars($_SERVER['PHP_SELF'])); //! Get the current page
//echo $current_page;
?>
<style>
         .navbar {
            position: sticky;
            top: 0;
            z-index: 99999;
        }
    </style>
    <nav class="navbar navbar-expand-lg bg-light p-3">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <div class="mx-auto">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                            <a class="nav-link <?= ($current_page == 'dashboard_tech_grad.php') ? 'active' : '' ?>" href="./dashboard_tech_grad.php">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link <?= ($current_page == 'job_search.php') ? 'active' : '' ?>" href="./job_search.php">Search jobs</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link <?= ($current_page == 'manage_profile.php') ? 'active' : '' ?>" href="./manage_profile.php">Manage profile</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link <?= ($current_page == 'saved_jobs.php') ? 'active' : '' ?>" href="./saved_jobs.php">Saved jobs</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </nav>