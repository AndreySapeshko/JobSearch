import pytest

from src.json_file_handler import JsonFileHandler
from config import PATH_TEST_VACANCIES_JSON, PATH_INVALID_FILE


@pytest.mark.parametrize('file_name, expected', [
    (PATH_TEST_VACANCIES_JSON, 10),
    (PATH_INVALID_FILE, 0)
])
def test_json_file_handler(file_name: str, expected: int) -> None:
    json_file_handler = JsonFileHandler(file_name)
    result = json_file_handler.read_from_file()
    assert len(result) == expected
