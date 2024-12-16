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
        .col-lg-3 {
            width: 15rem
        }
    </style>

</head>

<body>
    <?php include '../../../includes/navigation_users.php' ?>
    <div class="container scroll-hidden">
        <div class="row">
            <!-- First Form -->
            <div class="col-md-6">
                <form class="row g-3 mt-3">
                    <!-- First Name -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-first-name" class="form-control" id="first-name-input" placeholder="First name" required>
                            <label for="first-name-input">First Name</label>
                        </div>
                    </div>
                    <!-- Last Name -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-last-name" class="form-control" id="last-name-input" placeholder="Last name" required>
                            <label for="last-name-input">Last Name</label>
                        </div>
                    </div>
                    <!-- Phone Number -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="number" name="edit-phone" class="form-control" id="phone-number" placeholder="Phone #" min="0" required>
                            <label for="phone-number">Phone Number</label>
                        </div>
                    </div>
                    <!-- State/Region -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <select name="edit-state" class="form-control" id="state-input" required>
                                <option value="" disabled selected>Select Region</option>
                            </select>
                            <label for="state-input">Region</label>
                        </div>
                    </div>
                    <!-- City/Province -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <select name="edit-city-or-province" class="form-control" id="city-province-input" placeholder="City or Province" disabled>
                                <option value="">Select City/Province</option>
                            </select>
                            <label for="city-province-input">City or Province</label>
                        </div>
                    </div>
                    <!-- Municipality -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <select type="text" name="edit-municipality" class="form-control" id="municipality-input" placeholder="Municipality" disabled>
                            </select>
                            <label for="municipality-input">Municipality</label>
                        </div>
                    </div>
                    <!-- Zip Code -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-zip-code" class="form-control" id="zip-code-input" placeholder="Zip Code" required>
                            <label for="zip-code-input">Zip Code</label>
                        </div>
                    </div>
                    <!-- Street Number -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-street-number" class="form-control" id="street-number-input" placeholder="Street Number">
                            <label for="street-number-input">Street</label>
                        </div>
                    </div>
                    <!-- Email -->
                    <div class="col-md-12">
                        <div class="form-floating">
                            <input type="email" name="edit-email" class="form-control" id="email-input" placeholder="Email" required>
                            <label for="email-input">Email</label>
                        </div>
                    </div>
                    <!-- Password -->
                    <div class="col-md-12">
                        <div class="form-floating">
                            <input type="password" name="edit-password" class="form-control" id="password-input" placeholder="Create Password" min="8" max="16" required>
                            <label for="password-input">Create Password</label>
                        </div>
                    </div>
                    <!-- Confirm Password -->
                    <div class="col-md-12">
                        <div class="form-floating">
                            <input type="password" name="edit-confirm-password" class="form-control" id="confirm-password-input" placeholder="Confirm Password" min="8" max="16" required>
                            <label for="confirm-password-input">Confirm Password</label>
                        </div>
                    </div>
                    <!-- Terms -->
                    <div class="col-12">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="terms-check-1" required>
                            <label class="form-check-label" for="terms-check-1">
                                Agree to terms and conditions
                            </label>
                        </div>
                    </div>
                    <!-- Submit Button -->
                    <div class="col-12">
                        <button type="submit" class="btn btn-dark">Save changes</button>
                    </div>
                </form>
            </div>
            <!-- Second Form -->
            <div class="col-md-6">
                <form class="row g-3 mt-3">
                    <!-- Job Interest -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-job-interest" class="form-control" id="job-interest-input" placeholder="Job interest E.g Developer, Designer" required>
                            <label for="job-interest-input">Developer, Designer</label>
                        </div>
                    </div>
                    <!-- Employment Type -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <select name="edit-job-type" class="form-select" id="job-type-input" required>
                                <option value="">Select Employment Type</option>
                                <option value="Full-time">Full Time</option>
                                <option value="Part-time">Part Time</option>
                                <option value="Freelance">Freelance</option>
                                <option value="Internship">Internship</option>
                            </select>
                            <label for="job-type-input">Employment Type</label>
                        </div>
                    </div>
                    <!-- Preferred Location -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-preferred-location" class="form-control" id="preferred-location-input" placeholder="Preferred location" required>
                            <label for="preferred-location-input">Preferred location</label>
                        </div>
                    </div>
                    <!-- Expected Salary -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-expected-salary" class="form-control" id="expected-salary-input" placeholder="Expected salary" required>
                            <label for="expected-salary-input">Expected salary</label>
                        </div>
                    </div>
                    <!-- Terms -->
                    <div class="col-12">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="terms-check-2" required>
                            <label class="form-check-label" for="terms-check-2">
                                Agree to terms and conditions
                            </label>
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
</body>

</html>
