import pytest

from src.hh_reader_vacancies import HhReaderVacancies
from config import PATH_TEST_VACANCIES_JSON
from src.base_vacancy import BaseVacancy


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
    assert isinstance(result, list)
    assert len(result) == 2000
    for vacancy in result:
        assert isinstance(vacancy, BaseVacancy)
