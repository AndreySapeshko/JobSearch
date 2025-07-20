from abc import ABC

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


def test_get_all_subclasses() -> None:
    classes = get_all_subclasses(Animal)
    name_classes = ['Pigeon', 'HomingPigeon', 'Bird']
    for c in classes:
        assert c.__name__ in name_classes
        for name in name_classes:
            if c.__name__ == name:
                del name
