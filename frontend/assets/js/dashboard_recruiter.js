document.addEventListener("DOMContentLoaded", function () {
  // First check if session exists
  fetch('/root/frontend/src/auth/check_session.php')
  .then(response => response.json())
  .then(sessionData => {
      if (!sessionData.loggedIn || sessionData.userType !== 'employer') {
          throw new Error('Invalid session');
      }
      // Session is valid, get employer data
      return fetch('/root/frontend/src/auth/check_session.php')
          .then(response => response.json());
  })
  .then(sessionData => {
      if (sessionData && sessionData.employerData) {
          const parsedData = sessionData.employerData;
  const container = document.querySelector("#job-container");

  fetch("https://root-4ytd.onrender.com/api/get-table?table=jobs")
    .then((response) => response.json())
    .then((data) => {
      const jobs = data.data.filter((job) => job.employer_id === parsedData.employer_id);

      container.innerHTML = "";

      jobs.forEach((job) => {
        const jobCard = `
          <div class="col-lg-3 col-md-6 d-flex align-items-center justify-content-center">
            <div class="card" style="width: 18rem;">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h4 class="card-title">${job.job_title}</h4>
                  </div>
                  <div class="company-profile border" style="height: 50px; width: 50px; border-radius: 50px">
                    img
                  </div>
                </div>
                <h6 class="card-subtitle mb-2 text-body-secondary">Employer ID: ${job.employer_id}</h6>
                <p class="text-secondary">${job.location}</p>
                <p class="card-text">
                  <button type="button" disabled class="btn btn-outline-secondary btn-sm">${job.job_type}</button>
                  <h6>${job.salary_range}</h6>
                </p>
                <form action="#">
                  <div class="row">
                    <div class="col-md-8 p-1">
                      <button type="button" class="btn btn-sm btn-dark w-100">Edit</button>
                    </div>
                    <div class="col-md-4 p-1">
                      <button type="button" class="btn btn-sm btn-outline-secondary w-100">Delete</button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        `;
        container.innerHTML += jobCard;
      });
    })
    .catch((error) => console.error("Error fetching jobs:", error));
    }
})
.catch((error) => {
    console.error("Error fetching session data:", error);
});

document.getElementById("logout-button").addEventListener("click", function () {
  fetch('/root/frontend/src/auth/logout.php')
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        console.log("Session cleared successfully");
        window.location.href = "../../../src/auth/login.php";
      } else {
        throw new Error('Logout failed');
      }
    })
    .catch(error => {
      console.error("Error during logout:", error);
      // Force redirect even if logout fails
      window.location.href = "../../../src/auth/login.php";
    });
});
});