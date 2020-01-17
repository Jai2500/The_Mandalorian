from pawn import Pawn
import numpy as np


class Speed_Boost(Pawn):
    sprite = np.array([[')', ')']
                       [')', ')']])

    def __init__(self, position, obj_number, boost_speed):
        super().__init__(self.sprite, position, obj_number, pawn_type=7, is_solid=False)
        self.boost_speed = boost_speed


class Shield(Actor):
    