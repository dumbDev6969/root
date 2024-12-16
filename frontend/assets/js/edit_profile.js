document.addEventListener("DOMContentLoaded", function () {
  fetch("http://127.0.0.1:11352/api/reads?table=employers&id=4", {
    method: "GET",
    headers: {
      "accept": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      const employerData = data.data;
     

      document.getElementById("company-name-input").value = employerData.company_name;
      document.getElementById("phone-number").value = employerData.phone_number;
      document.getElementById("selected-state-input").innerHTML = employerData.state;
      document.getElementById("selected-city-province-input").innerHTML = employerData.city_or_province;
      document.getElementById("zip-code-input").value = employerData.zip_code;
      document.getElementById("street-number-input").value = employerData.street;
      document.getElementById("email-input").value = employerData.email;
      document.getElementById("password-input").value = employerData.password;
      document.getElementById("confirm-password-input").value = employerData.password;

      // Enable and populate the state and city/province dropdowns
      populateStateDropdown(employerData.state);
      populateCityProvinceDropdown(employerData.city_or_province);
    })
    .catch((error) => console.error("Error fetching employer data:", error));
});

function populateStateDropdown(selectedState) {
  fetch("http://127.0.0.1:11352/api/regions/")
    .then((response) => response.json())
    .then((regions) => {
      const stateInput = document.getElementById("state-input");
      stateInput.innerHTML = ""; // Clear existing options

      regions.forEach((region) => {
        const option = document.createElement("option");
        option.value = region.name;
        option.textContent = region.name;
        if (region.name === selectedState) {
          option.selected = true;
        }
        stateInput.appendChild(option);
      });

      stateInput.disabled = false;
    })
    .catch((error) => console.error("Error fetching regions:", error));
}

function populateCityProvinceDropdown(selectedCityProvince) {
  const stateInput = document.getElementById("state-input");
  stateInput.addEventListener("change", function () {
    const selectedState = stateInput.value;

    fetch(`http://127.0.0.1:11352/api/regions/${selectedState}/provinces/`)
      .then((response) => response.json())
      .then((provinces) => {
        const cityProvinceInput = document.getElementById("city-province-input");
        cityProvinceInput.innerHTML = ""; // Clear existing options

        provinces.forEach((province) => {
          const option = document.createElement("option");
          option.value = province.name;
          option.textContent = province.name;
          if (province.name === selectedCityProvince) {
            option.selected = true;
          }
          cityProvinceInput.appendChild(option);
        });

        cityProvinceInput.disabled = false;
      })
      .catch((error) => console.error("Error fetching provinces:", error));
  });

  // Trigger the change event to populate the city/province dropdown
  stateInput.dispatchEvent(new Event("change"));
}
