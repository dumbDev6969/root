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
    def __init__(self, host: str, user: str, password: str, database: str, db_path: str = 'fallback_db.sqlite', pool_size: int = 20) -> None:
        """Initialize the Database class with an attempt to connect to MySQL, fallback to SQLite."""
        self.db_type = None
        try:
            dbconfig = {
                "pool_name": "mypool",
                "pool_size": pool_size,
                "host": host,
                "user": user,
                "password": password,
                "database": database,
                "connect_timeout": 30,
                "pool_reset_session": True,
                "autocommit": True,
                "get_warnings": True,
                "raise_on_warnings": True,
                "connection_timeout": 60,
                "pool_reset_session": True,
                "consume_results": True
            }
            self.pool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
            self.db_type = 'mysql'
            logger.info(f"MySQL database connection pool created successfully with size {pool_size}")
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
            retries = 3
            while retries > 0:
                try:
                    connection = self.pool.get_connection()
                    if connection.is_connected():
                        return connection
                except mysql.connector.Error as e:
                    logger.error(f"Error getting connection from pool (retries left: {retries-1}): {e}")
                    retries -= 1
                    if retries == 0:
                        raise DatabaseError(f"Failed to get connection after 3 attempts: {e}")
            return None
        elif self.db_type == 'sqlite':
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
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

            if self.db_type == 'sqlite':
                params = tuple(params) if params else ()
                cursor = conn.cursor()
            else:
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
            if retries == 0:
                raise DatabaseError(f"Failed to execute query after 3 attempts: {e}")

        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    if self.db_type == 'mysql':
                        conn.close()  # Return connection to pool
                    else:
                        conn.close()  # Close SQLite connection
                except:
                    pass
                    conn.close()  # Close SQLite connection

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
                if self.db_type == 'mysql':
                    conn.close()  # Return connection to pool
                else:
                    conn.close()  # Close SQLite connection

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
    database=os.getenv('DB_NAME', 'jobsearch'),
    pool_size=32
)
