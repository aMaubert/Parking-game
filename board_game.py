from typing import List

from car_state import CarState
from enums.car_action import CAR_ACTION
from enums.direction import Direction
from enums.car_type import CarType

def is_impossible(case: str):
    if case == ' ' or case == '*':
        return False
    return True

class BoardGame:

    def __init__(self, board_game: List[str]):
        self.board_game = board_game
        self.height = len(board_game)
        self.width = len(board_game[0])

    def is_wall(self, x: int, y: int):
        if self.board_game[y][x] == '#':
            return True
        return False

    def deplacement_is_possible(self, car: CarState, action: CAR_ACTION):
        if car.direction == Direction.HORIZONTAL:
            if action == CAR_ACTION.FORWARD:
                if is_impossible(self.board_game[car.y][car.x + car.length]):
                    return False
            elif action == CAR_ACTION.BACKWARD:
                if is_impossible(self.board_game[car.y][car.x - 1]):
                    return False
        elif car.direction == Direction.VERTICAL:
            if action == CAR_ACTION.FORWARD:
                if is_impossible(self.board_game[car.y - 1][car.x]):
                    return False
            elif action == CAR_ACTION.BACKWARD:
                if is_impossible(self.board_game[car.y + car.length][car.x]):
                    return False
        return True

    def deplacement_will_crush_a_car(self, car: CarState, action: CAR_ACTION):
        if self.deplacement_is_possible(car, action):
            return False

        if car.direction == Direction.HORIZONTAL:
            if action == CAR_ACTION.FORWARD:
                if 'a' <= self.board_game[car.y][car.x + car.length] <= 'z':
                    return True
            elif action == CAR_ACTION.BACKWARD:
                if 'a' <= self.board_game[car.y][car.x - 1] <= 'z':
                    return True
        elif car.direction == Direction.VERTICAL:
            if action == CAR_ACTION.FORWARD:
                if 'a' <= self.board_game[car.y - 1][car.x] <= 'z':
                    return True
            elif action == CAR_ACTION.BACKWARD:
                if 'a' <= self.board_game[car.y + car.length][car.x] <= 'z':
                    return True
        return False

    def __repr__(self):
        return '\n'.join(self.board_game)
    def __eq__(self, other):
        if self.height != other.height or self.width != other.width:
            return False
        for row in range(self.height):
            for column in range(self.width):
                if self.board_game[row][column] != other.board_game[row][column] :
                    return False
        return True

    def compute_cars(self):
        cars = {}
        for row in range(self.height):
            for col in range(self.width):  ## On s'occupe pas des rebords # ni du *
                if 'a' <= self.board_game[row][col] <= 'z' and self.board_game[row][col] not in cars.keys():
                    cars_state = self.compute_car_state_from_pos(row=row, col=col, type=self.board_game[row][col])
                    cars.update({self.board_game[row][col]: cars_state})
        return dict(sorted(cars.items()))

    def compute_car_state_from_pos(self, row, col, type):
        direction = self.compute_direction(row=row, col=col)
        y, x = self.compute_starting_point(row=row, col=col, direction=direction)
        length = self.compute_length(y=y, x=x, direction=direction)
        if type == 'a':
            carType = CarType.RED
        elif type == 'b':
            carType = CarType.WHITE
        elif type == 'c':
            carType = CarType.GREY
        elif type == 'd':
            carType = CarType.BLUE
        elif type == 'e' or type == 'g':
            carType = CarType.YELLOW
        else:
            carType = CarType.BLACK
        return CarState(x=x, y=y, direction=direction, length=length, carType=carType)

    def compute_direction(self, row, col):
        direction = Direction.VERTICAL
        if self.board_game[row][col] == self.board_game[row][col + 1] or self.board_game[row][col] == \
                self.board_game[row][col - 1]:
            direction = Direction.HORIZONTAL
        return direction

    def compute_starting_point(self, row, col, direction):
        if direction == Direction.VERTICAL:
            if self.board_game[row][col] == self.board_game[row][col - 1]:
                return self.compute_starting_point(row, col - 1, direction)
            return row, col
        if self.board_game[row][col] == self.board_game[row - 1][col]:
            return self.compute_starting_point(row - 1, col, direction)
        return row, col

    def compute_length(self, y, x, direction):
        if direction == Direction.VERTICAL:
            if self.board_game[y][x] == self.board_game[y + 1][x]:
                return self.compute_length(y + 1, x, direction) + 1
            return 1
        if self.board_game[y][x] == self.board_game[y][x + 1]:
            return self.compute_length(y, x + 1, direction) + 1
        return 1

    def search_goal(self):
        for row in range(self.height):
            for column in range(self.width):
                if self.board_game[row][column] == '*':
                    return column, row
        raise Exception('Can\' find goal')
        pass

    def place_car(self, car_name: str, car: CarState):
        if car.is_horizontal():
            board_game_y = list(self.board_game[car.y])
            for column in range(car.x, car.x + car.length):
                board_game_y[column] = car_name
            self.board_game[car.y] = ''.join(board_game_y)
        else:
            for row in range(car.y, car.y + car.length):
                board_game_row = list(self.board_game[row])
                board_game_row[car.x] = car_name
                self.board_game[row] = ''.join(board_game_row)

    def position_is_empty(self, x: int, y: int):
        return self.board_game[y][x] == ' '

    def place_car_is_possible(self, car: CarState):
        if car.is_horizontal():
            for column in range(car.x, car.x + car.length):
                if not self.position_is_empty(column, car.y):
                    return False
        else:
            for row in range(car.y, car.y + car.length):
                if not self.position_is_empty(car.x, row):
                    return False
        # print('car can be placed :',car)
        # print(self)
        return True

    def is_all_cars_in_board(self, car_names: List[str]):
        for car_name in car_names:
            car_is_in_board = False
            for row in self.board_game:
                if car_name in row:
                    car_is_in_board = True
                    break
            if car_is_in_board is False:
                return False
        return True
