import uuid


def get_id():
    return str(uuid.uuid1())[:8]
