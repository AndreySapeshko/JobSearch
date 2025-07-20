from src.api_request_handler import ApiRequestHandler


class VacanciesHandler:
    """ Класс объект которого обрабатывает все вакансии полученные с различных сайтов """

    vacancies: list[dict]
    num_top_vacancies: int

    def __init__(self, vacancies: list[dict], num_top_vacancies: int) -> None:
        self.vacancies = vacancies
        self.num_top_vacancies = num_top_vacancies

    def get_top_vacancies(self) -> list:
        pass
