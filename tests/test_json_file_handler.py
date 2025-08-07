from pathlib import Path

import pytest

from config import PATH_INVALID_FILE, PATH_TEST_VACANCIES_JSON
from src.hh_reader_vacancies import HhReaderVacancies
from src.json_file_handler import JsonFileHandler
from src.vacancy import Vacancy


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


def test_create_vacancies_from_json() -> None:
    file_name = Path(__file__).parent.parent / 'data' / 'top_vacancies.json'
    json_file_handler = JsonFileHandler()
    vacancies = json_file_handler.create_vacancies_from_json(file_name)
    for vacancy in vacancies:
        assert isinstance(vacancy, Vacancy)


def test_write_in_new_file(vacancies) -> None:
    file_path = Path(__file__).parent.parent / 'data' / 'test_write_new_file.json'
    if file_path.exists():
        file_path.unlink()
    jfh = JsonFileHandler()
    jfh.write_in_file(vacancies=vacancies, file_name='test_write_new_file.json')
    vacancies_from_file = jfh.create_vacancies_from_json(file_path)
    for vacancy_from_file in vacancies_from_file:
        is_in_vacancies = False
        for vacancy in vacancies:
            if vacancy == vacancy_from_file:
                is_in_vacancies = True
        assert is_in_vacancies


def test_select_new_vacancies() -> None:
    new_vacancy = Vacancy('new', 'python', 150000, '150000', 'employer',
                   '3', 'requirement', 'responsibility', 'HTTPS://hh.ru')
    old_vacancy = Vacancy('3', 'python', 150000, '150000', 'employer',
                   '3', 'requirement', 'responsibility', 'HTTPS://hh.ru')
    vacancies = [new_vacancy, old_vacancy]
    file_path = Path(__file__).parent.parent / 'data' / 'test_select_vacancies.json'
    jfh = JsonFileHandler()
    vacancies = jfh.select_new_vacancies(vacancies,file_path)
    assert new_vacancy in vacancies
    assert old_vacancy not in vacancies
