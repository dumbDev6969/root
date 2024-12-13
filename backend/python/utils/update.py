from typing import Any
from utils.database import db, DatabaseError
from utils.logger import get_logger

logger = get_logger(__name__)

def update(table: str, id: int, **kwargs: Any) -> None:
    """Update a record in the specified table."""
    set_clause = ', '.join(f"{key} = %s" for key in kwargs.keys())
    sql = f'UPDATE {table} SET {set_clause} WHERE id = %s'
    try:
        db.execute_query(sql, (*kwargs.values(), id))
        logger.info(f"Updated record {id} in {table}")
    except DatabaseError as e:
        logger.error(f"Error updating record {id} in {table}: {e}")
        raise
