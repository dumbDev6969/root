console.log("jobseeker.js is loaded");

document.addEventListener("DOMContentLoaded", function () {
  const stateInput = document.getElementById("state-input");
  const cityProvinceInput = document.getElementById("city-province-input");
  const municipalityInput = document.getElementById("municipality-input");

  // Ensure dropdowns are populated dynamically
  const populateDropdowns = () => {
    const state = document.getElementById("hidden-region").value;
    const city_or_province = document.getElementById("hidden-province").value;
    const municipality = document.getElementById("hidden-municipality").value;

    if (state) stateInput.value = state;
    if (city_or_province) cityProvinceInput.value = city_or_province;
    if (municipality) municipalityInput.value = municipality;

    console.log("Dropdowns populated with hidden values:", state, city_or_province, municipality);
  };

  populateDropdowns();
});
document.querySelector("form").addEventListener("submit", function (event) {
  // Dynamically populate hidden input fields before form submission
  const stateInput = document.getElementById("state-input");
  const cityProvinceInput = document.getElementById("city-province-input");
  const municipalityInput = document.getElementById("municipality-input");

  document.getElementById("hidden-region").value = stateInput.options[stateInput.selectedIndex].text;
  document.getElementById("hidden-province").value = cityProvinceInput.options[cityProvinceInput.selectedIndex].text;
  document.getElementById("hidden-municipality").value = municipalityInput.options[municipalityInput.selectedIndex].text;

  console.log("Hidden inputs populated with names:", {
    region: stateInput.options[stateInput.selectedIndex].text,
    province: cityProvinceInput.options[cityProvinceInput.selectedIndex].text,
    municipality: municipalityInput.options[municipalityInput.selectedIndex].text,
  });
  event.preventDefault(); // Prevent default form submission

  const password_element = document.getElementById('password-input'); // input element
  const err_message = document.getElementById('error-message');
  const password = password_element.value;
  const confirmPassword = document.getElementById('confirm-password-input').value;

  // Clear previous error message and reset input styles
  err_message.textContent = ''; 
  password_element.classList.remove('is-invalid');

  // Password validation functions
  function hasUppercase(password) {
      const uppercaseRegex = /[A-Z]/;
      return uppercaseRegex.test(password); 
  }

  function hasSpecialCharacter(password) {
      const specialCharacterRegex = /[!@#$%^&*()_+=[\]{};':"\\|,.<>/?]/;
      return specialCharacterRegex.test(password);
  }

  function hasMinLength(password) {
      return password.length >= 8;
  }

  // Password validation checks
  if (!hasMinLength(password)) {
      // Set error message and style
      err_message.textContent = 'Password must be at least 8 characters long.';
      password_element.classList.add('is-invalid');
      return;
  }
  
  if (!hasUppercase(password)) {
      err_message.textContent = 'Password must contain at least one uppercase letter.';
      password_element.classList.add('is-invalid');
      return; 
  }

  if (!hasSpecialCharacter(password)) {
      err_message.textContent = 'Password must contain at least one special character.';
      password_element.classList.add('is-invalid');
      return; 
  }

  if (password !== confirmPassword) {
      err_message.textContent = 'Passwords do not match.';
      document.getElementById('confirm-password-input').classList.add('is-invalid');
      return; 
  }

  const formData = new FormData(event.target);
  console.log(formData);

  // Ensure hidden inputs are populated correctly
  const state = document.getElementById("hidden-region").value;
  const city_or_province = document.getElementById("hidden-province").value;
  const municipality = document.getElementById("hidden-municipality").value;
  console.log(state,city_or_province,municipality)

  const data = {
    table: "users",
    data: {
      first_name: formData.get("first-name"),
      last_name: formData.get("last-name"),
      phone_number: formData.get("phone"),
      state: state,
      city_or_province: city_or_province,
      municipality: municipality,
      zip_code: formData.get("zip-code"),
      street: formData.get("street-number"),
      email: formData.get("email"),
      password: formData.get("password"),
      created_at: new Date().toISOString().split("T")[0],
      updated_at: new Date().toISOString().split("T")[0],
    },
  };
  console.log("Submitting form data:", data);

  fetch("http://127.0.0.1:11352/api/signup/jobseeker", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data.message === 'User created successfully') {
        window.location.href = "auth/login.php"; // Redirect to login page
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    });
});
