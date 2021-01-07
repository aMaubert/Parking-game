import arcade

from agent import Agent
from board_game import BoardGame
from enums.car_color import CarColor
from enums.direction import Direction
from environment import Environment
from paramaters import SPRITE_SIZE, LEVELS, CHOOSEN_LEVEL, LEARNING_RATE, DISCOUNT_FACTOR
from qtable_coder import QTableCoder
from state import State


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

        self.sprite_cars = {}

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

        cars = self.agent.environment.board_game.compute_cars()
        for car_name, car_state in cars.items():
            if car_state.direction == Direction.HORIZONTAL:
                if car_name == CarColor.RED.value:
                    sprite = arcade.Sprite("./medias/red.png", 1)
                elif car_name == CarColor.WHITE.value:
                    sprite = arcade.Sprite("./medias/whiteRight.png", 1)
                elif car_name == CarColor.GREY.value:
                    sprite = arcade.Sprite("./medias/greyRight.png", 1)
                elif car_name == CarColor.BLUE.value:
                    sprite = arcade.Sprite("./medias/blueRight.png", 1)
                elif car_name == CarColor.YELLOW.value:
                    sprite = arcade.Sprite("./medias/yellowRight.png", 1)
                elif car_name == CarColor.BLACK.value:
                    sprite = arcade.Sprite("./medias/blackRight.png", 1)
                sprite.width = car_state.length * SPRITE_SIZE
                sprite.height = SPRITE_SIZE
            else:
                if car_name == CarColor.WHITE.value:
                    sprite = arcade.Sprite("./medias/whiteUp.png", 1)
                elif car_name == CarColor.GREY.value:
                    sprite = arcade.Sprite("./medias/greyUp.png", 1)
                elif car_name == CarColor.BLUE.value:
                    sprite = arcade.Sprite("./medias/blueUp.png", 1)
                elif car_name == CarColor.YELLOW.value:
                    sprite = arcade.Sprite("./medias/yellowUp.png", 1)
                elif car_name == CarColor.BLACK.value:
                    sprite = arcade.Sprite("./medias/blackUp.png", 1)
                sprite.width = SPRITE_SIZE
                sprite.height = car_state.length * SPRITE_SIZE
            sprite.center_x = car_state.x * SPRITE_SIZE + sprite.width * 0.5
            sprite.center_y = self.height - (car_state.y * SPRITE_SIZE + sprite.height * 0.5)

            self.sprite_cars[car_name] = sprite
            self.cars.append(sprite)

        self.goal = arcade.Sprite("./medias/Finish.png", 0.5)
        self.goal.center_x = self.agent.environment.goal[0] * self.goal.width + self.goal.width * 46.3
        self.goal.center_y = self.height - (self.agent.environment.goal[1] * self.goal.width + self.goal.width * 23.3)

    def update_cars(self, action):
        car_name, car_action = action
        sprite = self.sprite_cars.get(car_name)
        if not agent.has_win():
            cars = self.agent.environment.board_game.compute_cars()
            car_state = cars[car_name]

            sprite.center_x = car_state.x * SPRITE_SIZE + sprite.width * 0.5
            sprite.center_y = self.height - (car_state.y * SPRITE_SIZE + sprite.height * 0.5)
        else:
            x, y = self.agent.environment.goal
            sprite.center_x = x * SPRITE_SIZE + sprite.width * 0.5
            sprite.center_y = self.height - (y * SPRITE_SIZE + sprite.height * 0.5)

    def on_update(self, delta_time):

        if not agent.has_win():
            action = self.agent.best_action()
            self.agent.do(action)
            self.agent.update_policy()
            # Rafraichir l'affichage de la voiture qui a bougé
            self.update_cars(action=action)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.agent.reset()
            self.agent.environment.board_game = BoardGame(board_game=LEVELS[CHOOSEN_LEVEL].strip().split('\n'))
            self.setup()

    def on_draw(self):
        arcade.start_render()
        self.walls.draw()
        self.ground.draw()
        self.goal.draw()
        self.cars.draw()
        arcade.draw_text(f"Score: {self.agent.score}", 10, 10, arcade.csscolor.WHITE, 20)
        arcade.draw_text(f"Tentatives: {self.agent.tries}", 200, 10, arcade.csscolor.WHITE, 20)
        if self.agent.has_win():
            arcade.draw_text(f"Pour relancer, pressez 'R'.", 10,
                             (agent.environment.board_game.width * SPRITE_SIZE) - 40, arcade.csscolor.WHITE, 20)
            # TODO save the Q-Table
            self.agent.policy.save_table()


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

if __name__ == '__main__':

    table_coder = QTableCoder(LEARNING_RATE, DISCOUNT_FACTOR)
    loaded_qtable = None
    states = None
    if table_coder.is_chargeable():
        loaded_qtable = table_coder.load_table()
        states = State.init_from_qtable(loaded_qtable)


    # Initialiser l'environment
    environment = Environment(board=LEVELS[CHOOSEN_LEVEL], states=states)
    # Initialiser l'agent
    agent = Agent(environment, qtable=loaded_qtable)

    window = Window(agent)
    window.setup()
    arcade.run()
