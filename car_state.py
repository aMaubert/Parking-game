from enums.direction import Direction
from enums.car_type import CarType


class CarState:

    def __init__(self, x: int, y: int, direction: Direction, length: int, carType: CarType):
        self.x = x
        self.y = y
        self.direction = direction
        self.length = length
        self.carType = carType

    def __repr__(self):
        return '(x :' + str(self.x) + ' y : ' + str(self.y) + ' ,direction' + str(self.direction) + \
               ', length : ' + str(self.length) + ', carType : ' + str(self.carType) + ')'

    def is_horizontal(self):
        return self.direction == Direction.HORIZONTAL

    def is_vertical(self):
        return self.direction == Direction.VERTICAL