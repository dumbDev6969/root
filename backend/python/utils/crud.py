import mysql.connector
import os
from typing import Optional, List, Dict, Any

class CRUD:
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        """Initialize the CRUD class with MySQL connection details."""
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as e:
            print(f"Connection error: {e}")

    def create_tables(self) -> None:
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
            self.execute_query(query)

    def execute_query(self, sql: str, params: Optional[tuple] = ()) -> Optional[List[Dict[str, Any]]]:
        """Execute a SQL query with optional parameters."""
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"An error occurred: {e}")
            return None

    def create(self, table: str, **kwargs: Any) -> None:
        """Insert a new record into the specified table."""
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join('%s' for _ in kwargs)
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        self.execute_query(sql, tuple(kwargs.values()))

    def read(self, table: str, **kwargs: Any) -> Optional[List[Dict[str, Any]]]:
        """Read records from the specified table."""
        sql = f'SELECT * FROM {table}'
        if kwargs:
            conditions = ' AND '.join(f"{key} = %s" for key in kwargs.keys())
            sql += f' WHERE {conditions}'
            return self.execute_query(sql, tuple(kwargs.values()))
        else:
            return self.execute_query(sql)

    def update(self, table: str, id: int, **kwargs: Any) -> None:
        """Update a record in the specified table."""
        set_clause = ', '.join(f"{key} = %s" for key in kwargs.keys())
        sql = f'UPDATE {table} SET {set_clause} WHERE id = %s'
        self.execute_query(sql, (*kwargs.values(), id))

    def delete(self, table: str, id: int) -> None:
        """Delete a record from the specified table."""
        sql = f'DELETE FROM {table} WHERE id = %s'
        self.execute_query(sql, (id,))

    def get_all_jobs(self) -> Optional[List[Dict[str, Any]]]:
        """Retrieve all jobs from the jobs table."""
        return self.execute_query('SELECT * FROM jobs')

    def close(self) -> None:
        """Close the database connection."""
        self.connection.close()

# Example usage
if __name__ == "__main__":
    # Use environment variables for credentials
    crud = CRUD(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'jobsearch')
    )

    # Example INSERT queries
    crud.create('employers', company_name='Tech Corp', phone_number='1234567890', state='CA', zip_code='90001', email='contact@techcorp.com', password='securepassword', created_at='2023-10-01', updated_at='2023-10-01')
    # Add other example queries here
