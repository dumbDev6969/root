<?php
require_once '../../../includes/connection.php';

// response
$data = [
    'tech_grad' => 0,
    'employers' => 0
];

$conn = $db->get_conn();


$stmt = $conn->prepare('SELECT COUNT(user_id) FROM users');
if ($stmt && $stmt->execute()) {
    $stmt->bind_result($tech_count);
    $stmt->fetch();
    $data['tech_grad'] = $tech_count;
}
$stmt->close();


$stmt = $conn->prepare('SELECT COUNT(employer_id) FROM employers');
if ($stmt && $stmt->execute()) {
    $stmt->bind_result($emp_count);
    $stmt->fetch();
    $data['employers'] = $emp_count;
}
$stmt->close();


header('Content-Type: application/json');
echo json_encode($data, JSON_PRETTY_PRINT);
exit;
?>
