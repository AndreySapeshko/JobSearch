from src.api_request_handler import ApiRequestHandler
from src.base_vacancy import BaseVacancy


class VacanciesHandler:
    """ Класс объект которого обрабатывает все вакансии полученные с различных сайтов """

    vacancies: list[BaseVacancy]
    num_top_vacancies: int
    key_words: list

    def __init__(self, vacancies: list[BaseVacancy], num_top_vacancies: int, key_words: list) -> None:
        self.vacancies = vacancies
        self.num_top_vacancies = num_top_vacancies
        self.key_words = key_words

    def get_top_vacancies(self) -> list:
        pass
