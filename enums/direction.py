from enum import Enum


class Direction(Enum):
    VERTICAL = 'VERTICAL'
    HORIZONTAL = 'HORIZONTAL'

    def __repr__(self):
        return self.value