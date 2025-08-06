from pathlib import Path

from src.base_vacancy import BaseVacancy
from src.json_file_handler import JsonFileHandler
from src.reader_vacancies import ReaderVacancies
from src.vacancy import Vacancy
from tests.conftest import hh_vacancy


class HhReaderVacancies(ReaderVacancies):
    """ Класс объект которого из json файла с вакансиями hh.ru создает список с
    объектами типа BaseVacancy """

    def __init__(self, pages: int) -> None:
        self.pages = pages

    def __get_valid_id(self, hh_vacancy: dict) -> str:
        """ Проверяет параметр id для создания объекта класса Vacancy """

        if hh_vacancy.get('id'):
            return hh_vacancy.get('id')
        else:
            return 'id не указан'

    def __get_valid_name(self, hh_vacancy: dict) -> str:
        """ Проверяет параметр name для создания объекта класса Vacancy """

        if hh_vacancy.get('name'):
            return hh_vacancy.get('name')
        else:
            return 'Название вакансии не указано'

    def __get_valid_salary(self, hh_vacancy: dict) -> int:
        """ Проверяет параметр salary для создания объекта класса Vacancy """

        salary = 0
        if hh_vacancy.get('salary'):
            salary_from = hh_vacancy.get('salary').get('from')
            salary_to = hh_vacancy.get('salary').get('to')
            if salary_from:
                salary = salary_from
            if salary_to:
                salary = salary_to
            if salary_from and salary_to:
                salary = (salary_from + salary_to) / 2
        return salary

    def __get_valid_salary_range(self, hh_vacancy: dict) -> str:
        """ Проверяет параметр salary_range для создания объекта класса Vacancy """

        salary_range = 'Не указано'
        if hh_vacancy.get('salary'):
            salary_from = hh_vacancy.get('salary').get('from')
            salary_to = hh_vacancy.get('salary').get('to')
            if salary_from:
                salary_range = f'от {salary_from}'
            if salary_to:
                salary_range = f'до {salary_to}'
            if salary_from and salary_to:
                salary_range = f'от {salary_from} до {salary_to}'
        return salary_range

    def __get_valid_employer(self, hh_vacancy: dict) -> str:
        """ Проверяет параметр employer для создания объекта класса Vacancy """

        if hh_vacancy.get('employer') and hh_vacancy.get('employer').get('name'):
            return hh_vacancy.get('employer').get('name')
        else:
            return 'Работодатель не указан'

    def __get_valid_employer_id(self, hh_vacancy: dict) -> str:
        """ Проверяет параметр employer_id для создания объекта класса Vacancy """

        if hh_vacancy.get('employer') and hh_vacancy.get('employer').get('id'):
            return hh_vacancy.get('employer').get('id')
        else:
            return 'id работодателя не указан'

    def __get_valid_requirement(self, hh_vacancy: dict) -> str:
        """ Проверяет параметр requirement для создания объекта класса Vacancy """

        if hh_vacancy.get('snippet') and hh_vacancy.get('snippet').get('requirement'):
            return hh_vacancy.get('snippet').get('requirement')
        else:
            return 'Требования не указаны'

    def __get_valid_description(self, hh_vacancy: dict) -> str:
        """ Проверяет параметр description для создания объекта класса Vacancy """

        if hh_vacancy.get('snippet') and hh_vacancy.get('snippet').get('responsibility'):
            return hh_vacancy.get('snippet').get('responsibility')
        else:
            return 'Описание не указано'

    def __get_valid_url(self, hh_vacancy: dict) -> str:
        """ Проверяет параметр url для создания объекта класса Vacancy """

        if hh_vacancy.get('alternate_url'):
            return hh_vacancy.get('alternate_url')
        else:
            return 'Сылака на вакансию не указана'

    def create_vacancy_from_hh(self, hh_vacancy: dict) -> Vacancy:
        """ Метод принимает вакансию с сайта hh.ru из нее создает
        объект класса Vacancy и возвращает его """

        id = self.__get_valid_id(hh_vacancy)
        name = self.__get_valid_name(hh_vacancy)
        salary = self.__get_valid_salary(hh_vacancy)
        salary_range = self.__get_valid_salary_range(hh_vacancy)
        employer = self.__get_valid_employer(hh_vacancy)
        employer_id = self.__get_valid_employer_id(hh_vacancy)
        requirement = self.__get_valid_requirement(hh_vacancy)
        description = self.__get_valid_description(hh_vacancy)
        url = self.__get_valid_url(hh_vacancy)
        return Vacancy(id, name, salary, salary_range, employer, employer_id, requirement, description, url)

    def get_vacancies(self) -> list[BaseVacancy]:
        """ Из json файлов полученных с hh.ru с вакансиями создает список с
        объектами класса Vacancy, сортирует по убыванию зарплаты и возвращает
        список с запрошенным количеством топ вакансий """

        vacancies = []
        json_file_handler = JsonFileHandler()
        for page in range(self.pages):
            file_name = Path(__file__).parent.parent / 'data' / f'hh_vacancies_page_{page}.json'
            if Path.exists(file_name):
                hh_vacancies = json_file_handler.read_from_file(file_name).get('items')
                if hh_vacancies:
                    for hh_vacancy in hh_vacancies:
                        if hh_vacancy and not hh_vacancy['archived']:
                            vacancies.append(self.create_vacancy_from_hh(hh_vacancy))

        return vacancies
