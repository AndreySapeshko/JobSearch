import os
import pytest
import psycopg2
import unittest

from unittest.mock import MagicMock
from typing import Any
from dotenv import load_dotenv

from src.db_manager import DBManager


def test_db_manager() -> None:
    column_names = ['id_vacancy', 'hh_id_vacancy', 'name_vacancy', 'id_salary', 'id_employer',
                    'description', 'requirement', 'url']
    db_manager = DBManager()
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
        db_manager = DBManager()
        result = db_manager.get_data_from_table(mock_cursor, 'test_table')
        mock_cursor.execute.assert_called_once_with('SELECT * FROM test_table')

        self.assertEqual(result, mock_rows)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)


@pytest.mark.parametrize('args, expected', [
    ({'c1': 'data1', 'c2': 'data2', 'c3': 'data3'}, 1),
    ({'c1': 'new', 'c2': 'new', 'c3': 'new'}, None)
])
def test_get_arg_from_saved_data(args: list, expected: Any, saved_data: list) -> None:
    db_manager = DBManager()
    result = db_manager.get_arg_from_saved_data(args, saved_data=saved_data)
    assert result == expected


@pytest.mark.parametrize('args, saved_data, expected', [
    (['data1', 'data2', 'data3'], [], None),
    (['data1', 'data2', 'data3'], None, None)
])
def test_get_arg_from_saved_data_none(args: list, saved_data: Any, expected: Any) -> None:
    db_manager = DBManager()
    result = db_manager.get_arg_from_saved_data(args, saved_data=saved_data)
    assert result == expected


@pytest.mark.parametrize('table_name, values, returning, expected', [
    ('test_table', {'column1': 'data1', 'column2': 'data2', 'column3': 'data3'}, None,
     'INSERT INTO test_table (column1, column2, column3)\nVALUES (%(column1)s, %(column2)s, %(column3)s)\n'),
    ('test_table', {'column1': 'data1', 'column2': 'data2', 'column3': 'data3'}, 'returning_value',
     'INSERT INTO test_table (column1, column2, column3)\nVALUES (%(column1)s, %(column2)s, %(column3)s)\n'
     'RETURNING returning_value')
])
def test_create_insert_sql_query(table_name: str, values: dict, returning: str, expected: str) -> None:
    db_manager = DBManager()
    result = db_manager.create_insert_sql_query(table_name, values, returning=returning)
    assert result == expected


load_dotenv()
db_test = os.getenv('TEST_DB_NAME')


@pytest.mark.parametrize('db_name, expected', [(db_test, True), ('invalid_name', False)])
def test_check_database_exists(db_name: str, expected: bool) -> None:
    db_manager = DBManager()
    result = db_manager.check_database_exists(db_name)
    assert result == expected

