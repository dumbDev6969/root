document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".container .row");

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

        // Then fetch jobs
        return fetch("https://root-4ytd.onrender.com/api/get-table?table=jobs")
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch jobs');
                }
                return response.json();
            })
            .then(jobsData => {
                const jobs = jobsData.data.filter(job => job.employer_id === data.employer_id);
                
                container.innerHTML = "";

                if (jobs.length === 0) {
                    container.innerHTML = `
                        <div class="col-12 text-center">
                            <h3>No jobs found</h3>
                            <p class="text-muted">You haven't posted any jobs yet.</p>
                            <a href="post_job.php" class="btn btn-dark">Post a Job</a>
                        </div>
                    `;
                    return;
                }

                jobs.forEach(job => {
                    const jobCard = `
                        <div class="col-lg-3 col-md-6 mb-4">
                            <div class="card h-100">
                                <div class="card-body">
                                    <div class="d-flex justify-content-between align-items-center mb-3">
                                        <div>
                                            <h4 class="card-title">${job.job_title}</h4>
                                        </div>
                                        <div class="company-profile border d-flex align-items-center justify-content-center" style="height: 50px; width: 50px; border-radius: 50px">
                                            <i class="fas fa-building"></i>
                                        </div>
                                    </div>
                                    <p class="text-secondary mb-2"><i class="fas fa-map-marker-alt me-2"></i>${job.location}</p>
                                    <div class="mb-3">
                                        <span class="badge bg-light text-dark border">${job.job_type}</span>
                                        <span class="badge bg-light text-dark border">$${job.salary_range}</span>
                                    </div>
                                    <div class="row g-2">
                                        <div class="col-8">
                                            <button type="button" class="btn btn-dark btn-sm w-100" onclick="editJob('${job.job_id}')">
                                                <i class="fas fa-edit me-1"></i> Edit
                                            </button>
                                        </div>
                                        <div class="col-4">
                                            <button type="button" class="btn btn-outline-danger btn-sm w-100" onclick="deleteJob('${job.job_id}')">
                                                <i class="fas fa-trash-alt"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    container.innerHTML += jobCard;
                });
            });
    })
    .catch(error => {
        console.error("Error:", error);
        if (error.message.includes("Session expired") || error.message.includes("unauthorized")) {
            alert("Session expired. Please log in again.");
            window.location.href = "../../auth/login.php";
        } else {
            container.innerHTML = `
                <div class="col-12 text-center">
                    <h3>Error loading jobs</h3>
                    <p class="text-danger">${error.message}</p>
                    <button onclick="location.reload()" class="btn btn-dark">Try Again</button>
                </div>
            `;
        }
    });
});

function editJob(jobId) {
    // TODO: Implement edit functionality
    alert('Edit functionality coming soon!');
}

function deleteJob(jobId) {
    if (!confirm('Are you sure you want to delete this job?')) {
        return;
    }

    fetch(`https://root-4ytd.onrender.com/api/delete?table=jobs&id=${jobId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete job');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Job deleted successfully');
            location.reload();
        } else {
            throw new Error(data.message || 'Failed to delete job');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error deleting job: ' + error.message);
    });
}
