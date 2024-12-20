document.addEventListener("DOMContentLoaded", function () {
  fetch('/root/frontend/src/auth/store_session.php', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => response.json())
  .then(sessionData => {
      if (sessionData && sessionData.employerData) {
          const parsedData = sessionData.employerData;
  const container = document.querySelector("#job-container");

  fetch("http://localhost:10000/api/get-table%20?table=jobs")
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
  fetch('/root/frontend/src/auth/store_session.php', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(() => {
      console.log("Session data cleared");
  })
  .catch(error => {
      console.error("Error clearing session data:", error);
  });
  window.location.href = "../../../src/auth/login.php";
});
});