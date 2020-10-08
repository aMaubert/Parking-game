# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import arcade

LEVELS = ["""
########
#ccc d #
#    d #
# aa d *
#bbbf  #
#  efgg#
#  e hh#
########
""", """
########
#    d #
#    d #
# aa d *
#      #
#      #
#      #
########
"""]

FORWARD = 'FORWARD'
BACKWARD = 'BACKWARD'

VERTICAL = 'VERTICAL'
HORIZONTAL = 'HORIZONTAL'

ACTIONS_BY_CAR = [FORWARD, BACKWARD]


class CarState:

    def __init__(self, x, y, direction, length):
        self.x = x,
        self.y = y
        self.direction = direction
        self.length = length

    def __repr__(self):
        return 'x :' + str(self.x) + ',y : ' + str(self.y) + ' ,direction' + str(self.direction) + \
               ', length : ' + str(self.length)


ACTIONS = {('a', FORWARD): -1, ('a', BACKWARD): -1}  # Pour chaque voiture

State1 = (CarState(x=0, y=0, direction=VERTICAL, length=2), CarState(x=0, y=1, direction=VERTICAL, length=2))
State2 = (CarState(x=0, y=1, direction=VERTICAL, length=2), CarState(x=0, y=1, direction=VERTICAL, length=2))

q_table = {State1: ACTIONS}

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
#                                                                                                  Voiture A Avance   Voiture A recule  ...  Voiture Z Avance   Voiture Z recule  (NbCAR * Actions par voiture)
#  ((y,x,D,L),(y,x,D,L),(y,x,D,L),(y,x,D,L),(y,x,D,L),(y,x,D,L),(y,x,D,L),(y,x,D,L),(y,x,D,L))
#  (CarState, CarState, CarState, CarState)
#
#  1state = (CarState x NbCar)


REWARD_IMPOSSIBLE = -1000000
REWARD_SUCCESS = 1000000


#
# Une voiture c'est:
#   - une position de départ (x,y)
#   - Une direction (Horizontal / Vertical)
#   - une taille
#
# Une Action :
#   - Sélection d'une voiture (a,b,c, etc...)
#   - on l'Avance (vers le heut si voiture Vertical sinon vers la droite) ou
#         Recule (vers le bas sir voiture Vertical, sinon vers la gauche)
#
# Condition de Victoire du JEU :
#       La voiture 'A' à franchie la sortie (La sortie correspond au caractère '*' en haut)
#


class Environment:
    def __init__(self):
        self.states = {}
        lines = LEVELS[1].strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0])

        for row in range(self.height):
            for col in range(len(lines[row])):
                self.states[(row, col)] = lines[row][col]
                if lines[row][col] == '*':
                    self.goal = (row, col)
        print("self.states ", self.states)


SPRITE_SIZE = 64


class Agent:
    def __init__(self, environment):
        self.environment = environment

    def best_action(self):
        pass

    def update_policy(self):
        pass


class Window(arcade.Window):

    def __init__(self, agent):
        super().__init__(agent.environment.width * SPRITE_SIZE,
                         agent.environment.height * SPRITE_SIZE,
                         'Escape from Parking')
        self.agent = agent
        arcade.set_background_color(arcade.csscolor.DARK_BLUE)

    def setup(self):
        self.walls = arcade.SpriteList()
        self.cars = arcade.SpriteList()
        for state in self.agent.environment.states:
            print(state, self.agent.environment.states[state])
            if self.agent.environment.states[state] == '#':
                sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.5)
                sprite.center_x = state[1] * SPRITE_SIZE + SPRITE_SIZE * 0.5
                sprite.center_y = self.height - (state[0] * SPRITE_SIZE + SPRITE_SIZE * 0.5)
                self.walls.append(sprite)
            elif 'a' <= self.agent.environment.states[state] <= 'z':
                sprite = arcade.Sprite(":resources:images/space_shooter/playerShip2_orange.png", 0.5)
                sprite.center_x = state[1] * SPRITE_SIZE + SPRITE_SIZE * 0.5
                sprite.center_y = self.height - (state[0] * SPRITE_SIZE + SPRITE_SIZE * 0.5)
                self.cars.append(sprite)

        self.goal = arcade.Sprite(":resources:images/items/flagGreen1.png", 0.5)
        self.goal.center_x = self.agent.environment.goal[1] * self.goal.width + self.goal.width * 0.5
        self.goal.center_y = self.height - (self.agent.environment.goal[0] * self.goal.width + self.goal.width * 0.5)

    def update_player(self):
        pass

    def on_update(self, delta_time):
        pass

    def on_draw(self):
        arcade.start_render()
        self.walls.draw()
        self.goal.draw()
        self.cars.draw()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    environment = Environment()
    agent = Agent(environment)

    window = Window(agent)
    window.setup()
    arcade.run()

#
# Systeme de score proposition :
#
#   Dans le cas où une voitur sort du décor (position x,y == '#' ) : -100 points
#   Dans le cas où la voiture 'A' à franchie la sortie (position x,y == '*' ) : +100 points
#   Dans le cas où l'on est sur une case voiture (b,c,d,etc...) qui n'est pas la Voiture 'A':
#         - si les case voiture sont à l'extremité on perd moin de points que les case au centres
#         - Si les case de la voiture 'A' sont
#         #############################################################
#         #        ##        # #        ##        ##        ##        #
#         # -5pts  ## -10pts # # -15pts ## -15pts ## -10pts ## -5pts  #
#         #        ##        # #        ##        ##        ##        #
#         #############################################################
#         #        ##        # #        ##        ##        ##        #
#         # -10pts ## -15pts # # -20pts ## -20pts ## -15pts ## -10pts #
#         #        ##        # #        ##        ##        ##        #
#         #############################################################
#         #        ##        # #        ##        ##        ##
#         # -15pts ## -20pts # # -25pts ## -25pts ## -20pts ## -15pts    => GOAL
#         #        ##        # #        ##        ##        ##
#         #############################################################
#         #        ##        # #        ##        ##        ##        #
#         # -15pts ## -20pts # # -25pts ## -25pts ## -20pts ## -15pts #
#         #        ##        # #        ##        ##        ##        #
#         #############################################################
#         #        ##        # #        ##        ##        ##        #
#         # -10pts ## -15pts # # -20pts ## -20pts ## -15pts ## -10pts #
#         #        ##        # #        ##        ##        ##        #
#         #############################################################
#         #        ##        # #        ##        ##        ##        #
#         # -5pts  ## -10pts # # -15pts ## -15pts ## -10pts ## -5pts  #
#         #        ##        # #        ##        ##        ##        #
#         #############################################################
#
#
#
