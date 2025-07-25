import json
import os
from pathlib import Path

from src.base_vacancy import BaseVacancy
from src.file_handler import FileHandler


class JsonFileHandler(FileHandler):
    """ Класс объект которого обрабатывает файлы формата json.
     Записывает данные в файл, читает из файла и удаляет данные. """

    def __init__(self) -> None:
        pass

    def read_from_file(self, file_name: Path) -> dict:
        """ конвертирует json файл в python, если файла нет или пустой вернет пустой список """

        json_data: dict = {}
        # logger.info(f'проверяем существует ли файл {filename}')
        if os.path.exists(file_name):
            try:
                # logger.info('открываем файл для чтения')
                with open(file_name, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            except json.JSONDecodeError as jde:
                # logger.error(f'произошла ошибка при открытии файла {jde}')
                print(f'произошла ошибка при открытии файла {jde}')
                return json_data
            except FileNotFoundError as fnf:
                # logger.error(f'произошла ошибка при открытии файла {fnf}')
                print(f'произошла ошибка при открытии файла {fnf}')
                return json_data
            if data and len(data) != 0:
                json_data = data
        #             logger.info('конвертация успешно завершена')
        return json_data

    def vacancies_for_json(self, vacancies: list[BaseVacancy]) -> list[dict]:
        """ Принимает список объектов класса BaseVacancy, возвращает список словорей
         с именами и значениями параметров вакансии для сохранения в файл в формате json """

        to_json_vacancies = []
        for vacancy in vacancies:
            vacancy_dict = {}
            if hasattr(vacancy.__class__, '__slots__'):
                vacancy_dict = {name : getattr(vacancy, name) for name in vacancy.__class__.__slots__}
            else:
                for name, value in vars(vacancy).items():
                    vacancy_dict[name] = value
            to_json_vacancies.append(vacancy_dict)
        return to_json_vacancies

    def write_in_file(self, vacancies: list) -> None:
        """ Записывает данные в файл в формате json """

        vacancies_to_json = self.vacancies_for_json(vacancies)
        file_name = Path(__file__).parent.parent / 'data' / 'top_vacancies.json'
        with open(file_name, 'a', encoding='utf-8') as file:
            try:
                json.dump(vacancies_to_json, file, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f'Произошла ошибка при записи в файл: {e}')

    def delete_file(self, file_name: Path) -> None:
        pass
