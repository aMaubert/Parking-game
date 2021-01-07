# Q-table
#        U  D    L   R
# (0, 0) 6  -7   10  20
# (0, 1) 15 -100  5
#    :
# (5, 10)

# Q-table
#
#
#   Actions de base : Avancé et Reculé
#
#    (y,x,D,L)
#    Class CarState :
#        y: number
#        x: Number
#        direction:
#        Longueur:

#
#  Voiture A Avance   Voiture A recule  ...  Voiture Z Avance   Voiture Z recule  (NbCAR * Actions par voiture)
#  ((y,x,D,L),(y,x,D,L),(y,x,D,L),(y,x,D,L),(y,x,D,L),(y,x,D,L),(y,x,D,L),(y,x,D,L),(y,x,D,L))
#  (CarState, CarState, CarState, CarState)
#
#  1state = (CarState x NbCar)
from typing import List

from enums.car_action import CAR_ACTION
from paramaters import LEARNING_RATE, DISCOUNT_FACTOR
from qtable_coder import QTableCoder
from state import State


class Policy:  # Q-table
    def __init__(self, states: List[State], actions, qtable, learning_rate=LEARNING_RATE, discount_factor=DISCOUNT_FACTOR):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.actions = actions

        if qtable is not None :
            self.table = qtable
        else:
            self.init_table(states=states, actions=actions)

        self.table_coder = QTableCoder(self.learning_rate, self.discount_factor)

    def best_action(self, state: State):
        action = None
        for a in self.table[state.encode()]:
            if action is None or self.table[state.encode()][a] > self.table[state.encode()][action]:
                action = a

        return action

    def update(self, previous_state: State, state: State, last_action: (str, CAR_ACTION), reward: int):
        # Q(st, at) = Q(st, at) + learning_rate * (reward + discount_factor * max(Q(state)) - Q(st, at))
        # maxQ = max(self.table[state].values()
        # )

        if not state.encode() in self.table.keys():
            self.table[state.encode()] = {}
            for a in self.actions:
                self.table[state.encode()][a] = 0
        maxQ = max(self.table[state.encode()].values())
        self.table[previous_state.encode()][last_action] += self.learning_rate * \
                                                            (reward + self.discount_factor * maxQ -
                                                             self.table[previous_state.encode()][last_action])

    def init_table(self, states: List[State], actions):
        self.table = {}

        for s in states:
            state = tuple([(each_car_state.x, each_car_state.y, each_car_state.direction, each_car_state.length) for
                           each_car_state in s.value])
            self.table[state] = {}
            for a in actions:
                self.table[state][a] = 0

    def save_table(self):
        self.table_coder.save_table(self.table)

