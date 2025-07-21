import aiohttp
import asyncio
import json

from src.hh_api_request_handler import HhApiRequestHandler
from config import PATH_HH_VACANCIES_JSON





async def main():
    semaphore = asyncio.Semaphore(3)
    hh_request = HhApiRequestHandler('Python')
    async with aiohttp.ClientSession() as session:
        tasks = [
            hh_request.fetch_page(semaphore, session, hh_request, page)
            for page in range(20)
        ]
        results = await asyncio.gather(*tasks)
        successful_results = [page for page in results if page]
        for result in successful_results:
            print(type(result))



if __name__ == '__main__':
    asyncio.run(main())
