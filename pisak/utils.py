import uuid


def get_id():
    """Zwraca losowe id"""
    return str(uuid.uuid1())[:8]

class Singleton(type):
    """Singleton dla klas"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
