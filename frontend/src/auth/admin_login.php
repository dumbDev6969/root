<?php
// Prevent any output before headers
ini_set('display_errors', 0);
error_reporting(0);

// Start session
session_start();

// Check if admin is already logged in
if (isset($_SESSION['isLoggedIn']) && $_SESSION['isLoggedIn'] === true && $_SESSION['userType'] === 'admin') {
    header('Location: ../dashboard/admin/dashboard_admin.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login</title>
    <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&amp;display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="../../assets/links.css">
    <script src="../../assets/js/admin_login.js" defer></script>
    <style>
        .input-group {
            display: flex;
            align-items: center;
            background-color: #f0f2f5;
            border-radius: 10px;
            padding: 12px;
            width: 100%;
            max-width: 400px;
            margin-bottom: 15px;
        }
        .input-group i {
            color: #aaadb1;
            margin-right: 10px;
        }
        .input-group input {
            border: none;
            background: none;
            outline: none;
            flex-grow: 1;
            color: #6b717c;
        }
        .input-group .toggle-password {
            color: #b0b3b8;
            cursor: pointer;
        }
        .button {
            display: flex;
            align-items: center;
            border-radius: 10px;
            width: 100%;
            max-width: 400px;
            margin-bottom: 15px;
        }
        .btn-dark {
            height: 50px
        }
    </style>
</head>
<body>
    <div class="container vh-100 d-flex align-items-center justify-content-center">
        <div class="container p-4" style="min-width: 250px; width: 500px">
            <div class="row d-flex align-items-center justify-content-center">
                <div class="col-md-12 text-center w-25 d-flex align-items-center">
                    <i class="bi bi-shield-lock" style="font-size:5em;"></i>
                </div>
                <div class="col-md-12 text-center mt-2">
                    <h4>Admin Login</h4>
                    <p>Please enter your admin credentials to continue.</p>
                </div>
                <div class="col-md-12">
                    <form class="d-flex align-items-center justify-content-center flex-column" method="POST">
                        <div class="input-group">
                            <i class="bi bi-person"></i>
                            <input type="text" name="username" id="username" placeholder="Username" required>
                        </div>

                        <div class="input-group password-input">
                            <i class="bi bi-person-lock"></i>
                            <input type="password" name="password" id="password" placeholder="Password" required>
                            <i class="bi bi-eye toggle-password"></i>
                        </div>

                        <div class="button">
                            <button type="submit" class="btn btn-dark w-100">Login as Admin</button>
                        </div>
                        <div class="button">
                            <a href="login.php" class="btn btn-outline-dark w-100">Back to User Login</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            document.querySelector('.toggle-password').addEventListener('click', function () {
                const passwordInput = document.querySelector('.password-input input');
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);
                this.classList.toggle('bi-eye');
                this.classList.toggle('bi-eye-slash');
            });
        });
    </script>
</body>
</html>