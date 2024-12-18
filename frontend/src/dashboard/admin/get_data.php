<?php
require_once '../../../includes/connection.php';


function fetch_data($conn, $query) {
    $result = '';
    $stmt = $conn->prepare($query);
    if ($stmt && $stmt->execute()) {
        $stmt->bind_result($result);
        $stmt->fetch();
        $stmt->close();
        return $result;
    }// Default value if query fails
}

//  response data
$data = [
    'tech_grad' => 0,
    'employers' => 0,
    'jobs' => 0
];

$conn = $db->get_conn();

// Use the reusable function
$data['tech_grad'] = fetch_data($conn, 'SELECT COUNT(user_id) FROM users');
$data['employers'] = fetch_data($conn, 'SELECT COUNT(employer_id) FROM employers');
$data['jobs'] = fetch_data($conn, 'SELECT COUNT(job_id) FROM jobs');

// Return the JSON response
header('Content-Type: application/json');
echo json_encode($data, JSON_PRETTY_PRINT);
exit;
?>
