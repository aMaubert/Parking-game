
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


class Policy:  # Q-table
    def __init__(self):
        pass
