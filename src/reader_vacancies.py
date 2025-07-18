from abc import ABC

from src.base_vacancy import BaseVacancy


class ReaderVacancies(ABC):

    def read_from_file(self) -> list:
        pass

    def get_vacancies(self) -> list[BaseVacancy]:
        pass
