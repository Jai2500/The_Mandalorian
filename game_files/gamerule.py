import numpy as np


class Gamerule:
    '''
        This class decides contains all the game rules of the program
    '''

    def __init__(self, gravity, drag_coeff):
        self.gravity = gravity
        self.drag_coeff = drag_coeff

    def simulate_physics(self, pawn):
        pawn.velocity[0] += pawn.mass * self.gravity
        pawn.position[0] += pawn.velocity[0]
        return pawn
