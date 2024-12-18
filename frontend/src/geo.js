// geo.js: Logic to dynamically populate location fields (state, city/province, municipality)

document.addEventListener("DOMContentLoaded", function () {
  const stateInput = document.getElementById("state-input");
  const cityProvinceInput = document.getElementById("city-province-input");
  const municipalityInput = document.getElementById("municipality-input");

  // Fetch regions (states)
  fetch("../../../backend/python/routes/geo/region.json")
    .then((response) => response.json())
    .then((regions) => {
      regions.forEach((region) => {
        const option = document.createElement("option");
        option.value = region.code;
        option.textContent = region.name;
        stateInput.appendChild(option);
      });
    })
    .catch((error) => console.error("Error fetching regions:", error));

  // Populate city/province based on selected state
  const populateProvincesAndMunicipalities = (state, city_or_province, municipality) => {
      cityProvinceInput.innerHTML = '<option value="">Select City/Province</option>';
      municipalityInput.innerHTML = '<option value="">Select Municipality</option>';
      cityProvinceInput.disabled = true;
      municipalityInput.disabled = true;
  
      if (state) {
          fetch(`../../../backend/python/routes/geo/province.json?state=${state}`)
              .then((response) => response.json())
              .then((provinces) => {
                  provinces.forEach((province) => {
                      const option = document.createElement("option");
                      option.value = province.code;
                      option.textContent = province.name;
                      cityProvinceInput.appendChild(option);
                  });
                  cityProvinceInput.disabled = false;
  
                  // Preselect city/province if available
                  if (city_or_province) {
                      cityProvinceInput.value = city_or_province;
                      cityProvinceInput.dispatchEvent(new Event("change"));
                  }
              })
              .catch((error) => console.error("Error fetching provinces:", error));
      }
  };
  
  stateInput.addEventListener("change", function () {
      const selectedState = stateInput.value;
      populateProvincesAndMunicipalities(selectedState);
  });
  
  cityProvinceInput.addEventListener("change", function () {
      const selectedProvince = cityProvinceInput.value;
      municipalityInput.innerHTML = '<option value="">Select Municipality</option>';
      municipalityInput.disabled = true;
  
      if (selectedProvince) {
          fetch(`../../../backend/python/routes/geo/municipality.json?province=${selectedProvince}`)
              .then((response) => response.json())
              .then((municipalities) => {
                  municipalities.forEach((municipality) => {
                      const option = document.createElement("option");
                      option.value = municipality.code;
                      option.textContent = municipality.name;
                      municipalityInput.appendChild(option);
                  });
                  municipalityInput.disabled = false;
  
                  // Preselect municipality if available
                  if (municipality) {
                      municipalityInput.value = municipality;
                  }
              })
              .catch((error) => console.error("Error fetching municipalities:", error));
      }
  });
  
  // Prepopulate fields based on localStorage data
  const employerData = localStorage.getItem("userData");
  if (employerData) {
      const parsedData = JSON.parse(employerData);
      const { state, city_or_province, municipality } = parsedData;
      if (state) {
          stateInput.value = state;
          populateProvincesAndMunicipalities(state, city_or_province, municipality);
      }
  }

  // Populate municipality based on selected city/province
  cityProvinceInput.addEventListener("change", function () {
    const selectedProvince = cityProvinceInput.value;
    municipalityInput.innerHTML = '<option value="">Select Municipality</option>';
    municipalityInput.disabled = true;

    if (selectedProvince) {
      fetch(`../../../backend/python/routes/geo/municipality.json?province=${selectedProvince}`)
        .then((response) => response.json())
        .then((municipalities) => {
          municipalities.forEach((municipality) => {
            const option = document.createElement("option");
            option.value = municipality.code;
            option.textContent = municipality.name;
            municipalityInput.appendChild(option);
          });
          municipalityInput.disabled = false;
        })
        .catch((error) => console.error("Error fetching municipalities:", error));
    }
  });
});