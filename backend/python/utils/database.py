import mysql.connector
from mysql.connector import pooling
import os
from typing import Optional, List, Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass

class Database:
    def __init__(self, host: str, user: str, password: str, database: str, pool_size: int = 5) -> None:
        """Initialize the Database class with MySQL connection pool."""
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

    def close(self) -> None:
        """Close the database connection pool."""
        self.pool.close()
        logger.info("Database connection pool closed")

# Initialize the database connection
db = Database(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'jobsearch')
)
