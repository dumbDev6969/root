document.addEventListener("DOMContentLoaded", () => {
    const jobSearchInput = document.getElementById("job-search");
    const companySearchInput = document.getElementById("company-search");
    const salaryInput = document.getElementById("salary-input");
    const employmentTypeCheckboxes = document.querySelectorAll(".form-check-input");
    const jobList = document.getElementById("job-list");

    let jobs = [];

    async function fetchJobs() {
        try {
            const response = await fetch("https://root-4ytd.onrender.com/api/get-table?table=jobs");
            const data = await response.json();
            jobs = data.data;
            displayJobs(jobs);
        } catch (error) {
            console.error("Error fetching jobs:", error);
        }
    }

    function displayJobs(filteredJobs) {
        jobList.innerHTML = ""; // Clear existing content
        if (filteredJobs.length === 0) {
            jobList.innerHTML = "<p>No jobs match your criteria.</p>";
            return;
        }

        filteredJobs.forEach(job => {
            const jobCard = `
                <div class="col-md-3" style="width: 15.5rem;">
                    <div class="card" style="width: 15.5rem;">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <h5 class="card-title">${job.job_title}</h5>
                                </div>
                                <div class="company-profile border" style="height: 50px; width: 50px; border-radius: 50px">
                                    <img src="https://via.placeholder.com/50" alt="Company Logo">
                                </div>
                            </div>
                            <h6 class="card-subtitle mb-2 text-body-secondary">${job.location}</h6>
                            <p class="text-secondary">${job.job_type}</p>
                            <p class="card-text">
                                <button type="button" disabled class="btn btn-outline-secondary btn-sm">${job.job_type}</button>
                                <h6>${job.salary_range}</h6>
                            </p>
                        </div>
                    </div>
                </div>
            `;
            jobList.insertAdjacentHTML("beforeend", jobCard);
        });
    }

    function filterJobs() {
        const jobSearchValue = jobSearchInput.value.toLowerCase();
        const companySearchValue = companySearchInput.value.toLowerCase();
        const salaryValue = parseFloat(salaryInput.value) || 0;

        const selectedEmploymentTypes = Array.from(employmentTypeCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);

        const filteredJobs = jobs.filter(job => {
            const matchesJobTitle = job.job_title.toLowerCase().includes(jobSearchValue);
            const matchesCompany = job.location.toLowerCase().includes(companySearchValue);
            const matchesSalary = parseFloat(job.salary_range.replace(/[^0-9.-]+/g, "")) >= salaryValue;
            const matchesEmploymentType = selectedEmploymentTypes.length === 0 || selectedEmploymentTypes.includes(job.job_type);

            return matchesJobTitle && matchesCompany && matchesSalary && matchesEmploymentType;
        });

        displayJobs(filteredJobs);
    }

    // Event listeners
    jobSearchInput.addEventListener("input", filterJobs);
    companySearchInput.addEventListener("input", filterJobs);
    salaryInput.addEventListener("input", filterJobs);
    employmentTypeCheckboxes.forEach(checkbox => checkbox.addEventListener("change", filterJobs));

    // Fetch jobs on page load
    fetchJobs();
});