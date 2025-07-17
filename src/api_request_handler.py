from abc import ABC
from typing import Any


class ApiRequestHandler(ABC):
    """ Абстрактный класс определяющий обязательный метод отправки-получения get-запроса """

    def get_api_request(self) -> Any:
        pass
