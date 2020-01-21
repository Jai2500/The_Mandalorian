import numpy as np

class Gamerule:
    '''
        This class decides contains all the game rules of the program
    '''

    def __init__(self, gravity):
        self.__gravity = gravity

    def simulate_physics(self, pawn, speed_boost, g_size, screen_dim):
        # print(pawn)
        pawn_vel = pawn.get_velocity()
        pawn_pos = pawn.get_position()
        pawn_vel[0] += pawn.get_mass() * self.__gravity
        if pawn_vel[0] > 0:
            pawn_vel[0] = min(pawn_vel[0], pawn.get_max_velo()[0])
        else:
            pawn_vel[0] = -min(abs(pawn_vel[0]), pawn.get_max_velo()[0])
        pawn_pos[0] += pawn_vel[0]
        pawn_vel[1] -= pawn.get_drag_coeff() * pawn_vel[1]
        if pawn_vel[1] > 0:
            pawn_vel[1] = min(pawn_vel[1] + speed_boost, pawn.get_max_velo()[1] + speed_boost)
        else:
            pawn_vel[1] = -min(abs(pawn_vel[1]) + speed_boost, pawn.get_max_velo()[1] + speed_boost)
        pawn_pos[1] += pawn_vel[1]
        pawn.set_velocity(pawn_vel)
        if pawn_pos[0] < 0:
            pawn_pos[0] = 1
        if pawn_pos[0] + pawn.get_sprite().shape[0] >= g_size:
            pawn_pos[0] = g_size - pawn.get_sprite().shape[0]

        if pawn.get_pawn_type() == 8:
            if pawn_pos[1] <= 0:
                pawn_pos[1] = 0
            elif pawn_pos[1] + pawn.get_sprite().shape[1] >= screen_dim:
                pawn_pos[1] = screen_dim - pawn.get_sprite().shape[1]
        
        pawn.set_position(pawn_pos)
        return pawn

    def set_spawn_velo(self, pawn):
        if pawn.get_pawn_type() in [6, 8]:
            pass
        elif pawn.get_pawn_type() in [1, 2, 3, 4, 5]:
            pawn_vel = pawn.get_velocity()
            pawn_vel[1] = - 1.2
            pawn.set_velocity(pawn_vel)

        return pawn
