from pathlib import Path

import pytest

from src.json_file_handler import JsonFileHandler
from src.hh_reader_vacancies import HhReaderVacancies
from config import PATH_TEST_VACANCIES_JSON, PATH_INVALID_FILE


@pytest.mark.parametrize('file_name, expected', [
    (PATH_TEST_VACANCIES_JSON, 10),
    (PATH_INVALID_FILE, 0)
])
def test_json_file_handler(file_name: Path, expected: int) -> None:
    json_file_handler = JsonFileHandler()
    result = json_file_handler.read_from_file(file_name)
    assert len(result) == expected


def test_vacancies_for_json() -> None:
    hh_reader = HhReaderVacancies(1)
    vacancies = hh_reader.get_vacancies()
    json_file_handler = JsonFileHandler()
    json_vacancies = json_file_handler.vacancies_for_json(vacancies)
    assert len(json_vacancies) == 100
    assert len(json_vacancies[1]) == 7
