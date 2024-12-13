CREATE TABLE employers (
  employer_id INT NOT NULL AUTO_INCREMENT,
  company_name VARCHAR(30) NOT NULL,
  phone_number VARCHAR(12) NOT NULL,
  state VARCHAR(20) NOT NULL,
  city_or_province VARCHAR(30) NULL,
  zip_code VARCHAR(10) NOT NULL,
  street VARCHAR(10) NULL,
  email VARCHAR(30) NULL,
  password VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  PRIMARY KEY (employer_id)
);

CREATE TABLE jobs (
  job_id INT NOT NULL AUTO_INCREMENT,
  employer_id INT NOT NULL,
  job_title VARCHAR(30) NOT NULL,
  job_type ENUM('Full-time', 'Part-time', 'Freelance', 'Internship') NOT NULL,
  location VARCHAR(50) NOT NULL,
  salary_range VARCHAR(50) NOT NULL,
  job_description TEXT NOT NULL,
  requirements TEXT NOT NULL,
  created_at DATETIME NOT NULL,
  PRIMARY KEY (job_id),
  INDEX idx_employer_id (employer_id)
);

CREATE TABLE qualifications (
  qualification_id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  degree VARCHAR(30) NOT NULL,
  school_graduated VARCHAR(40) NOT NULL,
  certifications VARCHAR(255) NULL,
  specialized_training VARCHAR(100) NULL,
  PRIMARY KEY (qualification_id),
  INDEX idx_user_id (user_id)
);

CREATE TABLE saved_jobs (
  saved_job_id INT NOT NULL AUTO_INCREMENT,
  saved_at DATETIME NOT NULL,
  user_id INT NOT NULL,
  job_id INT NOT NULL,
  PRIMARY KEY (saved_job_id),
  INDEX idx_user_id (user_id),
  INDEX idx_job_id (job_id)
);

CREATE TABLE submitted_resume (
  submitted_resume_id INT NOT NULL AUTO_INCREMENT,
  resume_file_name VARCHAR(50) NOT NULL,
  resume_path VARCHAR(50) NOT NULL,
  submitted_at DATETIME NOT NULL,
  user_id INT NOT NULL,
  job_id INT NOT NULL,
  PRIMARY KEY (submitted_resume_id),
  INDEX idx_user_id (user_id),
  INDEX idx_job_id (job_id)
);

CREATE TABLE user_interest (
  interest_id INT NOT NULL AUTO_INCREMENT,
  job_interest VARCHAR(50) NOT NULL,
  job_type ENUM('Full-time', 'Part-time', 'Freelance', 'Internship') NOT NULL,
  preferred_location VARCHAR(50) NOT NULL,
  expected_salary_range VARCHAR(50) NOT NULL,
  created_at DATETIME NOT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (interest_id),
  INDEX idx_user_id (user_id)
);

CREATE TABLE users (
  user_id INT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(30) NOT NULL,
  phone_number VARCHAR(12) NOT NULL,
  state VARCHAR(20) NOT NULL,
  city_or_province VARCHAR(30) NULL,
  municipality VARCHAR(30) NOT NULL,
  zip_code VARCHAR(10) NOT NULL,
  street VARCHAR(10) NULL,
  email VARCHAR(30) NOT NULL,
  password VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  PRIMARY KEY (user_id)
) COMMENT 'user has one qualification';

ALTER TABLE qualifications
  ADD CONSTRAINT FK_users_TO_qualifications
    FOREIGN KEY (user_id)
    REFERENCES users (user_id);

ALTER TABLE jobs
  ADD CONSTRAINT FK_employers_TO_jobs
    FOREIGN KEY (employer_id)
    REFERENCES employers (employer_id);

ALTER TABLE saved_jobs
  ADD CONSTRAINT FK_users_TO_saved_jobs
    FOREIGN KEY (user_id)
    REFERENCES users (user_id);

ALTER TABLE saved_jobs
  ADD CONSTRAINT FK_jobs_TO_saved_jobs
    FOREIGN KEY (job_id)
    REFERENCES jobs (job_id);

ALTER TABLE submitted_resume
  ADD CONSTRAINT FK_users_TO_submitted_resume
    FOREIGN KEY (user_id)
    REFERENCES users (user_id);

ALTER TABLE submitted_resume
  ADD CONSTRAINT FK_jobs_TO_submitted_resume
    FOREIGN KEY (job_id)
    REFERENCES jobs (job_id);

ALTER TABLE user_interest
  ADD CONSTRAINT FK_users_TO_user_interest
    FOREIGN KEY (user_id)
    REFERENCES users (user_id);
