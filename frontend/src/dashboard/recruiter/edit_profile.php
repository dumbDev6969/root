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
    <div class="container p-5 scroll-hidden">
        <h4>Change profile</h4>
        <form class="row g-3 mt-3">


            <div class="col-md-12">
                <div class="form-floating">
                    <input type="text" name="company_name" class="form-control" id="company-name-input" placeholder="Company name" maxlength="30">
                    <label for="company-name-input" class="form-label">Company Name</label>
                </div>
            </div>

            <div class="col-md-12">
                <div class="form-floating">
                    <input type="number" name="phone_number" class="form-control" id="phone-number" placeholder="Phone #" min="0" max="999999999999">
                    <label for="phone-number" class="form-label">Phone Number</label>
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
            <input type="hidden" name="municipality" id="municipality-input">

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
                    <input type="text" name="zip_code" class="form-control" id="zip-code-input" placeholder="ZIP Code" maxlength="10">
                    <label for="zip-code-input" class="form-label">ZIP Code</label>
                </div>
            </div>

            <div class="col-md-6">
                <div class="form-floating">
                    <input type="text" name="street_number" class="form-control" id="street-number-input" placeholder="Street Number" maxlength="10">
                    <label for="street-number-input" class="form-label">Street Number</label>
                </div>
            </div>

            <div class="col-md-12">
                <div class="form-floating">
                    <input type="email" name="email" class="form-control" id="email-input" placeholder="Email" maxlength="30">
                    <label for="email-input" class="form-label">Email</label>
                </div>
            </div>

            <div class="col-md-12">
                <div class="form-floating">
                    <input type="password" name="password" class="form-control" id="password-input" placeholder="Password" maxlength="255">
                    <label for="password-input" class="form-label">Password</label>
                </div>
            </div>

            <div class="col-md-12">
                <div class="form-floating">
                    <input type="password" name="confirm-password" class="form-control" id="confirm-password-input" placeholder="Password" maxlength="255">
                    <label for="confirm-password-input" class="form-label">Confirm Password</label>
                </div>
            </div>

            <div class="col-12">
                <button type="submit" class="btn btn-dark">Save changes</button>
            </div>
        </form>

    </div>
</body>

</html>