from car_state import CarState
from enums.car_action import CAR_ACTION
from enums.direction import Direction
from copy import deepcopy

from policy import Policy


class Agent:
    def __init__(self, environment):
        self.environment = environment
        self.policy = Policy(environment.states, environment.init_actions())
        self.reset()

    def reset(self):
        self.state = self.environment.init_state
        self.previous_state = deepcopy(self.state)
        self.score = 0

    def best_action(self):
        return self.policy.best_action(self.state)

    def update_policy(self):
        self.policy.update(self.previous_state, self.state, self.last_action, self.reward)

    def do(self, action: (CarState, CAR_ACTION)):
        self.previous_state = deepcopy(self.state)
        self.state, self.reward = self.environment.apply(self.state, action)
        self.score += self.reward
        self.last_action = action

    def has_win(self):
        x , y = self.environment.goal
        for each_car in self.state.value:
            if each_car.direction == Direction.VERTICAL:
                continue
            if  each_car.x + each_car.length - 1 == x and \
                y == each_car.y :
                return True
        return False
