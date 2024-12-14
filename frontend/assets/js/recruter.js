document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const password = document.getElementById('password-input').value;
    const confirmPassword = document.getElementById('confirm-password-input').value;

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
        console.log("Error: Password must be at least 8 characters long.");
        return;
    }
    if (!hasUppercase(password)) {
        console.log("Error: Password must contain at least one uppercase letter.");
        return;
    }
    if (!hasSpecialCharacter(password)) {
        console.log("Error: Password must contain at least one special character.");
        return;
    }

    if (password !== confirmPassword) {
        alert('Passwords do not match. Please try again.');
        return;
    }

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
    // console.log(JSON.stringify(data));
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
