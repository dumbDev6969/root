
INSERT INTO employers (company_name, phone_number, state, city_or_province, zip_code, street, email, password, created_at, updated_at) VALUES
('Tech Solutions', '1234567890', 'California', 'Los Angeles', '90001', 'Main St', 'contact@techsolutions.com', 'hashedpassword1', NOW(), NOW()),
('Innovatech', '0987654321', 'New York', 'New York City', '10001', 'Broadway', 'info@innovatech.com', 'hashedpassword2', NOW(), NOW());


INSERT INTO jobs (employer_id, job_title, job_type, location, salary_range, job_description, requirements, created_at) VALUES
(1, 'Software Engineer', 'Full-time', 'Remote', '$70,000 - $90,000', 'Develop and maintain software applications.', 'Bachelors degree in Computer Science', NOW()),
(2, 'Data Analyst', 'Part-time', 'New York City', '$50,000 - $70,000', 'Analyze data and generate reports.', 'Experience with SQL and Python', NOW());


INSERT INTO users (first_name, last_name, phone_number, state, city_or_province, municipality, zip_code, street, email, password, created_at, updated_at) VALUES
('John', 'Doe', '1234567890', 'California', 'Los Angeles', 'Los Angeles', '90001', 'Main St', 'john.doe@example.com', 'hashedpassword3', NOW(), NOW()),
('Jane', 'Smith', '0987654321', 'New York', 'New York City', 'Manhattan', '10001', 'Broadway', 'jane.smith@example.com', 'hashedpassword4', NOW(), NOW());


INSERT INTO qualifications (user_id, degree, school_graduated, certifications, specialized_training) VALUES
(1, 'B.Sc. Computer Science', 'MIT', 'Certified Java Developer', 'Machine Learning'),
(2, 'M.Sc. Data Science', 'Stanford University', NULL, 'Data Analysis');


INSERT INTO saved_jobs (saved_at, user_id, job_id) VALUES
(NOW(), 1, 1),
(NOW(), 2, 2);


INSERT INTO submitted_resume (resume_file_name, resume_path, submitted_at, user_id, job_id) VALUES
('resume_john_doe.pdf', '/resumes/john_doe.pdf', NOW(), 1, 1),
('resume_jane_smith.pdf', '/resumes/jane_smith.pdf', NOW(), 2, 2);

INSERT INTO user_interest (job_interest, job_type, preferred_location, expected_salary_range, created_at, user_id) VALUES
('Software Development', 'Full-time', 'Remote', '$80,000 - $100,000', NOW(), 1),
('Data Science', 'Part-time', 'New York City', '$60,000 - $80,000', NOW(), 2);
