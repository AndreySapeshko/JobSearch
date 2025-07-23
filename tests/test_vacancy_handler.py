from src.vacancies_handler import VacanciesHandler
from src.hh_reader_vacancies import HhReaderVacancies


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
