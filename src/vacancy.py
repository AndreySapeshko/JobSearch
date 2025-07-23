from src.base_vacancy import BaseVacancy


class Vacancy(BaseVacancy):
    salary_range: str
    description: str
    requirement: str
    url: str

    __slots__ = ('name', 'salary', 'salary_range', 'employer', 'requirement', 'description', 'url')

    def __init__(self, name: str, salary: int, salary_range: str, employer: str, requirement: str, description: str, url: str) -> None:
        self.name = name
        self.salary = salary
        self.salary_range = salary_range
        self.employer = employer
        self.description = description
        self.requirement = requirement
        self.url = url

    def __str__(self) -> str:
        return f'Vacancy({self.name}, {self.salary}, {self.employer})'
