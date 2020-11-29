from enums.car_action import CAR_ACTION
from enums.direction import Direction
from enums.car_type import CarType


class CarState:

    def __init__(self, x: int, y: int, direction: Direction, length: int):
        self.x = x
        self.y = y
        self.direction = direction
        self.length = length

    def __repr__(self):
        return '(x :' + str(self.x) + ' y : ' + str(self.y) + ' ,direction' + str(self.direction) + \
               ', length : ' + str(self.length) + ')'

    def is_horizontal(self):
        return self.direction == Direction.HORIZONTAL

    def is_vertical(self):
        return self.direction == Direction.VERTICAL

    def update(self, action: CAR_ACTION):
        if self.is_horizontal():
            if action == CAR_ACTION.FORWARD  :
                self.x += 1
            elif action == CAR_ACTION.BACKWARD :
                self.x -= 1
            else:
                raise Exception('action should only be FORWARD or BACKWARD')
        elif self.is_vertical():
            if action == CAR_ACTION.FORWARD  :
                self.y -= 1
            elif action == CAR_ACTION.BACKWARD :
                self.y += 1
            else:
                raise Exception('action should only be FORWARD or BACKWARD')
            pass
        else:
            raise Exception("Car should be only vertical or horizontal")


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.direction == other.direction and self.length == other.length