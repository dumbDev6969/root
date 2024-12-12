
let selected_region = null;
fetch('http://127.0.0.1:11352/api/regions/')
.then(response => {
if (!response.ok) {
throw new Error('Network response was not ok ' + response.statusText);
}
return response.json();
})
.then(data => {
const selectElement = document.getElementById('state-input');

// Loop through the new regions and create option elements
data.forEach(region => {
const option = document.createElement('option');
option.value = region.code; // Set the value attribute
option.textContent = region.name; // Set the display text
selectElement.appendChild(option); // Append the option to the select element
});

// Add an event listener to the select element
selectElement.addEventListener('change', function() {
const selectedValue = selectElement.value; // Get the selected value
selected_region = selectedValue;
document.getElementById("city-province-input").disabled = false;
//     http://127.0.0.1:11352/api/regions/{selectedValue}/provinces/
// Fetch provinces based on the selected region
fetch(`http://127.0.0.1:11352/api/regions/${selected_region}/provinces/`)
.then(response => {
if (!response.ok) {
throw new Error('Network response was not ok ' + response.statusText);
}
return response.json();
})
.then(provinces => {
const cityProvinceSelect = document.getElementById("city-province-input");
cityProvinceSelect.innerHTML = ''; // Clear previous options

// Add a default option
const defaultOption = document.createElement('option');
defaultOption.value = '';
defaultOption.disabled = true;
defaultOption.selected = true;
defaultOption.textContent = 'Select City/Province';
cityProvinceSelect.appendChild(defaultOption);

// Loop through the provinces and create option elements
provinces.forEach(province => {
const option = document.createElement('option');
option.value = province.code; // Set the value attribute
option.textContent = province.name; // Set the display text
cityProvinceSelect.appendChild(option); // Append the option to the select element http://127.0.0.1:11352/api/provinces/015500000/municipalities/


cityProvinceSelect.addEventListener('change', function() {
const selectedValue = cityProvinceSelect.value; // Get the selected value
selected_region = selectedValue;
document.getElementById("municipality-input").disabled = false;
//     http://127.0.0.1:11352/api/regions/{selectedValue}/provinces/
// Fetch provinces based on the selected region
fetch(`http://127.0.0.1:11352/api/provinces/${selected_region}/municipalities/`)
.then(response => {
if (!response.ok) {
throw new Error('Network response was not ok ' + response.statusText);
}
return response.json();
})
.then(municipalities => {
const municipalitiesSelect = document.getElementById("municipality-input");
municipalitiesSelect.innerHTML = ''; // Clear previous options

// Add a default option
const defaultOption = document.createElement('option');
defaultOption.value = '';
defaultOption.disabled = true;
defaultOption.selected = true;
defaultOption.textContent = 'Select municipality';
municipalitiesSelect.appendChild(defaultOption);

// Loop through the provinces and create option elements
municipalities.forEach(municipality => {
console.log(municipality.code,municipality.name);
const option = document.createElement('option');
option.value = municipality.code; // Set the value attribute
option.textContent = municipality.name; // Set the display text
municipalitiesSelect.appendChild(option); // Append the option to the select element http://127.0.0.1:11352/api/provinces/015500000/municipalities/

});
})
.catch(error => {
console.error('There was a problem with the fetch operation for provinces:', error);
});

});
});
})
.catch(error => {
console.error('There was a problem with the fetch operation for provinces:', error);
});

});
})
.catch(error => {
console.error('There was a problem with the fetch operation:', error);
});
