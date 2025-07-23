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

    def __init__(self, pages: int) -> None:
        self.pages = pages


    def create_vacancy_from_hh(self, hh_vacancy: dict) -> Vacancy:
        """ Метод принимает вакансию с сайта hh.ru из нее создает
        объект класса Vacancy и возвращает его """

        name = hh_vacancy.get('name')
        salary = 0
        salary_range = 'Не указано'
        if hh_vacancy.get('salary'):
            salary_from = hh_vacancy.get('salary').get('from')
            salary_to = hh_vacancy.get('salary').get('to')
            if salary_from:
                salary = salary_from
                salary_range = f'от {salary_from}'
            if salary_to:
                salary = salary_to
                salary_range = f'до {salary_to}'
            if salary_from and salary_to:
                salary = (salary_from + salary_to) / 2
                salary_range = f'от {salary_from} до {salary_to}'
        employer = hh_vacancy.get('employer').get('name')
        requirement = hh_vacancy.get('snippet').get('requirement')
        description = hh_vacancy.get('snippet').get('responsibility')
        url = hh_vacancy.get('alternate_url')
        return Vacancy(name, salary, salary_range, employer, requirement, description, url)


    def get_vacancies(self) -> list[BaseVacancy]:
        """ Из json файлов полученных с hh.ru с вакансиями создает список с
        объектами класса Vacancy, сортирует по убыванию зарплаты и возвращает
        список с запрошенным количеством топ вакансий """

        vacancies = []
        for page in range(self.pages):
            file_name = Path(__file__).parent.parent / 'data' / f'hh_vacancies_page_{page}.json'
            if Path.exists(file_name):
                json_file_handler = JsonFileHandler(file_name)
                hh_vacancies = json_file_handler.read_from_file().get('items')
                for hh_vacancy in hh_vacancies:
                    if hh_vacancy and not hh_vacancy['archived']:
                        vacancies.append(self.create_vacancy_from_hh(hh_vacancy))

        return vacancies #sorted(vacancies, key=lambda x: x.salary, reverse=True)[:self.count_top]
