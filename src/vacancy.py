from src.base_vacancy import BaseVacancy


class Vacancy(BaseVacancy):
    """ Класс наследник BaseVacancy описывает вакансию с полями: наименование,
    зарплата (среднее значение), диапазон зарплаты, работодатель, описание, требования и ссылка.
    В классе реализованы магические методы сравнения по полю зарплата (среднее значение). """

    __salary_range: str
    __description: str
    __requirement: str
    __url: str

    __slots__ = ('name', 'salary', 'salary_range', 'employer', 'requirement', 'description', 'url')

    def __init__(self, name: str, salary: int, salary_range: str, employer: str,
                 requirement: str, description: str, url: str) -> None:
        self.__name = name
        self.__salary = salary
        self.__salary_range = salary_range
        self.__employer = employer
        self.__description = description
        self.__requirement = requirement
        self.__url = url

    def __str__(self) -> str:
        return f'Vacancy({self.name}, {self.salary}, {self.employer})'

    def __lt__(self, other: BaseVacancy) -> bool:
        return self.salary < other.salary

    def __le__(self, other: BaseVacancy) -> bool:
        return self.salary <= other.salary

    def __gt__(self, other: BaseVacancy) -> bool:
        return self.salary > other.salary

    def __ge__(self, other: BaseVacancy) -> bool:
        return self.salary >= other.salary

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary == other.salary
