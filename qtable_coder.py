from car_state import CarState
from enums.car_action import CAR_ACTION
from enums.direction import Direction
from paramaters import CHOOSEN_LEVEL, REWARD_SUCCESS, REWARD_IMPOSSIBLE, REWARD_DEFAULT
from os import path

from state import State


class QTableCoder:

    def __init__(self, learning_rate, discount_factor):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

    def is_chargeable(self):
        return path.isfile(self.file_name())

    def file_name(self):
        return 'tables/QTable_' + str(CHOOSEN_LEVEL) + '&' \
               + str(REWARD_SUCCESS) + '&' \
               + str(REWARD_IMPOSSIBLE) + '&' \
               + str(REWARD_DEFAULT) + '&' \
               + str(self.learning_rate) + '&' \
               + str(self.discount_factor) + '.txt'

    def save_table(self, table):
        f = open(self.file_name(), "w")
        for each_state, actions in table.items():
            f.write(str(each_state) + ":" + str(actions) + "\n")
        f.close()

    def load_table(self):
        table = {}
        f = open(self.file_name(), "r")

        for line in f:
            [key, value] = line.split(':', 1)
            state = self.decode_state(key)
            actions_and_reward = self.decode_rewards(value)
            table[state] = {}
            table[state] = actions_and_reward

        f.close()

        return table

    def decode_state(self, key: str):
        key = key.replace('(', '').replace(')', '')
        key = key.split(', ')
        cars_states = []
        while len(key) > 0 :
            try:
                x = int(key[0])
                y = int(key[1])
                direction = Direction(key[2])
                car_length = int(key[3])
                cars_states.append(CarState(x=x, y=y,direction=direction, length=car_length))
                key = key[4:]
            except:
                print('Wrong format')
                exit(1)
        state = State(state=tuple(cars_states))
        return state.encode()


    def decode_rewards(self, value):
        value = value.replace('{', '').replace('}', '').replace(', (',';(')
        res = {}
        for each_action_and_reward in value.split(';'):
            [car_with_action, reward] = each_action_and_reward.replace('(', '').replace(')', '').split(': ')
            [car_name, action] = car_with_action.split(', ')
            action = (car_name.replace("'", ""), CAR_ACTION(action) )
            res[action] = int(float(reward.strip()))

        return res