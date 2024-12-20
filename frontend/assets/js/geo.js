// Initialize geo dropdowns with current values
function initializeGeoDropdowns() {
    const stateInput = document.getElementById('state-input');
    const cityProvinceInput = document.getElementById('city-province-input');
    const municipalityInput = document.getElementById('municipality-input');

    // Load regions and set current value
    fetch('../../../backend/python/routes/geo/region.json')
        .then(response => response.json())
        .then(regions => {
            regions.forEach(region => {
                const option = document.createElement('option');
                option.value = region.code;
                option.textContent = region.name;
                if (region.name === userData.state) {
                    option.selected = true;
                }
                stateInput.appendChild(option);
            });
            
            // Trigger change event to load provinces if state is selected
            if (userData.state) {
                stateInput.dispatchEvent(new Event('change'));
            }
        })
        .catch(error => {
            console.error('Error loading regions:', error);
            alert('Error loading regions. Please try again later.');
        });

    // Add event listeners for cascading dropdowns
    stateInput.addEventListener('change', function() {
        loadProvinces(this.value, userData.city_or_province);
    });

    cityProvinceInput.addEventListener('change', function() {
        loadMunicipalities(this.value, userData.municipality);
    });
}

// Load provinces based on selected region
function loadProvinces(regionCode, selectedProvince) {
    const cityProvinceInput = document.getElementById('city-province-input');
    cityProvinceInput.innerHTML = '<option value="">Select City/Province</option>';
    cityProvinceInput.disabled = true;

    if (regionCode) {
        fetch('../../../backend/python/routes/geo/province.json')
            .then(response => response.json())
            .then(provinces => {
                provinces.forEach(province => {
                    const option = document.createElement('option');
                    option.value = province.code;
                    option.textContent = province.name;
                    if (province.name === selectedProvince) {
                        option.selected = true;
                    }
                    cityProvinceInput.appendChild(option);
                });
                cityProvinceInput.disabled = false;

                // Trigger change event to load municipalities if province is selected
                if (selectedProvince) {
                    cityProvinceInput.dispatchEvent(new Event('change'));
                }
            })
            .catch(error => {
                console.error('Error loading provinces:', error);
                alert('Error loading provinces. Please try again later.');
            });
    }
}

// Load municipalities based on selected province
function loadMunicipalities(provinceCode, selectedMunicipality) {
    const municipalityInput = document.getElementById('municipality-input');
    municipalityInput.innerHTML = '<option value="">Select Municipality</option>';
    municipalityInput.disabled = true;

    if (provinceCode) {
        fetch('../../../backend/python/routes/geo/municipality.json')
            .then(response => response.json())
            .then(municipalities => {
                municipalities.forEach(municipality => {
                    const option = document.createElement('option');
                    option.value = municipality.code;
                    option.textContent = municipality.name;
                    if (municipality.name === selectedMunicipality) {
                        option.selected = true;
                    }
                    municipalityInput.appendChild(option);
                });
                municipalityInput.disabled = false;
            })
            .catch(error => {
                console.error('Error loading municipalities:', error);
                alert('Error loading municipalities. Please try again later.');
            });
    }
}
