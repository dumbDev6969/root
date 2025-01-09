-- MySQL dump 10.13  Distrib 9.1.0, for Win64 (x86_64)
--
-- Host: localhost    Database: jobsearch
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `employer_reviews`
--

DROP TABLE IF EXISTS `employer_reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employer_reviews` (
  `id` varchar(36) NOT NULL,
  `employer_id` varchar(36) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `rating` tinyint NOT NULL,
  `title` varchar(200) DEFAULT NULL,
  `review_text` text,
  `pros` text,
  `cons` text,
  `is_anonymous` tinyint(1) DEFAULT '0',
  `is_verified` tinyint(1) DEFAULT '0',
  `status` enum('PENDING','APPROVED','REJECTED') DEFAULT 'PENDING',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_review` (`user_id`,`employer_id`),
  KEY `employer_id` (`employer_id`),
  CONSTRAINT `employer_reviews_chk_1` CHECK ((`rating` between 1 and 5))
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employer_reviews`
--

LOCK TABLES `employer_reviews` WRITE;
/*!40000 ALTER TABLE `employer_reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `employer_reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employers`
--

DROP TABLE IF EXISTS `employers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employers` (
  `employer_uuid` varchar(36) NOT NULL,
  `company_name` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `city_or_province` varchar(30) DEFAULT NULL,
  `zip_code` varchar(10) DEFAULT NULL,
  `street` varchar(200) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`employer_uuid`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employers`
--

LOCK TABLES `employers` WRITE;
/*!40000 ALTER TABLE `employers` DISABLE KEYS */;
INSERT INTO `employers` VALUES ('EMP230870c09bdaed','company001','company001@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$d/Sb1pePwjq6DSzDZI1g7A$ux0ucBdpkYKJfAONswi5YejOA7sWSLFXoIrldf34DFk','09207766194','Cagayan Valley','Cagayan','2413','007','2025-01-07 06:21:11','2025-01-07 06:21:11');
/*!40000 ALTER TABLE `employers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_alerts`
--

DROP TABLE IF EXISTS `job_alerts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_alerts` (
  `id` varchar(36) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `category_id` varchar(36) DEFAULT NULL,
  `keywords` varchar(200) DEFAULT NULL,
  `location` varchar(200) DEFAULT NULL,
  `job_type` enum('FULL_TIME','PART_TIME','CONTRACT','INTERNSHIP') DEFAULT NULL,
  `salary_min` decimal(10,2) DEFAULT NULL,
  `salary_max` decimal(10,2) DEFAULT NULL,
  `frequency` enum('DAILY','WEEKLY','MONTHLY') DEFAULT 'WEEKLY',
  `is_active` tinyint(1) DEFAULT '1',
  `last_sent` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `category_id` (`category_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_alerts`
--

LOCK TABLES `job_alerts` WRITE;
/*!40000 ALTER TABLE `job_alerts` DISABLE KEYS */;
/*!40000 ALTER TABLE `job_alerts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_applications`
--

DROP TABLE IF EXISTS `job_applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_applications` (
  `id` varchar(36) NOT NULL,
  `job_id` varchar(36) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `status` enum('PENDING','REVIEWED','SHORTLISTED','REJECTED','ACCEPTED') DEFAULT 'PENDING',
  `cover_letter` text,
  `resume_url` varchar(200) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `job_id` (`job_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_applications`
--

LOCK TABLES `job_applications` WRITE;
/*!40000 ALTER TABLE `job_applications` DISABLE KEYS */;
/*!40000 ALTER TABLE `job_applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_categories`
--

DROP TABLE IF EXISTS `job_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_categories` (
  `id` varchar(36) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_categories`
--

LOCK TABLES `job_categories` WRITE;
/*!40000 ALTER TABLE `job_categories` DISABLE KEYS */;
INSERT INTO `job_categories` VALUES ('CAT001','Software Development','Jobs related to software development and programming','2025-01-08 22:22:45','2025-01-08 22:22:45'),('CAT002','Web Development','Frontend and backend web development positions','2025-01-08 22:22:45','2025-01-08 22:22:45'),('CAT003','Data Science','Data analysis, machine learning, and AI positions','2025-01-08 22:22:45','2025-01-08 22:22:45'),('CAT004','DevOps','DevOps and cloud infrastructure positions','2025-01-08 22:22:45','2025-01-08 22:22:45'),('CAT005','Cybersecurity','Information security and cybersecurity positions','2025-01-08 22:22:45','2025-01-08 22:22:45');
/*!40000 ALTER TABLE `job_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs` (
  `id` varchar(36) NOT NULL,
  `employer_id` varchar(36) NOT NULL,
  `category_id` varchar(36) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `requirements` text,
  `location` varchar(200) DEFAULT NULL,
  `salary_range` varchar(100) DEFAULT NULL,
  `job_type` enum('FULL_TIME','PART_TIME','CONTRACT','INTERNSHIP') NOT NULL,
  `status` enum('DRAFT','PUBLISHED','CLOSED') DEFAULT 'DRAFT',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `employer_id` (`employer_id`),
  KEY `category_id` (`category_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES ('JOB001','EMP230870c09bdaed','CAT001','Senior Software Engineer','Lead development of enterprise applications','5+ years experience in Java/Python\nStrong system design skills','Manila','80,000 - 120,000','FULL_TIME','PUBLISHED','2025-01-08 22:23:02','2025-01-08 22:23:02'),('JOB002','EMP230870c09bdaed','CAT001','Junior Software Developer','Develop and maintain software applications','BS in Computer Science\nBasic programming skills','Makati','25,000 - 35,000','FULL_TIME','PUBLISHED','2025-01-08 22:23:02','2025-01-08 22:23:02'),('JOB003','EMP230870c09bdaed','CAT002','Frontend Developer','Create responsive web applications','React/Vue.js experience\nHTML/CSS expertise','BGC','40,000 - 60,000','FULL_TIME','PUBLISHED','2025-01-08 22:23:02','2025-01-08 22:23:02'),('JOB004','EMP230870c09bdaed','CAT002','Backend Developer','Design and implement APIs','Node.js/Python experience\nDatabase design skills','Ortigas','45,000 - 70,000','FULL_TIME','PUBLISHED','2025-01-08 22:23:02','2025-01-08 22:23:02'),('JOB005','EMP230870c09bdaed','CAT003','Data Scientist','Analyze complex data sets','Machine learning expertise\nPython/R proficiency','Manila','60,000 - 90,000','FULL_TIME','PUBLISHED','2025-01-08 22:23:02','2025-01-08 22:23:02'),('JOB006','EMP230870c09bdaed','CAT003','Data Analyst Intern','Support data analysis projects','Statistics background\nSQL knowledge','Makati','15,000 - 20,000','INTERNSHIP','PUBLISHED','2025-01-08 22:23:02','2025-01-08 22:23:02'),('JOB007','EMP230870c09bdaed','CAT004','DevOps Engineer','Manage cloud infrastructure','AWS/Azure experience\nCI/CD expertise','BGC','70,000 - 100,000','FULL_TIME','PUBLISHED','2025-01-08 22:23:02','2025-01-08 22:23:02'),('JOB008','EMP230870c09bdaed','CAT004','Cloud Solutions Architect','Design cloud architecture','Cloud certification\nSystem design experience','Makati','90,000 - 130,000','FULL_TIME','PUBLISHED','2025-01-08 22:23:02','2025-01-08 22:23:02'),('JOB009','EMP230870c09bdaed','CAT005','Security Engineer','Implement security measures','Security certifications\nNetwork security experience','Manila','65,000 - 95,000','FULL_TIME','PUBLISHED','2025-01-08 22:23:02','2025-01-08 22:23:02'),('JOB010','EMP230870c09bdaed','CAT005','Security Analyst','Monitor security systems','CISSP preferred\nIncident response experience','BGC','50,000 - 75,000','FULL_TIME','PUBLISHED','2025-01-08 22:23:02','2025-01-08 22:23:02'),('JOB011','EMP230870c09bdaed','CAT001','Part-time Mobile Developer','Develop mobile applications','React Native/Flutter experience\nMobile app development skills','Remote','30,000 - 45,000','PART_TIME','PUBLISHED','2025-01-08 22:23:17','2025-01-08 22:23:17'),('JOB012','EMP230870c09bdaed','CAT002','WordPress Developer','Maintain and customize WordPress sites','WordPress experience\nPHP knowledge','Quezon City','25,000 - 40,000','PART_TIME','PUBLISHED','2025-01-08 22:23:17','2025-01-08 22:23:17'),('JOB013','EMP230870c09bdaed','CAT003','ML Engineer Contract','Implement machine learning models','TensorFlow/PyTorch experience\nML deployment skills','Remote','80,000 - 120,000','CONTRACT','PUBLISHED','2025-01-08 22:23:17','2025-01-08 22:23:17'),('JOB014','EMP230870c09bdaed','CAT004','Junior DevOps Intern','Learn cloud operations','Basic Linux knowledge\nProgramming fundamentals','Makati','18,000 - 22,000','INTERNSHIP','PUBLISHED','2025-01-08 22:23:17','2025-01-08 22:23:17'),('JOB015','EMP230870c09bdaed','CAT005','Part-time Security Consultant','Security audits and consulting','Security background\nAudit experience','Remote','40,000 - 60,000','PART_TIME','PUBLISHED','2025-01-08 22:23:17','2025-01-08 22:23:17'),('JOB016','EMP230870c09bdaed','CAT001','Contract System Architect','Design system architecture','Architecture experience\nTechnical leadership','BGC','100,000 - 150,000','CONTRACT','PUBLISHED','2025-01-08 22:23:17','2025-01-08 22:23:17'),('JOB017','EMP230870c09bdaed','CAT002','UI/UX Developer','Design and implement user interfaces','UI/UX design skills\nFrontend development experience','Ortigas','45,000 - 65,000','FULL_TIME','PUBLISHED','2025-01-08 22:23:17','2025-01-08 22:23:17'),('JOB018','EMP230870c09bdaed','CAT003','Business Intelligence Analyst','Create data visualizations and reports','Power BI/Tableau experience\nSQL expertise','Makati','50,000 - 70,000','FULL_TIME','PUBLISHED','2025-01-08 22:23:17','2025-01-08 22:23:17'),('JOB019','EMP230870c09bdaed','CAT004','Site Reliability Engineer','Ensure system reliability','SRE experience\nMonitoring tools knowledge','BGC','75,000 - 110,000','FULL_TIME','PUBLISHED','2025-01-08 22:23:17','2025-01-08 22:23:17'),('JOB020','EMP230870c09bdaed','CAT005','Penetration Tester','Conduct security testing','Ethical hacking skills\nSecurity certifications','Manila','70,000 - 100,000','FULL_TIME','PUBLISHED','2025-01-08 22:23:17','2025-01-08 22:23:17');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `uuid` varchar(200) NOT NULL,
  `user_id` int NOT NULL,
  `employer_id` int NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `FK_users_TO_message` (`user_id`),
  KEY `FK_employers_TO_message` (`employer_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='can be sent by both user';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_image`
--

DROP TABLE IF EXISTS `profile_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile_image` (
  `profile_image_id` int NOT NULL AUTO_INCREMENT,
  `image` varchar(200) NOT NULL,
  `uploaded_at` datetime NOT NULL,
  `employer_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`profile_image_id`),
  KEY `FK_employers_TO_profile_image` (`employer_id`),
  KEY `FK_users_TO_profile_image` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='can be posted by all users';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_image`
--

LOCK TABLES `profile_image` WRITE;
/*!40000 ALTER TABLE `profile_image` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qualifications`
--

DROP TABLE IF EXISTS `qualifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qualifications` (
  `qualification_id` int NOT NULL AUTO_INCREMENT,
  `degree` varchar(30) NOT NULL,
  `school_graduated` varchar(40) NOT NULL,
  `certifications` varchar(255) DEFAULT NULL,
  `specialized_training` varchar(100) DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`qualification_id`),
  KEY `FK_users_TO_qualifications` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='has one user';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qualifications`
--

LOCK TABLES `qualifications` WRITE;
/*!40000 ALTER TABLE `qualifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `qualifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `saved_jobs`
--

DROP TABLE IF EXISTS `saved_jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `saved_jobs` (
  `id` varchar(36) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `job_id` varchar(36) NOT NULL,
  `notes` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_saved_job` (`user_id`,`job_id`),
  KEY `job_id` (`job_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `saved_jobs`
--

LOCK TABLES `saved_jobs` WRITE;
/*!40000 ALTER TABLE `saved_jobs` DISABLE KEYS */;
/*!40000 ALTER TABLE `saved_jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `submitted_resume`
--

DROP TABLE IF EXISTS `submitted_resume`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `submitted_resume` (
  `submitted_resume_id` int NOT NULL AUTO_INCREMENT,
  `resume_file_name` varchar(50) NOT NULL,
  `resume_path` varchar(255) NOT NULL,
  `submitted_at` datetime NOT NULL,
  `user_id` int NOT NULL,
  `employer_id` int NOT NULL,
  PRIMARY KEY (`submitted_resume_id`),
  KEY `FK_users_TO_submitted_resume` (`user_id`),
  KEY `FK_employers_TO_submitted_resume` (`employer_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='can be submitted by user to employer';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `submitted_resume`
--

LOCK TABLES `submitted_resume` WRITE;
/*!40000 ALTER TABLE `submitted_resume` DISABLE KEYS */;
/*!40000 ALTER TABLE `submitted_resume` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_interest`
--

DROP TABLE IF EXISTS `user_interest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_interest` (
  `interest_id` int NOT NULL AUTO_INCREMENT,
  `job_interest` varchar(50) NOT NULL,
  `job_type` enum('Full-time','Part-time','Freelance','Internship') NOT NULL,
  `preferred_location` varchar(50) NOT NULL,
  `expected_salary_range` varchar(50) NOT NULL,
  `created_at` datetime NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`interest_id`),
  KEY `FK_users_TO_user_interest` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='has one user';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_interest`
--

LOCK TABLES `user_interest` WRITE;
/*!40000 ALTER TABLE `user_interest` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_interest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` varchar(36) NOT NULL,
  `user_uuid` varchar(36) NOT NULL,
  `email` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  `two_factor_data` text,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `municipality` varchar(100) DEFAULT NULL,
  `zip_code` varchar(10) DEFAULT NULL,
  `street` varchar(200) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('','USR78586261a94696','jemcarlo43@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$XVy0VB7JC5PfD+zyyOyVGA$jOa+XDLcn/Si+23B/T5A6jwRwFNVV7LEKXOs9wnkb3U',NULL,'Jemcarlo','Austria','09207766194','Cagayan Valley','Allacapan','2413','007','2024-12-21 12:57:43','2024-12-21 13:15:21'),('USR786925c044c8e9','USR786925c044c8e9','jemcarlo46@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$q2LFYIaOmnnlqWdu6h/u5A$o4qFczXRzEZPHxJUZB+F3cqhDVbHSYlnrpZylh/6wTI',NULL,'Jemcarlo','Austria','09207766194','Cagayan Valley','Allacapan','2413','007','2024-12-21 13:15:26','2024-12-21 13:15:26');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-09  9:35:50
