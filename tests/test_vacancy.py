def test_vacancy(vacancy) -> None:
    assert vacancy.name == 'Python developer'
    assert vacancy.salary == 130000
    assert vacancy.salary_range == 'от 100000 до 160000'
    assert vacancy.employer == 'employer'
    assert vacancy.requirement == 'Крепкие знания <highlighttext>Python</highlighttext>. Опыт работы с FastAPI.'
    assert vacancy.description == 'Разработка программных продуктов в соответствии с требованиями проекта.'
    assert vacancy.url == 'https://hh.ru/vacancy/122884182'


def test_vacancy_compare(vacancy, vacancy1, vacancy2) -> None:
    assert vacancy < vacancy1
    assert not vacancy > vacancy1
    assert vacancy1 <= vacancy2
    assert vacancy1 == vacancy2
    assert vacancy1 > vacancy
