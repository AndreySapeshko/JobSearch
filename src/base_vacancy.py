from abc import ABC


class BaseVacancy(ABC):
    """ Абстрактный класс определяющий обязательные поля для
    наследников вакансий различных типов """

    name: str
    salary: int
    employer: str

    def __init__(self, name: str, salary: int, employer: str) -> None:
        pass
