from typing import Callable


def singleton(class_: type) -> Callable:
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class CurrentUser:
    def __init__(self) -> None:
        self.user_id = None
        self.period = None
