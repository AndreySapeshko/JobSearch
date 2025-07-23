from __future__ import annotations

import json
from threading import Semaphore

import aiohttp
import asyncio

from aiohttp import ClientSession
from pathlib import Path
from typing import Dict, Any

from src.api_request_handler import ApiRequestHandler


class HhApiRequestHandler(ApiRequestHandler):
    """ Класс объект которого получает по API данные по вакансиям с сайта hh.ru """

    __name_vacancy: str

    def __init__(self, name_vacancy: str) -> None:
        self.__name_vacancy = name_vacancy

    async def get_api_request(self, session: ClientSession, page: int = 0) -> Dict[str: Any]:
        url = "https://api.hh.ru/vacancies"
        params = {
            "text": self.__name_vacancy,
            "area": 1,
            "page": page,
            "per_page": 100
        }
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()

    async def save_vacancies_to_file(self, vacancies: Dict[str: Any], page: int) -> None:
        Path('data').mkdir(exist_ok=True)
        file_path = Path(f'data/hh_vacancies_page_{page}.json')
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

    async def fetch_page(self, semaphore: Semaphore, session: ClientSession,
                         handler: HhApiRequestHandler, page: int) -> Any:
        async with semaphore:
            try:
                vacancies = await handler.get_api_request(session, page)
                await handler.save_vacancies_to_file(vacancies, page)
                return vacancies
            except aiohttp.ClientError as e:
                print(f'Ошибка при получении страницы {page}: {e}')
                return None
