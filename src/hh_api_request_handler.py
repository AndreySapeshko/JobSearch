import aiohttp
import asyncio

from aiohttp import ClientSession

from src.api_request_handler import ApiRequestHandler


class HhApiRequestHandler(ApiRequestHandler):

    name_vacancy: str

    def __init__(self, name_vacancy: str) -> None:
        self.name_vacancy = name_vacancy

    async def get_api_request(self, session: ClientSession, page: int = 0) -> str:
        url = "https://api.hh.ru/vacancies"
        params = {
            "text": self.name_vacancy,
            "area": 1,
            "page": page,
            "per_page": 1
        }
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
