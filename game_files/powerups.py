import numpy as np
from pawn import Pawn


class Speed_Boost(Pawn):
    sprite = np.array([[')', ')'],
                       [')', ')']]).reshape(2, 2)

    def __init__(self, position, obj_number):
        super().__init__(self.sprite, position, obj_number, pawn_type=2, is_solid=False)
        self.is_activated = False

    def on_collision(self, other):
        if other.pawn_type == 8:
            self.is_activated = True 
            self.die()
