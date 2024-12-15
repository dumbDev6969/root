// login.js
document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');
  form.addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Make a POST request to the /login endpoint
    fetch('http://127.0.0.1:11352/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.message === 'welcome employer') {
        // Store received data in local storage or session storage
        if (data.personal_info) {
          localStorage.setItem('employerData', JSON.stringify(data.personal_info));
        } else {
          console.error('Personal info is missing in the response:', data);
        }
        // Redirect to the dashboard
        window.location.href = '../dashboard/recruiter/dashboard_recruiter.php';
      } else {
        console.error('Login failed:', data.message);
      }
    }).catch(error => console.error('Error:', error));
  });
});


// jobseeker.js

// Function to check if password has at least 1 uppercase letter




// document.querySelector('form').addEventListener('submit', function(event) {
//   event.preventDefault(); // Prevent default form submission

//   const password = document.getElementById('password-input').value;
//   const confirmPassword = document.getElementById('confirm-password-input').value;
 

//   const formData = new FormData(event.target);
//   const data = {
//       table: 'users',
//       data: {
//           first_name: formData.get('first-name'),
//           last_name: formData.get('last-name'),
//           phone_number: formData.get('phone'),
//           state: formData.get('state'),
//           city_or_province: formData.get('city-or-province'),
//           municipality: formData.get('municipality'),
//           zip_code: formData.get('zip-code'),
//           street: formData.get('street-number'),
//           email: formData.get('email'),
//           password: formData.get('password'),
//           created_at: new Date().toISOString().split('T')[0],
//           updated_at: new Date().toISOString().split('T')[0]
//       }
//   };
//   console.log('Submitting form data:', data);

//   fetch('http://127.0.0.1:11352/api/signup/jobseeker', {
//       method: 'POST',
//       headers: {
//           'Content-Type': 'application/json'
//       },
//       body: JSON.stringify(data)
//   })
//   .then(response => response.json())
//   .then(data => {
//       console.log(data);
//   })
//   .catch((error) => {
//       console.error('Error:', error);
//       alert('An error occurred. Please try again.');
//   });
