import mysql.connector
from mysql.connector import pooling
import os
from typing import Optional, List, Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass

class CRUD:
    def __init__(self, host: str, user: str, password: str, database: str, pool_size: int = 5) -> None:
        """Initialize the CRUD class with MySQL connection pool."""
        try:
            self.pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=pool_size,
                host=host,
                user=user,
                password=password,
                database=database
            )
            logger.info("Database connection pool created successfully")
        except mysql.connector.Error as e:
            logger.error(f"Error creating connection pool: {e}")
            raise DatabaseError(f"Failed to create database connection pool: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_connection(self):
        return self.pool.get_connection()

    def create_tables(self) -> None:
        """Create tables in the database."""
        queries = [
            '''
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
            ''',
            # Add other table creation queries here
        ]
        for query in queries:
            self.execute_query(query)

    def execute_query(self, sql: str, params: Optional[tuple] = ()) -> Optional[List[Dict[str, Any]]]:
        """Execute a SQL query with optional parameters."""
        with self.get_connection() as connection:
            try:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(sql, params)
                    if sql.strip().upper().startswith("SELECT"):
                        return cursor.fetchall()
                    else:
                        connection.commit()
                        return None
            except mysql.connector.Error as e:
                logger.error(f"Database error: {e}")
                raise DatabaseError(f"Failed to execute query: {e}")

    def create(self, table: str, **kwargs: Any) -> None:
        """Insert a new record into the specified table."""
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join('%s' for _ in kwargs)
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        try:
            self.execute_query(sql, tuple(kwargs.values()))
            logger.info(f"Created new record in {table}")
        except DatabaseError as e:
            logger.error(f"Error creating record in {table}: {e}")
            raise

    def read(self, table: str, **kwargs: Any) -> Optional[List[Dict[str, Any]]]:
        """Read records from the specified table."""
        sql = f'SELECT * FROM {table}'
        if kwargs:
            conditions = ' AND '.join(f"{key} = %s" for key in kwargs.keys())
            sql += f' WHERE {conditions}'
        try:
            return self.execute_query(sql, tuple(kwargs.values()) if kwargs else None)
        except DatabaseError as e:
            logger.error(f"Error reading from {table}: {e}")
            raise

    def update(self, table: str, id: int, **kwargs: Any) -> None:
        """Update a record in the specified table."""
        set_clause = ', '.join(f"{key} = %s" for key in kwargs.keys())
        sql = f'UPDATE {table} SET {set_clause} WHERE id = %s'
        try:
            self.execute_query(sql, (*kwargs.values(), id))
            logger.info(f"Updated record {id} in {table}")
        except DatabaseError as e:
            logger.error(f"Error updating record {id} in {table}: {e}")
            raise

    def delete(self, table: str, id: int) -> None:
        """Delete a record from the specified table."""
        sql = f'DELETE FROM {table} WHERE id = %s'
        try:
            self.execute_query(sql, (id,))
            logger.info(f"Deleted record {id} from {table}")
        except DatabaseError as e:
            logger.error(f"Error deleting record {id} from {table}: {e}")
            raise

    def get_all_jobs(self) -> Optional[List[Dict[str, Any]]]:
        """Retrieve all jobs from the jobs table."""
        try:
            return self.execute_query('SELECT * FROM jobs')
        except DatabaseError as e:
            logger.error(f"Error retrieving all jobs: {e}")
            raise

    def close(self) -> None:
        """Close the database connection pool."""
        self.pool.close()
        logger.info("Database connection pool closed")

# Example usage
if __name__ == "__main__":
    # Use environment variables for credentials
    with CRUD(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'jobsearch')
    ) as crud:
        # Example INSERT query
        try:
            crud.create('employers', 
                        company_name='Tech Corp', 
                        phone_number='1234567890', 
                        state='CA', 
                        zip_code='90001', 
                        email='contact@techcorp.com', 
                        password='securepassword', 
                        created_at='2023-10-01', 
                        updated_at='2023-10-01')
            logger.info("Example query executed successfully")
        except DatabaseError as e:
            logger.error(f"Failed to execute example query: {e}")
        # Add other example queries here
