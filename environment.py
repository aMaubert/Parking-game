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


class CarState:

    def __init__(self, x, y, direction, length):
        self.x = x,
        self.y = y
        self.direction = direction
        self.length = length

    def __repr__(self):
        return 'x :' + str(self.x) + ',y : ' + str(self.y) + ' ,direction' + str(self.direction) + \
               ', length : ' + str(self.length)


State1 = (CarState(x=0, y=0, direction=VERTICAL, length=2), CarState(x=0, y=1, direction=VERTICAL, length=2))
State2 = (CarState(x=0, y=1, direction=VERTICAL, length=2), CarState(x=0, y=1, direction=VERTICAL, length=2))


### Environnment => Positions de chaques voiture sur le plateau
class Environment:
    def __init__(self):
        self.states = {}
        lines = LEVELS[0].strip().split('\n')
        self.height = len(lines)
        self.width = len(lines[0])

        for row in range(self.height):
            for col in range(len(lines[row])):  ## On s'occupe pas des rebords # ni du *
                self.states[(row, col)] = lines[row][col]
                if lines[row][col] == '*':
                    self.goal = (row, col)
        print("self.states ", self.states)
