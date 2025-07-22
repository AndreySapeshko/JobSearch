from abc import ABC, abstractmethod

from src.base_vacancy import BaseVacancy


class ReaderVacancies(ABC):
    """ Абстрактный класс определяющий обязательные методы для
    наследников обрабатывающих данные с разных сайтов """

    @abstractmethod
    def get_vacancies(self) -> list[BaseVacancy]:
        pass
