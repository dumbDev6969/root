// login.js
document.addEventListener('DOMContentLoaded', function() {
  // Redirect to dashboard if employerData exists in localStorage
  const employerData = localStorage.getItem('employerData');
  if (employerData) {
    window.location.href = '../dashboard/recruiter/dashboard_recruiter.php';
    return;
  }

  const form = document.querySelector('form');
  form.addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Make a POST request to the /login endpoint
    fetch('https://root-4ytd.onrender.com/login', {
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
        // Store received data in localStorage
        if (data.personal_info) {
          localStorage.setItem('employerData', JSON.stringify(data.personal_info));
        } else {
          console.error('Personal info is missing in the response:', data);
        }
        // Redirect to the dashboard
        window.location.href = '../dashboard/recruiter/dashboard_recruiter.php';

      
      } else if (data.message === 'welcome user') {
            // Store received data in localStorage
        if (data.personal_info) {
          localStorage.setItem('userData', JSON.stringify(data.personal_info));
        } else {
          console.error('Personal info is missing in the response:', data);
        }
        // Redirect to the dashboard
        window.location.href = '../dashboard/tech_grad/dashboard_tech_grad.php';
        
      }
      else {
        alert('Login failed: ' + data.message); // Provide user feedback
      }
    }).catch(error => {
      console.error('Error:', error);
      alert('An error occurred during login. Please try again.');
    });
  });
});
