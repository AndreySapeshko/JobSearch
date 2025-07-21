import json
import logging
import os
from pathlib import Path

from src.base_vacancy import BaseVacancy
from src.reader_vacancies import ReaderVacancies
from src.json_file_handler import JsonFileHandler
from src.vacancy import Vacancy
from config import PATH_HH_VACANCIES_JSON


class HhReaderVacancies(ReaderVacancies):
    """ Класс объект которого из json файла с вакансиями hh.ru создает список с
    объектами типа BaseVacancy """

    def __init__(self, pages: int, count_top: int) -> None:
        self.pages = pages
        self.count_top = count_top

    def get_vacancies(self) -> list[BaseVacancy]:
        vacancies = []
        for page in range(self.pages):
            file_name = Path(__file__).parent.parent / 'data' / f'hh_vacancies_page_{page}.json'
            if Path.exists(file_name):
                json_file_handler = JsonFileHandler(file_name)
                hh_vacancies = json_file_handler.read_from_file().get('items')
                for vacancy in hh_vacancies:
                    if not vacancy['archived']:
                        name = vacancy.get('name')
                        salary = 0
                        if vacancy.get('salary'):
                            if vacancy.get('salary').get('from'):
                                salary = vacancy.get('salary').get('from')
                            if vacancy.get('salary').get('to'):
                                salary = vacancy.get('salary').get('to')
                            if vacancy.get('salary').get('from') and vacancy.get('salary').get('to'):
                                salary = (vacancy.get('salary').get('from') + vacancy.get('salary').get('to')) / 2
                        employer = vacancy.get('employer').get('name')
                        requirement = vacancy.get('snippet').get('requirement')
                        description = vacancy.get('snippet').get('responsibility')
                        vacancies.append(Vacancy(name, salary, employer, requirement, description))

        return sorted(vacancies, key=lambda x: x.salary, reverse=True)[:self.count_top]
