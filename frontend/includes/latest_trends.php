<?php
require_once '../includes/connection.php';

$store_data = '';

$columns = ['title', 'salary_range', 'job_type']; // data to retrieve

$columns_list = implode(',', array_map(function($col) {
    return '`' . $col . '`'; 
}, $columns));

$stmt = $db->get_conn()->prepare('SELECT '.$columns_list.' FROM jobs LIMIT 10;');

if ($stmt->execute()) {

    $stmt->bind_result($title, $salary_range, $job_type); // bind the results to match selected columns

    while ($stmt->fetch()) {
        $store_data .= '
                <div class="card mt-5 border-0" style="width: 250px">
                    <div class="card-body">
                        <h5 class="card-title">' . htmlspecialchars($title) . '</h5>
                        <h6 class="card-subtitle mb-2 text-body-secondary">' . htmlspecialchars($job_type) . '</h6>
                        <p class="">' . htmlspecialchars($salary_range) . '</p>
                    </div>
                </div>
                ';
            
    }
    //echo $store_data;
} else {
    echo "Error executing query: " . $stmt->error;
}
?>
