from enums.direction import Direction


class Agent:
    def __init__(self, environment):
        self.environment = environment

    def best_action(self):
        pass

    def update_policy(self):
        pass

    def has_win(self):
        x , y = self.environment.goal
        for each_car in self.environment.current_state.value:
            if each_car.direction == Direction.VERTICAL:
                continue
            if  each_car.x + each_car.length - 1 == x and \
                y == each_car.y :
                return True
        return False
