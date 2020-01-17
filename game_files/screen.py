'''
    Importing all the required modules
'''
import os
import time
import colorama as cl
import numpy as np
from pawn import Actor, Pawn, Bullet, Coin
from gamerule import Gamerule
from obstacles import Firebeam, Magnet

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
        self.game_score = 0

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
        to_delete = []
        for i in range(len(pawns)):
            pos_x = int(np.round(pawns[i].position[1]))
            pos_y = int(np.round(pawns[i].position[0]))

            obj_array = self.obj_arr[
                pos_y: pos_y + pawns[i].sprite.shape[0],
                pos_x: pos_x + pawns[i].sprite.shape[1],
                ]

            PAWN_DICT[pawns[i].obj_number] = i

            collision, position, velocity = pawns[i].check_collision(~np.isin(obj_array, [pawns[i].obj_number, 0]))
            # if i == 2:
                # print("Printing Obj array\n", obj_array, pawns[i].sprite[0, 1], collision, "\n\n")

            if collision is True:
                objs = np.unique(obj_array)
                for j in objs:
                    if j != 0:
                        pawns[PAWN_DICT[j]].on_collision(pawns[i])
                        if pawns[PAWN_DICT[j]].pawn_type == 4:
                            self.game_score += 1
                for j in objs:
                    if j != 0 and pawns[PAWN_DICT[j]].is_solid is True:
                        pawns[i].position = position
                        pawns[i].velocity = velocity
                        break

            if pawns[i].to_delete is False:
                # print(pawns[i].obj_number)
                self.obj_arr[pos_y: pos_y + pawns[i].sprite.shape[0],
                             pos_x: pos_x + pawns[i].sprite.shape[1]] \
                    = pawns[i].collision_box * pawns[i].obj_number

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

TEST_GAMERULE = Gamerule(0.3)
TEST_SHAPE = np.array([[' ', 'o', ' '],
                       ['/', '|', ' '],
                       ['|', '|', ' ']])

TEST_SHAPE_2 = np.array([[' ', '*', ' '],
                         ['/', 'o', '\\'],
                         ['|', '|', '|']])

test_obj_shape = np.array([['-', ' ', ' ', ' ', ' ', ' '],
                           [' ', '-', ' ', ' ', ' ', ' '],
                           [' ', ' ', '-', ' ', ' ', ' '],
                           [' ', ' ', ' ', '-', ' ', ' '],
                           [' ', ' ', ' ', ' ', '-', ' '],
                           [' ', ' ', ' ', ' ', ' ', '-']
                          ])


GROUND_SHAPE = np.array([['-' for i in range(screen_dim[1])]
                        for j in range(int(screen_dim[0] * 0.1))],
                        dtype='<U100')

ROOF_SHAPE = np.array([['-' for i in range(screen_dim[1])]],
                      dtype='<U100').reshape(1, screen_dim[1])


GROUND_OBJ = Pawn(GROUND_SHAPE, [screen_dim[0] - int(screen_dim[0] * 0.1), 0],
                  1, 0)

ROOF_OBJ = Pawn(ROOF_SHAPE, [0, 0], 10, 0)

test_obj = Pawn(test_obj_shape, [13, 10], 2)
test_magnet = Magnet([14, 12], 8, force_const=1.3)
TEST_PAWN = Actor(TEST_SHAPE, [4, 4], 4,  1, pawn_type=1)
TEST_PAWN_2 = Actor(TEST_SHAPE_2, [4, 12], 5, 1, pawn_type=1, lives=2)
test_firebeam = Firebeam([13, 4], 3)
test_bullet = Bullet([4, 10], 6, 0.01, 0)
PAWN_LIST = [GROUND_OBJ, test_obj, test_magnet, TEST_PAWN_2]

# for i in range(5):
#     a = Coin([i + 20, 7], i + 10)
#     PAWN_LIST = PAWN_LIST[:1+i] + [a] + PAWN_LIST[1 + i:]  

PAWN_ARRAY = np.array(PAWN_LIST)
MAGNET_LIST = [3]
PAWN_DICT = {}

# print(test_firebeam.type, test_firebeam.size)
_ = TERM_SCREEN.add_pawn(PAWN_ARRAY)
while True:
    # print(PAWN_DICT)
    time.sleep(0.1)
    TERM_SCREEN.reset_screen()
    # for i in MAGNET_LIST:
        # print(i)
        # print(PAWN_ARRAY[8])
    PAWN_ARRAY[PAWN_DICT[5]] = PAWN_ARRAY[PAWN_DICT[8]].on_trigger(PAWN_ARRAY[PAWN_DICT[5]])
        # print(PAWN_ARRAY[4])
    for i in range(len(PAWN_ARRAY)):
        PAWN_ARRAY[i] = TEST_GAMERULE.simulate_physics(PAWN_ARRAY[i])
    to_delete = TERM_SCREEN.add_pawn(PAWN_ARRAY)
    PAWN_ARRAY = np.delete(PAWN_ARRAY, to_delete)
    # print(TERM_SCREEN.game_score)
    TERM_SCREEN.draw()

# The position and the velocity keeps on increasing despite the ground
# How will this work?
# A fore and back cycle that first prints the fore and then the back ?
# Make a dictionary that refers object number to the object

# Make a dictionary of the magnets present on the screen and check for that with the isin command before deleting so that I can again go back to doing everything
# Update the object dictionary through an update dictionary option