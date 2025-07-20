import json
import os

from src.file_handler import FileHandler
from config import PATH_TEST_VACANCIES_JSON


class JsonFileHandler(FileHandler):

    def __init__(self, file_name) -> None:
        self.file_name = file_name

    def read_from_file(self) -> dict:
        """ конвертирует json файл в python, если файла нет или пустой вернет пустой список """

        json_data: dict = {}
        # logger.info(f'проверяем существует ли файл {filename}')
        if os.path.exists(self.file_name):
            try:
                # logger.info('открываем файл для чтения')
                with open(self.file_name, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            except json.JSONDecodeError as jde:
                # logger.error(f'произошла ошибка при открытии файла {jde}')
                return json_data
            except FileNotFoundError as fnf:
                #                 logger.error(f'произошла ошибка при открытии файла {fnf}')
                return json_data
            if data and len(data) != 0:
                json_data = data
        #             logger.info('конвертация успешно завершена')
        return json_data

    def write_in_file(self) -> None:
        pass
