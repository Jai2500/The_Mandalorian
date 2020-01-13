import numpy as np


class Pawn:
    def __init__(self, sprite, position, mass=0):
        self.mass = mass
        self.sprite = sprite
        self.velocity = np.array([0, 0], dtype=np.float64)
        self.collision_box = self.create_collision_box(sprite)
        self.position = np.array(position, dtype=np.float64)
        print(self.sprite.shape)

    def create_collision_box(self, obj_shape):
        collision_box = obj_shape != ' '
        return collision_box

    def on_collision(self):
        print("The object has collided")

    def get_sprite(self):
        return self.sprite, self.collision_box


class Actor(Pawn):

    def check_collision(self, out_arr):

        overlap_box = self.collision_box * out_arr
        # print(overlap_box)

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

            self.position = self.position + mpv
            self.velocity = self.velocity * (mpv == 0)


# class Character(Actor):
#     def on_collision(self, other): 

TEST_SHAPE = np.array([[' ', 'o', ' '],
                       [' /', '|', '\\'],
                       ['|', '|', '|']])
