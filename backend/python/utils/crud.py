import sqlite3

class CRUD:
    def __init__(self, db_name):
        """Initialize the CRUD class with a database name."""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def execute_query(self, sql, params=()):
        """Execute a SQL query with optional parameters."""
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def create(self, table, **kwargs):
        """Insert a new record into the specified table."""
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join('?' * len(kwargs))
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        self.execute_query(sql, tuple(kwargs.values()))

    def read(self, table, **kwargs):
        """Read records from the specified table."""
        sql = f'SELECT * FROM {table}'
        if kwargs:
            conditions = ' AND '.join(f"{key} = ?" for key in kwargs.keys())
            sql += f' WHERE {conditions}'
            return self.execute_query(sql, tuple(kwargs.values()))
        else:
            return self.execute_query(sql)

    def update(self, table, id, **kwargs):
        """Update a record in the specified table."""
        set_clause = ', '.join(f"{key} = ?" for key in kwargs.keys())
        sql = f'UPDATE {table} SET {set_clause} WHERE id = ?'
        self.execute_query(sql, (*kwargs.values(), id))

    def delete(self, table, id):
        """Delete a record from the specified table."""
        sql = f'DELETE FROM {table} WHERE id = ?'
        self.execute_query(sql, (id,))

    def close(self):
        """Close the database connection."""
        self.connection.close()

# # Example usage
# if __name__ == "__main__":
#     # Create an instance of the CRUD class
#     crud = CRUD('example.db')

#     # Create a table (for demonstration purposes)
#     crud.execute_query('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             age INTEGER NOT NULL
#         )
#     ''')

#     # Create a new user
#     crud.create('users', name='Alice', age=30)

#     # Read users
#     users = crud.read('users')
#     print("Users:", users)

#     # Update a user
#     crud.update('users', 1, name='Alice Smith', age=31)

#     # Read users again
#     users = crud.read('users')
#     print("Updated Users:", users)

#     # Delete a user
#     crud.delete('users', 1)

#     # Read users again
#     users = crud.read('users')
#     print("Users after deletion:", users)

#     # Close the connection
#     crud.close()
