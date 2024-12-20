function postJob() {
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
          const formData = new FormData(document.getElementById("postJobForm"));
          const data = {
              table: "jobs",
              data: {
                  ...Object.fromEntries(formData.entries()),
                  employer_id: parsedData.employer_id,
                  created_at: new Date().toISOString(),
              },
          };
  
          fetch("http://localhost:10000/api/create", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
              },
              body: JSON.stringify(data),
          })
          .then((response) => response.json())
          .then((data) => {
              console.log("API Response:", data); // Debugging line
              if (data.success === true && data.message === "Record created successfully") {
                  alert("Job created successfully.");
                  window.location.href = 'dashboard_recruiter.php';
              } else {
                  alert("Failed to create job. Please try again.");
              }
          })
          .catch((error) => {
              console.error("Error:", error);
          });
      } else {
          console.error("No employerData found in session");
          alert("Session expired. Please log in again.");
          window.location.href = "../../../src/auth/login.php";
      }
  })
  .catch(error => {
      console.error("Error fetching session data:", error);
      alert("Session expired. Please log in again.");
      window.location.href = "../../../src/auth/login.php";
  });

  fetch("http://localhost:10000/api/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("API Response:", data); // Debugging line
      if (data.success === true && data.message === "Record created successfully") {
        alert("Job created successfully.");
        window.location.href = 'dashboard_recruiter.php';
      } else {
        alert("Failed to create job. Please try again.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
