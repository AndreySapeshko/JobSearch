import json

import pytest

from config import PATH_TEST_VACANCIES_JSON
from src.vacancy import Vacancy


@pytest.fixture
def hh_vacancies_dict() -> dict:
    with open(PATH_TEST_VACANCIES_JSON) as f:
        data = json.load(f)
    return data


@pytest.fixture
def hh_vacancy() -> dict:
    return {
        'name': 'Python developer',
        'salary': {
            'from': 100000,
            'to': 160000
        },
        'employer': {
            'name': 'employer'
        },
        'snippet': {
            'requirement': 'Крепкие знания <highlighttext>Python</highlighttext>. Опыт работы с FastAPI.',
            'responsibility': 'Разработка программных продуктов в соответствии с требованиями проекта.'
        },
        'alternate_url': 'https://hh.ru/vacancy/122884182'
    }


@pytest.fixture
def vacancy() -> Vacancy:
    return Vacancy(
        'Python developer',
        130000,
        'от 100000 до 160000',
        'employer',
        'Крепкие знания <highlighttext>Python</highlighttext>. Опыт работы с FastAPI.',
        'Разработка программных продуктов в соответствии с требованиями проекта.',
        'https://hh.ru/vacancy/122884182'
    )


@pytest.fixture
def vacancy1() -> Vacancy:
    return Vacancy('python', 150000, '150000', 'employer',
                   'requirement', 'responsibility', 'HTTPS://hh.ru')


@pytest.fixture
def vacancy2() -> Vacancy:
    return Vacancy('python', 150000, '150000', 'employer',
                   'requirement', 'responsibility', 'HTTPS://hh.ru')
