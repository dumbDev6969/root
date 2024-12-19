import mysql.connector
from mysql.connector import pooling
import sqlite3
import os
from typing import Optional, List, Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass

class Database:
    def __init__(self, host: str, user: str, password: str, database: str, db_path: str = 'fallback_db.sqlite', pool_size: int = 20) -> None:
        """Initialize the Database class with an attempt to connect to MySQL, fallback to SQLite."""
        self.db_type = None
        try:
            dbconfig = {
                "pool_name": "mypool",
                "pool_size": pool_size,
                "host": "mysql-24a8087-mysql-server-jobs.c.aivencloud.com",
                "user": "avnadmin",
                "password": "AVNS_RCkju8DXtGBZrSXcWqk",
                "database": "jobsearch",
                "port": 16459,
                "charset": "utf8mb4",
                "connect_timeout": 10,
                "pool_reset_session": True,
                "autocommit": True,
                "get_warnings": True,
                "raise_on_warnings": True,
                "consume_results": True
            }
            self.pool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
            self.db_type = 'mysql'
            logger.info(f"MySQL database connection pool created successfully with size {pool_size}")
        except mysql.connector.Error as e:
            logger.error(f"Error creating MySQL connection pool: {e}, trying SQLite fallback")
            try:
                # Connection just for validation, not to keep it open
                conn = sqlite3.connect(db_path)
                conn.close()
                self.db_path = db_path
                self.db_type = 'sqlite'
                logger.info("SQLite database initialized successfully as fallback")
            except sqlite3.Error as e:
                logger.error(f"Error initializing SQLite database: {e}")
                raise DatabaseError(f"Failed to initialize any database connection: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db_type == 'mysql':
            self.close()

    def get_connection(self):
        """Get a new connection depending on the DB type."""
        if self.db_type == 'mysql':
            retries = 3
            while retries > 0:
                try:
                    connection = self.pool.get_connection()
                    if connection.is_connected():
                        return connection
                except mysql.connector.Error as e:
                    logger.error(f"Error getting connection from pool (retries left: {retries-1}): {e}")
                    retries -= 1
                    if retries == 0:
                        raise DatabaseError(f"Failed to get connection after 3 attempts: {e}")
            return None
        elif self.db_type == 'sqlite':
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            # Enable foreign key constraints for SQLite
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        else:
            raise DatabaseError("No database connection type is set.")
    def execute_query(self, sql: str, params: Optional[tuple] = ()) -> Optional[List[Dict[str, Any]]]:
        """Execute a SQL query with optional parameters."""
        conn = None
        cursor = None
        retries = 3
        last_error = None

        while retries > 0:
            try:
                conn = self.get_connection()
                if not conn:
                    retries -= 1
                    continue

                if self.db_type == 'sqlite':
                    params = tuple(params) if params else ()
                    cursor = conn.cursor()
                else:
                    cursor = conn.cursor(dictionary=True)

                cursor.execute(sql, params)
                if sql.strip().upper().startswith("SELECT"):
                    result = cursor.fetchall()
                else:
                    conn.commit()
                    result = cursor.lastrowid
                return result

            except (mysql.connector.Error, sqlite3.Error) as e:
                last_error = e
                logger.error(f"Database error (retries left: {retries-1}): {e}")
                if conn:
                    try:
                        conn.rollback()
                    except:
                        pass
                retries -= 1
                if retries == 0:
                    raise DatabaseError(f"Failed to execute query after 3 attempts: {e}")

            finally:
                if cursor:
                    try:
                        cursor.close()
                    except:
                        pass
                if conn:
                    try:
                        if self.db_type == 'mysql':
                            conn.close()  # Return connection to pool
                        else:
                            conn.close()  # Close SQLite connection
                    except Exception as e:
                        logger.error(f"Error closing connection: {e}")

    def execute_multiple_queries(self, sql: str) -> None:
        """Execute multiple SQL queries separated by semicolons."""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Split the SQL string into individual statements
            statements = sql.split(';')
            for statement in statements:
                if statement.strip():  # Skip empty statements
                    cursor.execute(statement)
            conn.commit()
        except (mysql.connector.Error, sqlite3.Error) as e:
            logger.error(f"Database error: {e}")
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise DatabaseError(f"Failed to execute multiple queries: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                if self.db_type == 'mysql':
                    conn.close()  # Return connection to pool
                else:
                    conn.close()  # Close SQLite connection

    def import_sql_file(self, file_path: str,sql_content:str) -> None:
        """Import an SQL file into the database."""
        if self.db_type == 'mysql':
            try:
                
                self.execute_multiple_queries(sql_content)
                logger.info(f"SQL file {file_path} imported successfully into MySQL database.")
            except Exception as e:
                logger.error(f"Failed to import SQL file {file_path} into MySQL: {e}")
                raise DatabaseError(f"Failed to import SQL file {file_path} into MySQL: {e}")
        elif self.db_type == 'sqlite':
            absolute_path = os.path.abspath(file_path)
            if not os.path.exists(absolute_path):
                logger.error(f"SQL file not found: {absolute_path}")
                raise FileNotFoundError(f"SQL file not found: {absolute_path}")
            file_path = absolute_path
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    sql_content = file.read()
                self.execute_multiple_queries(sql_content)
                logger.info(f"SQL file {file_path} imported successfully into SQLite database.")
            except Exception as e:
                logger.error(f"Failed to import SQL file {file_path} into SQLite: {e}")
                raise DatabaseError(f"Failed to import SQL file {file_path} into SQLite: {e}")
        else:
            logger.error("SQL file import is not supported for the current database type.")
            raise DatabaseError("SQL file import is not supported for the current database type.")
        
        if not os.path.exists(file_path):
            logger.error(f"SQL file not found: {file_path}")
            raise FileNotFoundError(f"SQL file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
            self.execute_multiple_queries(sql_content)
            logger.info(f"SQL file {file_path} imported successfully.")
        except Exception as e:
            logger.error(f"Failed to import SQL file {file_path}: {e}")
            raise DatabaseError(f"Failed to import SQL file {file_path}: {e}")

    def close(self) -> None:
        """Close the MySQL database connection pool."""
        if self.db_type == 'mysql':
            self.pool.close()
            logger.info("MySQL Database connection pool closed")

# Initialize the database connection
db = Database(
    host="mysql-24a8087-mysql-server-jobs.c.aivencloud.com",
    user="avnadmin",
    password="AVNS_RCkju8DXtGBZrSXcWqk",
    database="jobsearch",
    pool_size=32
)


a="""
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 19, 2024 at 06:58 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `jobsearch`
--
CREATE DATABASE IF NOT EXISTS `jobsearch` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `jobsearch`;

-- --------------------------------------------------------

--
-- Table structure for table `employers`
--

CREATE TABLE `employers` (
  `employer_id` int(11) NOT NULL,
  `company_name` varchar(30) NOT NULL,
  `phone_number` varchar(12) NOT NULL,
  `state` varchar(20) NOT NULL,
  `city_or_province` varchar(30) DEFAULT NULL,
  `zip_code` varchar(10) NOT NULL,
  `street` varchar(10) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employers`
--

INSERT INTO `employers` (`employer_id`, `company_name`, `phone_number`, `state`, `city_or_province`, `zip_code`, `street`, `email`, `password`, `created_at`, `updated_at`) VALUES
(1, 'Tech Solutions', '1234567890', 'California', 'Los Angeles', '90001', 'Main St', 'contact@techsolutions.com', 'hashedpassword1', '2024-12-11 17:20:28', '2024-12-11 17:20:28'),
(2, 'Innovatech', '0987654321', 'New York', 'New York City', '10001', 'Broadway', 'info@innovatech.com', 'hashedpassword2', '2024-12-11 17:20:28', '2024-12-11 17:20:28'),
(4, 'Innovatech', '0987654321', '010000000', '', '10001', '007', 'jemcarlo46@gmail.com', '$argon2id$v=19$m=65536,t=3,p=4$IJ7e9XwSDoS2P1tX7Qe8BA$u4Sco8oeI/w2ukK94H0CaXP/jM5nxR9mdb9UfNX9lg4', '2024-12-11 17:22:16', '2024-12-16 16:15:02'),
(8, 'Jemcarlo Austria', '09207766194', '020000000', NULL, '2413', '007', 'jemcarlo40@gmail.com', 'Abcd.123', '2024-12-16 00:00:00', '2024-12-16 00:00:00'),
(11, 'Jemcarlo Austria', '09207766194', '020000000', NULL, '2413', '007', 'jemcarlo43@gmail.com', 'Abcd.123', '2024-12-16 00:00:00', '2024-12-16 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `job_id` int(11) NOT NULL,
  `employer_id` int(11) NOT NULL,
  `job_title` varchar(30) NOT NULL,
  `job_type` enum('Full-time','Part-time','Freelance','Internship') NOT NULL,
  `location` varchar(50) NOT NULL,
  `salary_range` varchar(50) NOT NULL,
  `job_description` text NOT NULL,
  `requirements` text NOT NULL,
  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jobs`
--

INSERT INTO `jobs` (`job_id`, `employer_id`, `job_title`, `job_type`, `location`, `salary_range`, `job_description`, `requirements`, `created_at`) VALUES
(1, 1, 'Software Engineer', 'Full-time', 'Remote', '$70,000 - $90,000', 'Develop and maintain software applications.', 'Bachelor\'s degree in Computer Science', '2024-12-11 17:20:28'),
(2, 2, 'Data Analyst', 'Part-time', 'New York City', '$50,000 - $70,000', 'Analyze data and generate reports.', 'Experience with SQL and Python', '2024-12-11 17:20:28'),
(3, 1, 'Software Engineer', 'Full-time', 'Remote', '$70,000 - $90,000', 'Develop and maintain software applications.', 'Bachelors degree in Computer Science', '2024-12-11 17:22:16'),
(4, 2, 'Data Analyst', 'Part-time', 'New York City', '$50,000 - $70,000', 'Analyze data and generate reports.', 'Experience with SQL and Python', '2024-12-11 17:22:16'),
(5, 1, 'asdasd', 'Full-time', 'adasd', '111', 'asdasd', 'adasd', '2024-12-16 12:45:23'),
(6, 1, 'sample', 'Full-time', 'adasd', '100', 'sample', 'sample', '2024-12-16 04:46:22'),
(7, 4, 'ddd', 'Full-time', 'ddd', '666', 'tttt', 'tttt', '2024-12-16 04:57:38'),
(8, 4, 'ASDASDASD', 'Full-time', 'GGGG', '555', 'HHH', 'HHH', '2024-12-16 05:19:43'),
(9, 4, 'asdasdsad', 'Full-time', 'kkasdk', '123123', 'asdasd', 'adasd', '2024-12-16 05:22:16'),
(10, 4, 'job1', 'Full-time', 'asdas', '1000', 'job1', 'python', '2024-12-16 05:24:22'),
(11, 4, 'job2', 'Full-time', 'job2', '123', '123', '123', '2024-12-16 05:42:56'),
(12, 4, 'job23', 'Full-time', 'qweeq', '	12332', '12312', '123123', '2024-12-16 07:02:31');

-- --------------------------------------------------------

--
-- Table structure for table `qualifications`
--

CREATE TABLE `qualifications` (
  `qualification_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `degree` varchar(30) NOT NULL,
  `school_graduated` varchar(40) NOT NULL,
  `certifications` varchar(255) DEFAULT NULL,
  `specialized_training` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `qualifications`
--

INSERT INTO `qualifications` (`qualification_id`, `user_id`, `degree`, `school_graduated`, `certifications`, `specialized_training`) VALUES
(3, 1, 'B.Sc. Computer Science', 'MIT', 'Certified Java Developer', 'Machine Learning'),
(4, 2, 'M.Sc. Data Science', 'Stanford University', NULL, 'Data Analysis');

-- --------------------------------------------------------

--
-- Table structure for table `saved_jobs`
--

CREATE TABLE `saved_jobs` (
  `saved_job_id` int(11) NOT NULL,
  `saved_at` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `job_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `saved_jobs`
--

INSERT INTO `saved_jobs` (`saved_job_id`, `saved_at`, `user_id`, `job_id`) VALUES
(1, '2024-12-11 17:22:16', 1, 1),
(2, '2024-12-11 17:22:16', 2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `submitted_resume`
--

CREATE TABLE `submitted_resume` (
  `submitted_resume_id` int(11) NOT NULL,
  `resume_file_name` varchar(50) NOT NULL,
  `resume_path` varchar(50) NOT NULL,
  `submitted_at` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `job_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `submitted_resume`
--

INSERT INTO `submitted_resume` (`submitted_resume_id`, `resume_file_name`, `resume_path`, `submitted_at`, `user_id`, `job_id`) VALUES
(1, 'resume_john_doe.pdf', '/resumes/john_doe.pdf', '2024-12-11 17:22:16', 1, 1),
(2, 'resume_jane_smith.pdf', '/resumes/jane_smith.pdf', '2024-12-11 17:22:16', 2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `submitted_resumes`
--

CREATE TABLE `submitted_resumes` (
  `submitted_resume_id` int(11) NOT NULL,
  `resume_file_name` text NOT NULL,
  `resume_path` text NOT NULL,
  `submitted_at` text NOT NULL,
  `user_id` int(11) NOT NULL,
  `job_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `phone_number` varchar(12) NOT NULL,
  `state` varchar(20) NOT NULL,
  `city_or_province` varchar(30) DEFAULT NULL,
  `municipality` varchar(30) NOT NULL,
  `zip_code` varchar(10) NOT NULL,
  `street` varchar(10) DEFAULT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='user has one qualification';

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `phone_number`, `state`, `city_or_province`, `municipality`, `zip_code`, `street`, `email`, `password`, `created_at`, `updated_at`) VALUES
(1, 'John', 'Doe', '1234567890', 'California', 'Los Angeles', 'Los Angeles', '90001', 'Main St', 'john.doe@example.com', 'hashedpassword3', '2024-12-11 17:22:16', '2024-12-11 17:22:16'),
(2, 'Jane', 'Smith', '0987654321', 'New York', 'New York City', 'Manhattan', '10001', 'Broadway', 'jane.smith@example.com', 'hashedpassword4', '2024-12-11 17:22:16', '2024-12-11 17:22:16'),
(14, 'asdasd', 'asdasd', '09207766194', '090000000', '097200000', '097204000', '2413', '007', 'jemcarlo49@gmail.com', 'Abcd.123', '2024-12-16 00:00:00', '2024-12-16 00:00:00'),
(22, 'Jemcarlo', 'Austria', '09207766194', 'Ilocos Region', 'Ilocos Norte', 'Nueva Era', '2413', '007', 'jemcarlo55@gmail.com', 'asd', '0000-00-00 00:00:00', '2024-12-18 15:33:55'),
(23, 'Jem', 'Austria', '09457323970', 'Ilocos Region', 'Ilocos Sur', 'Banayoyo', '2413', '006 Parian', 'jemcarlo57@gmail.com', 'Abcd.123', '2024-12-18 00:00:00', '2024-12-18 00:00:00'),
(29, 'Jemcarlo', 'Austria', '09207766194', 'Ilocos Region', 'Ilocos Sur', 'Galimuyod', '2413', '007', 'asdasdasd@gmail.com', '$argon2id$v=19$m=65536,t=3,p=4$yY2KTi9mjpPw4oh5Y6vGfQ$6GWOV+Y20m+06BL4zD7fA4HkltV5TuXyqZz1ICi1+i0', '2024-12-18 19:03:28', '2024-12-18 19:03:28'),
(30, 'Jemcarlo', 'Austria', '09207766194', 'Ilocos Region', 'Ilocos Sur', 'Galimuyod', '2413', '007', 'hash123@gmail.com', '$argon2id$v=19$m=65536,t=3,p=4$+EHEgMnH0PYcTbP4xp9YZA$jS/+d4RgpD1D+A905Kkublb9nRBvawDSgqZczg1LEqw', '2024-12-18 19:03:55', '2024-12-18 19:03:55'),
(31, 'Jemcarlo', 'Austria', '09207766194', 'Ilocos Region', 'Ilocos Sur', 'Galimuyod', '2413', '007', 'hash44@gmail.com', '$argon2id$v=19$m=65536,t=3,p=4$INpwGmwqNITb7y0SGTuaMQ$7rKDd/rc5VFSH1u7uu9cq3lVcWQhXHXl3cNrn6cJ3v4', '2024-12-18 19:07:10', '2024-12-18 19:07:10'),
(32, 'Jemcarlo', 'Austria', '09207766194', 'Cagayan Valley', 'Isabela', 'Alicia', '2413', '007', 'hasgsad213@gmail.com', '$argon2id$v=19$m=65536,t=3,p=4$J1b3k2x87kkwAkHMQC13KA$xX9DvqwGPcgJ2la8MGWg3T7cyakQs+gp5ZxKoU8nJt0', '0000-00-00 00:00:00', '2024-12-18 19:29:30');

-- --------------------------------------------------------

--
-- Table structure for table `user_interest`
--

CREATE TABLE `user_interest` (
  `interest_id` int(11) NOT NULL,
  `job_interest` varchar(50) NOT NULL,
  `job_type` enum('Full-time','Part-time','Freelance','Internship') NOT NULL,
  `preferred_location` varchar(50) NOT NULL,
  `expected_salary_range` varchar(50) NOT NULL,
  `created_at` datetime NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_interest`
--

INSERT INTO `user_interest` (`interest_id`, `job_interest`, `job_type`, `preferred_location`, `expected_salary_range`, `created_at`, `user_id`) VALUES
(1, 'Software Development', 'Full-time', 'Remote', '$80,000 - $100,000', '2024-12-11 17:22:16', 1),
(2, 'Data Science', 'Part-time', 'New York City', '$60,000 - $80,000', '2024-12-11 17:22:16', 2);
-- Indexes for dumped tables
--

--
-- Indexes for table `employers`
--
ALTER TABLE `employers`
  ADD PRIMARY KEY (`employer_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`job_id`),
  ADD KEY `FK_employers_TO_jobs` (`employer_id`);

--
-- Indexes for table `qualifications`
--
ALTER TABLE `qualifications`
  ADD PRIMARY KEY (`qualification_id`),
  ADD KEY `FK_users_TO_qualifications` (`user_id`);

--
-- Indexes for table `saved_jobs`
--
ALTER TABLE `saved_jobs`
  ADD PRIMARY KEY (`saved_job_id`),
  ADD KEY `FK_users_TO_saved_jobs` (`user_id`),
  ADD KEY `FK_jobs_TO_saved_jobs` (`job_id`);

--
-- Indexes for table `submitted_resume`
--
ALTER TABLE `submitted_resume`
  ADD PRIMARY KEY (`submitted_resume_id`),
  ADD KEY `FK_users_TO_submitted_resume` (`user_id`),
  ADD KEY `FK_jobs_TO_submitted_resume` (`job_id`);

--
-- Indexes for table `submitted_resumes`
--
ALTER TABLE `submitted_resumes`
  ADD PRIMARY KEY (`submitted_resume_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `job_id` (`job_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `user_interest`
--
ALTER TABLE `user_interest`
  ADD PRIMARY KEY (`interest_id`),
  ADD KEY `FK_users_TO_user_interest` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `employers`
--
ALTER TABLE `employers`
  MODIFY `employer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `job_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `qualifications`
--
ALTER TABLE `qualifications`
  MODIFY `qualification_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `saved_jobs`
--
ALTER TABLE `saved_jobs`
  MODIFY `saved_job_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `submitted_resume`
--
ALTER TABLE `submitted_resume`
  MODIFY `submitted_resume_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `user_interest`
--
ALTER TABLE `user_interest`
  MODIFY `interest_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `jobs`
--
ALTER TABLE `jobs`
  ADD CONSTRAINT `FK_employers_TO_jobs` FOREIGN KEY (`employer_id`) REFERENCES `employers` (`employer_id`);

--
-- Constraints for table `qualifications`
--
ALTER TABLE `qualifications`
  ADD CONSTRAINT `FK_users_TO_qualifications` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `saved_jobs`
--
ALTER TABLE `saved_jobs`
  ADD CONSTRAINT `FK_jobs_TO_saved_jobs` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`),
  ADD CONSTRAINT `FK_users_TO_saved_jobs` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `submitted_resume`
--
ALTER TABLE `submitted_resume`
  ADD CONSTRAINT `FK_jobs_TO_submitted_resume` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`),
  ADD CONSTRAINT `FK_users_TO_submitted_resume` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `submitted_resumes`
--
ALTER TABLE `submitted_resumes`
  ADD CONSTRAINT `submitted_resumes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `submitted_resumes_ibfk_2` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`);

--
-- Constraints for table `user_interest`
--
ALTER TABLE `user_interest`
  ADD CONSTRAINT `FK_users_TO_user_interest` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

"""
