import aiohttp
import asyncio
import json

from src.hh_api_request_hendler import HhApiRequestHandler


async def main():
    hh_request = HhApiRequestHandler('Python')
    async with aiohttp.ClientSession() as session:
        tasks = [hh_request.get_api_request(session, page) for page in range(1)]
        results = await asyncio.gather(*tasks)
        for vacancies in results:
            with open('data/hh_vacancies.json', 'w', encoding='utf-8') as file:
                json.dump(vacancies, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    asyncio.run(main())
