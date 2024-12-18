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
    <script src="../../../assets/js/geo.js"></script>
    <script>
        const employerData = localStorage.getItem("userData");
        const parsedData = JSON.parse(employerData);
        document.addEventListener('DOMContentLoaded', function () {
            const userData = {
                user_id: parsedData.user_id,
                first_name: parsedData.first_name,
                last_name: parsedData.last_name,
                phone_number: parsedData.phone_number,
                email: parsedData.email,
                street: parsedData.street,
                municipality: parsedData.municipality,
                city_or_province: parsedData.city_or_province,
                state: parsedData.state,
                zip_code: parsedData.zip_code,
                created_at: parsedData.created_at,
                updated_at: parsedData.updated_at,
            };

            // Populate form fields
            document.getElementById('first-name-input').value = userData.first_name || '';
            document.getElementById('last-name-input').value = userData.last_name || '';
            document.getElementById('phone-number').value = userData.phone_number || '';
            document.getElementById('email-input').value = userData.email || '';
            document.getElementById('street-number-input').value = userData.street || '';
            document.getElementById('zip-code-input').value = userData.zip_code || '';

            // Ensure dropdowns are populated dynamically
            const stateInput = document.getElementById("state-input");
            const cityProvinceInput = document.getElementById("city-province-input");
            const municipalityInput = document.getElementById("municipality-input");

            if (userData.state) stateInput.value = userData.state;

            stateInput.addEventListener("change", function () {
                const selectedState = stateInput.value;
                cityProvinceInput.innerHTML = '<option value="">Select City/Province</option>';
                municipalityInput.innerHTML = '<option value="">Select Municipality</option>';
                cityProvinceInput.disabled = true;
                municipalityInput.disabled = true;

                if (selectedState) {
                    fetch(`../../../backend/python/routes/geo/province.json?state=${selectedState}`)
                        .then((response) => response.json())
                        .then((provinces) => {
                            provinces.forEach((province) => {
                                const option = document.createElement("option");
                                option.value = province.code;
                                option.textContent = province.name;
                                cityProvinceInput.appendChild(option);
                            });
                            cityProvinceInput.disabled = false;
                        })
                        .catch((error) => console.error("Error fetching provinces:", error));
                }
            });

            cityProvinceInput.addEventListener("change", function () {
                const selectedProvince = cityProvinceInput.value;
                municipalityInput.innerHTML = '<option value="">Select Municipality</option>';
                municipalityInput.disabled = true;

                if (selectedProvince) {
                    fetch(`../../../backend/python/routes/geo/municipality.json?province=${selectedProvince}`)
                        .then((response) => response.json())
                        .then((municipalities) => {
                            municipalities.forEach((municipality) => {
                                const option = document.createElement("option");
                                option.value = municipality.code;
                                option.textContent = municipality.name;
                                municipalityInput.appendChild(option);
                            });
                            municipalityInput.disabled = false;
                        })
                        .catch((error) => console.error("Error fetching municipalities:", error));
                }
            });

            if (userData.city_or_province) cityProvinceInput.value = userData.city_or_province;
            if (userData.municipality) municipalityInput.value = userData.municipality;
        });
    </script>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const form = document.querySelector('form');
            form.addEventListener('submit', function (event) {
                event.preventDefault();
    
                const formData = new FormData(form);
                const data = {};
    
                // Collect only fields with values
                formData.forEach((value, key) => {
                    if (value.trim() !== '') {
                        data[key] = value;
                    }
                });
    
                // Add table and id to the request
                const userId = parsedData.user_id; // Retrieve user ID from localStorage
                const requestBody = {
                    table: "users", // Specify the table name
                    id: userId,
                    data: {
                        ...(data["edit-first-name"] && { first_name: data["edit-first-name"] }),
                        ...(data["edit-last-name"] && { last_name: data["edit-last-name"] }),
                        ...(data["edit-phone"] && { phone_number: data["edit-phone"] }),
                        ...(data["edit-state"] && { state: document.getElementById("state-input").options[document.getElementById("state-input").selectedIndex].text }),
                        ...(data["edit-city-or-province"] && { city_or_province: document.getElementById("city-province-input").options[document.getElementById("city-province-input").selectedIndex].text }),
                        ...(data["edit-municipality"] && { municipality: document.getElementById("municipality-input").options[document.getElementById("municipality-input").selectedIndex].text }),
                        ...(data["edit-zip-code"] && { zip_code: data["edit-zip-code"] }),
                        ...(data["edit-street-number"] && { street: data["edit-street-number"] }),
                        ...(data["edit-email"] && { email: data["edit-email"] }),
                        ...(data["edit-password"] && { password: data["edit-password"] }),
                        created_at: null,
                        updated_at: new Date().toISOString(),
                    },
                };

                // Send data to /api/update
                fetch('http://127.0.0.1:11352/api/update', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestBody),
                })
                    .then(response => response.json())
                    .then(result => {
                        console.log('Update successful:', result);
                        alert('Profile updated successfully!');
                    })
                    .catch(error => {
                        console.error('Error updating profile:', error);
                        alert('An error occurred while updating the profile.');
                    });
            });
        });
    </script>
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
                    <p class="text-muted">Note: Leave fields blank if you do not wish to update them.</p>
                    <!-- First Name -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-first-name" class="form-control" id="first-name-input" placeholder="First name" requireeeeddds>
                            <label for="first-name-input">First Name</label>
                        </div>
                    </div>
                    <!-- Last Name -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-last-name" class="form-control" id="last-name-input" placeholder="Last name" requireeeeddds>
                            <label for="last-name-input">Last Name</label>
                        </div>
                    </div>
                    <!-- Phone Number -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="number" name="edit-phone" class="form-control" id="phone-number" placeholder="Phone #" min="0" requireeeeddds>
                            <label for="phone-number">Phone Number</label>
                        </div>
                    </div>
                    <!-- State/Region -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <select name="edit-state" class="form-control" id="state-input" requireeeeddds>
                                <option value=""  selected>Select Region</option>
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
                            <input type="text" name="edit-zip-code" class="form-control" id="zip-code-input" placeholder="Zip Code" requireeeeddds>
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
                            <input type="email" name="edit-email" class="form-control" id="email-input" placeholder="Email" requireeeeddds>
                            <label for="email-input">Email</label>
                        </div>
                    </div>
                    <!-- Password -->
                    <div class="col-md-12">
                        <div class="form-floating">
                            <input type="password" name="edit-password" class="form-control" id="password-input" placeholder="Create Password" min="8" max="16" requireeeeddds>
                            <label for="password-input">Create Password</label>
                        </div>
                    </div>
                    <!-- Confirm Password -->
                    <div class="col-md-12">
                        <div class="form-floating">
                            <input type="password" name="edit-confirm-password" class="form-control" id="confirm-password-input" placeholder="Confirm Password" min="8" max="16" requireeeeddds>
                            <label for="confirm-password-input">Confirm Password</label>
                        </div>
                    </div>
                    <!-- Terms -->
                    <div class="col-12">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="terms-check-1" requireeeeddds>
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
                            <input type="text" name="edit-job-interest" class="form-control" id="job-interest-input" placeholder="Job interest E.g Developer, Designer" requireeeeddds>
                            <label for="job-interest-input">Developer, Designer</label>
                        </div>
                    </div>
                    <!-- Employment Type -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <select name="edit-job-type" class="form-select" id="job-type-input" requireeeeddds>
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
                            <input type="text" name="edit-preferred-location" class="form-control" id="preferred-location-input" placeholder="Preferred location" requireeeeddds>
                            <label for="preferred-location-input">Preferred location</label>
                        </div>
                    </div>
                    <!-- Expected Salary -->
                    <div class="col-md-6">
                        <div class="form-floating">
                            <input type="text" name="edit-expected-salary" class="form-control" id="expected-salary-input" placeholder="Expected salary" requireeeeddds>
                            <label for="expected-salary-input">Expected salary</label>
                        </div>
                    </div>
                    <!-- Terms -->
                    <div class="col-12">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="terms-check-2" requireeeeddds>
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
