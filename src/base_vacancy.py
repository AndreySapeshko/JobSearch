from abc import ABC, abstractmethod


class BaseVacancy(ABC):
    """ Абстрактный класс определяющий обязательные поля для
    наследников вакансий различных типов """

    name: str
    salary: int
    employer: str
    requirement: str

    @abstractmethod
    def __init__(self, name: str, salary: int, employer: str, requirement: str) -> None:
        pass
