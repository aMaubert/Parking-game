
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
from state import State


class Policy:  # Q-table
    def __init__(self, states: List[State], actions, learning_rate = 0.1, discount_factor = 0.5):
        self.table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        for s in states:
            state = tuple([ (each_car_state.x, each_car_state.y, each_car_state.direction, each_car_state.length) for each_car_state in s.value ])
            self.table[state] = {}
            for a in actions:
                self.table[state][a] = 0

    def best_action(self, state: State):
        #TODO implement method

        #Here is a mocked value
        return state.value[0], CAR_ACTION.FORWARD

    def update(self, previous_state: State, state: State, last_action: CAR_ACTION, reward: int):
        #TODO implement this method
        pass
