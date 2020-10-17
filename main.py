import arcade

from agent import Agent
from environment import Environment


REWARD_IMPOSSIBLE = -1000000
REWARD_SUCCESS = 1000000

####
#  Definitions
####
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


SPRITE_SIZE = 64


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

    # window = Window(agent)
    # window.setup()
    # arcade.run()

    # # Initialiser l'environment
    # environment = Environment(MAZE)
    #
    # # Initialiser l'agent
    # agent = Agent(environment)
    #
    # # Boucle principale
    # # Tant que l'agent n'est pas sorti du labyrinthe
    # step = 1
    # while agent.state != environment.goal:
    #     # for step in range(10):
    #     # Choisir la meilleure action de l'agent
    #     action = agent.best_action()
    #
    #     # Obtenir le nouvel état de l'agent et sa récompense
    #     agent.do(action)
    #     print('#', step, 'ACTION:', action, 'STATE:', agent.previous_state, '->', agent.state, 'SCORE:', agent.score)
    #     step += 1
    #
    #     # A partir de St, St+1, at, rt+1, on met à jour la politique (policy, q-table, etc.)
    #     agent.update_policy()

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
