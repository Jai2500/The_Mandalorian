'''
    Importing all the required modules
'''
import os
import time
import colorama as cl
import numpy as np
from pawn import Actor, Pawn
from gamerule import Gamerule

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
        self.obj_arr = np.zeros((self.__screen_dim[0], self.__screen_dim[1]),
                                dtype=np.int32)

    def add_pawn(self, pawns):
        for i in range(len(pawns)):
            pos_x = int(np.round(pawns[i].position[1]))
            pos_y = int(np.round(pawns[i].position[0]))

            # print(pos_x, pos_y)
            pawns[i].check_collision(~np.isin(self.obj_arr[
                                    pos_y: pos_y + pawns[i].sprite.shape[0],
                                    pos_x: pos_x + pawns[i].sprite.shape[1]
                                    ], [i+1, 0]))

            pos_x = int(np.round(pawns[i].position[1]))
            pos_y = int(np.round(pawns[i].position[0]))

            # print(pos_x, pos_y)

            self.final_arr[pos_y: pos_y + pawns[i].sprite.shape[0],
                           pos_x: pos_x + pawns[i].sprite.shape[1]] = pawns[i].sprite

            self.obj_arr[pos_y: pos_y + pawns[i].sprite.shape[0],
                         pos_x: pos_x + pawns[i].sprite.shape[1]] \
                = pawns[i].collision_box * (i + 1)

    def draw(self):
        '''
            Draw the final image onto the screen
        '''
        print('\033[0;0H' + BG_BLUE, end='')
        self.final_arr[self.ground_height][0] = BG_GREEN + \
            self.final_arr[self.ground_height][0]
        final_img = ''.join(self.final_arr.ravel())
        print(final_img)


TEST_GAMERULE = Gamerule(0.3, 0.4)
TEST_SHAPE = np.array([[' ', 'o', ' '],
                       ['/', '|', ' '],
                       ['|', '|', ' ']])

TEST_SHAPE_2 = np.array([[' ', '*', ' '],
                       [' ', 'o', '\\'],
                       [' ', '|', '|']])

test_obj_shape = np.array([[' ', '-', '-'],
                          ['-', '-', '-']])

test_obj = Pawn(test_obj_shape, [17, ], 0)

TEST_PAWN = Actor(TEST_SHAPE, [4, 4], 0.3)
TEST_PAWN_2 = Actor(TEST_SHAPE_2, [10, 6], 0.3)
PAWN_ARRAY = np.array([test_obj, TEST_PAWN_2, TEST_PAWN])


TERM_SCREEN = Screen()
print(TERM_SCREEN.get_dim())
print("\033[0;0H")
os.system('clear')
while True:
    time.sleep(0.033)
    TERM_SCREEN.reset_screen()
    for i in range(len(PAWN_ARRAY)):
        PAWN_ARRAY[i] = TEST_GAMERULE.simulate_physics(PAWN_ARRAY[i])
    TERM_SCREEN.add_pawn(PAWN_ARRAY)

    TERM_SCREEN.draw()


# How will this work?
# A fore and back cycle that first prints the fore and then the back ?
