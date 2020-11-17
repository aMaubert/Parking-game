from enum import Enum


class CarType(Enum):
    RED = 'RED'
    BLUE = 'BLUE'
    GREY = 'GREY'
    YELLOW = 'YELLOW'
    BLACK = 'BLACK'
    WHITE = 'WHITE'

    def __repr__(self):
        return self.value
