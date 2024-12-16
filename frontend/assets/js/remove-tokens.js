// remove-tokens.js
document.addEventListener("DOMContentLoaded", function () {
  // Retrieve employerData from localStorage
  const employerData = localStorage.getItem("employerData");
  if (employerData) {
    const parsedData = JSON.parse(employerData);
    console.log("Loaded employerData:", parsedData);

    // Update the dashboard with employerData
    document.getElementById("company-name").textContent =
      parsedData.company_name || "Company Name";
    document.getElementById("industry-description").textContent =
      "Industry Description";
    document.getElementById("career-building").textContent = "Career Building";
    document.getElementById("date-started").textContent = parsedData.created_at
      ? new Date(parsedData.created_at).toLocaleDateString()
      : "dd/mm/yy";
  } else {
    console.log("No employerData found in localStorage");
    window.location.href = "../../../src/auth/login.php";
  }
});
