from src.hh_reader_vacancies import HhReaderVacancies
from config import PATH_TEST_VACANCIES_JSON
from src.base_vacancy import BaseVacancy


def test_hh_reader_vacancies() -> None:
    hh_reader = HhReaderVacancies(PATH_TEST_VACANCIES_JSON)
    result = hh_reader.get_vacancies()
    assert isinstance(result, list)
    assert len(result) == 1
    for vacancy in result:
        assert isinstance(vacancy, BaseVacancy)
