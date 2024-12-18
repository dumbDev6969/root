<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign up</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>

    <link rel="stylesheet" href="../assets/general.css">
    <link rel="stylesheet" href="../assets/links.css">
    <script src="../assets/js/geo.js"></script>
   
</head>



<body>
    <?php include '../includes/navigationV1.php' ?>
    <div class="container  p-5 scroll-hidden">
    <h4>Welcome job seeker!</h4>
        <form class="row g-3 mt-3">
        <div class="col-md-12">
              <div class="form-floating">
            <input type="hidden" class="form-control" id="hidden-region" name="selected-region">
            <input type="hidden" class="form-control" id="hidden-province" name="selected-province">
            <input type="hidden" class="form-control" id="hidden-municipality" name="selected-municipality">
        </div>
        </div>
      
           
            <!-- First Name -->
            <div class="col-md-6">
                <div class="form-floating">
                    <input type="text" name="first-name" class="form-control" id="first-name-input" placeholder="First name" required>
                    <label for="first-name-input">First Name</label>
                </div>
            </div>
            <!-- Last Name -->
            <div class="col-md-6">
                <div class="form-floating">
                    <input type="text" name="last-name" class="form-control" id="last-name-input" placeholder="Last name" required>
                    <label for="last-name-input">Last Name</label>
                </div>
            </div>
            <!-- Phone Number -->
            <div class="col-md-6">
                <div class="form-floating">
                    <input type="number" name="phone" class="form-control" id="phone-number" placeholder="Phone #" min="0" required>
                    <label for="phone-number">Phone Number</label>
                </div>
            </div>

            <div class="col-md-6">
                <div class="form-floating">
                    <select name="state" class="form-control" id="state-input" required>
                        <option value="" disabled selected>Select Region</option>
<!--                        <option value="Luzon">Luzon</option>-->
<!--                        <option value="Visayas">Visayas</option>-->
<!--                        <option value="Mindanao">Mindanao</option>-->
                    </select>
                    <label for="state-input">Region</label>
                </div>
            </div>

            <!-- City/Province -->
            <div class="col-md-6">
                <div class="form-floating">
                    <select  name="city-or-province" class="form-control" id="city-province-input" placeholder="City or Province" disabled>
                        <option value="" >Select City/Province</option>
                    </select>
                    <label for="city-province-input">City or Province</label>
                </div>
            </div>
            <div class="col-md-6">
                <div class="form-floating">
                    <select type="text" name="municipality" class="form-control" id="municipality-input" placeholder="Municipality" disabled>
                    </select>
                    <label for="municipality-input">Municipality</label>
                </div>
            </div>
            <!-- Zip Code -->
            <div class="col-md-6">
                <div class="form-floating">
                    <input type="text" name="zip-code" class="form-control" id="zip-code-input" placeholder="Zip Code" required>
                    <label for="zip-code-input">Zip Code</label>
                </div>
            </div>
            <!-- Street Number -->
            <div class="col-md-6">
                <div class="form-floating">
                    <input type="text" name="street-number" class="form-control" id="street-number-input" placeholder="Street Number">
                    <label for="street-number-input">Street</label>
                </div>
            </div>

            <!-- Email -->
            <div class="col-md-12">
                <div class="form-floating">
                    <input type="email" name="email" class="form-control" id="email-input" placeholder="Email" required>
                    <label for="email-input">Email</label>
                </div>
            </div>
            <!-- Password -->
            <div class="col-md-12">
                <div class="form-floating">
                    <input type="password" name="password" class="form-control" id="password-input" placeholder="Create Password" min="8" max="16" required>
                    <label for="password-input">Create Password</label>
                </div>
                <span id="error-message" class="text-danger"></span>
            </div>
            <!-- Confirm Password -->
            <div class="col-md-12">
                <div class="form-floating">
                    <input type="password" name="confirm-password" class="form-control" id="confirm-password-input" placeholder="Confirm Password" min="8" max="16" required>
                    <label for="confirm-password-input">Confirm Password</label>
                </div>
            </div>

            <div class="col-12">
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="terms-check" required>
                    <label class="form-check-label" for="terms-check">
                        Agree to terms and conditions
                    </label>
                </div>
            </div>
            <!-- Submit Button -->
            <div class="col-12">
                <button type="submit" class="btn btn-dark">Create Account</button>
            </div>
        </form>
    </div>
    <script src='../includes/scroll-animation.js'></script>
    <script src="../assets/js/geo.js"></script>
    <script src="../assets/js/jobseeker.js"></script>
</body>

</html>
