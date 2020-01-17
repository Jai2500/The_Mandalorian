import numpy as np

class Gamerule:
    '''
        This class decides contains all the game rules of the program
    '''

    def __init__(self, gravity):
        self.gravity = gravity

    def simulate_physics(self, pawn):
        # print(pawn)
        pawn.velocity[0] += pawn.mass * self.gravity + ((-1)**(pawn.velocity[0] > 0)) * pawn.drag_coeff \
            * pawn.velocity[0]
        if pawn.velocity[0] > 0:
            pawn.velocity[0] = min(pawn.velocity[0], 1)
        else:
            pawn.velocity[0] = -min(abs(pawn.velocity[0]), 1)
        pawn.position[0] += pawn.velocity[0]
        pawn.velocity[1] += ((-1)**(pawn.velocity[1] > 0)) * pawn.drag_coeff \
            * pawn.velocity[1]
        pawn.position[1] += pawn.velocity[1]
        # if pawn.pawn_type == 1:
        #     print(pawn.velocity, pawn.position)
        return pawn

    def simulate_force(self, pawn, force):
        pass
