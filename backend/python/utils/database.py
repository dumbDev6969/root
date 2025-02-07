import mysql.connector
from mysql.connector import pooling
import os
from typing import Optional, List, Dict, Any
from utils.logger import get_logger
from dotenv import load_dotenv
import sqlite3
# Load environment variables
load_dotenv()

logger = get_logger(__name__)

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass

class Database:
     # Default to online database
    
    def __init__(self, host: str, user: str, password: str, database: str, db_path: str = 'fallback_db.sqlite', pool_size: int = 20) -> None:
        """Initialize the Database class with an attempt to connect to MySQL, fallback to SQLite."""
        self.db_type = None
        self.db_path = db_path
        max_retries = 3
        retry_count = 0
        last_error = None
        self.server = {"local": False, "online": True}

        while retry_count < max_retries:
            try:
                # Configure connection based on server setting
                if self.server["local"]:
                    dbconfig = {
                        "pool_name": "mypool",
                        "pool_size": int(os.getenv('DB_POOL_SIZE', pool_size)),
                        "host": "localhost",  # Local XAMPP MySQL server
                        "user": "root",       # Default XAMPP user
                        "password": "",       # Default XAMPP password
                        "database": os.getenv('DB_NAME'),
                        "port": 3306,         # Default XAMPP port
                        "charset": "utf8mb4",
                        "connect_timeout": 10,
                        "pool_reset_session": True,
                        "autocommit": True,
                        "get_warnings": True,
                        "raise_on_warnings": True,
                        "consume_results": True
                    }
                else:
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
        """Get a new connection with retry logic and connection verification."""
        retries = 3
        while retries > 0:
            try:
                connection = self.pool.get_connection()
                # Verify connection is working with a simple query
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.close()
                return connection
            except mysql.connector.Error as e:
                logger.error(f"Error getting connection from pool (retries left: {retries-1}): {e}")
                retries -= 1
                if retries > 0:
                    import time
                    time.sleep(2)  # Wait 2 seconds before retrying
                else:
                    raise DatabaseError(f"Failed to get connection after 3 attempts: {e}")
            except Exception as e:
                logger.error(f"Unexpected error getting connection: {e}")
                retries -= 1
                if retries > 0:
                    import time
                    time.sleep(2)
                else:
                    raise DatabaseError(f"Failed to verify connection: {e}")
        raise DatabaseError("Failed to get a valid database connection")

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

    def verify_connection(self) -> bool:
        """Verify database connection is working."""
        try:
            conn = self.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.close()
                conn.close()
                return True
            return False
        except Exception as e:
            logger.error(f"Connection verification failed: {e}")
            return False

    def close(self) -> None:
        """Close the database connection pool."""
        try:
            self.pool.close()
            logger.info("MySQL Database connection pool closed")
        except Exception as e:
            logger.error(f"Error closing connection pool: {e}")

# Initialize the database connection
db = Database(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    pool_size=int(os.getenv('DB_POOL_SIZE', 32))
)
