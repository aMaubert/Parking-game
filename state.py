from car_state import CarState
from enums.car_action import CAR_ACTION


class State:

    def __init__(self, state: tuple):
        self.value = state

    def __repr__(self):
        ret = "State("
        for each_car_state in self.value:
            ret += f"(x={each_car_state.x}, y={each_car_state.y}, direction={each_car_state.direction}, length={each_car_state.length})\t"
        ret += ")\n"
        return ret

    @staticmethod
    def from_cars(cars: {str: CarState}):
        state = []
        for each_car, each_car_state in cars.items():
            state.append(each_car_state)
        return State(state=tuple(state))

    @staticmethod
    def init_from_qtable(qtable):
        states = []
        for each_state_tuple in qtable:
            car_states = []
            for each_car_state_tuple in each_state_tuple:
                print(each_car_state_tuple, type(each_car_state_tuple))
                x = each_car_state_tuple[0]
                y = each_car_state_tuple[1]
                direction = each_car_state_tuple[2]
                length = each_car_state_tuple[3]
                car_states.append(CarState(x=x, y=y, direction=direction, length=length))
            states.append(State(state=tuple(car_states)))
        return states

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

    def contains(self, car: CarState):
        for each in self.value:
            if each == car:
                return True
        return False
        pass

    def update(self, car_state: CarState, car_action: CAR_ACTION):
        index_car = self.value.index(car_state)

        cars_list = list(self.value)

        car_state.update(action=car_action)

        cars_list[index_car] = car_state

        self.value = tuple(cars_list)
        return self

    def encode(self):
        return tuple(
            [(each_car_state.x, each_car_state.y, each_car_state.direction, each_car_state.length) for each_car_state in
             self.value])
