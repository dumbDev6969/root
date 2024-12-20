<?php
// Prevent any output before headers
ini_set('display_errors', 0);
error_reporting(0);

// Set headers first
header('Content-Type: application/json');

// Start session if not already started
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Clear all session data
$_SESSION = array();

// Delete the session cookie
if (isset($_COOKIE[session_name()])) {
    setcookie(session_name(), '', time() - 3600, '/');
}

// Destroy the session
session_destroy();

// Clear session from server storage
session_write_close();

if (isset($_SERVER['HTTP_X_REQUESTED_WITH']) && 
    strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest') {
    // AJAX request, return JSON response
    echo json_encode(['status' => 'success', 'message' => 'Logged out successfully']);
} else {
    // Regular request, redirect to login page
    header('Location: login.php');
    exit;
}
?>