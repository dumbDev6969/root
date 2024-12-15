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
    def __init__(self, host: str, user: str, password: str, database: str, db_path: str = 'fallback_db.sqlite', pool_size: int = 5) -> None:
        """Initialize the Database class with an attempt to connect to MySQL, fallback to SQLite."""
        self.db_type = None
        try:
            self.pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=pool_size,
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.db_type = 'mysql'
            logger.info("MySQL database connection pool created successfully")
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
            return self.pool.get_connection()
        elif self.db_type == 'sqlite':
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        else:
            raise DatabaseError("No database connection type is set.")

    def execute_query(self, sql: str, params: Optional[tuple] = ()) -> Optional[List[Dict[str, Any]]]:
        """Execute a SQL query with optional parameters."""
        conn = self.get_connection()
        if self.db_type == 'sqlite':
            params = tuple(params) if params else ()
        try:
            with conn.cursor() if self.db_type == 'mysql' else conn:
                cursor = conn.execute(sql, params) if self.db_type == 'sqlite' else conn.cursor(dictionary=True)
                cursor.execute(sql, params)
                if sql.strip().upper().startswith("SELECT"):
                    return cursor.fetchall()
                else:
                    conn.commit()
                    return None
        except (mysql.connector.Error, sqlite3.Error) as e:
            logger.error(f"Database error: {e}")
            raise DatabaseError(f"Failed to execute query: {e}")
        finally:
            if self.db_type == 'sqlite':
                conn.close()

    def execute_multiple_queries(self, sql: str) -> None:
        """Execute multiple SQL queries separated by semicolons."""
        conn = self.get_connection()
        try:
            with conn.cursor() if self.db_type == 'mysql' else conn:
                # Split the SQL string into individual statements
                statements = sql.split(';')
                for statement in statements:
                    if statement.strip():  # Skip empty statements
                        cursor = conn.execute(statement) if self.db_type == 'sqlite' else conn.cursor()
                        cursor.execute(statement)
                conn.commit()
        except (mysql.connector.Error, sqlite3.Error) as e:
            logger.error(f"Database error: {e}")
            raise DatabaseError(f"Failed to execute multiple queries: {e}")
        finally:
            if self.db_type == 'sqlite':
                conn.close()

    def close(self) -> None:
        """Close the MySQL database connection pool."""
        if self.db_type == 'mysql':
            self.pool.close()
            logger.info("MySQL Database connection pool closed")

# Initialize the database connection
db = Database(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'jobsearch')
)

# # Execute multiple queries to create tables
# db.execute_multiple_queries("""
# CREATE TABLE IF NOT EXISTS employers (
#     employer_id INTEGER PRIMARY KEY,
#     company_name TEXT NOT NULL,
#     phone_number TEXT NOT NULL,
#     state TEXT NOT NULL,
#     city_or_province TEXT,
#     zip_code TEXT NOT NULL,
#     street TEXT,
#     email TEXT,
#     password TEXT NOT NULL,
#     created_at TEXT NOT NULL,
#     updated_at TEXT NOT NULL
# );

# CREATE TABLE IF NOT EXISTS jobs (
#     job_id INTEGER PRIMARY KEY,
#     employer_id INTEGER NOT NULL,
#     job_title TEXT NOT NULL,
#     job_type TEXT CHECK(job_type IN ('Full-time', 'Part-time', 'Freelance', 'Internship')) NOT NULL,
#     location TEXT NOT NULL,
#     salary_range TEXT NOT NULL,
#     job_description TEXT NOT NULL,
#     requirements TEXT NOT NULL,
#     created_at TEXT NOT NULL,
#     FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
# );

# CREATE TABLE IF NOT EXISTS qualifications (
#     qualification_id INTEGER PRIMARY KEY,
#     user_id INTEGER NOT NULL,
#     degree TEXT NOT NULL,
#     school_graduated TEXT NOT NULL,
#     certifications TEXT,
#     specialized_training TEXT,
#     FOREIGN KEY (user_id) REFERENCES users(user_id)
# );

# CREATE TABLE IF NOT EXISTS saved_jobs (
#     saved_job_id INTEGER PRIMARY KEY,
#     saved_at TEXT NOT NULL,
#     user_id INTEGER NOT NULL,
#     job_id INTEGER NOT NULL,
#     FOREIGN KEY (user_id) REFERENCES users(user_id),
#     FOREIGN KEY (job_id) REFERENCES jobs(job_id)
# );

# CREATE TABLE IF NOT EXISTS submitted_resumes (
#     submitted_resume_id INTEGER PRIMARY KEY,
#     resume_file_name TEXT NOT NULL,
#     resume_path TEXT NOT NULL,
#     submitted_at TEXT NOT NULL,
#     user_id INTEGER NOT NULL,
#     job_id INTEGER NOT NULL,
#     FOREIGN KEY (user_id) REFERENCES users(user_id),
#     FOREIGN KEY (job_id) REFERENCES jobs(job_id)
# );

# CREATE TABLE IF NOT EXISTS user_interest (
#     interest_id INTEGER PRIMARY KEY,
#     job_interest TEXT NOT NULL,
#     job_type TEXT CHECK(job_type IN ('Full-time', 'Part-time', 'Freelance', 'Internship')) NOT NULL,
#     preferred_location TEXT NOT NULL,
#     expected_salary_range TEXT NOT NULL,
#     created_at TEXT NOT NULL,
#     user_id INTEGER NOT NULL,
#     FOREIGN KEY (user_id) REFERENCES users(user_id)
# );

# CREATE TABLE IF NOT EXISTS users (
#     user_id INTEGER PRIMARY KEY,
#     first_name TEXT NOT NULL,
#     last_name TEXT NOT NULL,
#     phone_number TEXT NOT NULL,
#     state TEXT NOT NULL,
#     city_or_province TEXT,
#     municipality TEXT NOT NULL,
#     zip_code TEXT NOT NULL,
#     street TEXT,
#     email TEXT NOT NULL,
#     password TEXT NOT NULL,
#     created_at TEXT NOT NULL,
#     updated_at TEXT NOT NULL
# );
# """)

