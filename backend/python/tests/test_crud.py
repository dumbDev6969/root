import unittest
from unittest.mock import patch, MagicMock
from utils.crud import CRUD, DatabaseError

class TestCRUD(unittest.TestCase):
    @patch('mysql.connector.pooling.MySQLConnectionPool')
    def setUp(self, mock_pool):
        self.mock_pool = mock_pool
        self.crud = CRUD(host='localhost', user='test', password='test', database='test_db')

    def test_create(self):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        self.crud.get_connection = MagicMock(return_value=mock_connection)
        mock_connection.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        self.crud.create('test_table', name='Test', value=123)

        mock_cursor.execute.assert_called_once_with(
            'INSERT INTO test_table (name, value) VALUES (%s, %s)',
            ('Test', 123)
        )
        mock_connection.commit.assert_called_once()

    def test_read(self):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        self.crud.get_connection = MagicMock(return_value=mock_connection)
        mock_connection.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'Test', 'value': 123}]

        result = self.crud.read('test_table', id=1)

        mock_cursor.execute.assert_called_once_with(
            'SELECT * FROM test_table WHERE id = %s',
            (1,)
        )
        self.assertEqual(result, [{'id': 1, 'name': 'Test', 'value': 123}])

    def test_update(self):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        self.crud.get_connection = MagicMock(return_value=mock_connection)
        mock_connection.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        self.crud.update('test_table', 1, name='Updated Test', value=456)

        mock_cursor.execute.assert_called_once_with(
            'UPDATE test_table SET name = %s, value = %s WHERE id = %s',
            ('Updated Test', 456, 1)
        )
        mock_connection.commit.assert_called_once()

    def test_delete(self):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        self.crud.get_connection = MagicMock(return_value=mock_connection)
        mock_connection.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        self.crud.delete('test_table', 1)

        mock_cursor.execute.assert_called_once_with(
            'DELETE FROM test_table WHERE id = %s',
            (1,)
        )
        mock_connection.commit.assert_called_once()

    def test_database_error(self):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        self.crud.get_connection = MagicMock(return_value=mock_connection)
        mock_connection.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Database error")

        with self.assertRaises(DatabaseError):
            self.crud.create('test_table', name='Test', value=123)

if __name__ == '__main__':
    unittest.main()
