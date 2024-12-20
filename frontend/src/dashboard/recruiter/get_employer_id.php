<?php
// Prevent any output before headers
ini_set('display_errors', 0);
error_reporting(0);

// Start session
session_start();

// Set JSON header
header('Content-Type: application/json');

// Check if user is logged in and is an employer
if (!isset($_SESSION['isLoggedIn']) || !$_SESSION['isLoggedIn'] || $_SESSION['userType'] !== 'employer') {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

// Check if employer data exists in session
if (!isset($_SESSION['employerData']) || !isset($_SESSION['employerData']['employer_id'])) {
    http_response_code(400);
    echo json_encode(['error' => 'No employer data found']);
    exit;
}

// Return the employer_id
echo json_encode([
    'success' => true,
    'employer_id' => $_SESSION['employerData']['employer_id']
]);
?>