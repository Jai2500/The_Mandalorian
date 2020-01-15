import numpy as np

class Gamerule:
    '''
        This class decides contains all the game rules of the program
    '''

    def __init__(self, gravity):
        self.gravity = gravity

    def simulate_physics(self, pawn):
        pawn.position[0] += pawn.velocity[0]
        pawn.velocity[0] += pawn.mass * self.gravity
        pawn.position[1] += pawn.velocity[1]
        pawn.velocity[1] += ((-1)**(pawn.velocity[1] > 0)) * pawn.drag_coeff \
            * pawn.velocity[1]

        return pawn
