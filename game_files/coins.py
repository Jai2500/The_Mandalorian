from pawn import Pawn
import numpy as np

class Coin(Pawn):

    art = np.array(['o']).reshape(1, 1)

    def __init__(self, position, obj_number):
        super().__init__(self.art, position, obj_number, pawn_type=1, is_solid=False)

    def on_collision(self, other):
        if other.get_pawn_type() == 8:
            other.set_score(other.get_score() + 1)
            self.die()
            return 1
