import aiohttp
import asyncio
import json

from src.hh_api_request_handler import HhApiRequestHandler
from src.hh_reader_vacancies import HhReaderVacancies
from src.vacancies_handler import VacanciesHandler
from src.json_file_handler import JsonFileHandler
from src.db_manager import DBManager
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
    vacancies = handler.filter_vacancies()
    top_vacancies = handler.get_top_vacancies()
    file_handler = JsonFileHandler()
    file_handler.write_in_file(top_vacancies)
    db_manager = DBManager()
    db_manager.update_database(vacancies)
    for vacancy in top_vacancies:
        print(vacancy)
    print('\nВсе работодатели с количеством вакансий: ')
    employers = db_manager.get_companies_and_vacancies_count()
    for emploer in employers:
        print(emploer)
    print(f'\nСредняя зарплата по всем вакансиям: {db_manager.get_avg_salary()}')
    print('\nВакансии с зарплатой выше средней: ')
    high_vacancies = db_manager.get_vacancies_with_higher_salary()
    for vacancy in high_vacancies:
        print(vacancy)
    key_word = 'middle'
    print(f'\nВакансии название которых содержет {key_word}: ')
    filtered_vacancies = db_manager.get_vacancies_with_keyword(key_word)
    for vacancy in filtered_vacancies:
        print(vacancy)



if __name__ == '__main__':
    asyncio.run(main())
