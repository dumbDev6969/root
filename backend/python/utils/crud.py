import mysql.connector
from mysql.connector import pooling
import sqlite3
from typing import Optional, List, Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass

class CRUD:
    def __init__(self, db):
        """Initialize the CRUD class with a Database instance."""
        self.db = db
        if not self.db.verify_connection():
            raise DatabaseError("Failed to verify database connection during CRUD initialization")
        logger.info("CRUD operations initialized with verified database connection")

    def verify_foreign_key(self, table: str, column: str, value: Any) -> bool:
        """Verify if a foreign key reference exists."""
        try:
            # Extract the referenced table from common foreign key patterns
            referenced_table = column.replace('_id', 's')  # e.g., employer_id -> employers
            query = f"SELECT COUNT(*) as count FROM {referenced_table} WHERE {column} = %s"
            result = self.db.execute_query(query, (value,))
            return result[0]['count'] > 0 if result else False
        except Exception as e:
            logger.error(f"Error verifying foreign key: {e}")
            return False

    def create(self, table: str, data: Dict[str, Any]) -> int:
        """Create a new record in the specified table."""
        try:
            # Verify foreign key constraints before insert
            if table == 'jobs' and 'employer_id' in data:
                if not self.verify_foreign_key('employers', 'employer_id', data['employer_id']):
                    raise DatabaseError(f"Invalid employer_id: {data['employer_id']} does not exist")

            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            logger.debug(f"Executing query: {query} with values: {tuple(data.values())}")
            
            result = self.db.execute_query(query, tuple(data.values()))
            if result is None:
                raise DatabaseError("Failed to create record: No result returned")
            return result
        except mysql.connector.Error as e:
            error_msg = str(e)
            logger.error(f"MySQL error creating record: {error_msg}")
            if "foreign key constraint fails" in error_msg.lower():
                # Extract the constraint details for better error message
                raise DatabaseError(f"Foreign key constraint failed: Please ensure referenced IDs exist")
            elif "duplicate entry" in error_msg.lower():
                raise DatabaseError("A record with these details already exists")
            else:
                raise DatabaseError(f"Database error: {error_msg}")
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating record: {e}")
            raise DatabaseError(f"Failed to create record: {e}")

    def read(self, table: str, conditions: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Read records from the specified table."""
        query = f"SELECT * FROM {table}"
        params = ()

        if conditions:
            where_clause = ' AND '.join([f"{key} = %s" for key in conditions.keys()])
            query += f" WHERE {where_clause}"
            params = tuple(conditions.values())

        try:
            return self.db.execute_query(query, params)
        except Exception as e:
            logger.error(f"Error reading records: {e}")
            raise DatabaseError(f"Failed to read records: {e}")

    def update(self, table: str, data: Dict[str, Any], conditions: Dict[str, Any]) -> int:
        """Update records in the specified table."""
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        where_clause = ' AND '.join([f"{key} = %s" for key in conditions.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = tuple(list(data.values()) + list(conditions.values()))

        try:
            result = self.db.execute_query(query, params)
            return result.rowcount if result else 0
        except Exception as e:
            logger.error(f"Error updating records: {e}")
            raise DatabaseError(f"Failed to update records: {e}")

    def delete(self, table: str, conditions: Dict[str, Any]) -> int:
        """Delete records from the specified table."""
        where_clause = ' AND '.join([f"{key} = %s" for key in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        params = tuple(conditions.values())

        try:
            result = self.db.execute_query(query, params)
            return result.rowcount if result else 0
        except Exception as e:
            logger.error(f"Error deleting records: {e}")
            raise DatabaseError(f"Failed to delete records: {e}")
