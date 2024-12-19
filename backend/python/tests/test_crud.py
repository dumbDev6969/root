import unittest
from unittest.mock import patch, MagicMock
from utils.crud import CRUD, DatabaseError

class TestCRUD(unittest.TestCase):
    def setUp(self):
        # Create a mock database instance
        self.mock_db = MagicMock()
        self.crud = CRUD(db=self.mock_db)

    def test_create(self):
        # Test data
        table = 'test_table'
        data = {'name': 'Test', 'value': 123}
        
        # Configure mock
        self.mock_db.execute_query.return_value = 1

        # Execute create operation
        result = self.crud.create(table, data)

        # Verify the query execution
        self.mock_db.execute_query.assert_called_once_with(
            'INSERT INTO test_table (name, value) VALUES (%s, %s)',
            ('Test', 123)
        )
        self.assertEqual(result, 1)

    def test_read(self):
        # Test data
        table = 'test_table'
        conditions = {'id': 1}
        expected_result = [{'id': 1, 'name': 'Test', 'value': 123}]
        
        # Configure mock
        self.mock_db.execute_query.return_value = expected_result

        # Execute read operation
        result = self.crud.read(table, conditions)

        # Verify the query execution
        self.mock_db.execute_query.assert_called_once_with(
            'SELECT * FROM test_table WHERE id = %s',
            (1,)
        )
        self.assertEqual(result, expected_result)

    def test_update(self):
        # Test data
        table = 'test_table'
        data = {'name': 'Updated Test', 'value': 456}
        conditions = {'id': 1}
        
        # Configure mock
        mock_result = MagicMock()
        mock_result.rowcount = 1
        self.mock_db.execute_query.return_value = mock_result

        # Execute update operation
        result = self.crud.update(table, data, conditions)

        # Verify the query execution
        self.mock_db.execute_query.assert_called_once_with(
            'UPDATE test_table SET name = %s, value = %s WHERE id = %s',
            ('Updated Test', 456, 1)
        )
        self.assertEqual(result, 1)

    def test_delete(self):
        # Test data
        table = 'test_table'
        conditions = {'id': 1}
        
        # Configure mock
        mock_result = MagicMock()
        mock_result.rowcount = 1
        self.mock_db.execute_query.return_value = mock_result

        # Execute delete operation
        result = self.crud.delete(table, conditions)

        # Verify the query execution
        self.mock_db.execute_query.assert_called_once_with(
            'DELETE FROM test_table WHERE id = %s',
            (1,)
        )
        self.assertEqual(result, 1)

    def test_database_error(self):
        # Test data
        table = 'test_table'
        data = {'name': 'Test', 'value': 123}
        
        # Configure mock to raise an exception
        self.mock_db.execute_query.side_effect = Exception("Database error")

        # Verify that DatabaseError is raised
        with self.assertRaises(DatabaseError):
            self.crud.create(table, data)

if __name__ == '__main__':
    unittest.main()
