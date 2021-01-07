


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
#     c#
#     c#
# aa  c*
#    b #
#    b #
#    b #
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
#   d  #
#   d  #
# aadb *
#    b #
#    b #
# ccc  #
########
""", """
########
#ccc d #
#    d #
#aa  d *
#bbb   #
#  e   #
#  e   #
########
""","""
########
#ccc d #
#    d #
#aa  d *
#   bbb#
#  e   #
#  e   #
########
"""]

CHOOSEN_LEVEL = 2

SPRITE_SIZE = 64


REWARD_IMPOSSIBLE = -100000000
REWARD_SUCCESS = 500
REWARD_DEFAULT = -1

LEARNING_RATE = 1
DISCOUNT_FACTOR = 0.5