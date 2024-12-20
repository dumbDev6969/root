<?php
// Prevent any output before headers
ini_set('display_errors', 0);
error_reporting(0);

// Configure session
ini_set('session.cookie_lifetime', '86400'); // 24 hours
ini_set('session.gc_maxlifetime', '86400'); // 24 hours

// Set headers first
header('Content-Type: application/json');

// Start session with secure parameters
session_set_cookie_params([
    'lifetime' => 86400,
    'path' => '/',
    'domain' => '',
    'secure' => true,
    'httponly' => true,
    'samesite' => 'Strict'
]);
session_start();

// Function to validate personal info data
function validatePersonalInfo($data) {
    if (!is_array($data)) {
        return false;
    }

    $requiredFields = ['first_name', 'last_name', 'email'];
    foreach ($requiredFields as $field) {
        if (!isset($data[$field]) || empty(trim($data[$field]))) {
            return false;
        }
    }

    // Validate email format
    if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
        return false;
    }

    return true;
}

try {
    // Check request method
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        throw new Exception('Invalid request method');
    }

    // Get JSON input
    $input = file_get_contents('php://input');
    if (!$input) {
        throw new Exception('No input data provided');
    }

    // Decode JSON
    $data = json_decode($input, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception('Invalid JSON data');
    }

    // Validate personal info
    if (!isset($data['personal_info']) || !validatePersonalInfo($data['personal_info'])) {
        throw new Exception('Invalid personal info data');
    }

    // Store data in session
    $personal_info = $data['personal_info'];
    
    // Determine user type from the data
    if (isset($personal_info['employer_id'])) {
        $_SESSION['employerData'] = $personal_info;
        $_SESSION['userType'] = 'employer';
    } else {
        $_SESSION['userData'] = $personal_info;
        $_SESSION['userType'] = 'user';
    }
    
    $_SESSION['isLoggedIn'] = true;

    // Force session write
    session_write_close();
    session_start();

    // Verify session was stored correctly
    if (!isset($_SESSION['isLoggedIn']) || !$_SESSION['isLoggedIn']) {
        throw new Exception('Failed to store session data');
    }

    if ($_SESSION['userType'] === 'employer' && !isset($_SESSION['employerData'])) {
        throw new Exception('Failed to store employer data');
    }

    if ($_SESSION['userType'] === 'user' && !isset($_SESSION['userData'])) {
        throw new Exception('Failed to store user data');
    }

    // Return success response
    echo json_encode([
        'status' => 'success',
        'message' => 'Session data stored successfully',
        'userType' => $_SESSION['userType']
    ]);

} catch (Exception $e) {
    // Clear any partial session data on error
    session_unset();
    session_destroy();

    // Return error response
    http_response_code(400);
    echo json_encode([
        'status' => 'error',
        'message' => $e->getMessage()
    ]);
}
?>