from src.hh_reader_vacancies import HhReaderVacancies
from src.vacancies_handler import VacanciesHandler

hh_reader = HhReaderVacancies(1)
vacancies = hh_reader.get_vacancies()
handler = VacanciesHandler(vacancies, 10, [])


def test_vacancy_handler_sorted() -> None:
    vacancies = handler.sort_vacancy(reverse=True)
    assert vacancies[0] >= vacancies[1]
    vacancies = handler.sort_vacancy()
    assert vacancies[-1] >= vacancies[-2]


def test_vacancy_handler_top() -> None:
    vacancies = handler.get_top_vacancies()
    assert len(vacancies) == 10
    assert vacancies[0] >= vacancies[1]
    assert vacancies[0] > vacancies[-1]


def test_vacancy_handler_filter_without_key() -> None:
    filtered_vacancies = handler.filter_vacancies()
    assert len(filtered_vacancies) == 100


def test_vacancy_handler_filter(vacancy, vacancy1, vacancy2) -> None:
    key_words = ['Python', 'developer']
    handler = VacanciesHandler([vacancy, vacancy1, vacancy2], 10, key_words)
    filtered_vacancies = handler.filter_vacancies()
    for vacancy in filtered_vacancies:
        is_in_vacancy = False
        for word in key_words:
            if vacancy.name and word in vacancy.name:
                is_in_vacancy = True
                break
            if vacancy.requirement and word in vacancy.requirement:
                is_in_vacancy = True
                break
        assert is_in_vacancy is True
