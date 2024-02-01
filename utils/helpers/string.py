import uuid


def valid_uuidv4(value: str) -> bool:
    try:
        val = uuid.UUID(value, version=4)
        return str(val) == value
    except ValueError:
        return False
    
def make_uuid4(text: str):
    return uuid.UUID(text, version=4)