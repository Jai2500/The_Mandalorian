import numpy as np
from pawn import Pawn


class Firebeam(Pawn):
    def __init__(self, position, obj_number, lives=1):
        sprite = self.create_sprite()
        super().__init__(sprite, position, obj_number, mass=0, pawn_type=0, lives=lives)

    def create_sprite(self):
        self.type = np.random.randint(1, 4)
        self.size = np.random.randint(3, 8)
        if self.type == 1:
            # print("E1")
            return np.array(['*'] + ['-'] * (self.size - 2) + ['*']).reshape(1, self.size)
        elif self.type == 2:
            # print("E2")
            return np.array(['*'] + ['|'] * (self.size - 2) + ['*']).reshape(
                self.size, 1)
        else:
            sprite = []
            for i in range(self.size):
                sprite.append(
                    [' '] * i + ['*'] + [' '] * (self.size - i - 1)
                )
            return np.array(sprite)

    def on_collision(self, other):
        if other.pawn_type == 1:  # Player
            other.die()
            if other.lives > 0:
                self.die()
        elif other.pawn_type == 2:
            self.die()
            other.die()
        else:
            if np.random.random() < 0.5:
                self.die()
            else:
                other.die()


class Magnet(Pawn):
    sprite = np.array([['|', '|'],
                       ['-', '-']])

    def __init__(self, position, obj_number, lives=1, force_const= 0.05):
        super().__init__(self.sprite, position, obj_number, lives=lives, pawn_type=5)
        self.force_const = force_const
        # self.velocity[1] = 0.5
        self.drag_coeff = 0
        self.is_solid = False

    def on_trigger(self, pawn):
        # print("Entered here")
        dist = np.linalg.norm(self.position - pawn.position)
        diff = self.position - pawn.position
        pawn.velocity[0] += self.force_const *\
                np.round(diff[0]) / (dist**1.4 + 10)
        
        # if diff[0] > 0:
        #     pawn.velocity[0] += min(self.force_const *\
        #         np.round(diff[0]) / (dist**1.8 + 10), 0.5)
        # else: 
        #     pawn.velocity[0] += max(self.force_const *\
        #         np.round(diff[0]) / (dist**1.5 + 10), -0.5)
        pawn.velocity[1] += self.force_const *\
            np.round(diff[1]) / (dist**1.4 + 10)
        # print(dist, "dist")
        # print(self.force_const * int(self.position[1] - pawn.position[1]) / (dist**2 + 1), "X")
        # print(self.force_const * int(np.round(self.position[0] - pawn.position[0])) / (dist**2 + 1), "Y")
        # print(pawn)
        return pawn

# Maybe try to reduce the velocity of the player by a constant times norm
# of the distance between them for each successive frame
# 1/r effectively
