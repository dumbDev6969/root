import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
server = {"local": False, "online": True}

if server["local"]:
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': os.getenv('DB_NAME'),
        'port': 3306,
        'charset': 'utf8mb4',
        'pool_name': 'mypool',
        'pool_size': int(os.getenv('DB_POOL_SIZE', 20)),
        'connect_timeout': 10,
        'pool_reset_session': True,
        'autocommit': True
    }
else:
    DB_CONFIG = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'charset': 'utf8mb4',
        'pool_name': 'mypool',
        'pool_size': int(os.getenv('DB_POOL_SIZE', 20)),
        'connect_timeout': 10,
        'pool_reset_session': True,
        'autocommit': True
    }


# Create a connection pool
try:
    pool = mysql.connector.pooling.MySQLConnectionPool(**DB_CONFIG)
    print("Connection pool created successfully")
except Error as e:
    print(f"Error creating pool: {e}")

from utils.database import db

def get_connection():
    """
    Establishes and returns a connection using the Database class, with fallback to SQLite.
    """
    try:
        connection = db.get_connection()
        return connection
    except Exception as e:
        print(f"Error while getting database connection: {e}")
        return None

# ---------------------- Employers CRUD Operations ----------------------

def create_employer(employer_uuid, company_name, phone_number, state, zip_code, password, email=None,
                    city_or_province=None, street=None):
    """
    Creates a new employer record.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor()
        query = """
            INSERT INTO employers (employer_uuid, company_name, phone_number, state, zip_code, password, email, city_or_province, street, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        created_at = datetime.now()
        current_time = created_at
        cursor.execute(query, (
            employer_uuid, company_name, phone_number, state, zip_code, password, email,
            city_or_province, street, current_time, current_time
        ))
        connection.commit()
        return {'success': True, 'message': 'Employer created successfully.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def read_employer(employer_id):
    """
    Retrieves an employer record by employer_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM employers WHERE employer_id = %s"
        cursor.execute(query, (employer_id,))
        result = cursor.fetchone()
        if result:
            return {'success': True, 'message':result}
        else:
            return {'success': False, 'message': 'Employer not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def update_employer(employer_id, **kwargs):
    """
    Updates an employer record. Accepts keyword arguments for fields to update.
    """
    try:
        if not kwargs:
            return {'success': False, 'message': 'No fields to update provided.'}
        
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor()
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = %s")
            values.append(value)
        fields.append("updated_at = %s")
        values.append(datetime.now())
        values.append(employer_id)
        set_clause = ", ".join(fields)
        query = f"UPDATE employers SET {set_clause} WHERE employer_id = %s"
        cursor.execute(query, tuple(values))
        connection.commit()
        if cursor.rowcount:
            return {'success': True, 'message': 'Employer updated successfully.'}
        else:
            return {'success': False, 'message': 'Employer not found or no changes made.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_employer(employer_id):
    """
    Deletes an employer record by employer_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor()
        query = "DELETE FROM employers WHERE employer_id = %s"
        cursor.execute(query, (employer_id,))
        connection.commit()
        if cursor.rowcount:
            return {'success': True, 'message': 'Employer deleted successfully.'}
        else:
            return {'success': False, 'message': 'Employer not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# ---------------------- Jobs CRUD Operations ----------------------

def create_job(employer_id, job_title, job_type, location, salary_range, job_description, requirements, created_at=None):
    """
    Creates a new job record.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}

        # Verify employer exists
        cursor = connection.cursor(dictionary=True)
        verify_query = "SELECT employer_id FROM employers WHERE employer_id = %s"
        cursor.execute(verify_query, (employer_id,))
        if not cursor.fetchone():
            return {'success': False, 'message': f'Employer with ID {employer_id} does not exist.'}

        # Validate job_type
        valid_job_types = ['Full-time', 'Part-time', 'Freelance', 'Internship']
        if job_type not in valid_job_types:
            return {'success': False, 'message': f'Invalid job_type. Must be one of: {", ".join(valid_job_types)}'}
        
        cursor = connection.cursor()
        query = """
            INSERT INTO jobs (employer_id, job_title, job_type, location, salary_range, job_description, requirements, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        current_time = created_at if created_at else datetime.now()
        cursor.execute(query, (
            employer_id, job_title, job_type, location, salary_range,
            job_description, requirements, current_time
        ))
        connection.commit()
        return {'success': True, 'message': 'Job created successfully.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def read_job(job_id):
    """
    Retrieves a job record by job_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM jobs WHERE job_id = %s"
        cursor.execute(query, (job_id,))
        result = cursor.fetchone()
        if result:
            return {'success': True, 'message':result}
        else:
            return {'success': False, 'message': 'Job not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def update_job(job_id, **kwargs):
    """
    Updates a job record. Accepts keyword arguments for fields to update.
    """
    try:
        if not kwargs:
            return {'success': False, 'message': 'No fields to update provided.'}
        
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor()
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = %s")
            values.append(value)
        fields.append("updated_at = %s")
        values.append(datetime.now())
        values.append(job_id)
        set_clause = ", ".join(fields)
        query = f"UPDATE jobs SET {set_clause} WHERE job_id = %s"
        cursor.execute(query, tuple(values))
        connection.commit()
        if cursor.rowcount:
            return {'success': True, 'message': 'Job updated successfully.'}
        else:
            return {'success': False, 'message': 'Job not found or no changes made.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_job(job_id):
    """
    Deletes a job record by job_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor()
        query = "DELETE FROM jobs WHERE job_id = %s"
        cursor.execute(query, (job_id,))
        connection.commit()
        if cursor.rowcount:
            return {'success': True, 'message': 'Job deleted successfully.'}
        else:
            return {'success': False, 'message': 'Job not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# ---------------------- Qualifications CRUD Operations ----------------------

def create_qualification(user_id, degree, school_graduated, certifications=None, specialized_training=None):
    """
    Creates a new qualification record.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor()
        query = """
            INSERT INTO qualifications (user_id, degree, school_graduated, certifications, specialized_training)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user_id, degree, school_graduated, certifications, specialized_training
        ))
        connection.commit()
        return {'success': True, 'message': 'Qualification created successfully.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def read_qualification(qualification_id):
    """
    Retrieves a qualification record by qualification_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM qualifications WHERE qualification_id = %s"
        cursor.execute(query, (qualification_id,))
        result = cursor.fetchone()
        if result:
            return {'success': True, 'message':result}
        else:
            return {'success': False, 'message': 'Qualification not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def update_qualification(qualification_id, **kwargs):
    """
    Updates a qualification record. Accepts keyword arguments for fields to update.
    """
    try:
        if not kwargs:
            return {'success': False, 'message': 'No fields to update provided.'}
        
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor()
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = %s")
            values.append(value)
        set_clause = ", ".join(fields)
        values.append(qualification_id)
        query = f"UPDATE qualifications SET {set_clause} WHERE qualification_id = %s"
        cursor.execute(query, tuple(values))
        connection.commit()
        if cursor.rowcount:
            return {'success': True, 'message': 'Qualification updated successfully.'}
        else:
            return {'success': False, 'message': 'Qualification not found or no changes made.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_qualification(qualification_id):
    """
    Deletes a qualification record by qualification_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor()
        query = "DELETE FROM qualifications WHERE qualification_id = %s"
        cursor.execute(query, (qualification_id,))
        connection.commit()
        if cursor.rowcount:
            return {'success': True, 'message': 'Qualification deleted successfully.'}
        else:
            return {'success': False, 'message': 'Qualification not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# ---------------------- Saved Jobs CRUD Operations ----------------------

def create_saved_job(user_id, job_id):
    """
    Creates a new saved job record.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor()
        query = """
            INSERT INTO saved_jobs (saved_at, user_id, job_id)
            VALUES (%s, %s, %s)
        """
        current_time = datetime.now()
        cursor.execute(query, (
            current_time, user_id, job_id
        ))
        connection.commit()
        return {'success': True, 'message': 'Job saved successfully.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def read_saved_job(saved_job_id):
    """
    Retrieves a saved job record by saved_job_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}

        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM saved_jobs WHERE saved_job_id = %s"
        cursor.execute(query, (saved_job_id,))
        result = cursor.fetchone()
        if result:
            return {'success': True, 'message':result}
        else:
            return {'success': False, 'message': 'Saved job not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def update_saved_job(saved_job_id, **kwargs):
    """
    Updates a saved job record. Accepts keyword arguments for fields to update.
    """
    try:
        if not kwargs:
            return {'success': False, 'message': 'No fields to update provided.'}

        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}

        cursor = connection.cursor()
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = %s")
            values.append(value)
        set_clause = ", ".join(fields)
        values.append(saved_job_id)
        query = f"UPDATE saved_jobs SET {set_clause} WHERE saved_job_id = %s"
        cursor.execute(query, tuple(values))
        connection.commit()
        if cursor.rowcount:
            return {'success': True, 'message': 'Saved job updated successfully.'}
        else:
            return {'success': False, 'message': 'Saved job not found or no changes made.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_saved_job(saved_job_id):
    """
    Deletes a saved job record by saved_job_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}

        cursor = connection.cursor()
        query = "DELETE FROM saved_jobs WHERE saved_job_id = %s"
        cursor.execute(query, (saved_job_id,))
        connection.commit()
        if cursor.rowcount:
            return {'success': True, 'message': 'Saved job deleted successfully.'}
        else:
            return {'success': False, 'message': 'Saved job not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# ---------------------- Submitted Resume CRUD Operations ----------------------

def create_submitted_resume(resume_file_name, resume_path, user_id, job_id):
    """
    Creates a new submitted resume record.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor()
        query = """
            INSERT INTO submitted_resume (resume_file_name, resume_path, submitted_at, user_id, job_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        current_time = datetime.now()
        cursor.execute(query, (
            resume_file_name, resume_path, current_time, user_id, job_id
        ))
        connection.commit()
        return {'success': True, 'message': 'Resume submitted successfully.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def read_submitted_resume(submitted_resume_id):
    """
    Retrieves a submitted resume record by submitted_resume_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}

        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM submitted_resume WHERE submitted_resume_id = %s"
        cursor.execute(query, (submitted_resume_id,))
        result = cursor.fetchone()
        if result:
            return {'success': True, 'message':result}
        else:
            return {'success': False, 'message': 'Submitted resume not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def update_submitted_resume(submitted_resume_id, **kwargs):
    """
    Updates a submitted resume record. Accepts keyword arguments for fields to update.
    """
    try:
        if not kwargs:
            return {'success': False, 'message': 'No fields to update provided.'}

        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}

        cursor = connection.cursor()
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = %s")
            values.append(value)
        set_clause = ", ".join(fields)
        values.append(submitted_resume_id)
        query = f"UPDATE submitted_resume SET {set_clause} WHERE submitted_resume_id = %s"
        cursor.execute(query, tuple(values))
        connection.commit()
        if cursor.rowcount:
            return {'success': True, 'message': 'Submitted resume updated successfully.'}
        else:
            return {'success': False, 'message': 'Submitted resume not found or no changes made.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_submitted_resume(submitted_resume_id):
    """
    Deletes a submitted resume record by submitted_resume_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}

        cursor = connection.cursor()
        query = "DELETE FROM submitted_resume WHERE submitted_resume_id = %s"
        cursor.execute(query, (submitted_resume_id,))
        connection.commit()
        if cursor.rowcount:
            return {'success': True, 'message': 'Submitted resume deleted successfully.'}
        else:
            return {'success': False, 'message': 'Submitted resume not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# ---------------------- User Interest CRUD Operations ----------------------

def create_user_interest(job_interest, job_type, preferred_location, expected_salary_range, user_id):
    """
    Creates a new user interest record.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}

        cursor = connection.cursor()
        query = """
            INSERT INTO user_interest (job_interest, job_type, preferred_location, expected_salary_range, created_at, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        current_time = datetime.now()
        cursor.execute(query, (
            job_interest, job_type, preferred_location, expected_salary_range, current_time, user_id
        ))
        connection.commit()
        return {'success': True, 'message': 'User interest created successfully.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def read_user_interest(interest_id):
    """
    Retrieves a user interest record by interest_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}

        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM user_interest WHERE interest_id = %s"
        cursor.execute(query, (interest_id,))
        result = cursor.fetchone()
        
        if result:
            return {'success': True, 'message':result}
        else:
            return {'success': False, 'message': 'User interest not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def update_user_interest(interest_id, **kwargs):
    """
    Updates a user interest record. Accepts keyword arguments for fields to update.
    """
    try:
        if not kwargs:
            return {'success': False, 'message': 'No fields to update provided.'}

        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}

        cursor = connection.cursor()
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = %s")
            values.append(value)
        set_clause = ", ".join(fields)
        values.append(interest_id)
        query = f"UPDATE user_interest SET {set_clause} WHERE interest_id = %s"
        cursor.execute(query, tuple(values))
        connection.commit()
        if cursor.rowcount:
            return {'success': True, 'message': 'User interest updated successfully.'}
        else:
            return {'success': False, 'message': 'User interest not found or no changes made.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_user_interest(interest_id):
    """
    Deletes a user interest record by interest_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}

        cursor = connection.cursor()
        query = "DELETE FROM user_interest WHERE interest_id = %s"
        cursor.execute(query, (interest_id,))
        connection.commit()
        if cursor.rowcount:
            return {'success': True, 'message': 'User interest deleted successfully.'}
        else:
            return {'success': False, 'message': 'User interest not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# ---------------------- Users CRUD Operations ----------------------

def create_user(user_uuid, first_name, last_name, phone_number, state, municipality, zip_code, email, password,
                street=None):
    """
    Creates a new user record.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}

        cursor = connection.cursor()
        query = """
            INSERT INTO users (user_uuid, first_name, last_name, phone_number, state, municipality, zip_code, email, password, street, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        current_time = datetime.now()
        cursor.execute(query, (
            user_uuid, first_name, last_name, phone_number, state, municipality, zip_code,
            email, password, street, current_time, current_time
        ))
        connection.commit()
        return {'success': True, 'message': 'User created successfully.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def read_user(user_id):
    """
    Retrieves a user record by user_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result:
            return {'success': True, 'message':result}
        else:
            return {'success': False, 'message': 'User not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def read_email_user(email):
    """
    Retrieves a user record by user_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return {'success': True, 'message':result}
        else:
            return {'success': False, 'message': 'User not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def read_email_employers(email):
    """
    Retrieves an employer record by email.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM employers WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return {'success': True, 'message':result}
        else:
            return {'success': False, 'message': 'User not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def update_user(user_id, **kwargs):
    """
    Updates a user record. Accepts keyword arguments for fields to update.
    """
    try:
        if not kwargs:
            return {'success': False, 'message': 'No fields to update provided.'}
        
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor()
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = %s")
            values.append(value)
        fields.append("updated_at = %s")
        values.append(datetime.now())
        values.append(user_id)
        set_clause = ", ".join(fields)
        query = f"UPDATE users SET {set_clause} WHERE user_id = %s"
        try:
            print(f"Executing query: {query}")
            print(f"With values: {values}")
            cursor.execute(query, tuple(values))
        except Error as e:
            print(f"Database error: {e}")
            raise
        connection.commit()
        if cursor.rowcount:
            return {'success': True, 'message': 'User updated successfully.'}
        else:
            return {'success': False, 'message': 'User not found or no changes made.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_user(user_id):
    """
    Deletes a user record by user_id.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}
        
        cursor = connection.cursor()
        query = "DELETE FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()
        if cursor.rowcount:
            return {'success': True, 'message': 'User deleted successfully.'}
        else:
            return {'success': False, 'message': 'User not found.'}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# ---------------------- Retrieve All Records ----------------------

def get_all_records(table_name):
    """
    Retrieves all records from the specified table.
    """
    try:
        connection = get_connection()
        if not connection:
            return {'success': False, 'message': 'Database connection failed.'}

        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        results = cursor.fetchall()
        return {'success': True, 'message': results}
    except Error as e:
        return {'success': False, 'message': str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# if __name__ == "__main__":
    # Example operations. Uncomment to use.

    # Create a new user
    # response = create_user(
    #     first_name="John",
    #     last_name="Doe",
    #     phone_number="123-456-7890",
    #     state="California",
    #     municipality="Los Angeles",
    #     zip_code="90001",
    #     email="john.doe@example.com",
    #     password="securepassword",
    #     city_or_province="Los Angeles",
    #     street="123 Main St"
    # )
    # print(response)

    # Read user information
    # response = read_user(user_id=1)
    # print(response)

    # Update user information
    # response = update_user(user_id=1, phone_number="098-765-4321")
    # print(response)

    # Delete a user
    # response = delete_user(user_id=1)
