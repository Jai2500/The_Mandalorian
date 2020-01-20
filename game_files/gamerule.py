import numpy as np

class Gamerule:
    '''
        This class decides contains all the game rules of the program
    '''

    def __init__(self, gravity):
        self.gravity = gravity

    def simulate_physics(self, pawn, speed_boost, g_size, screen_dim):
        # print(pawn)
        pawn.velocity[0] += pawn.mass * self.gravity
        if pawn.velocity[0] > 0:
            pawn.velocity[0] = min(pawn.velocity[0], pawn.max_velo[0])
        else:
            pawn.velocity[0] = -min(abs(pawn.velocity[0]), pawn.max_velo[0])
        pawn.position[0] += pawn.velocity[0]
        pawn.velocity[1] -= pawn.drag_coeff * pawn.velocity[1]
        if pawn.velocity[1] > 0:
            pawn.velocity[1] = min(pawn.velocity[1] + speed_boost, pawn.max_velo[1] + speed_boost)
        else:
            pawn.velocity[1] = -min(abs(pawn.velocity[1]) + speed_boost, pawn.max_velo[1] + speed_boost)
        pawn.position[1] += pawn.velocity[1]
        if pawn.position[0] < 0:
            pawn.position[0] = 1
        if pawn.position[0] + pawn.sprite.shape[0] >= g_size:
            pawn.position[0] = g_size - pawn.sprite.shape[0]

        if pawn.pawn_type == 8:
            if pawn.position[1] <= 0:
                pawn.position[1] = 0
            elif pawn.position[1] + pawn.sprite.shape[1] >= screen_dim:
                pawn.position[1] = screen_dim - pawn.sprite.shape[1]

        return pawn

    def set_spawn_velo(self, pawn):
        if pawn.pawn_type in [6, 8]:
            pass
        elif pawn.pawn_type in [1, 2, 3, 4, 5]:
            pawn.velocity[1] = - 1.2

        return pawn
