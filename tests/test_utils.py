from abc import ABC
from pytest import CaptureFixture

from src.utils import get_all_subclasses, create_instances_of_subclasses


class Animal(ABC):

    def get_name(self) -> str:
        pass


class Bird(Animal):

    def get_name(self) -> str:
        return 'Bird'


class Pigeon(Bird):

    def get_name(self) -> str:
        return 'Pigeon'


class HomingPigeon(Pigeon):

    def get_name(self) -> str:
        return 'Homing pigeon'


class AnimalWithError(Animal):

    def __init__(self):
        raise TypeError('Ошибка при создании объекта')

    def get_name(self) -> str:
        return 'AnimalWithError'


def test_get_all_subclasses() -> None:
    classes = get_all_subclasses(Animal)
    name_classes = ['Pigeon', 'HomingPigeon', 'Bird', 'AnimalWithError']
    for subclass in classes:
        name_class = subclass.__name__
        assert name_class in name_classes
        for name in name_classes:
            if name_classes == name:
                del name


def test_create_instances_of_subclasses() -> None:
    instances = create_instances_of_subclasses(Animal)
    name_classes = ['Pigeon', 'Homing pigeon', 'Bird']
    for instance in instances:
        name_class = instance.get_name()
        assert name_class in name_classes
        name_classes = [name for name in name_classes if name_class != name]


def test_error_create_instances_of_subclasses(capsys: CaptureFixture[str]) -> None:
    create_instances_of_subclasses(Animal)
    captured = capsys.readouterr()
    assert captured.out == 'Не удалось создать AnimalWithError: Ошибка при создании объекта\n'
