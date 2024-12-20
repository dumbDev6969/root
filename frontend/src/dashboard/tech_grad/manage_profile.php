<?php
// Prevent any output before headers
ini_set('display_errors', 0);
error_reporting(0);

// Start session
session_start();

// Check if user is logged in and is a tech grad user
if (!isset($_SESSION['isLoggedIn']) || !$_SESSION['isLoggedIn'] || $_SESSION['userType'] !== 'user') {
    header('Location: ../../auth/login.php');
    exit;
}

// Get user data
$userData = $_SESSION['userData'];
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manage Profile</title>
    <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <link href="../../../assets/links.css" rel="stylesheet" />
    <link rel="stylesheet" href="../../../assets/scroll-animation.css">
    <script src='../../../includes/scroll-animation.js'></script>
    <script src="../../../assets/js/geo.js"></script>
    <script src="../../../assets/js/profile_update.js"></script>
    <style>
        .col-lg-3 {
            width: 15rem
        }
    </style>
</head>

<body>
    <?php include '../../../includes/navigation_users.php' ?>
    <div class="container scroll-hidden">
        <div class="row">
            <!-- First Form - Personal Information -->
            <div class="col-md-6">
                <form class="row g-3 mt-3" id="personal-info-form">
                    <p class="text-muted">Note: Leave fields blank if you do not wish to update them.</p>
                    <!-- First Name -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-first-name" class="form-control" id="first-name-input" placeholder="First name" value="<?php echo htmlspecialchars($userData['first_name']); ?>">
                            <label for="first-name-input">First Name</label>
                        </div>
                    </div>
                    <!-- Last Name -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-last-name" class="form-control" id="last-name-input" placeholder="Last name" value="<?php echo htmlspecialchars($userData['last_name']); ?>">
                            <label for="last-name-input">Last Name</label>
                        </div>
                    </div>
                    <!-- Phone Number -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="number" name="edit-phone" class="form-control" id="phone-number" placeholder="Phone #" min="0" value="<?php echo htmlspecialchars($userData['phone_number']); ?>">
                            <label for="phone-number">Phone Number</label>
                        </div>
                    </div>
                    <!-- State/Region -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <select name="edit-state" class="form-control" id="state-input">
                                <option value="">Select Region</option>
                            </select>
                            <label for="state-input">Region</label>
                        </div>
                    </div>
                    <!-- City/Province -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <select name="edit-city-or-province" class="form-control" id="city-province-input" disabled>
                                <option value="">Select City/Province</option>
                            </select>
                            <label for="city-province-input">City or Province</label>
                        </div>
                    </div>
                    <!-- Municipality -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <select name="edit-municipality" class="form-control" id="municipality-input" disabled>
                                <option value="">Select Municipality</option>
                            </select>
                            <label for="municipality-input">Municipality</label>
                        </div>
                    </div>
                    <!-- Zip Code -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-zip-code" class="form-control" id="zip-code-input" placeholder="Zip Code" value="<?php echo htmlspecialchars($userData['zip_code']); ?>">
                            <label for="zip-code-input">Zip Code</label>
                        </div>
                    </div>
                    <!-- Street Number -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-street-number" class="form-control" id="street-number-input" placeholder="Street Number" value="<?php echo htmlspecialchars($userData['street']); ?>">
                            <label for="street-number-input">Street</label>
                        </div>
                    </div>
                    <!-- Email -->
                    <div class="col-md-12">
                        <div class="form-floating">
                            <input type="email" name="edit-email" class="form-control" id="email-input" placeholder="Email" value="<?php echo htmlspecialchars($userData['email']); ?>">
                            <label for="email-input">Email</label>
                        </div>
                    </div>
                    <!-- Password -->
                    <div class="col-md-12">
                        <div class="form-floating">
                            <input type="password" name="edit-password" class="form-control" id="password-input" placeholder="Create Password" minlength="8" maxlength="16">
                            <label for="password-input">New Password (optional)</label>
                        </div>
                    </div>
                    <!-- Confirm Password -->
                    <div class="col-md-12">
                        <div class="form-floating">
                            <input type="password" name="edit-confirm-password" class="form-control" id="confirm-password-input" placeholder="Confirm Password" minlength="8" maxlength="16">
                            <label for="confirm-password-input">Confirm New Password</label>
                        </div>
                    </div>
                    <!-- Submit Button -->
                    <div class="col-12">
                        <button type="submit" class="btn btn-dark">Save changes</button>
                    </div>
                </form>
            </div>
            <!-- Second Form - Job Preferences -->
            <div class="col-md-6">
                <form class="row g-3 mt-3" id="job-preferences-form">
                    <!-- Job Interest -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-job-interest" class="form-control" id="job-interest-input" placeholder="Job interest E.g Developer, Designer" value="<?php echo htmlspecialchars($userData['job_interest'] ?? ''); ?>">
                            <label for="job-interest-input">Developer, Designer</label>
                        </div>
                    </div>
                    <!-- Employment Type -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <select name="edit-job-type" class="form-select" id="job-type-input">
                                <option value="">Select Employment Type</option>
                                <option value="Full-time" <?php echo ($userData['job_type'] ?? '') === 'Full-time' ? 'selected' : ''; ?>>Full Time</option>
                                <option value="Part-time" <?php echo ($userData['job_type'] ?? '') === 'Part-time' ? 'selected' : ''; ?>>Part Time</option>
                                <option value="Freelance" <?php echo ($userData['job_type'] ?? '') === 'Freelance' ? 'selected' : ''; ?>>Freelance</option>
                                <option value="Internship" <?php echo ($userData['job_type'] ?? '') === 'Internship' ? 'selected' : ''; ?>>Internship</option>
                            </select>
                            <label for="job-type-input">Employment Type</label>
                        </div>
                    </div>
                    <!-- Preferred Location -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-preferred-location" class="form-control" id="preferred-location-input" placeholder="Preferred location" value="<?php echo htmlspecialchars($userData['preferred_location'] ?? ''); ?>">
                            <label for="preferred-location-input">Preferred location</label>
                        </div>
                    </div>
                    <!-- Expected Salary -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-expected-salary" class="form-control" id="expected-salary-input" placeholder="Expected salary" value="<?php echo htmlspecialchars($userData['salary_range'] ?? ''); ?>">
                            <label for="expected-salary-input">Expected salary</label>
                        </div>
                    </div>
                    <!-- Submit Button -->
                    <div class="col-12">
                        <button type="submit" class="btn btn-dark">Save changes</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script>
        // Pass PHP session data to JavaScript
        const userData = <?php echo json_encode($userData); ?>;
        
        // Initialize geo dropdowns when document is ready
        document.addEventListener('DOMContentLoaded', function() {
            initializeGeoDropdowns();
        });
    </script>
</body>
</html>
