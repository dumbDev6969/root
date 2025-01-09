from typing import Optional, List, Dict, Any
from utils.database import db, DatabaseError
from utils.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)

def serialize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """Serialize row data, converting datetime objects to ISO format strings."""
    if not row:
        return row
    
    serialized = {}
    for key, value in row.items():
        if isinstance(value, datetime):
            serialized[key] = value.isoformat()
        else:
            serialized[key] = value
    return serialized

def read(table: str, **kwargs: Any) -> Optional[List[Dict[str, Any]]]:
    """Read records from the specified table."""
    sql = f'SELECT * FROM {table}'
    if kwargs:
        conditions = ' AND '.join(f"{key} = %s" for key in kwargs.keys())
        sql += f' WHERE {conditions}'
    try:
        results = db.execute_query(sql, tuple(kwargs.values()) if kwargs else None)
        if results:
            return [serialize_row(row) for row in results]
        return results
    except DatabaseError as e:
        logger.error(f"Error reading from {table}: {e}")
        raise

def get_all_jobs() -> Optional[List[Dict[str, Any]]]:
    """Retrieve all jobs from the jobs table."""
    try:
        results = db.execute_query('SELECT * FROM jobs')
        if results:
            return [serialize_row(row) for row in results]
        return results
    except DatabaseError as e:
        logger.error(f"Error retrieving all jobs: {e}")
        raise
