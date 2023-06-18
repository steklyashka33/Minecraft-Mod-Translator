from dataclasses import dataclass

@dataclass(init=False)
class DataClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            