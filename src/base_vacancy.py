from abc import ABC


class BaseVacancy(ABC):

    name: str
    salary: int

    def __init__(self, name: str, salary: int):
        pass
