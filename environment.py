from typing import List
from copy import deepcopy

from board_game import BoardGame
from car_state import CarState
from enums.car_action import CAR_ACTION
from state import State

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

REWARD_IMPOSSIBLE = -100000000
REWARD_SUCCESS = 500
REWARD_DEFAULT = -1


def state_already_found(board: BoardGame, states: List[BoardGame]):
    for each_board in states:
        if board == each_board:
            return True
    return False


class Environment:
    def __init__(self, board: str):
        lines = board.strip().split('\n')

        self.board_game = BoardGame(board_game=lines)

        self.cars = self.board_game.compute_cars()
        # {'a' : CarState(x=, y=, length=, direction=),
        #  'b' : CarState(x=, y=, length=, direction=D)}

        self.goal = self.board_game.search_goal()

        self.init_state = State.from_cars(deepcopy(self.cars))

        #init_state = (CarState(),CarState(),CarState())

        self.states = self.compute_states()
        # states = [(CarState(),CarState(),CarState()), (CarState(),CarState(),CarState()), (CarState(),CarState(),CarState())]

        self.cars = self.board_game.compute_cars()


        print("states \n", self.states)
        print("self.cars ", self.cars)

    @staticmethod
    def fetch_car_name(cars: {str: CarState}, car_state_to_search: CarState):
        for car_name, state_car in cars.items():
            if state_car == car_state_to_search:
                return car_name
        raise Exception('Should retrieve the car')

    def init_actions(self):
        actions = []
        cars = deepcopy(self.cars)
        for each_car_name, each_car_state in cars.items():
            actions.append((each_car_name, CAR_ACTION.FORWARD))
            actions.append((each_car_name, CAR_ACTION.BACKWARD))
        return actions

    def compute_states(self):
        states = []
        for car_name, car_state in self.cars.items():
            # Generate a new state
            board_games = self.generate_new_sate(car_name=car_name)
            # add state
            for board_game in board_games:
                cars = board_game.compute_cars()  # Compute the cars states
                state = State.from_cars(cars)  # Create the state
                states.append(state)
        return states

    def generate_new_sate(self, car_name: str):
        board_games = []
        current_car: CarState = deepcopy(self.cars[car_name])
        if current_car.is_horizontal():
            ##Longeur de 2
            for start_x in range(MARGIN_WALL,
                                 self.board_game.width - current_car.length):  # Pour chaque position possible de cette voiture
                # place first car
                new_board = BoardGame(empty_board.strip().split('\n'))
                current_car.x = start_x
                new_board.place_car(car_name=car_name, car=current_car)
                # Place other cars
                self.place_remaining_cars(board=new_board, placed_cars=[car_name], board_games=board_games)

        else:
            for start_y in range(MARGIN_WALL,
                                 self.board_game.height - current_car.length):  # Pour chaque position possible de cette voiture
                # place first car
                new_board = BoardGame(empty_board.strip().split('\n'))
                current_car.y = start_y
                new_board.place_car(car_name=car_name, car=current_car)

                # Place other cars
                self.place_remaining_cars(board=new_board, placed_cars=[car_name], board_games=board_games)
        return board_games

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

    ### Recursif
    def place_remaining_cars(self, board: BoardGame, placed_cars: List[str], board_games: List[BoardGame]):

        if len(placed_cars) == len(self.cars.keys()):
            if board.is_all_cars_in_board(list(self.cars.keys())):
                if not state_already_found(board=board, states=board_games):
                    board_games.append(board)
                    print(board)
            else:
                raise Exception('Error in place_remaining_cars .')
            return

        for car_name, car_state in self.cars.items():  # Pour chaque Voiture
            if car_name in placed_cars:
                continue
            board_each_car = deepcopy(board)
            placed_cars_each_car = deepcopy(placed_cars)

            if car_state.is_horizontal():
                for start_x in range(MARGIN_WALL,
                                     self.board_game.width - car_state.length):  # Pour chaque position possible de cette voiture
                    # Copy the board
                    board_each_car_pos_x = deepcopy(board_each_car)
                    placed_cars_each_car_pos_x = deepcopy(placed_cars_each_car)

                    car_state.x = start_x

                    if board_each_car_pos_x.place_car_is_possible(car=car_state) and\
                       car_name not in placed_cars_each_car_pos_x:
                        board_each_car_pos_x.place_car(car_name=car_name, car=car_state)

                        placed_cars_each_car_pos_x.append(car_name)
                        self.place_remaining_cars(board=deepcopy(board_each_car_pos_x),
                                                  placed_cars=deepcopy(placed_cars_each_car_pos_x),
                                                  board_games=board_games)

            else:
                for start_y in range(MARGIN_WALL,
                                     self.board_game.height - car_state.length):  # Pour chaque position possible de cette voiture

                    # Copy the board and placed cars
                    board_each_car_pos_y = deepcopy(board_each_car)
                    placed_cars_each_car_pos_y = deepcopy(placed_cars_each_car)

                    car_state.y = start_y

                    if board_each_car_pos_y.place_car_is_possible(car=car_state) and \
                            car_name not in placed_cars_each_car_pos_y:
                        board_each_car_pos_y.place_car(car_name=car_name, car=car_state)

                        placed_cars_each_car_pos_y.append(car_name)
                        self.place_remaining_cars(board=deepcopy(board_each_car_pos_y),
                                                  placed_cars=placed_cars_each_car_pos_y, board_games=board_games)

    def apply(self, state: State, action: (str, CAR_ACTION)):

        car_name, car_action = deepcopy(action)
        cars = self.board_game.compute_cars()
        car_state = cars[car_name]

        car_name = Environment.fetch_car_name(cars=cars, car_state_to_search=car_state)

        if car_state in state.value:
            new_state = state.update(car_state=car_state, car_action=car_action)
            if new_state not in self.states and not self.game_won(state=new_state):
                raise Exception('New State is not identified .')
        else:
            raise Exception('Error car_state  not  found in  the states array')


        if self.game_won(state=new_state):
            reward = REWARD_SUCCESS
        else:
            reward = REWARD_DEFAULT

        self.board_game.remove_car(car_name=car_name)
        self.board_game.place_car(car_name=car_name, car=car_state)

        return new_state, reward

    def action_is_impossible(self, action: (str, CAR_ACTION) ):
        cars = self.board_game.compute_cars()
        car_name, car_action = action
        car_state = cars[car_name]
        x, y = self.goal


        if car_state.is_horizontal() :
            if car_action == CAR_ACTION.FORWARD :
                if x == car_state.x + car_state.length and car_state.y == y:
                    print("GAGNER")
                    return False

                return not self.board_game.position_is_empty(car_state.x + car_state.length, car_state.y)
            else:
                return not self.board_game.position_is_empty(car_state.x - 1, car_state.y)
        elif car_state.is_vertical():
            if car_action == CAR_ACTION.FORWARD:
                return not self.board_game.position_is_empty(car_state.x, car_state.y - 1)
            else:
                return not self.board_game.position_is_empty(car_state.x, car_state.y + car_state.length)
        return False


    def game_won(self, state: State):
        x, y = self.goal
        for each_car in state.value:
            if each_car.is_vertical():
                continue
            if each_car.x + each_car.length - 1 == x and \
                    y == each_car.y:
                return True
        return False
