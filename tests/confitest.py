import json

import pytest

from config import PATH_TEST_VACANCIES_JSON


@pytest.fixture
def hh_vacancies_dict():
    with open(PATH_TEST_VACANCIES_JSON) as f:
        data = json.load(f)
    return data
