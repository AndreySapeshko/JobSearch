import aiohttp
import asyncio
import json

from src.hh_api_request_handler import HhApiRequestHandler
from src.hh_reader_vacancies import HhReaderVacancies
from src.vacancies_handler import VacanciesHandler
from src.json_file_handler import JsonFileHandler
from config import PATH_HH_VACANCIES_JSON
from tests.test_vacancy_handler import handler


async def main():
    search_query = input('Введите запрос: ')
    num_top_vacancies = int(input('Введите количество вакансий для вывода в топ N: '))
    key_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    semaphore = asyncio.Semaphore(3)
    hh_request = HhApiRequestHandler(search_query)
    number_of_pages = 20
    async with aiohttp.ClientSession() as session:
        tasks = [
            hh_request.fetch_page(semaphore, session, hh_request, page)
            for page in range(number_of_pages)
        ]
        results = await asyncio.gather(*tasks)
        successful_results = [page for page in results if page]
    hh_reader = HhReaderVacancies(number_of_pages)
    vacancies = hh_reader.get_vacancies()
    handler = VacanciesHandler(vacancies, num_top_vacancies, key_words)
    handler.filter_vacancies()
    top_vacancies = handler.get_top_vacancies()
    file_handler = JsonFileHandler()
    file_handler.write_in_file(top_vacancies)
    for vacancy in top_vacancies:
        print(vacancy)


if __name__ == '__main__':
    asyncio.run(main())
