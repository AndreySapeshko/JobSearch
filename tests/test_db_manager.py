import psycopg2
import unittest

from unittest.mock import MagicMock

from src.db_manager import DBManager

def test_db_manager() -> None:
    column_names = ['id_vacancy', 'hh_id_vacancy', 'name_vacancy', 'id_salary', 'id_employeer',
                    'description', 'requirement', 'url']
    db_manager = DBManager('localhost', 'hh_vacancies', 'andrdd17', 'u|D".s&qcX')
    with psycopg2.connect(
            host=db_manager.host,
            database=db_manager.database,
            user=db_manager.user,
            password=db_manager.password) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'vacancies'
                ORDER BY ordinal_position
            """)
            rows = cur.fetchall()
            for i in range(len(rows)):
                assert rows[i][0] == column_names[i]


class TestDatabaseMethods(unittest.TestCase):
    def test_get_data_from_table(self):
        mock_cursor = MagicMock()
        mock_rows = [(1, 'data1'), (2, 'data2')]
        mock_cursor.fetchall.return_value = mock_rows
        db_manager = DBManager('localhost', 'hh_vacancies', 'andrdd17', 'u|D".s&qcX')  # Замените на ваш класс
        result = db_manager.get_data_from_table(mock_cursor, 'test_table')
        mock_cursor.execute.assert_called_once_with('SELECT * FROM test_table')

        self.assertEqual(result, mock_rows)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
