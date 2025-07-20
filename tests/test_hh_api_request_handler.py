import pytest
import aiohttp

from unittest.mock import AsyncMock, patch

from aiohttp import ClientSession

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
