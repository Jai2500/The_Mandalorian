import numpy as np
from datetime import datetime


class Pawn:
    def __init__(self, sprite, position, obj_number, mass=0, pawn_type=0,
                 lives=1, drag_coeff=0.0, is_solid=True, max_velo=[5, 5]):
        self.mass = mass
        self.sprite = sprite
        self.velocity = np.array([0, 0], dtype=np.float64)
        self.collision_box = self.create_collision_box(sprite)
        self.position = np.array(position, dtype=np.float64)
        self.obj_number = obj_number
        self.pawn_type = pawn_type
        self.to_delete = False
        self.lives = lives
        self.drag_coeff = drag_coeff
        self.is_solid = is_solid
        self.max_velo = max_velo
        # print(self.sprite.shape)

    def create_collision_box(self, obj_shape):
        collision_box = obj_shape != ' '
        return collision_box

    def check_collision(self, out_arr, collision_box_size):
        overlap_box = self.collision_box[:, collision_box_size[0]:collision_box_size[1]] * out_arr
        if np.sum(overlap_box) > 0:
            return True, self.position, self.velocity
        else:
            return False, self.position, self.velocity

    def on_trigger(self, pawn):
        pass

    def on_collision(self, other):
        return "The object has collided"

    def get_sprite(self):
        return self.sprite, self.collision_box

    def die(self):
        self.lives -= 1
        if self.lives <= 0:
            self.to_delete = True


class Actor(Pawn):

    def check_collision(self, out_arr, collision_box_size):
        # print(out_arr.shape)
        overlap_box = self.collision_box[:, collision_box_size[0]:collision_box_size[1]] * out_arr

        # Version 1.2 based on the Z-index
        # Possible issues: -- Way to compare the Z-index

        if np.sum(overlap_box) > 0:
            mpv = np.array([10000, 10000])
            if self.velocity[0] > 0.0:
                row_sums = np.sum(overlap_box, axis=1)
                non_zero = np.nonzero(row_sums)[0]
                if non_zero.size > 0:
                    mpv[0] = -1 * (self.sprite.shape[0] -
                                   np.min(non_zero))
            elif self.velocity[0] < 0.0:
                row_sums = np.sum(overlap_box, axis=1)
                non_zero = np.nonzero(row_sums)[0]
                if non_zero.size > 0:
                    mpv[0] = np.max(non_zero)

            if self.velocity[1] > 0.0:
                col_sums = np.sum(overlap_box, axis=0)
                non_zero = np.nonzero(col_sums)[0]
                if non_zero.size > 0:
                    mpv[1] = -1 * np.max(non_zero)
            elif self.velocity[1] < 0.0:
                col_sums = np.sum(overlap_box, axis=0)
                non_zero = np.nonzero(col_sums)[0]
                if non_zero.size > 0:
                    mpv[1] = self.sprite.shape[1] - np.min(non_zero)

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

            new_position = self.position + mpv
            new_velocity = self.velocity - (mpv != 0) * self.velocity
            # if self.pawn_type == 1:
            #     print(new_velocity, "After collision")
            return True, new_position, new_velocity

        return False, self.position, self.velocity


class Character(Actor):

    def __init__(self, sprite, position, obj_number, mass=0, pawn_type=0,
                 lives=1, drag_coeff=0.3, is_solid=True, shield_sprite = None):
        super().__init__(sprite, position, obj_number, mass, pawn_type, lives,
                         drag_coeff, is_solid, max_velo=[2, 2])
        self.shield_active = False
        self.normal_sprite = self.sprite
        self.curr_lives = self.lives
        self.normal_collision_box = self.create_collision_box(self.normal_sprite)
        self.timestamp = datetime.now()
        if shield_sprite is None:
            self.shield_sprite = np.array([['O' for i in range(self.sprite.shape[1] + 2)] for j in range(self.sprite.shape[0] + 2)])
            self.shield_sprite[1:1 + self.sprite.shape[0], 1:self.sprite.shape[1] + 1] = self.sprite
        else:
            self.shield_sprite = shield_sprite
        self.shield_collision_box = self.create_collision_box(self.shield_sprite)
        self.score = 0

    def activate_shield(self):
        if self.shield_active is True:
            return

        now = datetime.now()
        if (now - self.timestamp).seconds > 5:
            self.shield_active = True
            self.sprite = self.shield_sprite
            self.collision_box = self.shield_collision_box
            self.timestamp = now
            self.curr_lives = self.lives
            self.lives = 100000000
            return

    def deactivate_shield(self):
        if self.shield_active is False:
            return

        self.shield_active = False
        self.sprite = self.normal_sprite
        self.collision_box = self.normal_collision_box
        self.timestamp = datetime.now()
        self.lives = self.curr_lives
        return


class Bullet(Pawn):

    sprite = np.array(['>', '-', '-', '-', '-', '>']).reshape(1, 6)

    def __init__(self, position, obj_number, drag_coeff, mass=0):
        super().__init__(self.sprite, position, obj_number, mass=mass,
                         drag_coeff=drag_coeff, pawn_type=9, max_velo=[0,3])
        self.velocity[1] = 3
        self.is_solid = False





# Refactor code -->
# Pawn is all the things that exist on the board
# Actor similar to things that can move and can stop on collision
# Maybe add a player class after this
# Each of the obstacles will be individual classes
# Do I need to revamp the system of force? 
