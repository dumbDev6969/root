from utils.database import db, DatabaseError
from utils.logger import get_logger

logger = get_logger(__name__)

def delete(table: str, id: int) -> None:
    """Delete a record from the specified table."""
    sql = f'DELETE FROM {table} WHERE id = %s'
    try:
        db.execute_query(sql, (id,))
        logger.info(f"Deleted record {id} from {table}")
    except DatabaseError as e:
        logger.error(f"Error deleting record {id} from {table}: {e}")
        raise
