import asyncio

import pytest
import aiohttp

from unittest.mock import AsyncMock, MagicMock
from pathlib import Path
from aiohttp import ClientSession
from asyncio import Semaphore

from src.hh_api_request_handler import HhApiRequestHandler


@pytest.mark.asyncio
async def test_hh_api_request():
    mock_session = AsyncMock(spec=ClientSession)
    mock_response = AsyncMock()
    # mock_response.raise_for_status = AsyncMock()
    mock_response.json.return_value = {'key': 'value'}
    mock_session.get.return_value.__aenter__.return_value = mock_response
    hh_request = HhApiRequestHandler('Python')
    result = await hh_request.get_api_request(mock_session)
    assert result == {'key': 'value'}


@pytest.mark.asyncio
async def test_hh_save_to_file() -> None:
    test_dict = {'key': 'value'}
    hh_request = HhApiRequestHandler('Python')
    await hh_request.save_vacancies_to_file(test_dict, 20)
    assert Path.exists(Path(f'data/hh_vacancies_page_{20}.json'))


@pytest.mark.asyncio
async def test_fetch_page_success():
    mock_semaphore = AsyncMock(spec=Semaphore)
    mock_session = AsyncMock(spec=ClientSession)
    mock_handler = MagicMock()

    test_vacancies = {"items": [{"id": 1, "name": "Python dev"}]}
    mock_handler.get_api_request = AsyncMock(return_value=test_vacancies)
    mock_handler.save_vacancies_to_file = AsyncMock()

    instance = HhApiRequestHandler('Python')
    result = await instance.fetch_page(
        semaphore=mock_semaphore,
        session=mock_session,
        handler=mock_handler,
        page=1
    )

    assert result == test_vacancies
    mock_handler.get_api_request.assert_awaited_once_with(mock_session, 1)
    mock_handler.save_vacancies_to_file.assert_awaited_once_with(test_vacancies, 1)
    mock_semaphore.__aenter__.assert_awaited_once()


@pytest.mark.asyncio
async def test_fetch_page_failure():
    mock_semaphore = AsyncMock(spec=Semaphore)
    mock_session = AsyncMock(spec=ClientSession)
    mock_handler = MagicMock()

    mock_handler.get_api_request = AsyncMock(side_effect=aiohttp.ClientError("API недоступен"))

    instance = HhApiRequestHandler('Python')
    result = await instance.fetch_page(
        semaphore=mock_semaphore,
        session=mock_session,
        handler=mock_handler,
        page=2
    )

    assert result is None
    mock_handler.save_vacancies_to_file.assert_not_called()
