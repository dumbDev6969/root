import sqlite3

# Connect/Create SQLite3 Database
conn = sqlite3.connect("fallback_db.db")
cursor = conn.cursor()

# Schema creation functions
def create_employers_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employers (
            employer_id INTEGER PRIMARY KEY,
            company_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            state TEXT NOT NULL,
            city_or_province TEXT,
            zip_code TEXT NOT NULL,
            street TEXT,
            email TEXT UNIQUE,
            password TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL
        )
    """)

def create_jobs_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id INTEGER PRIMARY KEY,
            employer_id INTEGER NOT NULL,
            job_title TEXT NOT NULL,
            job_type TEXT NOT NULL CHECK(job_type IN ('Full-time', 'Part-time', 'Freelance', 'Internship')),
            location TEXT NOT NULL,
            salary_range TEXT NOT NULL,
            job_description TEXT NOT NULL,
            requirements TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
        )
    """)

def create_qualifications_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qualifications (
            qualification_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            degree TEXT NOT NULL,
            school_graduated TEXT NOT NULL,
            certifications TEXT,
            specialized_training TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

def create_saved_jobs_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_jobs (
            saved_job_id INTEGER PRIMARY KEY,
            saved_at DATETIME NOT NULL,
            user_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (job_id) REFERENCES jobs(job_id)
        )
    """)

def create_submitted_resumes_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submitted_resumes (
            submitted_resume_id INTEGER PRIMARY KEY,
            resume_file_name TEXT NOT NULL,
            resume_path TEXT NOT NULL,
            submitted_at DATETIME NOT NULL,
            user_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (job_id) REFERENCES jobs(job_id)
        )
    """)

def create_user_interest_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_interest (
            interest_id INTEGER PRIMARY KEY,
            job_interest TEXT NOT NULL,
            job_type TEXT NOT NULL CHECK(job_type IN ('Full-time', 'Part-time', 'Freelance', 'Internship')),
            preferred_location TEXT NOT NULL,
            expected_salary_range TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

def create_users_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            state TEXT NOT NULL,
            city_or_province TEXT,
            municipality TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            street TEXT,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL
        )
    """)

# Call functions to create tables
create_employers_table()
create_jobs_table()
create_qualifications_table()
create_saved_jobs_table()
create_submitted_resumes_table()
create_user_interest_table()
create_users_table()

# Commit and close the connection
conn.commit()
conn.close()

print("SQLite tables created successfully.")