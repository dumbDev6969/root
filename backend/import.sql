-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 11, 2024 at 01:56 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

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
(3, 'Tech Solutions', '1234567890', 'California', 'Los Angeles', '90001', 'Main St', 'contact@techsolutions.com', 'hashedpassword1', '2024-12-11 17:22:16', '2024-12-11 17:22:16'),
(4, 'Innovatech', '0987654321', 'New York', 'New York City', '10001', 'Broadway', 'info@innovatech.com', 'hashedpassword2', '2024-12-11 17:22:16', '2024-12-11 17:22:16'),
(5, 'Jemcarlo Austria', '09207766194', '010000000', '012800000', '2413', '007', 'jemcarlo46@gmail.com', 'asd', '2024-12-11 00:00:00', '2024-12-11 00:00:00');

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
(4, 2, 'Data Analyst', 'Part-time', 'New York City', '$50,000 - $70,000', 'Analyze data and generate reports.', 'Experience with SQL and Python', '2024-12-11 17:22:16');

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
(7, 'Jemcarlo', 'Austria', '09207766194', '010000000', '012800000', '012801000', '2413', '007', 'jemcarlo46@gmail.com', 'asd', '2024-12-11 00:00:00', '2024-12-11 00:00:00'),
(8, 'Jemcarlo', 'Austria', '09207766194', '010000000', '012800000', '012814000', '2413', '007', 'jemcarlo46@gmail.com', 'asd', '2024-12-11 00:00:00', '2024-12-11 00:00:00');

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

--
-- Indexes for dumped tables
--

--
-- Indexes for table `employers`
--
ALTER TABLE `employers`
  ADD PRIMARY KEY (`employer_id`);

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
  MODIFY `employer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `job_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

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
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

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
-- Constraints for table `user_interest`
--
ALTER TABLE `user_interest`
  ADD CONSTRAINT `FK_users_TO_user_interest` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
