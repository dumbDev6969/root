<?php
require_once '../includes/connection.php';

$store_data = '';

$columns = ['job_title', 'salary_range', 'job_type']; // data to retriev

$columns_list = implode(',', array_map(function($col) {
    return '`' . $col . '`'; 
}, $columns));

$stmt = $db->get_conn()->prepare('SELECT '.$columns_list.' FROM jobs LIMIT 10;');

if ($stmt->execute()) {

    $stmt->bind_result($job, $salary, $job_type); // bind the results

    while ($stmt->fetch()) {
        $store_data .= '
                <div class="card mt-5 border-0" style="width: 24rem;">
                    <div class="card-body">
                        <h5 class="card-title">' . htmlspecialchars($job) . '</h5>
                        <h6 class="card-subtitle mb-2 text-body-secondary">' . htmlspecialchars($job_type) . '</h6>
                        <p class="">' . htmlspecialchars($salary) . '</p>
                    </div>
                </div>';
            
    }
    //echo $store_data;
} else {
    echo "Error executing query: " . $stmt->error;
}
?>
