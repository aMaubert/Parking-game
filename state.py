from car_state import CarState


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
