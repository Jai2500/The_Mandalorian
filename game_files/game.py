import os
import time
from datetime import datetime
import colorama as cl
import numpy as np
from pawn import Pawn, Bullet, Character
from gamerule import Gamerule
from obstacles import Firebeam, Magnet, Boss_Enemy, Solid_Objects
from kbhit import KBHit
from powerups import Speed_Boost
from collections import deque
from coins import Coin
from screen import Screen


cl.init()
BG_BLUE = cl.Back.BLUE
BG_GREEN = cl.Back.GREEN


_KBHIT = KBHit()

ObjNumber = 3

TERM_SCREEN = Screen()
SCREEN_DIM = TERM_SCREEN.get_dim()
GROUND_SIZE = [SCREEN_DIM[0] - int(SCREEN_DIM[0] * 0.1), 0]
GAMERULE = Gamerule(0.3)

speed_boost = 0

pawns = {
    0: deque([]),  # Ground + Roof
    1: deque([]),  # Coins
    2: deque([]),  # Speed Boost
    3: deque([]),  # Solid Objects
    4: deque([]),  # Firebeams
    5: deque([]),  # Magnets
    6: deque([]),  # Boss
    7: deque([]),  # Boss Bullets
    8: deque([]),  # Player
    9: deque([]),  # Player Bullets
}


def generate_spawn_order():
    spawn_order = []
    for pawn_type in pawns:
        spawn_order += pawns[pawn_type]

    return spawn_order


def delete_pawns(to_delete):
    for pawn_type in pawns:
        pawns[pawn_type] = deque([obj for obj in pawns[pawn_type] if obj.get_obj_number()
                            not in to_delete])
        # print(to_delete)


def spawn_coins(y):
    size = np.random.randint(4, 9, 2)
    size[0] = min(size[0], GROUND_SIZE[0] - y)
    coin_list = []
    global ObjNumber
    for i in range(size[0]):
        for j in range(size[1]):
            # print(j)
            coin_list.append(GAMERULE.set_spawn_velo(Coin([y + i, SCREEN_DIM[1] + j], ObjNumber)))
            ObjNumber += 1
    # for i in coin_list:
    #     print(i.position)
    pawns[1] += coin_list


def spawn_pawns():
    global ObjNumber
    # improve the spawning by position of player
    # Setting the probabilities of spawning
    prob_coins = 0.02 
    prob_speed_boost = 0.01 
    prob_solid_objects = 0.05 
    prob_firebeams = 0.07 
    prob_magnets = 0.01

    # Spawning Coins
    prob = np.random.random()
    if prob < prob_coins + 1e-6:
        y = np.random.randint(0, GROUND_SIZE[0] - 1)
        spawn_coins(y)

    # Spawning speed_boost
    # for i in range(np.random.randint(1, 2)):
    prob = np.random.random()
    if prob < prob_speed_boost + 1e-6:
        y = np.random.randint(0, GROUND_SIZE[0] - 2)
        pawns[2].append(GAMERULE.set_spawn_velo(Speed_Boost([y, SCREEN_DIM[1]
                                                                + 1],
                                                            ObjNumber)))
        ObjNumber += 1

    # Spawning Solid Objects
    prob = np.random.random()
    if prob < prob_solid_objects + 1e-6:
        # for i in range(np.random.randint(1, 2)):
        y = np.random.randint(0, GROUND_SIZE[0] - 3)
        pawns[3].append(GAMERULE.set_spawn_velo(Solid_Objects([y,
                        SCREEN_DIM[1] + 1], ObjNumber, GROUND_SIZE[0])))
        ObjNumber += 1

    # Spawning Firebeams
    prob = np.random.random()
    if prob < prob_firebeams + 1e-6:
        # for i in range(np.random.randint(1, 3)):
        y = np.random.randint(0, GROUND_SIZE[0] - 3)
        pawns[4].append(GAMERULE.set_spawn_velo(Firebeam([y, SCREEN_DIM[1]
                                                             + 1], ObjNumber, 
                                                             GROUND_SIZE[0])))
        ObjNumber += 1

    # Spawning Magnet
    # for i in range(np.random.randint(1, 2)):
    prob = np.random.random()
    if prob < prob_magnets + 1e-6:
        y = np.random.randint(0, GROUND_SIZE[0] - 2)
        pawns[5].append(GAMERULE.set_spawn_velo(Magnet([y, SCREEN_DIM[1]
                                                        + 1], ObjNumber)))
        ObjNumber += 1


dragon_spawned = False


def spawn_boss():
    global ObjNumber
    global dragon_spawned
    if dragon_spawned is False:
        pawns[6].append(Boss_Enemy([GROUND_SIZE[0] - 20, SCREEN_DIM[1] - 45], ObjNumber, 40))
        ObjNumber += 1
        dragon_spawned = True



TEST_SHAPE_2 = np.array([[' ', '*', ' '],
                         ['/', 'o', '\\'],
                         ['|', '|', '|']])

GROUND_SHAPE = np.array([['-' for i in range(SCREEN_DIM[1])]
                        for j in range(int(SCREEN_DIM[0] * 0.1))],
                        dtype='<U100')

pawns[0].append(Pawn(GROUND_SHAPE, [SCREEN_DIM[0] - int(SCREEN_DIM[0] * 0.1), 0], 1))

pawns[8].append(Character(TEST_SHAPE_2, [6, 12], 2, 1, pawn_type=8, lives=10))

speed_boost_times = []

to_delete = []


step = 0

prob_boss_bullet = 0.3

std_velocity_frame = 1.4

distance_moved = 0

init_time = datetime.now()

win = False

print('\033[2J')
print('\x1B[?25l')

while(True):
    time.sleep(0.033)
    if distance_moved <= 200:
        spawn_pawns()
    else:
        spawn_boss()
    now = datetime.now()

    if (now - init_time).seconds > 150:
        break

    if len(pawns[8]) == 0:
        break

    if len(pawns[6]) == 0 and dragon_spawned is True:
        win = True
        break

    TERM_SCREEN.reset_screen()

    for i in range(len(pawns[8])):
        if pawns[8][i].get_shield_active() is True:
            if (now - pawns[8][i].get_timestamp()).seconds > 5:
                pawns[8][i].deactivate_shield()

    if _KBHIT.kbhit():
        inp = _KBHIT.getch().lower()
        if inp == 'q':
            break
        elif inp == 'e':
            pawns[9].append(Bullet([pawns[8][0].get_position()[0], pawns[8][0].get_position()[1] + 2], ObjNumber, 0))
            ObjNumber += 1
        else:
            pawns[8][0].control(inp)

    for i in range(len(pawns[5])):
        pawns[8][0] = pawns[5][i].on_trigger(pawns[8][0])

    old_size = len(speed_boost_times)
    speed_boost_times = [time for time in speed_boost_times if (now - time).seconds < 10]
    decrease = old_size - len(speed_boost_times)
    speed_boost -= decrease * 0.01

    for i in range(len(pawns[2])):
        if pawns[2][i].is_activated is True:
            speed_boost += 0.01
            speed_boost_times.append(now)

    for i in range(len(pawns[6])):
        pawns[6][i].move(pawns[8][0], GROUND_SIZE[0])
        prob = np.random.random()
        if prob < prob_boss_bullet + 1e-6:
            pawns[7].append(pawns[6][0].launch_bullet(ObjNumber))
            ObjNumber += 1

    for i in range(len(pawns[7])):
        pawns[7][i].move(pawns[8][0], GROUND_SIZE[0])

    for i in pawns:
        if i in [0, 6]:
            pass
        else:
            for j in range(len(pawns[i])):
                pawns[i][j] = GAMERULE.simulate_physics(pawns[i][j], speed_boost, GROUND_SIZE[0], SCREEN_DIM[1])

    spawn_order = generate_spawn_order()

    to_delete += TERM_SCREEN.add_pawn(spawn_order, GROUND_SIZE[0])

    delete_pawns(to_delete)

    TERM_SCREEN.draw()
    # print(distance_moved)
    distance_moved += (std_velocity_frame + speed_boost)

os.system('clear')
print('\033[2H', cl.Style.RESET_ALL)

win_string = cl.Back.BLACK + '''
_/      _/    _/_/    _/    _/      _/          _/    _/_/    _/      _/   
 _/  _/    _/    _/  _/    _/      _/          _/  _/    _/  _/_/    _/    
  _/      _/    _/  _/    _/      _/    _/    _/  _/    _/  _/  _/  _/     
 _/      _/    _/  _/    _/        _/  _/  _/    _/    _/  _/    _/_/      
_/        _/_/      _/_/            _/  _/        _/_/    _/      _/  
'''

lose_string = cl.Back.BLACK + '''
_/      _/    _/_/    _/    _/      _/          _/_/      _/_/_/  _/_/_/_/_/   
 _/  _/    _/    _/  _/    _/      _/        _/    _/  _/            _/        
  _/      _/    _/  _/    _/      _/        _/    _/    _/_/        _/         
 _/      _/    _/  _/    _/      _/        _/    _/        _/      _/          
_/        _/_/      _/_/        _/_/_/_/    _/_/    _/_/_/        _/   
'''

if win is True:
    print(win_string)
else:
    print(lose_string)
