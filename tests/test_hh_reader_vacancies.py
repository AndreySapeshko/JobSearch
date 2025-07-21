import pytest

from src.hh_reader_vacancies import HhReaderVacancies
from config import PATH_TEST_VACANCIES_JSON
from src.base_vacancy import BaseVacancy


@pytest.mark.parametrize('pages, count_top', [(20, 50), (22, 30)])
def test_hh_reader_vacancies(pages: int, count_top: int) -> None:
    hh_reader = HhReaderVacancies(pages, count_top)
    result = hh_reader.get_vacancies()
    assert isinstance(result, list)
    assert len(result) == count_top
    for vacancy in result:
        assert isinstance(vacancy, BaseVacancy)
