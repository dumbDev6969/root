import mysql.connector

class CRUD:
    def __init__(self, host, user, password, database):
        """Initialize the CRUD class with MySQL connection details."""
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()
        #self.create_tables()

    def create_tables(self):
        """Create tables in the database."""
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS employers (
                employer_id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                phone_number VARCHAR(20) NOT NULL,
                state VARCHAR(50) NOT NULL,
                city_or_province VARCHAR(50),
                zip_code VARCHAR(10) NOT NULL,
                street VARCHAR(255),
                email VARCHAR(255),
                password VARCHAR(255) NOT NULL,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL
            )
        ''')
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS jobs (
                job_id INT AUTO_INCREMENT PRIMARY KEY,
                employer_id INT NOT NULL,
                job_title VARCHAR(255) NOT NULL,
                job_type VARCHAR(50) NOT NULL,
                location VARCHAR(255) NOT NULL,
                salary_range VARCHAR(50) NOT NULL,
                job_description TEXT NOT NULL,
                requirements TEXT NOT NULL,
                created_at DATETIME NOT NULL,
                FOREIGN KEY (employer_id) REFERENCES employers (employer_id)
            )
        ''')
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS qualifications (
                qualification_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                degree VARCHAR(255) NOT NULL,
                school_graduated VARCHAR(255) NOT NULL,
                certifications TEXT,
                specialized_training TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS saved_jobs (
                saved_job_id INT AUTO_INCREMENT PRIMARY KEY,
                saved_at DATETIME NOT NULL,
                user_id INT NOT NULL,
                job_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (job_id) REFERENCES jobs (job_id)
            )
        ''')
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS submitted_resume (
                submitted_resume_id INT AUTO_INCREMENT PRIMARY KEY,
                resume_file_name VARCHAR(255) NOT NULL,
                resume_path VARCHAR(255) NOT NULL,
                submitted_at DATETIME NOT NULL,
                user_id INT NOT NULL,
                job_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (job_id) REFERENCES jobs (job_id)
            )
        ''')
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS user_interest (
                interest_id INT AUTO_INCREMENT PRIMARY KEY,
                job_interest VARCHAR(255) NOT NULL,
                job_type VARCHAR(50) NOT NULL,
                preferred_location VARCHAR(255) NOT NULL,
                expected_salary_range VARCHAR(50) NOT NULL,
                created_at DATETIME NOT NULL,
                user_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                phone_number VARCHAR(20) NOT NULL,
                state VARCHAR(50) NOT NULL,
                city_or_province VARCHAR(50),
                municipality VARCHAR(50) NOT NULL,
                zip_code VARCHAR(10) NOT NULL,
                street VARCHAR(255),
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL
            )
        ''')

    def execute_query(self, sql, params=()):
        """Execute a SQL query with optional parameters."""
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"An error occurred: {e}")
            return None

    def create(self, table, **kwargs):
        """Insert a new record into the specified table."""
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join('%s' for _ in kwargs)
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        self.execute_query(sql, tuple(kwargs.values()))

    def read(self, table, **kwargs):
        """Read records from the specified table."""
        sql = f'SELECT * FROM {table}'
        if kwargs:
            conditions = ' AND '.join(f"{key} = %s" for key in kwargs.keys())
            sql += f' WHERE {conditions}'
            return self.execute_query(sql, tuple(kwargs.values()))
        else:
            return self.execute_query(sql)

    def update(self, table, id, **kwargs):
        """Update a record in the specified table."""
        set_clause = ', '.join(f"{key} = %s" for key in kwargs.keys())
        sql = f'UPDATE {table} SET {set_clause} WHERE id = %s'
        self.execute_query(sql, (*kwargs.values(), id))

    def delete(self, table, id):
        """Delete a record from the specified table."""
        sql = f'DELETE FROM {table} WHERE id = %s'
        self.execute_query(sql, (id,))

    def close(self):
        """Close the database connection."""
        self.connection.close()

# Example usage
if __name__ == "__main__":
    # Create an instance of the CRUD class
    crud = CRUD(host='localhost', user='root', password='', database='jobsearch')

    # Example INSERT queries
    crud.create('employers', company_name='Tech Corp', phone_number='1234567890', state='CA', zip_code='90001', email='contact@techcorp.com', password='securepassword', created_at='2023-10-01', updated_at='2023-10-01')
    crud.create('jobs', employer_id=1, job_title='Software Engineer', job_type='Full-time', location='Remote', salary_range='80k-100k', job_description='Develop software solutions.', requirements='3+ years experience', created_at='2023-10-01')
    crud.create('qualifications', user_id=1, degree='BSc Computer Science', school_graduated='Tech University')
    crud.create('saved_jobs', saved_at='2023-10-01', user_id=1, job_id=1)
    crud.create('submitted_resume', resume_file_name='resume.pdf', resume_path='/resumes/', submitted_at='2023-10-01', user_id=1, job_id=1)
    crud.create('user_interest', job_interest='Software Development', job_type='Full-time', preferred_location='Remote', expected_salary_range='80k-100k', created_at='2023-10-01', user_id=1)
    crud.create('users', first_name='John', last_name='Doe', phone_number='0987654321', state='CA', municipality='Los Angeles', zip_code='90001', email='john.doe@example.com', password='anotherpassword', created_at='2023-10-01', updated_at='2023-10-01')

    # Example UPDATE queries
    # crud.update('employers', 1, company_name='Tech Innovations', updated_at='2023-10-02')
    # crud.update('jobs', 1, job_title='Senior Software Engineer', updated_at='2023-10-02')
    # crud.update('qualifications', 1, degree='MSc Computer Science')
    # crud.update('saved_jobs', 1, saved_at='2023-10-02')
    # crud.update('submitted_resume', 1, resume_file_name='updated_resume.pdf')
    # crud.update('user_interest', 1, job_interest='Advanced Software Development')
    # crud.update('users', 1, first_name='Jonathan', updated_at='2023-10-02')
