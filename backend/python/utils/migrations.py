import mysql.connector
from mysql.connector import pooling
import os
from typing import List
from utils.logger import get_logger

logger = get_logger(__name__)

class DatabaseMigration:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }

    def execute_migration(self, migration_sql: str):
        try:
            with mysql.connector.connect(**self.config) as connection:
                with connection.cursor() as cursor:
                    for result in cursor.execute(migration_sql, multi=True):
                        if result.with_rows:
                            logger.info(f"Rows produced by statement '{result.statement}': {result.fetchall()}")
                        else:
                            logger.info(f"Number of rows affected by statement '{result.statement}': {result.rowcount}")
            logger.info("Migration executed successfully")
        except mysql.connector.Error as err:
            logger.error(f"Error executing migration: {err}")
            raise

    def run_migrations(self, migrations: List[str]):
        for migration in migrations:
            logger.info(f"Executing migration: {migration}")
            self.execute_migration(migration)

# Example migrations
migrations = [
    """
    CREATE TABLE IF NOT EXISTS migration_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        migration_name VARCHAR(255) NOT NULL,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    ALTER TABLE employers
    ADD COLUMN IF NOT EXISTS profile_picture VARCHAR(255);
    """,
    # Add more migrations as needed
]

if __name__ == "__main__":
    migration_runner = DatabaseMigration(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'jobsearch')
    )
    migration_runner.run_migrations(migrations)
