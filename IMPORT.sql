CREATE TABLE employers (
  employer_id      INT          NOT NULL AUTO_INCREMENT,
  employer_uuid    VARCHAR(36)  NOT NULL,
  company_name     VARCHAR(30)  NOT NULL,
  phone_number     INT          NOT NULL,
  state            VARCHAR(20)  NOT NULL,
  city_or_province VARCHAR(30)  NULL,
  zip_code         VARCHAR(10)  NOT NULL,
  street           VARCHAR(10)  NULL,
  email            VARCHAR(30)  NULL,
  password         VARCHAR(255) NOT NULL,
  created_at       DATETIME     NOT NULL,
  updated_at       DATETIME     NOT NULL,
  PRIMARY KEY (employer_id)
) COMMENT 'can post many jobs, receive resume, message';

CREATE TABLE jobs (
  job_id          INT                                                       NOT NULL AUTO_INCREMENT,
  job_title       VARCHAR(30)                                               NOT NULL,
  job_type        ENUM('Full-time', 'Part-time', 'Freelance', 'Internship') NOT NULL,
  location        VARCHAR(50)                                               NOT NULL,
  salary_range    VARCHAR(50)                                               NOT NULL,
  job_description TEXT                                                      NOT NULL,
  requirements    TEXT                                                      NOT NULL,
  created_at      DATETIME                                                  NOT NULL,
  employer_id     INT                                                       NOT NULL,
  PRIMARY KEY (job_id)
) COMMENT 'can be posted by employer';

CREATE TABLE message (
  uuid        VARCHAR(255) NOT NULL,
  user_id     INT          NOT NULL,
  employer_id INT          NOT NULL,
  PRIMARY KEY (uuid)
) COMMENT 'can be sent by both user';

CREATE TABLE profile_image (
  profile_image_id INT NOT NULL AUTO_INCREMENT,
  image            VARCHAR(255)  NOT NULL,
  uploaded_at      DATETIME NOT NULL,
  employer_id      INT,
  user_id          INT,
  PRIMARY KEY (profile_image_id)
) COMMENT 'can be posted by all users';

CREATE TABLE qualifications (
  qualification_id     INT          NOT NULL AUTO_INCREMENT,
  degree               VARCHAR(30)  NOT NULL,
  school_graduated     VARCHAR(40)  NOT NULL,
  certifications       VARCHAR(255) NULL,
  specialized_training VARCHAR(100) NULL,
  user_id              INT          NOT NULL,
  PRIMARY KEY (qualification_id)
) COMMENT 'has one user';

CREATE TABLE saved_jobs (
  saved_job_id INT NOT NULL AUTO_INCREMENT,
  user_id      INT NOT NULL,
  job_id       INT NOT NULL,
  PRIMARY KEY (saved_job_id)
) COMMENT 'can be saved by user';

CREATE TABLE submitted_resume (
  submitted_resume_id INT          NOT NULL AUTO_INCREMENT,
  resume_file_name    VARCHAR(50) NOT NULL,
  resume_path         VARCHAR(255) NOT NULL,
  submitted_at        DATETIME    NOT NULL,
  user_id             INT         NOT NULL,
  employer_id         INT         NOT NULL,
  PRIMARY KEY (submitted_resume_id)
) COMMENT 'can be submitted by user to employer';

CREATE TABLE user_interest (
  interest_id           INT                                                       NOT NULL AUTO_INCREMENT,
  job_interest          VARCHAR(50)                                               NOT NULL,
  job_type              ENUM('Full-time', 'Part-time', 'Freelance', 'Internship') NOT NULL,
  preferred_location    VARCHAR(50)                                               NOT NULL,
  expected_salary_range VARCHAR(50)                                               NOT NULL,
  created_at            DATETIME                                                  NOT NULL,
  user_id               INT                                                       NOT NULL,
  PRIMARY KEY (interest_id)
) COMMENT 'has one user';

CREATE TABLE users (
  user_id      INT          NOT NULL AUTO_INCREMENT,
  user_uuid    VARCHAR(36) NOT NULL,
  first_name   VARCHAR(20)  NOT NULL,
  last_name    VARCHAR(30)  NOT NULL,
  phone_number INT          NOT NULL,
  state        VARCHAR(20)  NOT NULL,
  municipality VARCHAR(30)  NOT NULL,
  zip_code     VARCHAR(10)  NOT NULL,
  street       VARCHAR(10)  NULL,
  email        VARCHAR(30)  NOT NULL,
  password     VARCHAR(255) NOT NULL,
  created_at   DATETIME     NOT NULL,
  updated_at   DATETIME     NOT NULL,
  PRIMARY KEY (user_id)
) COMMENT 'can have qualification,save job, submit resume, add interest, message, add profile image';

ALTER TABLE qualifications
  ADD CONSTRAINT FK_users_TO_qualifications
    FOREIGN KEY (user_id)
    REFERENCES users(user_id);

ALTER TABLE user_interest
  ADD CONSTRAINT FK_users_TO_user_interest
    FOREIGN KEY (user_id)
    REFERENCES users (user_id);

ALTER TABLE saved_jobs
  ADD CONSTRAINT FK_users_TO_saved_jobs
    FOREIGN KEY (user_id)
    REFERENCES users (user_id);

ALTER TABLE jobs
  ADD CONSTRAINT FK_employers_TO_jobs
    FOREIGN KEY (employer_id)
    REFERENCES employers (employer_id);

ALTER TABLE saved_jobs
  ADD CONSTRAINT FK_jobs_TO_saved_jobs
    FOREIGN KEY (job_id)
    REFERENCES jobs (job_id);

ALTER TABLE submitted_resume
  ADD CONSTRAINT FK_users_TO_submitted_resume
    FOREIGN KEY (user_id)
    REFERENCES users (user_id);

ALTER TABLE submitted_resume
  ADD CONSTRAINT FK_employers_TO_submitted_resume
    FOREIGN KEY (employer_id)
    REFERENCES employers (employer_id);

ALTER TABLE message
  ADD CONSTRAINT FK_users_TO_message
    FOREIGN KEY (user_id)
    REFERENCES users (user_id);

ALTER TABLE profile_image
  ADD CONSTRAINT FK_employers_TO_profile_image
    FOREIGN KEY (employer_id)
    REFERENCES employers (employer_id);

ALTER TABLE profile_image
  ADD CONSTRAINT FK_users_TO_profile_image
    FOREIGN KEY (user_id)
    REFERENCES users (user_id);

ALTER TABLE message
  ADD CONSTRAINT FK_employers_TO_message
    FOREIGN KEY (employer_id)
    REFERENCES employers (employer_id);
