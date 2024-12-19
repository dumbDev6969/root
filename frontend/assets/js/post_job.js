function postJob() {
  const employerData = localStorage.getItem("employerData");
  const formData = new FormData(document.getElementById("postJobForm"));
  const parsedData = JSON.parse(employerData);
  const data = {
    table: "jobs",
    data: {
      ...Object.fromEntries(formData.entries()),
      employer_id: parsedData.employer_id,
      created_at: new Date().toISOString(),
    },
  };

  fetch("https://root-4ytd.onrender.com/api/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message == "Job created successfully.") {
        alert("Job created successfully.");
        window.location.href = 'dashboard_recruiter.php';
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
