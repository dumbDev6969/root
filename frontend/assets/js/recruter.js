document.querySelector('form').addEventListener('submit', function(event) {
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

    // Collect form data
    const formData = new FormData(event.target);
    const data = {
        table: 'employers',
        data: {
            company_name: formData.get('company_name'),
            phone_number: formData.get('phone_number'),
            state: formData.get('state'),
            city_or_province: formData.get('city-or-province'),
            zip_code: formData.get('zip_code'),
            street: formData.get('street_number'),
            email: formData.get('email'),
            password: formData.get('password'),
            created_at: new Date().toISOString().split('T')[0],
            updated_at: new Date().toISOString().split('T')[0]
        }
    };

    // Send data to the server
    fetch('http://127.0.0.1:11352/api/signup/recruter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        alert('Success: ' + data.message);
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});
