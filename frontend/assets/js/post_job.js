function postJob() {
    console.log("Starting job post process...");
    const formData = new FormData(document.getElementById("postJobForm"));
    
    // First get the employer_id from PHP session
    fetch('get_employer_id.php')
    .then(response => {
        if (!response.ok) {
            throw new Error('Session expired or unauthorized');
        }
        return response.json();
    })
    .then(data => {
        if (!data.success || !data.employer_id) {
            throw new Error('No employer ID found');
        }

        // Create job data with employer_id
        const jobData = {
            table: "jobs",
            data: {
                ...Object.fromEntries(formData.entries()),
                employer_id: data.employer_id,
                created_at: new Date().toISOString(),
            },
        };

        // Create the job
        return fetch("http://localhost:10000/api/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(jobData),
            credentials: 'include' // Include cookies for session
        });
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to create job');
        }
        return response.json();
    })
    .then(data => {
        console.log("API Response:", data);
        if (data.success === true && data.message === "Record created successfully") {
            alert("Job posted successfully!");
            window.location.href = 'dashboard_recruiter.php';
        } else {
            throw new Error(data.message || "Failed to create job");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        if (error.message.includes("Session expired") || error.message.includes("unauthorized")) {
            alert("Session expired. Please log in again.");
            window.location.href = "../../auth/login.php";
        } else {
            alert("Error creating job: " + error.message);
        }
    });
}
