document.addEventListener("DOMContentLoaded", function () {
  // Get employer ID from localStorage or another source
  const employerId = 1; // Using the ID from your console log
  fetch(`http://127.0.0.1:11352/api/reads?table=employers&id=${employerId}`, {
    method: "GET",
    headers: {
      "accept": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (!data || !data.data) {
        throw new Error('No employer data received');
      }
      
      const employerData = data.data;
      console.log('Loaded employerData:', employerData);
      
      // Safely set input values with fallbacks
      document.getElementById("company-name-input").value = employerData.company_name || '';
      document.getElementById("phone-number").value = employerData.phone_number || '';
      // Initialize dropdowns with the data
      if (employerData.state) {
        populateStateDropdown(employerData.state, employerData.city_or_province || null);
      }
      document.getElementById("zip-code-input").value = employerData.zip_code || '';
      document.getElementById("street-number-input").value = employerData.street || '';
      document.getElementById("email-input").value = employerData.email || '';
      
      // Don't pre-fill password fields for security
      document.getElementById("password-input").value = '';
      document.getElementById("confirm-password-input").value = '';

      // Only populate dropdowns if we have state data
      if (employerData.state) {
        populateStateDropdown(employerData.state, employerData.city_or_province || null);
      }
    })
    .catch((error) => console.error("Error fetching employer data:", error));

  const form = document.getElementById("edit-profile-form");
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    
    // Check if any fields were modified
    const fieldsModified = Object.values({
      company_name: document.getElementById("company-name-input").value,
      phone_number: document.getElementById("phone-number").value,
      state: document.getElementById("state-input").value,
      city_or_province: document.getElementById("city-province-input").value,
      zip_code: document.getElementById("zip-code-input").value,
      street: document.getElementById("street-number-input").value,
      email: document.getElementById("email-input").value,
      password: document.getElementById("password-input").value,
    }).some(value => value !== '');

    if (!fieldsModified) {
      alert("Note: You can leave fields blank if you don't want to change them, but at least one field must be modified to update your profile.");
      return;
    }

    // Validate passwords match
    const password = document.getElementById("password-input").value;
    const confirmPassword = document.getElementById("confirm-password-input").value;
    
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    
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
        id: employerId,
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
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((regions) => {
      if (!Array.isArray(regions)) {
        throw new Error('Expected regions array from API');
      }

      const stateInput = document.getElementById("state-input");
      if (!stateInput) {
        throw new Error('State input element not found');
      }

      const currentSelectedValue = selectedState || stateInput.value;
      stateInput.innerHTML = "";

      // Add default option
      const defaultOption = document.createElement("option");
      defaultOption.value = "";
      defaultOption.textContent = "Select Region";
      defaultOption.disabled = true;
      defaultOption.selected = !currentSelectedValue;
      stateInput.appendChild(defaultOption);

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

      // Remove existing event listener before adding new one
      const newStateInput = stateInput.cloneNode(true);
      stateInput.parentNode.replaceChild(newStateInput, stateInput);
      newStateInput.addEventListener("change", function () {
        populateCityProvinceDropdown(this.value, null);
      });
    })
    .catch((error) => {
      console.error("Error fetching regions:", error);
      alert("Failed to load regions. Please try again later.");
    });
}

function populateCityProvinceDropdown(selectedStateCode, selectedCityProvince) {
  if (!selectedStateCode) {
    console.warn('No state code provided for city/province dropdown');
    return;
  }
  
  fetch(`http://127.0.0.1:11352/api/regions/${encodeURIComponent(selectedStateCode)}/provinces/`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((provinces) => {
      if (!Array.isArray(provinces)) {
        throw new Error('Expected provinces array from API');
      }

      const cityProvinceInput = document.getElementById("city-province-input");
      if (!cityProvinceInput) {
        throw new Error('City/Province input element not found');
      }

      cityProvinceInput.innerHTML = "";

      // Add default option
      const defaultOption = document.createElement("option");
      defaultOption.value = "";
      defaultOption.textContent = "Select City/Province";
      defaultOption.disabled = true;
      defaultOption.selected = !selectedCityProvince;
      cityProvinceInput.appendChild(defaultOption);

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
    .catch((error) => {
      console.error("Error fetching provinces:", error);
      alert("Failed to load cities/provinces. Please try again later.");
    });
}