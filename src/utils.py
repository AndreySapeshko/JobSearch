def get_all_subclasses(cls: type) -> set:
    """ Рекурсивно получает всех наследников класса """

    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in get_all_subclasses(c)]
    )


def create_instances_of_subclasses(parent_class: type) -> list:
    """ Получает списко объектов всех классов наследников """

    instances = []
    for subclass in get_all_subclasses(parent_class):
        try:
            instances.append(subclass())
        except TypeError as e:
            print(f"Не удалось создать {subclass.__name__}: {e}")
    return instances
