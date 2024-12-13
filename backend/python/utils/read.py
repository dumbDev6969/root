from typing import Optional, List, Dict, Any
from utils.database import db, DatabaseError
from utils.logger import get_logger

logger = get_logger(__name__)

def read(table: str, **kwargs: Any) -> Optional[List[Dict[str, Any]]]:
    """Read records from the specified table."""
    sql = f'SELECT * FROM {table}'
    if kwargs:
        conditions = ' AND '.join(f"{key} = %s" for key in kwargs.keys())
        sql += f' WHERE {conditions}'
    try:
        return db.execute_query(sql, tuple(kwargs.values()) if kwargs else None)
    except DatabaseError as e:
        logger.error(f"Error reading from {table}: {e}")
        raise

def get_all_jobs() -> Optional[List[Dict[str, Any]]]:
    """Retrieve all jobs from the jobs table."""
    try:
        return db.execute_query('SELECT * FROM jobs')
    except DatabaseError as e:
        logger.error(f"Error retrieving all jobs: {e}")
        raise
