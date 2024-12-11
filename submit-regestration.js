// document.querySelector('form').addEventListener('submit', function(event) {
//     event.preventDefault(); // Prevent default form submission

//     const password = document.getElementById('password-input').value;
//     const confirmPassword = document.getElementById('confirm-password-input').value;

//     if (password !== confirmPassword) {
//         alert('Passwords do not match. Please try again.');
//         return;
//     }

//     const formData = new FormData(event.target);
//     const data = {
//         table: 'users',
//         data: {
//             first_name: formData.get('first-name'),
//             last_name: formData.get('last-name'),
//             phone_number: formData.get('phone'),
//             state: formData.get('state'),
//             city_or_province: formData.get('city-or-province'),
//             municipality: formData.get('municipality'),
//             zip_code: formData.get('zip-code'),
//             street_number: formData.get('street-number'),
//             email: formData.get('email'),
//             password: formData.get('password'),
//             created_at: new Date().toISOString().split('T')[0],
//             updated_at: new Date().toISOString().split('T')[0]
//         }
//     }
    

//     fetch('http://127.0.0.1:11352/api/create', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(data)
//     })
//     .then(response => response.json())
//     .then(data => {
//         alert('Success: ' + data.message);
//         alert(JSON.stringify(data));
//     })
//     .catch((error) => {
//         console.error('Error:', error);
//         alert('An error occurred. Please try again.');
//     });
// });

document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const password = document.getElementById('password-input').value;
    const confirmPassword = document.getElementById('confirm-password-input').value;

    if (password !== confirmPassword) {
        alert('Passwords do not match. Please try again.');
        return;
    }

    const formData = new FormData(event.target);
    const currentDate = new Date().toISOString().split('T')[0];
    const data = {
        table: 'users',
        data: {
            first_name: formData.get('first-name'),
            last_name: formData.get('last-name'),
            phone_number: formData.get('phone'),
            state: formData.get('state'),
            city_or_province: formData.get('city-or-province'),
            municipality: formData.get('municipality'),
            zip_code: formData.get('zip-code'),
            street_number: formData.get('street-number'),
            email: formData.get('email'),
            password: formData.get('password'),
            created_at: currentDate,
            updated_at: currentDate
        }
    };

    console.log('Sending data:', data);  // Log the data object for debugging

    fetch('http://127.0.0.1:11352/api/create', {
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
