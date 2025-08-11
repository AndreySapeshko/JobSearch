import json
from typing import Any

import pytest

from config import PATH_TEST_VACANCIES_JSON
from src.vacancy import Vacancy
from src.json_file_handler import JsonFileHandler


@pytest.fixture
def hh_vacancies_dict() -> Any:
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
        '1',
        'Python developer',
        130000,
        'от 100000 до 160000',
        'employer',
        '1',
        'Крепкие знания <highlighttext>Python</highlighttext>. Опыт работы с FastAPI.',
        'Разработка программных продуктов в соответствии с требованиями проекта.',
        'https://hh.ru/vacancy/122884182'
    )


@pytest.fixture
def vacancy1() -> Vacancy:
    return Vacancy('2', 'python', 150000, '150000', 'employer',
                   '2', 'requirement', 'responsibility', 'HTTPS://hh.ru')


@pytest.fixture
def vacancy2() -> Vacancy:
    return Vacancy('3', 'python', 150000, '150000', 'employer',
                   '3', 'requirement', 'responsibility', 'HTTPS://hh.ru')


@pytest.fixture
def vacancy3() -> Vacancy:
    return Vacancy('3', 'python', 150000, '150000', 'employer',
                   '3', 'requirement', 'responsibility', 'HTTPS://hh.ru')


@pytest.fixture
def vacancies() -> list[Vacancy]:
    vacancies =[
        Vacancy(
        '1',
        'Python developer',
        130000,
        'от 100000 до 160000',
        'employer',
        '1',
        'Крепкие знания <highlighttext>Python</highlighttext>. Опыт работы с FastAPI.',
        'Разработка программных продуктов в соответствии с требованиями проекта.',
        'https://hh.ru/vacancy/122884182'
    ),
        Vacancy('2', 'python', 150000, '150000', 'employer',
                '2', 'requirement', 'responsibility', 'HTTPS://hh.ru'),
        Vacancy('3', 'python', 150000, '150000', 'employer',
                '3', 'requirement', 'responsibility', 'HTTPS://hh.ru')
    ]
    return vacancies
