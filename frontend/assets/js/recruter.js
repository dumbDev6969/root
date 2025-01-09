document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    // Set hidden input values with actual text from select options
    const stateInput = document.getElementById("state-input");
    const cityProvinceInput = document.getElementById("city-province-input");
    
    document.getElementById("hidden-region").value = stateInput.options[stateInput.selectedIndex].text;
    document.getElementById("hidden-province").value = cityProvinceInput.options[cityProvinceInput.selectedIndex].text;

    const password_element = document.getElementById('password-input');
    const email_element = document.getElementById('email-input');
    const phone_element = document.getElementById('phone-number');
    const err_message = document.getElementById('error-message');
    const password = password_element.value;
    const confirmPassword = document.getElementById('confirm-password-input').value;

    // Clear previous error message and reset input styles
    err_message.textContent = '';
    password_element.classList.remove('is-invalid');
    email_element.classList.remove('is-invalid');
    phone_element.classList.remove('is-invalid');

    // Phone number validation
    const phoneNumber = phone_element.value;
    if (phoneNumber.length > 12) {
        err_message.textContent = 'Phone number must not exceed 12 digits';
        phone_element.classList.add('is-invalid');
        return;
    }

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

    // Collect form data
    const formData = new FormData(event.target);
    
    // Get the actual location names from hidden inputs
    const state = document.getElementById("hidden-region").value;
    const city_or_province = document.getElementById("hidden-province").value;
    
    const data = {
        table: 'employers',
        data: {
            company_name: formData.get('company_name'),
            phone_number: formData.get('phone_number'),
            state: state,
            city_or_province: city_or_province,
            zip_code: formData.get('zip_code'),
            street: formData.get('street_number'),
            email: formData.get('email'),
            password: formData.get('password'),
            created_at: new Date().toISOString().split('T')[0],
            updated_at: new Date().toISOString().split('T')[0]
        }
    };

    // Send data to the server
    fetch('https://root-4ytd.onrender.com/api/signup/recruter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Email already exists') {
            err_message.textContent = 'Email already exists';
            email_element.classList.add('is-invalid');
        } else if (data.message === 'Employer created successfully') {
            alert('Account created successfully!');
            window.location.href = '/frontend/src/auth/login.php';
        } else {
            throw new Error(data.detail || 'An error occurred during registration');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        // Check if account was created despite the error
        fetch('https://root-4ytd.onrender.com/api/verify-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: formData.get('email') })
        })
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                alert('Account created successfully!');
                window.location.href = '/frontend/src/auth/login.php';
            } else {
                err_message.textContent = error.message || 'An error occurred. Please try again.';
            }
        })
        .catch(() => {
            err_message.textContent = error.message || 'An error occurred. Please try again.';
        });
    });
});