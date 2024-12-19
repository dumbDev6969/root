# str="ngrok http --url=big-swan-adversely.ngrok-free.app 3306"

qry = """
CREATE TABLE IF NOT EXISTS `employers` (
  `employer_id` int(11) NOT NULL AUTO_INCREMENT,
  `employer_uuid` varchar(100) NOT NULL,
  `company_name` varchar(30) NOT NULL,
  `phone_number` varchar(12) NOT NULL,
  `state` varchar(20) NOT NULL,
  `city_or_province` varchar(30) DEFAULT NULL,
  `zip_code` varchar(10) NOT NULL,
  `street` varchar(10) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`employer_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `employer_uuid` (`employer_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `jobs` (
  `job_id` int(11) NOT NULL AUTO_INCREMENT,
  `employer_id` int(11) NOT NULL,
  `job_title` varchar(30) NOT NULL,
  `job_type` enum('Full-time','Part-time','Freelance','Internship') NOT NULL,
  `location` varchar(50) NOT NULL,
  `salary_range` varchar(50) NOT NULL,
  `job_description` text NOT NULL,
  `requirements` text NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`job_id`),
  KEY `FK_employers_TO_jobs` (`employer_id`),
  CONSTRAINT `FK_employers_TO_jobs` FOREIGN KEY (`employer_id`) REFERENCES `employers` (`employer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_uuid` varchar(100) NOT NULL,
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
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_uuid` (`user_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='user has one qualification';

CREATE TABLE IF NOT EXISTS `qualifications` (
  `qualification_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `degree` varchar(30) NOT NULL,
  `school_graduated` varchar(40) NOT NULL,
  `certifications` varchar(255) DEFAULT NULL,
  `specialized_training` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`qualification_id`),
  KEY `FK_users_TO_qualifications` (`user_id`),
  CONSTRAINT `FK_users_TO_qualifications` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `saved_jobs` (
  `saved_job_id` int(11) NOT NULL AUTO_INCREMENT,
  `saved_at` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `job_id` int(11) NOT NULL,
  PRIMARY KEY (`saved_job_id`),
  KEY `FK_users_TO_saved_jobs` (`user_id`),
  KEY `FK_jobs_TO_saved_jobs` (`job_id`),
  CONSTRAINT `FK_users_TO_saved_jobs` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `FK_jobs_TO_saved_jobs` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



CREATE TABLE IF NOT EXISTS `submitted_resume` (
  `submitted_resume_id` int(11) NOT NULL AUTO_INCREMENT,
  `resume_file_name` varchar(50) NOT NULL,
  `resume_path` varchar(50) NOT NULL,
  `submitted_at` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `job_id` int(11) NOT NULL,
  PRIMARY KEY (`submitted_resume_id`),
  KEY `FK_users_TO_submitted_resume` (`user_id`),
  KEY `FK_jobs_TO_submitted_resume` (`job_id`),
  CONSTRAINT `FK_users_TO_submitted_resume` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `FK_jobs_TO_submitted_resume` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `user_interest` (
  `interest_id` int(11) NOT NULL AUTO_INCREMENT,
  `job_interest` varchar(50) NOT NULL,
  `job_type` enum('Full-time','Part-time','Freelance','Internship') NOT NULL,
  `preferred_location` varchar(50) NOT NULL,
  `expected_salary_range` varchar(50) NOT NULL,
  `created_at` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`interest_id`),
  KEY `FK_users_TO_user_interest` (`user_id`),
  CONSTRAINT `FK_users_TO_user_interest` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

"""

import pymysql

timeout = 10
connection = pymysql.connect(
    charset="utf8mb4",
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db="jobsearch",
    host="mysql-24a8087-mysql-server-jobs.c.aivencloud.com",
    password="AVNS_RCkju8DXtGBZrSXcWqk",
    read_timeout=timeout,
    port=16459,
    user="avnadmin",
    write_timeout=timeout,
)
  
try:
    cursor = connection.cursor()
   
    for statement in qry.split(';'):
        if statement.strip():
            cursor.execute(statement)
    connection.commit()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    connection.close()
