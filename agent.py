from car_state import CarState
from enums.car_action import CAR_ACTION
from enums.direction import Direction
from copy import deepcopy

from environment import REWARD_IMPOSSIBLE
from policy import Policy
from state import State


class Agent:
    def __init__(self, environment):
        self.environment = environment
        self.policy = Policy(environment.states, environment.init_actions())
        self.init_state = deepcopy(environment.init_state.value)
        self.tries = 0
        self.reset()

    def reset(self):
        self.state = State(state=self.init_state)
        print(self.init_state)
        self.previous_state = deepcopy(self.state)
        self.score = 0
        self.tries += 1

    def best_action(self):
        action = self.policy.best_action(self.state)
        count = 0
        while self.environment.action_is_impossible(action=action):
            self.policy.table[self.state.encode()][action] = REWARD_IMPOSSIBLE

            # if count == 500:
            #     print("count ", count)
            #     exit(1)
            # count += 1

            action = self.policy.best_action(self.state)
        print(action)
        print(self.environment.board_game)
        return action

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
