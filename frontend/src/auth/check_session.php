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

// Check if user is logged in and session is valid
if (isset($_SESSION['isLoggedIn']) && $_SESSION['isLoggedIn'] === true) {
    if (isset($_SESSION['userType'])) {
        // Return full session data for the dashboard
        echo json_encode([
            'loggedIn' => true,
            'userType' => $_SESSION['userType'],
            'status' => 'success',
            'employerData' => isset($_SESSION['employerData']) ? $_SESSION['employerData'] : null,
            'userData' => isset($_SESSION['userData']) ? $_SESSION['userData'] : null
        ]);
    } else {
        // Session exists but missing user type
        session_unset();
        session_destroy();
        echo json_encode([
            'loggedIn' => false,
            'userType' => null,
            'status' => 'error',
            'message' => 'Invalid session state'
        ]);
    }
} else {
    // No active session
    echo json_encode([
        'loggedIn' => false,
        'userType' => null,
        'status' => 'success',
        'message' => 'No active session'
    ]);
}
?>