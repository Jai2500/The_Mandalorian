'''
    Importing all the required modules
'''
import os
import time
import colorama as cl
import numpy as np
from pawn import Actor
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
        i = 1
        for pawn in pawns:
            pos_x = int(np.round(pawn.position[1]))
            pos_y = int(np.round(pawn.position[0]))
            self.final_arr[pos_y: pos_y + pawn.sprite.shape[0],
                           pos_x: pos_x + pawn.sprite.shape[1]] = pawn.sprite
            self.obj_arr[pos_y: pos_y + pawn.sprite.shape[0],
                         pos_x: pos_x + pawn.sprite.shape[1]] \
                = np.ones(pawn.sprite.shape) * i
            i += 1

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

TEST_SHAPE_2 = np.array([[' ', 'o', ' '],
                       [' ', 'o', '\\'],
                       [' ', '|', '|']])


TEST_PAWN = Actor(TEST_SHAPE, [4, 4], 0.5)
TEST_PAWN_2 = Actor(TEST_SHAPE_2, [10, 5], 0.02)
PAWN_ARRAY = np.array([TEST_PAWN, TEST_PAWN_2])

TERM_SCREEN = Screen()
print(TERM_SCREEN.get_dim())
print("\033[0;0H")
os.system('clear')
while True:
    time.sleep(0.13)
    for i in range(len(PAWN_ARRAY)):
        PAWN_ARRAY[i] = TEST_GAMERULE.simulate_physics(PAWN_ARRAY[i])
    TERM_SCREEN.reset_screen()
    TERM_SCREEN.add_pawn(PAWN_ARRAY)
    for i in range(len(PAWN_ARRAY)):
        pos_x = int(np.round(PAWN_ARRAY[i].position[1]))
        pos_y = int(np.round(PAWN_ARRAY[i].position[0]))
        PAWN_ARRAY[i].check_collision(TERM_SCREEN.obj_arr[
                                pos_y: pos_y + PAWN_ARRAY[i].sprite.shape[0],
                                pos_x: pos_x + PAWN_ARRAY[i].sprite.shape[1]
                                ] - (i + 1))
    TERM_SCREEN.reset_screen()
    TERM_SCREEN.add_pawn(PAWN_ARRAY)
    TERM_SCREEN.draw()


# How will this work?
# A fore and back cycle that first prints the fore and then the back ?
