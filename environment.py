from enum import Enum
from typing import List
from copy import deepcopy


class CAR_ACTION(Enum):
    FORWARD = 'FORWARD'
    BACKWARD = 'BACKWARD'

    def __repr__(self):
        return self.value

    def change_action(self):
        if self == CAR_ACTION.FORWARD:
            return CAR_ACTION.BACKWARD
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

    def is_horizontal(self):
        return self.direction == Direction.HORIZONTAL

    def is_vertical(self):
        return self.direction == Direction.VERTICAL


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

    def compute_cars(self):
        cars = {}
        for row in range(self.height):
            for col in range(self.width):  ## On s'occupe pas des rebords # ni du *
                if 'a' <= self.board_game[row][col] <= 'z' and self.board_game[row][col] not in cars.keys():
                    cars_state = self.compute_car_state_from_pos(row=row, col=col)
                    cars.update({self.board_game[row][col]: cars_state})
        return dict(sorted(cars.items()))

    def compute_car_state_from_pos(self, row, col):
        direction = self.compute_direction(row=row, col=col)
        y, x = self.compute_starting_point(row=row, col=col, direction=direction)
        length = self.compute_length(y=y, x=x, direction=direction)
        return CarState(x=x, y=y, direction=direction, length=length)

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


empty_board = """
########
#      #
#      #
#      *
#      #
#      #
#      #
########
"""

MARGIN_WALL = 1


class Environment:
    def __init__(self, board: str):
        lines = board.strip().split('\n')

        self.board_game = BoardGame(board_game=lines)

        self.cars = self.board_game.compute_cars()

        self.goal = self.board_game.search_goal()

        self.init_state = State.from_cars(self.cars)

        self.compute_states()

        self.states = State.states_from_cars(cars=self.cars, board_game=self.board_game)

        actions = self.init_actions(self.cars)

        print("self.cars ", self.cars)
        print("actions :", actions)
        print("states")

        self.current_state = deepcopy(self.init_state)

        for state in self.states:
            print(state)
            if State((CarState(x=2, y=3, direction=Direction.HORIZONTAL, length=2),
                      CarState(x=5, y=3, direction=Direction.VERTICAL, length=3))) == state:
                print("Equal")

    def init_actions(self, cars):
        actions = {}
        for each_car, each_car_state in cars.items():
            actions.update({(each_car, CAR_ACTION.FORWARD): 0})
            actions.update({(each_car, CAR_ACTION.BACKWARD): 0})
        return actions

    def compute_states(self):
        states = []
        print('Ciycy')

        for car_name, car_state in self.cars.items():
            print('car ', car_name)
            # Generate a new state
            states_current_car = self.generate_new_sate(car_name=car_name)
            # add state
            print(states_current_car)

        exit(1)
        return states

    def generate_new_sate(self, car_name: str):
        states = []
        current_car: CarState = deepcopy(self.cars[car_name])
        print('GENERATE NEW STATES with base : ' , car_name)
        print(self.board_game)
        if current_car.is_horizontal():
            for start_x in range(MARGIN_WALL,
                                 self.board_game.width - current_car.length):  # Pour chaque position possible de cette voiture
                # place first car
                new_board = BoardGame(empty_board.strip().split('\n'))
                current_car.x = start_x
                new_board.place_car(car_name=car_name, car=current_car)
                print(new_board)
                # Place other cars
                self.place_remaining_cars(board=new_board, placed_cars=[car_name], states=states)

        else:
            for start_y in range(MARGIN_WALL,
                                 self.board_game.height - current_car.length):  # Pour chaque position possible de cette voiture
                # place first car
                new_board = BoardGame(empty_board.strip().split('\n'))
                current_car.y = start_y
                new_board.place_car(car_name=car_name, car=current_car)

                # Place other cars
                self.place_remaining_cars(board=new_board, placed_cars=[car_name], states=states)

        return states

    def allCarsOrder(self, placed_cars: List[str]):
        all_sort_possible = []
        keys = list(self.cars.keys())
        for i in range(0, len(self.cars)):
            key = keys.pop(0)
            if key not in placed_cars:
                keys.append(key)
            new_order = {}
            for car_name in keys:
                new_order.update({car_name: self.cars[car_name]})
            if len(self.cars) - len(placed_cars) > len(all_sort_possible):
                all_sort_possible.append(new_order)
        return all_sort_possible

    # Recursif
    def place_remaining_cars(self, board: BoardGame, placed_cars: List[str], states: List[BoardGame]):

        if len(placed_cars) == len(self.cars.keys()) :
            if board.is_all_cars_in_board(list(self.cars.keys()) ):
                # print(placed_cars, list(self.cars.keys()))
                # print('all cars placed : ')
                # print(board)
                if board not in states:
                    states.append(board)
            else:
                print(list(self.cars.keys()), '  board.is_all_cars_in_board(list(self.cars.keys())  ', board.is_all_cars_in_board(list(self.cars.keys())) )
                print(board)
                print('ABANDONNED')
                exit(1)
            # states.append(board)
            return
        for ordered_cars in self.allCarsOrder(placed_cars): #Pour chaque ordre de voitures possible

            # print('new Order : ', list(ordered_cars.keys()))
            board_ordered_cars = deepcopy(board)
            placed_cars_each_cars_order = deepcopy(placed_cars)

            # print('state Board each Orders of cars')
            # print(board_ordered_cars)
            for car_name, car_state in ordered_cars.items(): # Pour chaque Voiture

                if car_name in placed_cars_each_cars_order:
                    # print('car : ', car_name, ' already in placed cars : ', placed_cars)
                    continue
                board_each_car = deepcopy(board_ordered_cars)
                placed_cars_each_car = deepcopy(placed_cars_each_cars_order)

                # print('new car ', car_name, '    placed_cars : ', placed_cars_each_car)
                # print('state Board each car ')
                # print(board_each_car)

                if car_state.is_horizontal():
                    for start_x in range(MARGIN_WALL,
                                         self.board_game.width - car_state.length):  # Pour chaque position possible de cette voiture
                        # Copy the board
                        board_each_car_pos_x = deepcopy(board_each_car)
                        placed_cars_each_car_pos_x = deepcopy(placed_cars_each_car)

                        car_state.x = start_x

                        # print('start_x ', start_x, '  car name ', car_name, '   state : ', car_state, '  placed cars : ', placed_cars_each_car_pos_x)
                        # print('board_each_car_pos_x.place_car_is_possible(car=car_state) ', board_each_car_pos_x.place_car_is_possible(car=car_state))
                        # print('car_name not in placed_cars_each_car_pos_x ', car_name not in placed_cars_each_car_pos_x)
                        # print(board_each_car_pos_x)
                        if board_each_car_pos_x.place_car_is_possible(car=car_state) and car_name not in placed_cars_each_car_pos_x:
                            # print('place_car_is_possible ', car_state)
                            board_each_car_pos_x.place_car(car_name=car_name, car=car_state)

                            # print('new Car placed ', car_name)
                            # print(board_each_car_pos_x)
                            # Place other cars
                            placed_cars_each_car_pos_x.append(car_name)
                            self.place_remaining_cars(board=deepcopy(board_each_car_pos_x), placed_cars=deepcopy(placed_cars_each_car_pos_x), states=states)

                else:
                    for start_y in range(MARGIN_WALL,
                                         self.board_game.height - car_state.length):  # Pour chaque position possible de cette voiture

                        # Copy the board and placed cars
                        board_each_car_pos_y = deepcopy(board_each_car)
                        placed_cars_each_car_pos_y = deepcopy(placed_cars_each_car)

                        car_state.y = start_y

                        # print('start_y ', start_y, '  car name ', car_name, '   state : ', car_state, '  placed cars : ', placed_cars_each_car_pos_y)

                        if board_each_car_pos_y.place_car_is_possible(car=car_state) and car_name not in placed_cars_each_car_pos_y:
                            # print('place_car_is_possible ', car_state)
                            board_each_car_pos_y.place_car(car_name=car_name, car=car_state)
                            # print('new Car placed ', car_name)
                            # print(board_each_car_pos_y)
                            # Place other cars
                            placed_cars_each_car_pos_y.append(car_name)
                            self.place_remaining_cars(board=deepcopy(board_each_car_pos_y), placed_cars=placed_cars_each_car_pos_y, states=states)
        # print('Finish place_remaining_cars Board Impossible')
        # print(board)
