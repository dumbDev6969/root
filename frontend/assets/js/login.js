// login.js
document.addEventListener('DOMContentLoaded', function() {
  // Check session status first before any redirects
  fetch('check_session.php')
    .then(async response => {
      const text = await response.text();
      let data;
      try {
        data = JSON.parse(text);
      } catch (e) {
        console.error('Invalid JSON response from session check:', text);
        throw new Error('Server returned invalid JSON response during session check');
      }
      
      if (data.loggedIn && data.status === 'success') {
        console.log('Active session found:', data.userType);
        if (data.userType === 'employer') {
          window.location.href = '../dashboard/recruiter/dashboard_recruiter.php';
          return;
        } else if (data.userType === 'user') {
          window.location.href = '../dashboard/tech_grad/dashboard_tech_grad.php';
          return;
        }
      }
    })
    .catch(error => {
      console.error('Error checking session:', error);
      // Clear any potentially corrupted session data
      fetch('logout.php').catch(err => console.error('Error clearing session:', err));
    });

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
    .then(async response => {
      const text = await response.text();
      let data;
      try {
        data = JSON.parse(text);
      } catch (e) {
        console.error('Invalid JSON response:', text);
        throw new Error('Server returned invalid JSON response');
      }
      
      if (data.message === 'welcome employer' || data.message === 'welcome user') {
        if (!data.personal_info) {
          console.error('Personal info is missing in the response:', data);
          alert('Login failed: Missing personal information');
          return;
        }

        // Store in PHP session
        fetch('store_session.php', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ personal_info: data.personal_info })
        })
        .then(async response => {
          const text = await response.text();
          let sessionResponse;
          try {
            sessionResponse = JSON.parse(text);
          } catch (e) {
            console.error('Invalid JSON response from session storage:', text);
            throw new Error('Server returned invalid JSON response during session storage');
          }
          if (sessionResponse.status === 'success') {
            console.log('Session data stored successfully');
            // Verify session was stored before redirect
            fetch('check_session.php')
              .then(async response => {
                const sessionCheck = await response.json();
                if (sessionCheck.loggedIn && sessionCheck.status === 'success') {
                  // Redirect based on user type
                  if (data.message === 'welcome employer') {
                    window.location.href = '../../src/dashboard/recruiter/dashboard_recruiter.php';
                  } else {
                    window.location.href = '../../src/dashboard/tech_grad/dashboard_tech_grad.php';
                  }
                } else {
                  throw new Error('Session verification failed');
                }
              })
              .catch(error => {
                console.error('Session verification failed:', error);
                alert('Login failed: Could not verify session. Please try again.');
              });
          } else {
            console.error('Failed to store session data:', sessionResponse.message);
            alert('Failed to store session data. Please try again.');
          }
        })
        .catch(error => {
          console.error('Error while storing session data:', error);
          alert('Error storing session data. Please try again.');
        });
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
