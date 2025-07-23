from src.vacancy import Vacancy


vacancy = Vacancy(
    'Python developer',
    130000,
    'от 100000 до 160000',
    'employer',
    'Крепкие знания <highlighttext>Python</highlighttext>. Опыт работы с FastAPI.',
    'Разработка программных продуктов в соответствии с требованиями проекта.',
    'https://hh.ru/vacancy/122884182'
)
vacancy1 = Vacancy('python', 150000, '150000', 'employer',
                   'requirement', 'responsibility', 'HTTPS://hh.ru')
vacancy2 = Vacancy('python', 150000, '150000', 'employer',
                   'requirement', 'responsibility', 'HTTPS://hh.ru')


def test_vacancy() -> None:
    assert vacancy.name == 'Python developer'
    assert vacancy.salary == 130000
    assert vacancy.salary_range == 'от 100000 до 160000'
    assert vacancy.employer == 'employer'
    assert vacancy.requirement == 'Крепкие знания <highlighttext>Python</highlighttext>. Опыт работы с FastAPI.'
    assert vacancy.description == 'Разработка программных продуктов в соответствии с требованиями проекта.'
    assert vacancy.url == 'https://hh.ru/vacancy/122884182'


def test_vacancy_compare() -> None:
    assert vacancy < vacancy1
    assert not vacancy > vacancy1
    assert vacancy1 <= vacancy2
    assert vacancy1 == vacancy2
    assert vacancy1 > vacancy
