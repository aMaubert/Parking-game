from enum import Enum


class CarColor(Enum):
    RED = 'a'
    BLUE = 'b'
    GREY = 'c'
    YELLOW = 'd'
    BLACK = 'e'
    WHITE = 'f'

    def __repr__(self):
        return self.value
