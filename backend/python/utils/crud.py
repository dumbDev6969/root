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
        logger.info("CRUD operations initialized with the provided database connection")

    def create(self, table: str, data: Dict[str, Any]) -> int:
        """Create a new record in the specified table."""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            result = self.db.execute_query(query, tuple(data.values()))
            return result.lastrowid if result else None
        except Exception as e:
            logger.error(f"Error creating record: {e}")
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
