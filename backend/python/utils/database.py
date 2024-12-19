import mysql.connector
from mysql.connector import pooling
import os
from typing import Optional, List, Dict, Any
from utils.logger import get_logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = get_logger(__name__)

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass

class Database:
    def __init__(self, host: str, user: str, password: str, database: str, db_path: str = 'fallback_db.sqlite', pool_size: int = 20) -> None:
        """Initialize the Database class with an attempt to connect to MySQL, fallback to SQLite."""
        self.db_type = None
        self.db_path = db_path
        max_retries = 3
        retry_count = 0
        last_error = None

        while retry_count < max_retries:
            try:
                dbconfig = {
                    "pool_name": "mypool",
                    "pool_size": int(os.getenv('DB_POOL_SIZE', pool_size)),
                    "host": os.getenv('DB_HOST'),
                    "user": os.getenv('DB_USER'),
                    "password": os.getenv('DB_PASSWORD'),
                    "database": os.getenv('DB_NAME'),
                    "port": int(os.getenv('DB_PORT', 3306)),
                    "charset": "utf8mb4",
                    "connect_timeout": 10,
                    "pool_reset_session": True,
                    "autocommit": True,
                    "get_warnings": True,
                    "raise_on_warnings": True,
                    "consume_results": True
                }
                self.pool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
                self.db_type = 'mysql'
                logger.info(f"MySQL database connection pool created successfully with size {pool_size}")
                return
            except mysql.connector.Error as e:
                last_error = e
                retry_count += 1
                logger.error(f"Error creating MySQL connection pool (attempt {retry_count}/{max_retries}): {e}")
                if retry_count < max_retries:
                    logger.info(f"Retrying connection in 5 seconds...")
                    import time
                    time.sleep(5)  # Wait 5 seconds before retrying

        # If MySQL connection fails after all retries, try SQLite fallback
        try:
            import sqlite3
            self.db_type = 'sqlite'
            logger.info(f"Falling back to SQLite database at {db_path}")
        except Exception as e:
            raise DatabaseError(f"Failed to establish any database connection. MySQL error: {last_error}, SQLite error: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_connection(self):
        """Get a new connection depending on the DB type with retry logic."""
        if self.db_type == 'mysql':
            retries = 3
            while retries > 0:
                try:
                    connection = self.pool.get_connection()
                    if connection.is_connected():
                        return connection
                except mysql.connector.Error as e:
                    logger.error(f"Error getting connection from pool (retries left: {retries-1}): {e}")
                    retries -= 1
                    if retries > 0:
                        import time
                        time.sleep(2)  # Wait 2 seconds before retrying
                    else:
                        raise DatabaseError(f"Failed to get connection after 3 attempts: {e}")
            return None
        elif self.db_type == 'sqlite':
            import sqlite3
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            # Enable foreign key constraints for SQLite
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        else:
            raise DatabaseError("No database connection type is set.")

    def execute_query(self, sql: str, params: Optional[tuple] = ()) -> Optional[List[Dict[str, Any]]]:
        """Execute a SQL query with optional parameters."""
        conn = None
        cursor = None
        retries = 3
        last_error = None

        while retries > 0:
            try:
                conn = self.get_connection()
                if not conn:
                    retries -= 1
                    continue

                cursor = conn.cursor(dictionary=True)
                cursor.execute(sql, params)
                
                if sql.strip().upper().startswith("SELECT"):
                    result = cursor.fetchall()
                else:
                    conn.commit()
                    result = cursor.lastrowid
                return result

            except (mysql.connector.Error, sqlite3.Error) as e:
                last_error = e
                logger.error(f"Database error (retries left: {retries-1}): {e}")
                if conn:
                    try:
                        conn.rollback()
                    except:
                        pass
                retries -= 1
                if retries > 0:
                    import time
                    time.sleep(2)  # Wait 2 seconds before retrying
                else:
                    raise DatabaseError(f"Failed to execute query after 3 attempts: {e}")

            finally:
                if cursor:
                    try:
                        cursor.close()
                    except:
                        pass
                if conn:
                    try:
                        conn.close()  # Return connection to pool or close SQLite connection
                    except Exception as e:
                        logger.error(f"Error closing connection: {e}")

    def execute_multiple_queries(self, sql: str) -> None:
        """Execute multiple SQL queries separated by semicolons."""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Split the SQL string into individual statements
            statements = sql.split(';')
            for statement in statements:
                if statement.strip():  # Skip empty statements
                    cursor.execute(statement)
            conn.commit()
        except (mysql.connector.Error, sqlite3.Error) as e:
            logger.error(f"Database error: {e}")
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise DatabaseError(f"Failed to execute multiple queries: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()  # Return connection to pool or close SQLite connection

    def import_sql_file(self, file_path: str, sql_content: str) -> None:
        """Import an SQL file into the database."""
        try:
            self.execute_multiple_queries(sql_content)
            logger.info(f"SQL file {file_path} imported successfully into database.")
        except Exception as e:
            logger.error(f"Failed to import SQL file {file_path}: {e}")
            raise DatabaseError(f"Failed to import SQL file {file_path}: {e}")

    def close(self) -> None:
        """Close the database connection pool if using MySQL."""
        if self.db_type == 'mysql':
            self.pool.close()
            logger.info("MySQL Database connection pool closed")

# Initialize the database connection
db = Database(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    pool_size=int(os.getenv('DB_POOL_SIZE', 32))
)
