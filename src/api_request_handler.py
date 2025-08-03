from abc import ABC, abstractmethod
from typing import Any


class ApiRequestHandler(ABC):
    """ Абстрактный класс определяющий обязательный метод отправки-получения get-запроса """

    @abstractmethod
    def get_api_request(self) -> Any:
        pass
