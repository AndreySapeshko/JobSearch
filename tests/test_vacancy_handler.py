from src.vacancies_handler import VacanciesHandler
from src.hh_reader_vacancies import HhReaderVacancies


def test_vacancy_handler_sorted() -> None:
    hh_reader = HhReaderVacancies(1)
    vacancies = hh_reader.get_vacancies()
    handler = VacanciesHandler(vacancies, 10, [])
    vacancies = handler.sorted_vacancy(reverse=True)
    assert vacancies[0] >= vacancies[1]
    vacancies = handler.sorted_vacancy()
    assert vacancies[-1] >= vacancies[-2]
