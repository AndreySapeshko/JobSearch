import json
import logging
import os

from src.base_vacancy import BaseVacancy
from src.reader_vacancies import ReaderVacancies
from src.json_file_handler import JsonFileHandler
from src.vacancy import Vacancy
from config import PATH_HH_VACANCIES_JSON


class HhReaderVacancies(ReaderVacancies):
    """ Класс объект которого из json файла с вакансиями hh.ru создает список с
    объектами типа BaseVacancy """

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def get_vacancies(self) -> list[BaseVacancy]:
        json_file_handler = JsonFileHandler(self.file_name)
        hh_vacancies = json_file_handler.read_from_file().get('items')
        vacancies = []
        for vacancy in hh_vacancies:
            if not vacancy['archived']:
                name = vacancy.get('name')
                salary = 0
                if vacancy.get('salary'):
                    if vacancy.get('salary').get('from'):
                        salary = vacancy.get('salary').get('from')
                    if vacancy.get('salary').get('to'):
                        salary = vacancy
                    if vacancy.get('salary').get('from') and vacancy.get('salary').get('to'):
                        salary = (vacancy.get('salary').get('from') + vacancy.get('salary').get('to')) / 2
                employer = vacancy.get('employer').get('name')
                requirement = vacancy.get('snippet').get('requirement')
                description = vacancy.get('snippet').get('responsibility')
                vacancies.append(Vacancy(name, salary, employer, requirement, description))
        return sorted(vacancies, key=lambda x: x.salary)


hh_reader = HhReaderVacancies(PATH_HH_VACANCIES_JSON)
vacancies = hh_reader.get_vacancies()
for vacancy in vacancies:
    print(vacancy)
