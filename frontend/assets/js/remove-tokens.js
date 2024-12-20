// remove-tokens.js
document.addEventListener("DOMContentLoaded", function () {
    // First verify the session is valid
    fetch('../../auth/check_session.php')
        .then(response => response.json())
        .then(data => {
            if (!data.loggedIn || data.status !== 'success' || data.userType !== 'employer') {
                throw new Error('Invalid session state');
            }

            // Session is valid, continue with the existing session data
            return data;
        })
        .then(sessionData => {

            if (!sessionData.loggedIn || !sessionData.employerData) {
                throw new Error('No employer data found');
            }

            const parsedData = sessionData.employerData;
            console.log("Loaded employerData:", parsedData);

            // Update the dashboard with employerData
            const elements = {
                "company-name": parsedData.company_name || "Company Name",
                "industry-description": "Tech Industry Job Experts", // Static text as per design
                "career-building": "Building Careers in Technology", // Static text as per design
                "date-started": parsedData.created_at
                    ? new Date(parsedData.created_at).toLocaleDateString()
                    : "dd/mm/yy"
            };

            // Update each element if it exists
            Object.entries(elements).forEach(([id, value]) => {
                const element = document.getElementById(id);
                if (element) {
                    element.textContent = value;
                }
            });

            // Set profile image if available
            if (parsedData.profile_image) {
                const profileDiv = document.querySelector('.border.border-dark');
                if (profileDiv) {
                    profileDiv.style.backgroundImage = `url(${parsedData.profile_image})`;
                    profileDiv.style.backgroundSize = 'cover';
                    profileDiv.style.backgroundPosition = 'center';
                }
            }
        })
        .catch(error => {
            console.error("Session error:", error);
            // Clear any invalid session data
            fetch('../../auth/logout.php')
                .then(() => {
                    console.log("Session cleared, redirecting to login");
                    window.location.href = '../../auth/login.php';
                })
                .catch(err => {
                    console.error("Error during logout:", err);
                    // Force redirect if logout fails
                    window.location.href = '../../auth/login.php';
                });
        });
});
