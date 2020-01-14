import numpy as np


class Pawn:
    def __init__(self, sprite, position, mass=0, is_player=False, lives=1):
        self.mass = mass
        self.sprite = sprite
        self.velocity = np.array([0, 0], dtype=np.float64)
        self.collision_box = self.create_collision_box(sprite)
        self.position = np.array(position, dtype=np.float64)
        self.is_player = is_player
        self.to_delete = False
        self.lives = lives
        # print(self.sprite.shape)

    def create_collision_box(self, obj_shape):
        collision_box = obj_shape != ' '
        return collision_box

    def check_collision(self, out_arr):
        overlap_box = self.collision_box * out_arr
        if np.sum(overlap_box) > 0:
            return True
        else:
            return False

    def on_trigger(self, other):
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

    def check_collision(self, out_arr):

        overlap_box = self.collision_box * out_arr
        # print(overlap_box, self.sprite[0])

        # Version 1.2 based on the Z-index
        # Possible issues: -- Way to compare the Z-index

        if np.sum(overlap_box) > 0:
            mpv = np.array([0, 0])
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
        #     mpv = np.array([0,0])
        #     if self.velocity[0] != 0:
        #         row_sums = np.sum(overlap_box, axis = 1)
        #         non_zero = np.nonzero(row_sums)[0]

            self.position = self.position + mpv
            self.velocity = self.velocity * (mpv == 0)
            return True

        return False


# Refactor code -->
# Pawn is all the things that exist on the board
# Actor similar to things that can move and can stop on collision
# Maybe add a player class after this
# Each of the obstacles will be individual classes