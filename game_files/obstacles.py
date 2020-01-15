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
            return np.array(['*'] + ['-'] * (self.size - 2) + ['*']).reshape(
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
