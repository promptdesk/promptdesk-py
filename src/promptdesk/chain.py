import uuid

class Chain:
    def __init__(self, name) -> None:
        self.uuid = str(uuid.uuid4())
        self.name = name
        pass