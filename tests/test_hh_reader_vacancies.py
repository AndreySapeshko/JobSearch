from pathlib import Path

import pytest

from src.base_vacancy import BaseVacancy
from src.hh_reader_vacancies import HhReaderVacancies
from src.json_file_handler import JsonFileHandler


def test_create_vacancy_from_hh(hh_vacancy) -> None:
    hh_reader = HhReaderVacancies(20)
    vacancy = hh_reader.create_vacancy_from_hh(hh_vacancy)
    assert vacancy.name == 'Python developer'
    assert vacancy.salary == 130000
    assert vacancy.salary_range == 'от 100000 до 160000'
    assert vacancy.employer == 'employer'
    assert vacancy.description == 'Разработка программных продуктов в соответствии с требованиями проекта.'
    assert vacancy.requirement == 'Крепкие знания <highlighttext>Python</highlighttext>. Опыт работы с FastAPI.'
    hh_vacancy['salary']['from'] = None
    vacancy_without_from = hh_reader.create_vacancy_from_hh(hh_vacancy)
    assert vacancy_without_from.salary == 160000
    assert vacancy_without_from.salary_range == 'до 160000'
    hh_vacancy['salary'] = None
    vacancy_without_salary = hh_reader.create_vacancy_from_hh(hh_vacancy)
    assert vacancy_without_salary.salary == 0
    assert vacancy_without_salary.salary_range == 'Не указано'


@pytest.mark.parametrize('pages', [(20), (22)])
def test_hh_reader_vacancies(pages: int) -> None:
    hh_reader = HhReaderVacancies(pages)
    result = hh_reader.get_vacancies()
    json_file_handler = JsonFileHandler()
    file_name = Path(__file__).parent.parent / 'data' / 'hh_vacancies_page_0.json'
    found_vacancies = json_file_handler.read_from_file(file_name)['found']
    assert isinstance(result, list)
    assert len(result) == found_vacancies
    for vacancy in result:
        assert isinstance(vacancy, BaseVacancy)


def test_get_valid_name(hh_vacancy) -> None:
    hh_reader = HhReaderVacancies(1)
    assert hh_reader._HhReaderVacancies__get_valid_name(hh_vacancy) == 'Python developer'
    hh_vacancy['name'] = None
    assert hh_reader._HhReaderVacancies__get_valid_name(hh_vacancy) == 'Название вакансии не указано'


def test_get_valid_salary(hh_vacancy) -> None:
    hh_reader = HhReaderVacancies(1)
    assert hh_reader._HhReaderVacancies__get_valid_salary(hh_vacancy) == 130000
    hh_vacancy['salary'] = None
    assert hh_reader._HhReaderVacancies__get_valid_salary(hh_vacancy) == 0


def test_get_valid_salary_range(hh_vacancy) -> None:
    hh_reader = HhReaderVacancies(1)
    assert hh_reader._HhReaderVacancies__get_valid_salary_range(hh_vacancy) == 'от 100000 до 160000'
    hh_vacancy['salary'] = None
    assert hh_reader._HhReaderVacancies__get_valid_salary_range(hh_vacancy) == 'Не указано'


def test_get_valid_employer(hh_vacancy) -> None:
    hh_reader = HhReaderVacancies(1)
    assert hh_reader._HhReaderVacancies__get_valid_employer(hh_vacancy) == 'employer'
    hh_vacancy['employer'] = None
    assert hh_reader._HhReaderVacancies__get_valid_employer(hh_vacancy) == 'Работодатель не указан'


def test_get_valid_requirement(hh_vacancy) -> None:
    hh_reader = HhReaderVacancies(1)
    assert (hh_reader._HhReaderVacancies__get_valid_requirement(hh_vacancy)
            == 'Крепкие знания <highlighttext>Python</highlighttext>. Опыт работы с FastAPI.')
    hh_vacancy['snippet'] = None
    assert hh_reader._HhReaderVacancies__get_valid_requirement(hh_vacancy) == 'Требования не указаны'


def test_get_valid_description(hh_vacancy) -> None:
    hh_reader = HhReaderVacancies(1)
    assert (hh_reader._HhReaderVacancies__get_valid_description(hh_vacancy)
            == 'Разработка программных продуктов в соответствии с требованиями проекта.')
    hh_vacancy['snippet'] = None
    assert hh_reader._HhReaderVacancies__get_valid_description(hh_vacancy) == 'Описание не указано'


def test_get_valid_url(hh_vacancy) -> None:
    hh_reader = HhReaderVacancies(1)
    assert hh_reader._HhReaderVacancies__get_valid_url(hh_vacancy) == 'https://hh.ru/vacancy/122884182'
    hh_vacancy['alternate_url'] = None
    assert hh_reader._HhReaderVacancies__get_valid_url(hh_vacancy) == 'Сылака на вакансию не указана'
