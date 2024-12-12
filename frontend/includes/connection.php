<?php
class Database {
    private $conn;
    
    function __construct($server, $username, $password, $database){
        $this->conn = new mysqli($server, $username, $password, $database);
        
        if ($this->conn->connect_error){
            die ('err: ' . $this->conn->connect_error);
        }
    }

    // function avoid_inject($data){
    //     return $this->conn->real_escape_string($data);
    // }

    public function get_conn() {
        return $this->conn;
    }

    function __destruct(){
        if ($this->conn) {
            $this->conn->close();
        }
    }
}

$db = new Database('localhost', 'root', '', 'jobsearch');


?>