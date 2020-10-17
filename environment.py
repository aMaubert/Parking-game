from enum import Enum
from typing import List
from collections import OrderedDict
from copy import copy, deepcopy

LEVELS = ["""
########
#ccc d #
#    d #
# aa d *
#bbbf  #
#  efgg#
#  e hh#
########
""", """
########
#      #
#      #
# aa b *
# d  b #
# d  b #
# d ccc#
########
""","""
########
#ccc d #
#    d #
# aa d *
#bbb   #
#  e gg#
#  e hh#
########
"""]


class CAR_ACTION(Enum):
    FORWARD = 'FORWARD'
    BACKWARD = 'BACKWARD'

    def __repr__(self):
        return self.value

    def change_action(self):
        if self == CAR_ACTION.FORWARD:
            return  CAR_ACTION.BACKWARD
        return CAR_ACTION.FORWARD


class Direction(Enum):
    VERTICAL = 'VERTICAL'
    HORIZONTAL = 'HORIZONTAL'

    def __repr__(self):
        return self.value


class CarState:

    def __init__(self, x: int, y: int, direction: Direction, length: int):
        self.x = x
        self.y = y
        self.direction = direction
        self.length = length

    def __repr__(self):
        return '(x :' + str(self.x) + ' y : ' + str(self.y) + ' ,direction' + str(self.direction) + \
               ', length : ' + str(self.length) + ')'


def is_impossible(case: str):
    if case == ' ' or case == '*':
        return False
    return True


def is_car(case: str):
    if 'a' <= case <= 'z':
        return True
    return False


def is_win(case: str):
    if case == '*':
        return True
    return False


class BoardGame:

    def __init__(self, board_game: List[str]):
        self.board_game = board_game

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

    def car_blocking_movement(self, car: CarState, action: CAR_ACTION):
        if not self.deplacement_will_crush_a_car(car=car, action=action):
            return None
        if car.direction == Direction.HORIZONTAL:
            if action == CAR_ACTION.FORWARD:
                return self.board_game[car.y][car.x + car.length]
            elif action == CAR_ACTION.BACKWARD:
                return self.board_game[car.y][car.x - 1]
        elif car.direction == Direction.VERTICAL:
            if action == CAR_ACTION.FORWARD:
                return self.board_game[car.y - 1][car.x]
            elif action == CAR_ACTION.BACKWARD:
                return self.board_game[car.y + car.length][car.x]
        raise Exception('Impossible car_blocking_movement exception')

    def deplacement(self, car: CarState, action: CAR_ACTION):
        if car.direction == Direction.HORIZONTAL:
            if action == CAR_ACTION.FORWARD:
                if is_impossible(self.board_game[car.y][car.x + car.length]):
                    return None
                list_mot = list(self.board_game[car.y])
                list_mot[car.x + car.length] = self.board_game[car.y][car.x]
                list_mot[car.x] = ' '
                self.board_game[car.y] = ''.join(list_mot)
                car.x += 1
            elif action == CAR_ACTION.BACKWARD:
                if is_impossible(self.board_game[car.y][car.x - 1]):
                    return None
                row_y = list(self.board_game[car.y])
                row_y[car.x - 1] = self.board_game[car.y][car.x + (car.length - 1)]
                row_y[car.x + (car.length - 1)] = ' '
                self.board_game[car.y] = ''.join(row_y)
                car.x -= 1
        else:
            if action == CAR_ACTION.FORWARD:
                if is_impossible(self.board_game[car.y - 1][car.x]):
                    return None
                row_y_minus_1 = list(self.board_game[car.y - 1])
                row_y_minus_1[car.x] = self.board_game[car.y + (car.length - 1)][car.x]
                self.board_game[car.y - 1] = ''.join(row_y_minus_1)

                row_y_plus_length_minus_1 = list(self.board_game[car.y + (car.length - 1)])
                row_y_plus_length_minus_1[car.x] = ' '
                self.board_game[car.y + (car.length - 1)] = ''.join(row_y_plus_length_minus_1)
                car.y -= 1
            elif action == CAR_ACTION.BACKWARD:
                if is_impossible(self.board_game[car.y + car.length][car.x]):
                    return None
                row_y_plus_length = list(self.board_game[car.y + car.length])
                row_y_plus_length[car.x] = self.board_game[car.y][car.x]
                self.board_game[car.y + car.length] = ''.join(row_y_plus_length)

                row_y = list(self.board_game[car.y])
                row_y[car.x] = ' '
                self.board_game[car.y] = ''.join(row_y)
                car.y += 1
        return car

    def make_way(self,cars: {str: CarState}, car: CarState, action: CAR_ACTION):
        #TODO tant que la position a liberer n'est pas libre
        print('car : ', self.board_game[car.y][car.x], ' ', car, '  action :', action)
        x , y = BoardGame.compute_position_to_unblock(car, action)
        car_to_move_away = cars[self.board_game[y][x]]
        if not self.deplacement_is_possible(car=car_to_move_away, action=CAR_ACTION.FORWARD) and \
           not self.deplacement_is_possible(car=car_to_move_away, action=CAR_ACTION.BACKWARD):
            print('Voiture ', self.board_game[y][x],'Coincé' )
            if self.deplacement_will_crush_a_car(car=car_to_move_away, action=CAR_ACTION.FORWARD):
                self.make_way(cars=cars, car=car_to_move_away, action=CAR_ACTION.FORWARD)
            elif self.deplacement_will_crush_a_car(car=car_to_move_away, action=CAR_ACTION.BACKWARD):
                self.make_way(cars=cars, car=car_to_move_away, action=CAR_ACTION.BACKWARD)
            else:
                print('Voiture ', self.board_game[y][x],'Coincé , IMPOSSIBLE logiquement')
                exit(1)
        given_direction = CAR_ACTION.BACKWARD
        count = 0
        while is_car(self.board_game[y][x]):
            count += 1
            if count == 60:
                print('COUNT arrivé  à ', str(count),' donc bloker')
                exit(1)
            if self.deplacement_is_possible(car=car_to_move_away, action=given_direction):
                print(x, y, ' ', self.board_game[y][x])
                self.deplacement(car=car_to_move_away, action=given_direction)
                print(x, y, ' ', self.board_game[y][x])
                print('Save the state in make_way')
                print(self)
                continue
            if self.deplacement_will_crush_a_car(car=car_to_move_away, action=given_direction):
                # TODO DO make_way on the car that syuck the current car
                self.make_way(cars=cars, car=car_to_move_away, action=given_direction)
                continue

            given_direction = given_direction.change_action()

            if self.deplacement_is_possible(car=car_to_move_away, action=given_direction):
                print(x,y, ' ', self.board_game[y][x])
                self.deplacement(car=car_to_move_away, action=given_direction)
                print(x, y, ' ', self.board_game[y][x])
                print('Save the state in make_way')
                print(self)
                continue

            if self.deplacement_will_crush_a_car(car=car_to_move_away, action=given_direction):
                self.make_way(cars=cars, car=car_to_move_away, action=given_direction)
                continue
            else:
                print('case bloquante ', self.board_game[y][x], ' pos : ', x , y)


    def __repr__(self):
        return '\n'.join(self.board_game)

    @staticmethod
    def compute_position_to_unblock(car: CarState, action:CAR_ACTION):
        if action == CAR_ACTION.FORWARD:
            if car.direction == Direction.HORIZONTAL:
                return car.x + car.length, car.y
            elif car.direction == Direction.VERTICAL:
                return car.x, car.y - 1
        elif action == CAR_ACTION.BACKWARD:
            if car.direction == Direction.HORIZONTAL:
                return car.x - 1, car.y
            elif car.direction == Direction.VERTICAL:
                return car.x, car.y + car.length
        raise Exception('compute_position_to_unblock error')


class State:

    def __init__(self, state: tuple):
        self.value = state

    def __repr__(self):
        ret = ""
        for each_car_state in self.value:
            ret += f"(x={each_car_state.x}, y={each_car_state.y}, direction={each_car_state.direction}, length={each_car_state.length})\t"
        return ret

    @staticmethod
    def from_cars(cars: {str: CarState}):
        state = []
        for each_car, each_car_state in cars.items():
            state.append(each_car_state)
        return State(state=tuple(state))

    def __eq__(self, other):
        if len(self.value) != len(other.value):
            return False
        for each_car_state in self.value:
            exist = False
            for each_car_state_other in other.value:
                if each_car_state.y == each_car_state_other.y and \
                        each_car_state.x == each_car_state_other.x and \
                        each_car_state.direction == each_car_state_other.direction and \
                        each_car_state.length == each_car_state_other.length:
                    exist = True
                    break
            if not exist:
                return False

        return True

    @staticmethod
    def states_from_cars(cars: {str: CarState}, board_game: BoardGame):
        states = []
        print(board_game)
        print("Save initial State")
        print()
        for car, car_state in cars.items():
            print()
            print('Compute states for car ', car)
            print('Computes states for BACKWARD')
            State.compute_states_backward(deepcopy(cars), deepcopy(car_state), deepcopy(board_game))
            print('Computes states for FORWARD')
            State.compute_states_forward(deepcopy(cars), deepcopy(car_state), deepcopy(board_game))

        return states

    @staticmethod
    def compute_states_backward(cars: {str: CarState}, car_state: CarState, board_game: BoardGame):
        states = []
        x = car_state.x
        y = car_state.y

        if car_state.direction == Direction.HORIZONTAL:
            while not is_impossible(board_game.board_game[y][x - 1]) or is_car(board_game.board_game[y][x - 1]):
                if not is_car(board_game.board_game[y][x - 1]):
                    board_game.deplacement(cars[board_game.board_game[y][x]], CAR_ACTION.BACKWARD)
                    x -= 1
                    car_state.x = x
                    print('Save the State')
                    print(board_game)
                else:
                    board_game.make_way(cars=cars, car=car_state, action=CAR_ACTION.BACKWARD)

        else:
            while not is_impossible(board_game.board_game[y + car_state.length][x]) or is_car(board_game.board_game[y + car_state.length][x]):
                if not is_car(board_game.board_game[y + car_state.length][x]):
                    board_game.deplacement(cars[board_game.board_game[y][x]], CAR_ACTION.BACKWARD)
                    y += 1
                    car_state.y = y
                    print('Save the State')
                    print(board_game)
                else:
                    board_game.make_way(cars=cars, car=car_state, action=CAR_ACTION.BACKWARD)

        return states

    @staticmethod
    def compute_states_forward(cars: {str: CarState}, car_state: CarState, board_game: BoardGame):
        states = []
        x = car_state.x
        y = car_state.y

        if car_state.direction == Direction.HORIZONTAL:
            while ( not is_impossible(board_game.board_game[y][x + car_state.length]) and not is_win(board_game.board_game[y][x + car_state.length]) ) or\
                    is_car(board_game.board_game[y][x + car_state.length]):
                if not board_game.deplacement_will_crush_a_car(car=car_state, action=CAR_ACTION.FORWARD):
                    board_game.deplacement(car=cars[board_game.board_game[y][x + 1]], action=CAR_ACTION.FORWARD)
                    x += 1
                    car_state.x = x
                    print('Save the state')
                    print(board_game)
                else:
                    board_game.make_way(cars=cars, car=car_state, action=CAR_ACTION.FORWARD)

        else:
            while not is_impossible(board_game.board_game[y - 1][x]) or is_car(board_game.board_game[y - 1][x]):
                if not board_game.deplacement_will_crush_a_car(car=car_state, action=CAR_ACTION.FORWARD) :
                    board_game.deplacement(cars[board_game.board_game[y][x]], CAR_ACTION.FORWARD)
                    y -= 1
                    car_state.y = y
                    print('Save the state')
                    print(board_game)

                else:
                    board_game.make_way(cars=cars, car=car_state, action=CAR_ACTION.FORWARD)

        return states




### Environnment => Positions de chaques voiture sur le plateau
class Environment:
    def __init__(self):
        self.states = []

        lines = LEVELS[1].strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0])

        self.cars = self.init_cars(board_game=lines, height=self.height, width=self.width)

        self.init_state = State.from_cars(self.cars)

        board_game = BoardGame(lines)

        self.states = State.states_from_cars(cars=self.cars, board_game=board_game)

        actions = self.init_actions(self.cars)
        print("self.cars ", self.cars)
        print("actions :", actions)
        print("states")

        for state in self.states:
            print(state)
            if State((CarState(x=2, y=3, direction=Direction.HORIZONTAL, length=2),
                      CarState(x=5, y=3, direction=Direction.VERTICAL, length=3))) == state:
                print("Equal")

    def init_cars(self, board_game: List[str], height: int, width: int):
        cars = {}
        for row in range(height):
            for col in range(width):  ## On s'occupe pas des rebords # ni du *
                if 'a' <= board_game[row][col] <= 'z' and board_game[row][col] not in cars.keys():
                    cars_state = self.carStateFromRowAndCol(lines=board_game, row=row, col=col)
                    cars.update({board_game[row][col]: cars_state})
        return dict(sorted(cars.items()))

    def carStateFromRowAndCol(self, lines: List[str], row: int, col: int):
        direction = self.directionFromLevel(lines=lines, row=row, col=col)
        y, x = self.compute_starting_point(lines=lines, row=row, col=col, direction=direction)
        length = self.compute_length(lines=lines, y=y, x=x, direction=direction)
        car_state = CarState(x=x, y=y, direction=direction, length=length)
        return car_state

    def directionFromLevel(self, lines: List[str], row: int, col: int):
        direction = Direction.VERTICAL
        if lines[row][col] == lines[row][col + 1] or lines[row][col] == lines[row][col - 1]:
            direction = Direction.HORIZONTAL
        return direction

    def compute_starting_point(self, lines: List[str], row: int, col: int, direction: Direction):
        if direction == Direction.VERTICAL:
            if lines[row][col] == lines[row][col - 1]:
                return self.compute_starting_point(lines, row, col - 1, direction)
            return row, col
        if lines[row][col] == lines[row - 1][col]:
            return self.compute_starting_point(lines, row - 1, col, direction)

        return row, col

    def compute_length(self, lines, y, x, direction):
        if direction == Direction.VERTICAL:
            if lines[y][x] == lines[y + 1][x]:
                return self.compute_length(lines, y + 1, x, direction) + 1
            return 1
        if lines[y][x] == lines[y][x + 1]:
            return self.compute_length(lines, y, x + 1, direction) + 1
        return 1

    def init_actions(self, cars):
        actions = {}
        for each_car, each_car_state in cars.items():
            actions.update({(each_car, CAR_ACTION.FORWARD): 0})
            actions.update({(each_car, CAR_ACTION.BACKWARD): 0})
        return actions
