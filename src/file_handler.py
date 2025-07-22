from abc import ABC, abstractmethod


class FileHandler(ABC):
    """ Абстрактный класс определяющий обязательные методы для наследников
    обрабатывающих файлы различных форматов """

    @abstractmethod
    def read_from_file(self) -> None:
        pass

    @abstractmethod
    def write_in_file(self) -> None:
        pass
