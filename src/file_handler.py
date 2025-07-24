from abc import ABC, abstractmethod
from pathlib import Path

from src.base_vacancy import BaseVacancy


class FileHandler(ABC):
    """ Абстрактный класс определяющий обязательные методы для наследников
    обрабатывающих файлы различных форматов """

    @abstractmethod
    def read_from_file(self, file_name: Path) -> None:
        pass

    @abstractmethod
    def write_in_file(self, vacancies: BaseVacancy) -> None:
        pass

    @abstractmethod
    def delete_file(self, file_name: Path) -> None:
        pass
