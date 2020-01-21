import numpy as np
from datetime import datetime


class Pawn:
    def __init__(self, sprite, position, obj_number, mass=0, pawn_type=0,
                 lives=1, drag_coeff=0.0, is_solid=True, max_velo=[5, 5]):
        self._mass = mass
        self._sprite = sprite
        self._velocity = np.array([0, 0], dtype=np.float64)
        self._collision_box = self.create_collision_box(sprite)
        self._position = np.array(position, dtype=np.float64)
        self._obj_number = obj_number
        self._pawn_type = pawn_type
        self._to_delete = False
        self._lives = lives
        self._drag_coeff = drag_coeff
        self._is_solid = is_solid
        self._max_velo = max_velo

    def get_mass(self):
        return self._mass

    def get_sprite(self):
        return self._sprite

    def get_velocity(self):
        return self._velocity

    def set_velocity(self, velocity):
        self._velocity = velocity

    def get_collision_box(self):
        return self._collision_box

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position

    def get_obj_number(self):
        return self._obj_number

    def get_pawn_type(self):
        return self._pawn_type

    def get_to_delete(self):
        return self._to_delete

    def get_lives(self):
        return self._lives

    def get_drag_coeff(self):
        return self._drag_coeff

    def get_is_solid(self):
        return self._is_solid

    def get_max_velo(self):
        return self._max_velo

    def set_to_delete(self, to_delete):
        self._to_delete = to_delete

    def create_collision_box(self, obj_shape):
        collision_box = obj_shape != ' '
        return collision_box

    def check_collision(self, out_arr, collision_box_size):
        overlap_box = self._collision_box[:, collision_box_size[0]:collision_box_size[1]] * out_arr
        if np.sum(overlap_box) > 0:
            return True, self._position, self._velocity
        else:
            return False, self._position, self._velocity

    def on_trigger(self, pawn):
        pass

    def on_collision(self, other):
        return "The object has collided"

    def die(self):
        self._lives -= 1
        if self._lives <= 0:
            self._to_delete = True


class Actor(Pawn):

    def check_collision(self, out_arr, collision_box_size):
        # print(out_arr.shape)
        overlap_box = self._collision_box[:, collision_box_size[0]:collision_box_size[1]] * out_arr

        # Version 1.2 based on the Z-index
        # Possible issues: -- Way to compare the Z-index

        if np.sum(overlap_box) > 0:
            mpv = np.array([10000, 10000])
            if self._velocity[0] > 0.0:
                row_sums = np.sum(overlap_box, axis=1)
                non_zero = np.nonzero(row_sums)[0]
                if non_zero.size > 0:
                    mpv[0] = -1 * (self._sprite.shape[0] -
                                   np.min(non_zero))
            elif self._velocity[0] < 0.0:
                row_sums = np.sum(overlap_box, axis=1)
                non_zero = np.nonzero(row_sums)[0]
                if non_zero.size > 0:
                    mpv[0] = np.max(non_zero)

            if self._velocity[1] > 0.0:
                col_sums = np.sum(overlap_box, axis=0)
                non_zero = np.nonzero(col_sums)[0]
                if non_zero.size > 0:
                    mpv[1] = -1 * np.max(non_zero)
            elif self._velocity[1] < 0.0:
                col_sums = np.sum(overlap_box, axis=0)
                non_zero = np.nonzero(col_sums)[0]
                if non_zero.size > 0:
                    mpv[1] = self._sprite.shape[1] - np.min(non_zero)

        # if np.sum(overlap_box) > 0:
        #     mpv = np.array([0, 0])
        #     row_sums = np.sum(overlap_box, axis=1)
        #     non_zero = np.nonzero(row_sums)[0]
        #     if non_zero.size > 0:
        #         met_a = self.sprite.shape[0] - np.min(non_zero)
        #         met_b = np.max(non_zero)
        #         if met_a < met_b:
        #             mpv[0] = - met_a
        #         else:
        #             mpv[0] =  met_b

        #     col_sums = np.sum(overlap_box, axis=0)
        #     non_zero = np.nonzero(col_sums)[0]
        #     if non_zero.size > 0:
        #         met_a = self.sprite.shape[1] - np.min(non_zero)
        #         met_b = np.max(non_zero)
        #         if met_a < met_b:
        #             mpv[1] = met_a
        #         else:
        #             mpv[1] = - met_b

            # print(mpv, "MPV")
            if abs(mpv[0]) < abs(mpv[1]):
                mpv[1] = 0
            elif abs(mpv[1]) < abs(mpv[0]):
                mpv[0] = 0
            elif mpv[0] == 10000 and mpv[1] == 10000:
                mpv[0] = 0
                mpv[1] = 0
            # print(mpv) 

        # if np.sum(overlap_box) > 0:
        #     mpv = np.array([0,0])
        #     if self.velocity[0] != 0:
        #         row_sums = np.sum(overlap_box, axis = 1)
        #         non_zero = np.nonzero(row_sums)[0]

            new_position = self._position + mpv
            new_velocity = self._velocity - (mpv != 0) * self._velocity
            # if self.pawn_type == 1:
            #     print(new_velocity, "After collision")
            return True, new_position, new_velocity

        return False, self._position, self._velocity


class Character(Actor):

    def __init__(self, sprite, position, obj_number, mass=0, pawn_type=0,
                 lives=1, drag_coeff=0.3, is_solid=True, shield_sprite = None):
        super().__init__(sprite, position, obj_number, mass, pawn_type, lives,
                         drag_coeff, is_solid, max_velo=[2, 2])
        self.__shield_active = False
        self.__normal_sprite = self._sprite
        self.__curr_lives = self._lives
        self.__normal_collision_box = self.create_collision_box(self.__normal_sprite)
        self.__timestamp = datetime.now()
        if shield_sprite is None:
            self.__shield_sprite = np.array([['O' for i in range(self._sprite.shape[1] + 2)] for j in range(self.get_sprite().shape[0] + 2)])
            self.__shield_sprite[1:1 + self._sprite.shape[0], 1:self._sprite.shape[1] + 1] = self.get_sprite()
        else:
            self.__shield_sprite = shield_sprite
        self.__shield_collision_box = self.create_collision_box(self.__shield_sprite)
        self.__score = 0

    def get_shield_active(self):
        return self.__shield_active

    def get_timestamp(self):
        return self.__timestamp

    def get_score(self):
        return self.__score

    def set_score(self, score):
        self.__score = score

    def activate_shield(self):
        if self.__shield_active is True:
            return

        now = datetime.now()
        if (now - self.__timestamp).seconds > 5:
            self.__shield_active = True
            self._sprite = self.__shield_sprite 
            self._collision_box = self.__shield_collision_box
            self.__timestamp = now
            self.__curr_lives = self._lives
            self._lives = 100000000
            return

    def deactivate_shield(self):
        if self.__shield_active is False:
            return

        self.__shield_active = False
        self._sprite = self.__normal_sprite
        self._collision_box = self.__normal_collision_box
        self.__timestamp = datetime.now()
        self._lives = self.__curr_lives
        return

    def control(self, inp):
        if inp == 'w':
            self._velocity[0] -= 2
        elif inp == 'a':
            self._velocity[1] -= 1
        elif inp == 'd':
            self._velocity[1] += 1
        elif inp == ' ':
            self.activate_shield()


class Bullet(Pawn):

    art = np.array(['>', '-', '-', '-', '-', '>']).reshape(1, 6)

    def __init__(self, position, obj_number, drag_coeff, mass=0):
        super().__init__(self.art, position, obj_number, mass=mass,
                         drag_coeff=drag_coeff, pawn_type=9, max_velo=[0,3])
        self._velocity[1] = 3
        self._is_solid = False





# Refactor code -->
# Pawn is all the things that exist on the board
# Actor similar to things that can move and can stop on collision
# Maybe add a player class after this
# Each of the obstacles will be individual classes
# Do I need to revamp the system of force? 
