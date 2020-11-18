from enums.direction import Direction


class Agent:
    def __init__(self, environment):
        self.environment = environment

    def reset(self):
        self.state = self.environment.init_state
        self.previous_state = self.state
        self.score = 0

    def best_action(self):
        #return self.policy.best_action(self.state)
        pass

    def update_policy(self):
        pass

    def do(self, action):
        self.previous_state = self.state
        #self.state
        #self.reward
        self.score += self.reward
        self.last_action = action

    def has_win(self):
        x , y = self.environment.goal
        for each_car in self.environment.current_state.value:
            if each_car.direction == Direction.VERTICAL:
                continue
            if  each_car.x + each_car.length - 1 == x and \
                y == each_car.y :
                return True
        return False
