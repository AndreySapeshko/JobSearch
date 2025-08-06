from src.base_vacancy import BaseVacancy


class Vacancy(BaseVacancy):
    """ Класс наследник BaseVacancy описывает вакансию с полями: наименование,
    зарплата (среднее значение), диапазон зарплаты, работодатель, описание, требования и ссылка.
    В классе реализованы магические методы сравнения по полю зарплата (среднее значение). """

    __salary_range: str
    __description: str
    __requirement: str
    __url: str

    __slots__ = ('__name', '__salary', '__salary_range', '__employer', '__requirement', '__description', '__url')

    def __init__(self, id: str, name: str, salary: int, salary_range: str, employer: str,
                 employer_id: str, requirement: str, description: str, url: str) -> None:
        self.__id = id
        self.__name = name
        self.__salary = salary
        self.__salary_range = salary_range
        self.__employer = employer
        self.__employer_id = employer_id
        self.__description = description
        self.__requirement = requirement
        self.__url = url

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def salary(self) -> int:
        return self.__salary

    @property
    def salary_range(self) -> str:
        return self.__salary_range

    @property
    def employer(self) -> str:
        return self.__employer

    @property
    def employer_id(self) -> str:
        return self.__employer_id

    @property
    def description(self) -> str:
        return self.__description

    @property
    def requirement(self) -> str:
        return self.__requirement

    @property
    def url(self) -> str:
        return self.__url

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
        return (self.name == other.name and self.salary == other.salary
                and self.salary_range == other.salary_range and self.employer == other.employer
                and self.description == other.description and self.requirement == other.requirement
                and self.url == other.url)
