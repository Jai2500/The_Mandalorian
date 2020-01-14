'''
    Importing all the required modules
'''
import os
import time
import colorama as cl
import numpy as np
from pawn import Actor, Pawn
from gamerule import Gamerule
from obstacles import Firebeam

cl.init()
BG_BLUE = cl.Back.BLUE
BG_GREEN = cl.Back.GREEN


class Screen:
    '''
        The object of the Screen of the computer.
        Parameters:
            Ground_Height (int)   - Height of the ground
            self.__screen_dim[0]  - Height of the terminal
            self.__screen_dim[1]  - Width of the terminal
    '''

    def __init__(self):
        '''
            Initializes the screen object with the basic parameters
        '''
        self.__screen_dim = \
            np.array(os.popen('stty size', 'r').read().split(), dtype='int')
        self.final_arr = np.array([[' ' for i in range(self.__screen_dim[1])]
                                   for j in range(self.__screen_dim[0])],
                                  dtype='<U100')
        self.ground_height = self.__screen_dim[0] - \
            int(self.__screen_dim[0] * 0.10)
        self.obj_arr = np.zeros((self.__screen_dim[0], self.__screen_dim[1]),
                                dtype=np.int32)

    def get_dim(self):
        '''
            Returns the height and width of the screen. Used as a wrapper
        '''
        return self.__screen_dim

    def reset_screen(self):
        self.final_arr = np.array([[' ' for i in range(self.__screen_dim[1])]
                                   for j in range(self.__screen_dim[0])],
                                  dtype='<U100')
        self.final_arr[self.ground_height][0] = BG_GREEN + \
            self.final_arr[self.ground_height][0]
        self.obj_arr = np.ones((self.__screen_dim[0], self.__screen_dim[1]),
                                dtype=np.int32) * -1

    def add_pawn(self, pawns):
        to_delete = []
        for i in range(len(pawns)):
            pos_x = int(np.round(pawns[i].position[1]))
            pos_y = int(np.round(pawns[i].position[0]))

            obj_array = self.obj_arr[
                pos_y: pos_y + pawns[i].sprite.shape[0],
                pos_x: pos_x + pawns[i].sprite.shape[1],
                ]

            collision = pawns[i].check_collision(~np.isin(obj_array, [i, -1]))

            if collision is True:
                objs = np.unique(obj_array)
                for j in objs:
                    pawns[j].on_collision(pawns[i])

            if pawns[i].to_delete is False:
                self.obj_arr[pos_y: pos_y + pawns[i].sprite.shape[0],
                             pos_x: pos_x + pawns[i].sprite.shape[1]] \
                    = pawns[i].collision_box * i

                pos_x = int(np.round(pawns[i].position[1]))
                pos_y = int(np.round(pawns[i].position[0]))

                self.final_arr[pos_y: pos_y + pawns[i].sprite.shape[0],
                               pos_x: pos_x + pawns[i].sprite.shape[1]
                               ] = pawns[i].sprite
            else:
                to_delete.append(i)
        return np.array(to_delete, dtype=np.int)

    def draw(self):
        '''
            Draw the final image onto the screen
        '''
        print('\033[0;0H' + BG_BLUE, end='')
        self.final_arr[self.ground_height][0] = BG_GREEN + \
            self.final_arr[self.ground_height][0]
        final_img = ''.join(self.final_arr.ravel())
        print(final_img)


TERM_SCREEN = Screen()
screen_dim = TERM_SCREEN.get_dim()


TEST_GAMERULE = Gamerule(0.3, 0.4)
TEST_SHAPE = np.array([[' ', 'o', ' '],
                       ['/', '|', ' '],
                       ['|', '|', ' ']])

TEST_SHAPE_2 = np.array([[' ', '*', ' '],
                         [' ', 'o', '\\'],
                         [' ', '|', '|']])

test_obj_shape = np.array([[' ', '-', '-'],
                          ['-', '-', '-']])


GROUND_SHAPE = np.array([['-' for i in range(screen_dim[1])]
                        for j in range(int(screen_dim[0] * 0.1))],
                        dtype='<U100')

GROUND_OBJ = Pawn(GROUND_SHAPE, [screen_dim[0] - int(screen_dim[0] * 0.1), 0],
                  0)

test_obj = Pawn(test_obj_shape, [13, 10], 0)

TEST_PAWN = Actor(TEST_SHAPE, [4, 4], 0.3, is_player=True)
TEST_PAWN_2 = Actor(TEST_SHAPE_2, [4, 4], 0.3, is_player=True)
test_firebeam = Firebeam([17, 4])
PAWN_ARRAY = np.array([GROUND_OBJ, test_firebeam, TEST_PAWN, TEST_PAWN_2])

print(test_firebeam.type, test_firebeam.size)

while True:
    time.sleep(0.1)
    TERM_SCREEN.reset_screen()
    for i in range(len(PAWN_ARRAY)):
        PAWN_ARRAY[i] = TEST_GAMERULE.simulate_physics(PAWN_ARRAY[i])
    to_delete = TERM_SCREEN.add_pawn(PAWN_ARRAY)
    PAWN_ARRAY = np.delete(PAWN_ARRAY, to_delete)
    # print(to_delete, "To delete")
    TERM_SCREEN.draw()

# The position and the velocity keeps on increasing despite the ground
# How will this work?
# A fore and back cycle that first prints the fore and then the back ?
# Make a dictionary that refers object number to the object