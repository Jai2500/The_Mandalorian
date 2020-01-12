import colorama as cl
import os
import numpy as np
import time

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
        '''Initializes the screen object with the basic parameters'''
        self.__screen_dim = \
            np.array(os.popen('stty size', 'r').read().split(), dtype='int')
        self.final_arr = np.array([[' ' for i in range(self.__screen_dim[1])] 
                                  for j in range(self.__screen_dim[0])],
                                  dtype='<U100')
        self.ground_height = self.__screen_dim[0] - 5

    def get_dim(self):
        return self.__screen_dim

    def draw(self):
        print('\033[0;0H' + BG_BLUE, end='')
        self.final_arr[self.ground_height][0] = BG_GREEN + self.final_arr[self.ground_height][0]
        final_img = ''.join(self.final_arr.ravel())
        print(final_img)


a = Screen()
print(a.get_dim())
print("\033[0;0H")
while True:
    time.sleep(0.033)
    a.draw()


# How will this work?
# A fore and back cycle that first prints the fore and then the back ?
