'''
    Importing all the required modules
'''
import os
import colorama as cl
import numpy as np

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
        self.__screen_dim[0] -= 2
        self.__final_arr = np.array([[' ' for i in range(self.__screen_dim[1])]
                                   for j in range(self.__screen_dim[0])],
                                  dtype='<U100')

        self.__color_map = np.array([[BG_BLUE for i in range(self.__screen_dim[1])]
                                   for j in range(self.__screen_dim[0])],
                                  dtype='<U100')
        self.__ground_height = self.__screen_dim[0] - \
            int(self.__screen_dim[0] * 0.10)
        self.__obj_arr = np.zeros((self.__screen_dim[0], self.__screen_dim[1]),
                                dtype=np.int32)
        self.__game_score = 0

    def get_dim(self):
        '''
            Returns the height and width of the screen. Used as a wrapper
        '''
        return self.__screen_dim

    def reset_screen(self):
        self.__final_arr = np.array([[' ' for i in range(self.__screen_dim[1])]
                                   for j in range(self.__screen_dim[0])],
                                  dtype='<U100')
        self.__color_map = np.array([[BG_BLUE for i in range(self.__screen_dim[1])]
                            for j in range(self.__screen_dim[0])],
                            dtype='<U100')
        ground_color = np.array([[BG_GREEN for i in range(self.__screen_dim[1])]
                                for j in range(self.__ground_height, self.__screen_dim[0])],
                                dtype='<U100')
        # for i in range(self.__screen_dim[1]):
        self.__color_map[self.__ground_height:, :] = ground_color
        self.__obj_arr = np.zeros((self.__screen_dim[0], self.__screen_dim[1]),
                                dtype=np.int32)

    def add_pawn(self, pawns, g_size):
        to_delete = []
        for i in range(len(pawns)):
            pos_x = int(np.round(pawns[i].get_position()[1]))
            pos_y = int(np.round(pawns[i].get_position()[0]))

            if pawns[i].get_pawn_type() != 0:
                if pos_y < 0:
                    pos_y = 1
                elif pos_y + pawns[i].get_sprite().shape[0] >= g_size:
                    pos_y = g_size - pawns[i].get_sprite().shape[0] 

            if pawns[i].get_pawn_type() == 8:
                if pos_x <= 0:
                    pos_x = 0
                elif pos_x + pawns[i].get_sprite().shape[1] >= self.__screen_dim[1]:
                    pos_x = self.__screen_dim[1] - pawns[i].get_sprite().shape[1]

            if pawns[i].get_position()[1] > self.__screen_dim[1]:
                pawns[i].set_to_delete(True)
            elif pawns[i].get_position()[1] + pawns[i].get_sprite().shape[1] < 0:
                pawns[i].set_to_delete(True)

            if pawns[i].get_to_delete() is False:
                obj_array = self.__obj_arr[
                    pos_y: pos_y + pawns[i].get_sprite().shape[0],
                    max(0, pos_x): min(self.__screen_dim[1], pos_x + pawns[i].get_sprite().shape[1]),
                    ]

                # PAWN_DICT[pawns[i].obj_number] = i
                # print(pawns[i], pos_x, pos_y)

                collision_box_size = [max(0, -pos_x), min(self.__screen_dim[1] - pos_x, pawns[i].get_sprite().shape[1])]

                collision, position, velocity = pawns[i].check_collision(~np.isin(obj_array, [pawns[i].get_obj_number(), 0]), collision_box_size)

                if collision is True:
                    objs = np.unique(obj_array)
                    for j in objs:
                        if j != 0:
                            for k in range(len(pawns)):
                                if pawns[k].get_obj_number() == j:
                                    pawns[k].on_collision(pawns[i])
                                if pawns[k].get_pawn_type() == 1:
                                    self.__game_score += 1
                    for j in objs:
                        if j != 0:
                            for k in range(len(pawns)):
                                if pawns[k].get_obj_number() == j:
                                    if pawns[k].get_is_solid() is True:
                                        pawns[i].set_position(position)
                                        pawns[i].set_velocity(velocity)
                                        break

            if pawns[i].get_to_delete() is False:

                pos_x = int(np.round(pawns[i].get_position()[1]))
                pos_y = int(np.round(pawns[i].get_position()[0]))

                if pawns[i].get_pawn_type() != 0:
                    if pos_y < 0:
                        pos_y = 1
                    elif pos_y + pawns[i].get_sprite().shape[0] >= g_size:
                        pos_y = g_size - pawns[i].get_sprite().shape[0]

                if pawns[i].get_pawn_type() == 8:
                    if pos_x < 0:
                        pos_x = 0
                    elif pos_x + pawns[i].get_sprite().shape[1] >= self.__screen_dim[1]:
                        pos_x = self.__screen_dim[1] - pawns[i].get_sprite().shape[1]

                self.__obj_arr[pos_y: pos_y + pawns[i].get_sprite().shape[0],
                             max(0, pos_x): min(self.__screen_dim[1], pos_x + pawns[i].get_sprite().shape[1])] \
                    = pawns[i].get_collision_box()[:, max(0, - pos_x): min(self.__screen_dim[1] - pos_x, pawns[i].get_sprite().shape[1])] * pawns[i].get_obj_number()

                self.__final_arr[pos_y: pos_y + pawns[i].get_sprite().shape[0],
                               max(0, pos_x): min(self.__screen_dim[1], pos_x + pawns[i].get_sprite().shape[1])
                               ] = pawns[i].get_sprite()[:, max(0, - pos_x): min(self.__screen_dim[1] - pos_x, pawns[i].get_sprite().shape[1])]

                self.__color_map[pos_y: pos_y + pawns[i].get_sprite().shape[0],
                               max(0, pos_x): min(self.__screen_dim[1], pos_x + pawns[i].get_sprite().shape[1])
                               ] = pawns[i].get_color_map()[:, max(0, - pos_x): min(self.__screen_dim[1] - pos_x, pawns[i].get_sprite().shape[1])]
            else:
                to_delete.append(pawns[i].get_obj_number())
        return to_delete

    def draw(self, game_state):
        '''
            Draw the final image onto the screen
        '''
        print('\033[0;0H' + cl.Back.LIGHTBLACK_EX, end='')
        print("Game Score: " + str(game_state[0]) + " Time Left: " + str(game_state[1]) + " Lives Left: " + str(game_state[2]) + "                          ")
        print(BG_BLUE, end='')
        ground_color = np.array([[BG_GREEN for i in range(self.__screen_dim[1])]
                        for j in range(self.__ground_height, self.__screen_dim[0])],
                        dtype='<U100')
        self.__color_map[self.__ground_height:, :] = ground_color
        # self.final_arr[self.ground_height][0] = BG_GREEN + \
        #     self.final_arr[self.ground_height][0]
        self.__final_arr = np.core.defchararray.add(self.__color_map, self.__final_arr)
        final_img = ''.join(self.__final_arr.ravel())
        print(final_img)
