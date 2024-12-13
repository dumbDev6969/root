from typing import Any
from utils.database import db, DatabaseError
from utils.logger import get_logger

logger = get_logger(__name__)

def create(table: str, **kwargs: Any) -> None:
    """Insert a new record into the specified table."""
    columns = ', '.join(kwargs.keys())
    placeholders = ', '.join('%s' for _ in kwargs)
    sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
    try:
        db.execute_query(sql, tuple(kwargs.values()))
        logger.info(f"Created new record in {table}")
    except DatabaseError as e:
        logger.error(f"Error creating record in {table}: {e}")
        raise

def create_tables() -> None:
    """Create tables in the database."""
    queries = [
        '''
        CREATE TABLE IF NOT EXISTS employers (
            employer_id INT AUTO_INCREMENT PRIMARY KEY,
            company_name VARCHAR(255) NOT NULL,
            phone_number VARCHAR(20) NOT NULL,
            state VARCHAR(50) NOT NULL,
            city_or_province VARCHAR(50),
            zip_code VARCHAR(10) NOT NULL,
            street VARCHAR(255),
            email VARCHAR(255),
            password VARCHAR(255) NOT NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL
        )
        ''',
        # Add other table creation queries here
    ]
    for query in queries:
        db.execute_query(query)
    logger.info("Tables created successfully")
