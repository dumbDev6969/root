document.addEventListener("DOMContentLoaded", () => {
  let selected_region = null;
  fetch("https://root-4ytd.onrender.com/api/regions/")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      return response.json();
    })
    .then((data) => {
      const selectElement = document.getElementById("state-input");

      data.forEach((region) => {
        const option = document.createElement("option");
        option.value = region.code;
        option.textContent = region.name;
        selectElement.appendChild(option);
      });

      const hiddenRegionInput = document.createElement("input");
      hiddenRegionInput.type = "hidden";
      hiddenRegionInput.id = "hidden-region";
      hiddenRegionInput.name = "selected-region";
      document.body.appendChild(hiddenRegionInput);

      selectElement.addEventListener("change", function () {
        const selectedOption = selectElement.options[selectElement.selectedIndex];
        hiddenRegionInput.value = selectedOption.textContent; // Store name instead of code
        console.log("Region selected:", hiddenRegionInput.value); // Debugging log
        selected_region = selectElement.value;
        document.getElementById("city-province-input").disabled = false;
        fetch(`https://root-4ytd.onrender.com/api/regions/${selected_region}/provinces/`)
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok " + response.statusText);
            }
            return response.json();
          })
          .then((provinces) => {
            const cityProvinceSelect = document.getElementById("city-province-input");
            cityProvinceSelect.innerHTML = "";
            const hiddenProvinceInput = document.createElement("input");
            hiddenProvinceInput.type = "hidden";
            hiddenProvinceInput.id = "hidden-province";
            hiddenProvinceInput.name = "selected-province";
            document.body.appendChild(hiddenProvinceInput);

            const defaultOption = document.createElement("option");
            defaultOption.value = "";
            defaultOption.disabled = true;
            defaultOption.selected = true;
            defaultOption.textContent = "Select City/Province";
            cityProvinceSelect.appendChild(defaultOption);

            provinces.forEach((province) => {
              const option = document.createElement("option");
              option.value = province.code;
              option.textContent = province.name;
              cityProvinceSelect.appendChild(option);
            });

            cityProvinceSelect.addEventListener("change", function () {
              const selectedOption = cityProvinceSelect.options[cityProvinceSelect.selectedIndex];
              hiddenProvinceInput.value = selectedOption.textContent; // Store name instead of code
              console.log("Province selected:", hiddenProvinceInput.value); // Debugging log
              const selectedProvinceValue = cityProvinceSelect.value;
              document.getElementById("municipality-input").disabled = false;
              fetch(`https://root-4ytd.onrender.com/api/provinces/${selectedProvinceValue}/municipalities/`)
                .then((response) => {
                  if (!response.ok) {
                    throw new Error("Network response was not ok " + response.statusText);
                  }
                  return response.json();
                })
                .then((municipalities) => {
                  const municipalitiesSelect = document.getElementById("municipality-input");
                  municipalitiesSelect.innerHTML = "";

                  const hiddenMunicipalityInput = document.createElement("input");
                  hiddenMunicipalityInput.type = "hidden";
                  hiddenMunicipalityInput.id = "hidden-municipality";
                  hiddenMunicipalityInput.name = "selected-municipality";
                  document.body.appendChild(hiddenMunicipalityInput);

                  const defaultMunicipalityOption = document.createElement("option");
                  defaultMunicipalityOption.value = "";
                  defaultMunicipalityOption.disabled = true;
                  defaultMunicipalityOption.selected = true;
                  defaultMunicipalityOption.textContent = "Select municipality";
                  municipalitiesSelect.appendChild(defaultMunicipalityOption);

                  municipalities.forEach((municipality) => {
                    const option = document.createElement("option");
                    option.value = municipality.code;
                    option.textContent = municipality.name;
                    municipalitiesSelect.appendChild(option);
                  });

                  municipalitiesSelect.addEventListener("change", function () {
                    const selectedOption = municipalitiesSelect.options[municipalitiesSelect.selectedIndex];
                    hiddenMunicipalityInput.value = selectedOption.textContent; // Store name instead of code
                    console.log("Municipality selected:", hiddenMunicipalityInput.value); // Debugging log
                  });
                })
                .catch((error) => {
                  console.error("There was a problem fetching municipalities:", error);
                });
            });
          })
          .catch((error) => {
            console.error("There was a problem fetching provinces:", error);
          });
      });
    })
    .catch((error) => {
      console.error("There was a problem fetching regions:", error);
    });
});
