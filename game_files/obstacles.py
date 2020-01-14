import numpy as np
from pawn import Pawn


class Firebeam(Pawn):
    def __init__(self, position, mass=0, lives=1):
        sprite = self.create_sprite()
        super().__init__(sprite, position, mass, is_player=False, lives=lives)

    def create_sprite(self):
        self.type = np.random.randint(1, 4)
        self.size = np.random.randint(3, 8)
        if self.type == 1:
            print("E1")
            return np.array(['*'] + ['-'] * (self.size - 2) + ['*']).reshape(1, self.size)
        elif self.type == 2:
            print("E2")
            return np.array(['*'] + ['-'] * (self.size - 2) + ['*']).reshape(
                self.size, 1)
        else:
            sprite = []
            # print("Entered here")
            for i in range(self.size):
                # print(i)
                sprite.append(
                              [' '] * i + ['*'] + [' '] * (self.size - i - 1)
                              )
                # print(sprite)
            return np.array(sprite)

    def on_collision(self, other):
        if other.is_player is True:  # Player
            other.die()
            # print("Entered here")
        elif other.is_player is False:
            self.die()
        else:
            if np.random.random() < 0.5:
                self.die()
            else:
                other.die()
