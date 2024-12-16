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

      populateStateDropdown(employerData.state, employerData.city_or_province);
    })
    .catch((error) => console.error("Error fetching employer data:", error));

  const form = document.getElementById("edit-profile-form");
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    
    const updatedData = {
      company_name: document.getElementById("company-name-input").value,
      phone_number: document.getElementById("phone-number").value,
      state: document.getElementById("state-input").value,
      city_or_province: document.getElementById("city-province-input").value,
      zip_code: document.getElementById("zip-code-input").value,
      street: document.getElementById("street-number-input").value,
      email: document.getElementById("email-input").value,
      password: document.getElementById("password-input").value,
    };
    fetch("http://127.0.0.1:11352/api/update", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "accept": "application/json",
      },
      body: JSON.stringify({
        table: "employers",
        id: 4,
        data: updatedData,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        alert("Profile updated successfully!");
        console.log("Update response:", data);
      })
      .catch((error) => {
        console.error("Error updating profile:", error);
      });
  });
});

function populateStateDropdown(selectedState, selectedCityProvince) {
  fetch("http://127.0.0.1:11352/api/regions/")
      .then((response) => response.json())
    .then((regions) => {
      const stateInput = document.getElementById("state-input");
      const currentSelectedValue = selectedState || stateInput.value;
      stateInput.innerHTML = "";

      regions.forEach((region) => {
          const option = document.createElement("option");
        option.value = region.code;
        option.textContent = region.name;

        if (region.code === currentSelectedValue) {
            option.selected = true;
          populateCityProvinceDropdown(region.code, selectedCityProvince);
          }
        stateInput.appendChild(option);
        });

      stateInput.disabled = false;
      stateInput.addEventListener("change", function () {
        populateCityProvinceDropdown(stateInput.value, null);
      });
      })
    .catch((error) => console.error("Error fetching regions:", error));
}

function populateCityProvinceDropdown(selectedStateCode, selectedCityProvince) {
  if (!selectedStateCode) return;
  
  fetch(`http://127.0.0.1:11352/api/regions/${encodeURIComponent(selectedStateCode)}/provinces/`)
      .then((response) => response.json())
      .then((provinces) => {
        const cityProvinceInput = document.getElementById("city-province-input");
      cityProvinceInput.innerHTML = "";

        provinces.forEach((province) => {
          const option = document.createElement("option");
        option.value = province.code;
        option.textContent = province.name;

          if (province.code === selectedCityProvince || province.name === selectedCityProvince) {
            option.selected = true;
          }
          cityProvinceInput.appendChild(option);
        });

        cityProvinceInput.disabled = false;
      })
      .catch((error) => console.error("Error fetching provinces:", error));
}