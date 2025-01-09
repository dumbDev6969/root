// Form validation and submission handler
async function handleFormSubmission(form, type) {
    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...';

    try {
        const formData = new FormData(form);
        const data = {};
        
        // Validation rules
        const validations = {
            'edit-email': {
                required: true,
                pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                message: 'Please enter a valid email address'
            },
            'edit-first-name': {
                required: true,
                pattern: /^[a-zA-Z\s]{2,}$/,
                message: 'First name must be at least 2 characters and contain only letters'
            },
            'edit-last-name': {
                required: true,
                pattern: /^[a-zA-Z\s]{2,}$/,
                message: 'Last name must be at least 2 characters and contain only letters'
            },
            'edit-phone': {
                pattern: /^\d{10,}$/,
                transform: value => value.replace(/\D/g, ''),
                message: 'Please enter a valid phone number (at least 10 digits)'
            }
        };

        // Collect and validate form data
        const errors = [];
        formData.forEach((value, key) => {
            if (key === 'edit-confirm-password') return;
            
            const cleanValue = value.trim();
            if (!cleanValue) {
                if (validations[key]?.required) {
                    errors.push(`${key.replace('edit-', '').replace(/-/g, ' ')} is required`);
                }
                return;
            }

            // Validate if rules exist
            if (validations[key]) {
                const rule = validations[key];
                const valueToTest = rule.transform ? rule.transform(cleanValue) : cleanValue;
                if (rule.pattern && !rule.pattern.test(valueToTest)) {
                    errors.push(rule.message);
                    return;
                }
            }

            data[key] = cleanValue;
        });

        // Check password if provided
        const password = formData.get('edit-password');
        const confirmPassword = formData.get('edit-confirm-password');
        if (password || confirmPassword) {
            if (password !== confirmPassword) {
                errors.push('Passwords do not match');
            } else if (password.length < 8 || password.length > 16) {
                errors.push('Password must be between 8 and 16 characters');
            }
        }

        if (errors.length > 0) {
            throw new Error(errors.join('\n'));
        }

        const formattedData = {};
        Object.entries(data).forEach(([key, value]) => {
            const apiKey = key.replace('edit-', '').replace(/-/g, '_');
            
            // Compare with original data and only include changes
            if (userData[apiKey] !== value) {
                // Special handling for select elements
                if (['state', 'city_or_province', 'municipality'].includes(apiKey)) {
                    const select = document.getElementById(key + '-input');
                    if (select && select.selectedIndex >= 0) {
                        formattedData[apiKey] = select.options[select.selectedIndex].text;
                    }
                } else {
                    formattedData[apiKey] = value;
                }
            }
        });

        
        // Fix field name mismatch
        if (formattedData.phone) {
            formattedData.phone_number = formattedData.phone;
            delete formattedData.phone;
        }
        
        if (formattedData.street_number) {
            formattedData.street = formattedData.street_number;
            delete formattedData.street_number;
        }
        
        // Remove redundant user_id field
        delete formattedData.user_id;
        
        // Validate zip_code length
        if (formattedData.zip_code && formattedData.zip_code.length > 10) {
            formattedData.zip_code = formattedData.zip_code.slice(0, 10);
        }

        // Debugging: Log formatted data
        console.log("Formatted Data:", formattedData);

        // Prepare request body
        const requestBody = {
            table: "users",
            id: userData.user_id,
            data: formattedData
        };
        console.log("Request Body:", JSON.stringify(requestBody, null, 2));

        // Send update request with retry logic
        let retries = 3;
        let response;
        while (retries > 0) {
            try {
                response = await fetch('https://root-4ytd.onrender.com/api/update', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify(requestBody)
                });
                break;
            } catch (error) {
                retries--;
                if (retries === 0) throw new Error('Could not connect to server. Please try again later.');
                await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second before retry
            }
        }

        // Parse and check API response
        const result = await response.json();
        
        // Log the full response for debugging
        console.log("Server response:", result);
        
        if (!response.ok) {
            throw new Error(result.message || `Server error: ${response.status}`);
        }
        
        // Check if the response indicates success (handle both success formats)
        if (result.success === true || result.status === 'success' || result.message==='User updated successfully.' ) {
            // Handle successful update
            console.log("Success:", result.message);
            
            // Update session data
            const sessionResponse = await fetch('../../auth/store_session.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    personal_info: {
                        ...userData,
                        ...formattedData
                    }
                })
            });
        
            const sessionResult = await sessionResponse.json();
            
            // Update local data regardless of session update
            Object.assign(userData, formattedData);
            
            // Show success message and reload
            alert(`${type === 'personal' ? 'Personal information' : 'Job preferences'} updated successfully!`);
            setTimeout(() => window.location.reload(), 1000);
            return;
        }
        
        // Handle non-success response
        throw new Error(result.message || 'Update failed');

        // Success case is now handled in the session update block above

    } catch (error) {
        console.error('Error updating profile:', error);
        
        // Handle specific error types
        let errorMessage;
        if (error.message.includes('Could not connect to server')) {
            errorMessage = 'Could not connect to server. Please check your internet connection and try again.';
        } else if (error.message.includes('Invalid server response')) {
            errorMessage = 'Server returned an invalid response. Please try again later.';
        } else if (error.message.includes('session refresh failed')) {
            errorMessage = 'Your session has expired. Please log in again.';
            // Redirect to login after error
            setTimeout(() => {
                window.location.href = '../../auth/login.php';
            }, 2000);
        } else {
            errorMessage = error.message;
        }
        
        alert(`Error: ${errorMessage}`);
    } finally {
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.innerHTML = 'Save changes';
        }
        
        // Re-enable all form inputs
        const inputs = form.querySelectorAll('input, select, button');
        inputs.forEach(input => input.disabled = false);
    }
}

// Initialize form handlers
document.addEventListener('DOMContentLoaded', function() {
    ['personal-info-form', 'job-preferences-form'].forEach(formId => {
        document.getElementById(formId)?.addEventListener('submit', async function(event) {
            event.preventDefault();
            await handleFormSubmission(this, formId === 'personal-info-form' ? 'personal' : 'preferences');
        });
    });
});