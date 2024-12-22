# Frontend JWT Integration Guide

## Overview

This guide explains how to integrate JWT (JSON Web Token) authentication with the frontend application. Our backend uses a secure JWT implementation with access and refresh tokens, along with support for two-factor authentication (2FA).

## Authentication Flow

### 1. Login Process

```javascript
async function login(email, password) {
    try {
        const response = await fetch('http://localhost:10000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password }),
            credentials: 'include' // Important for cookie handling
        });

        const data = await response.json();

        if (data.two_factor_enabled) {
            // Redirect to 2FA verification
            window.location.href = `/2fa-verify.html?user_id=${data.user_id}`;
        } else {
            // Store user type and redirect
            localStorage.setItem('user_type', data.user_type);
            redirectBasedOnUserType(data.user_type);
        }
    } catch (error) {
        console.error('Login failed:', error);
    }
}
```

### 2. JWT Token Management

```javascript
// Utility functions for JWT handling
const TokenManager = {
    getAccessToken() {
        return localStorage.getItem('access_token');
    },

    setAccessToken(token) {
        localStorage.setItem('access_token', token);
    },

    removeTokens() {
        localStorage.removeItem('access_token');
    },

    // Add Authorization header to requests
    getAuthHeaders() {
        const token = this.getAccessToken();
        return token ? { 'Authorization': `Bearer ${token}` } : {};
    }
};
```

### 3. Protected API Requests

```javascript
async function makeAuthenticatedRequest(url, options = {}) {
    try {
        const headers = {
            ...options.headers,
            ...TokenManager.getAuthHeaders()
        };

        const response = await fetch(url, {
            ...options,
            headers,
            credentials: 'include'
        });

        if (response.status === 401) {
            // Token expired or invalid
            // Redirect to login
            window.location.href = '/login.html';
            return null;
        }

        return await response.json();
    } catch (error) {
        console.error('Request failed:', error);
        return null;
    }
}
```

### 4. Two-Factor Authentication

```javascript
async function verify2FA(userId, token) {
    try {
        const response = await fetch('http://localhost:10000/2fa/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: userId, token }),
            credentials: 'include'
        });

        const data = await response.json();
        if (data.success) {
            // Store user type and redirect
            localStorage.setItem('user_type', data.user_type);
            redirectBasedOnUserType(data.user_type);
        }
    } catch (error) {
        console.error('2FA verification failed:', error);
    }
}
```

## Implementation Steps

1. **Initialize Authentication**:
   ```javascript
   // Add to your main.js or similar
   document.addEventListener('DOMContentLoaded', () => {
       // Check if user is authenticated
       const token = TokenManager.getAccessToken();
       if (!token) {
           window.location.href = '/login.html';
       }
   });
   ```

2. **Protected Routes**:
   ```javascript
   // Add to each protected page
   function checkAuth() {
       const token = TokenManager.getAccessToken();
       if (!token) {
           window.location.href = '/login.html';
           return false;
       }
       return true;
   }
   ```

3. **Logout Implementation**:
   ```javascript
   async function logout() {
       try {
           await fetch('http://localhost:10000/logout', {
               method: 'POST',
               headers: TokenManager.getAuthHeaders(),
               credentials: 'include'
           });
       } catch (error) {
           console.error('Logout failed:', error);
       } finally {
           TokenManager.removeTokens();
           window.location.href = '/login.html';
       }
   }
   ```

## Error Handling

```javascript
function handleAuthError(error) {
    if (error.status === 401) {
        // Unauthorized - redirect to login
        TokenManager.removeTokens();
        window.location.href = '/login.html';
    } else if (error.status === 403) {
        // Forbidden - user doesn't have permission
        alert('You do not have permission to access this resource');
    } else {
        // Other errors
        console.error('Authentication error:', error);
        alert('An error occurred. Please try again later.');
    }
}
```

## Security Best Practices

1. **Token Storage**:
   - Store tokens in memory for SPAs
   - Use HttpOnly cookies for refresh tokens
   - Clear tokens on logout

2. **Request Security**:
   - Always use HTTPS in production
   - Include CSRF protection
   - Implement request timeouts

3. **Error Handling**:
   - Never expose sensitive information in error messages
   - Implement proper logging
   - Handle all error cases gracefully

## Example Usage

### Profile Page Implementation

```javascript
// profile.js
document.addEventListener('DOMContentLoaded', async () => {
    if (!checkAuth()) return;

    try {
        const profile = await makeAuthenticatedRequest('http://localhost:10000/api/profile/current');
        if (profile) {
            displayProfile(profile);
        }
    } catch (error) {
        handleAuthError(error);
    }
});
```

### Job Application Implementation

```javascript
// job-application.js
async function submitApplication(jobId, applicationData) {
    if (!checkAuth()) return;

    try {
        const result = await makeAuthenticatedRequest(
            `http://localhost:10000/api/jobs/apply`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    job_id: jobId,
                    ...applicationData
                })
            }
        );

        if (result.success) {
            alert('Application submitted successfully!');
            window.location.href = '/applications.html';
        }
    } catch (error) {
        handleAuthError(error);
    }
}
```

## Testing

1. **Token Validation**:
   ```javascript
   function isTokenValid(token) {
       if (!token) return false;
       try {
           const payload = JSON.parse(atob(token.split('.')[1]));
           return payload.exp > Date.now() / 1000;
       } catch (error) {
           return false;
       }
   }
   ```

2. **Authentication Check**:
   ```javascript
   async function checkAuthStatus() {
       try {
           const response = await makeAuthenticatedRequest('http://localhost:10000/api/auth/status');
           return response.authenticated === true;
       } catch (error) {
           return false;
       }
   }
   ```

## Troubleshooting

1. **Common Issues**:
   - Token expiration handling
   - CORS configuration
   - Cookie settings
   - 2FA flow interruptions

2. **Solutions**:
   - Implement proper token refresh
   - Configure CORS headers correctly
   - Set appropriate cookie attributes
   - Handle 2FA state properly

## Additional Resources

- Backend API Documentation
- Security Guidelines
- Error Code Reference
- Testing Documentation

For more detailed information about specific endpoints and responses, refer to the API documentation.