from abc import ABC


class FileHandler(ABC):

    def read_from_file(self, file_name: str) -> None:
        pass

    def write_in_file(self, file_name: str) -> None:
        pass
