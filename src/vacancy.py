from src.base_vacancy import BaseVacancy


class Vacancy(BaseVacancy):

    description: str
    requirement: str

    def __init__(self, name: str, salary: int, employer: str, requirement: str, description: str) -> None:
        self.name = name
        self.salary = salary
        self.employer = employer
        self.description = description
        self.requirement = requirement

    def __str__(self) -> str:
        return f'Vacancy({self.name}, {self.salary}, {self.employer})'
