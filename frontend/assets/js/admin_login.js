document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('https://root-4ytd.onrender.com/api/admin-login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                }),
                credentials: 'omit'
            });

            const data = await response.json();

            if (data.success) {
                // Store session data
                sessionStorage.setItem('isLoggedIn', 'true');
                sessionStorage.setItem('userType', 'admin');
                sessionStorage.setItem('userData', JSON.stringify(data.user));

                // Redirect to admin dashboard
                window.location.href = '../dashboard/admin/dashboard_admin.php';
            } else {
                alert(data.message || 'Login failed. Please check your credentials.');
            }
        } catch (error) {
            console.error('Login error:', error);
            alert('Login failed. Please try again later.');
        }
    });

    // Toggle password visibility
    document.querySelector('.toggle-password').addEventListener('click', function() {
        const passwordInput = document.querySelector('.password-input input');
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.classList.toggle('bi-eye');
        this.classList.toggle('bi-eye-slash');
    });
});