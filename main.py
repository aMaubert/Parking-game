import arcade

from agent import Agent
from enums.direction import Direction
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
#      #
#      #
# aa b *
# d  b #
# d  b #
# d ccc#
########
""", """
########
#ccc d #
#    d #
#    d *
#bbb   #
#  e gg#
#  e hh#
########
"""]

SPRITE_SIZE = 64


class Window(arcade.Window):

    def __init__(self, agent):
        super().__init__(agent.environment.board_game.width * SPRITE_SIZE,
                         agent.environment.board_game.height * SPRITE_SIZE,
                         'Escape from Parking')
        self.agent = agent
        arcade.set_background_color(arcade.csscolor.DARK_BLUE)

    def setup(self):
        self.walls = arcade.SpriteList()
        self.cars = arcade.SpriteList()
        self.ground = arcade.SpriteList()
        for row in range(self.agent.environment.board_game.height):
            for column in range(self.agent.environment.board_game.width):
                if self.agent.environment.board_game.is_wall(x=column, y=row):
                    if row == 0 and column == 0:
                        sprite = arcade.Sprite("./medias/grassTileDownRight.png", 0.5)
                    elif row == 0 and column == self.agent.environment.board_game.width - 1:
                        sprite = arcade.Sprite("./medias/grassTileDownLeft.png", 0.5)
                    elif row == self.agent.environment.board_game.height - 1 and column == 0:
                        sprite = arcade.Sprite("./medias/grassTileTopRight.png", 0.5)
                    elif row == self.agent.environment.board_game.height - 1 and column == self.agent.environment.board_game.width - 1:
                        sprite = arcade.Sprite("./medias/grassTileTopLeft.png", 0.5)
                    elif row == 0:
                        sprite = arcade.Sprite("./medias/grassTileDown.png", 0.5)
                    elif row == self.agent.environment.board_game.height - 1:
                        sprite = arcade.Sprite("./medias/grassTileUp.png", 0.5)
                    elif column == 0:
                        sprite = arcade.Sprite("./medias/grassTileRight.png", 0.5)
                    elif column == self.agent.environment.board_game.width - 1:
                        sprite = arcade.Sprite("./medias/grassTileLeft.png", 0.5)
                    sprite.center_x = column * SPRITE_SIZE + SPRITE_SIZE * 0.5
                    sprite.center_y = self.height - (row * SPRITE_SIZE + SPRITE_SIZE * 0.5)
                    self.walls.append(sprite)
                else:
                    sprite = arcade.Sprite("./medias/groundTile.png", 0.5)
                    sprite.center_x = column * SPRITE_SIZE + SPRITE_SIZE * 0.5
                    sprite.center_y = self.height - (row * SPRITE_SIZE + SPRITE_SIZE * 0.5)
                    self.ground.append(sprite)

        # Sprite size : 64.
        for car_state in self.agent.environment.current_state.value:
            print("car : " + str(car_state))
            if car_state.direction == Direction.HORIZONTAL:
                if car_state.length == 2:
                    sprite = arcade.Sprite("./medias/minicarYellowRight.png", 1)
                elif car_state.length == 3:
                    sprite = arcade.Sprite("./medias/pickupGrayRight.png", 1)
                elif car_state.length == 4:
                    sprite = arcade.Sprite("./medias/touringcarWhiteRight.png", 1)
                sprite.width = car_state.length * SPRITE_SIZE
                sprite.height = SPRITE_SIZE
            else:
                if car_state.length == 2:
                    sprite = arcade.Sprite("./medias/minicarYellowUp.png", 1)
                elif car_state.length == 3:
                    sprite = arcade.Sprite("./medias/pickupGrayUp.png", 1)
                elif car_state.length == 4:
                    sprite = arcade.Sprite("./medias/touringcarWhiteUp.png", 1)
                sprite.width = SPRITE_SIZE
                sprite.height = car_state.length * SPRITE_SIZE
            sprite.center_x = car_state.x * SPRITE_SIZE + sprite.width * 0.5
            sprite.center_y = self.height - (car_state.y * SPRITE_SIZE + sprite.height * 0.5)
            self.cars.append(sprite)

        self.goal = arcade.Sprite("./medias/Finish.png", 0.5)
        self.goal.center_x = self.agent.environment.goal[0] * self.goal.width + self.goal.width * 46.3
        self.goal.center_y = self.height - (self.agent.environment.goal[1] * self.goal.width + self.goal.width * 23.3)

    def update_player(self):
        pass

    def on_update(self, delta_time):
        pass

    def on_draw(self):
        arcade.start_render()
        self.walls.draw()
        self.ground.draw()
        self.goal.draw()
        self.cars.draw()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Initialiser l'environment
    environment = Environment(board=LEVELS[1])

    # Initialiser l'agent
    agent = Agent(environment)

    print(environment.goal)
    window = Window(agent)
    window.setup()
    arcade.run()

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
