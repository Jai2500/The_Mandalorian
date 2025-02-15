import numpy as np
from pawn import Pawn, Actor


class Firebeam(Pawn):
    def __init__(self, position, obj_number, g_size, lives=1):
        art = self.create_sprite(g_size, position)
        super().__init__(art, position, obj_number, mass=0, pawn_type=4, lives=lives)
        self.generate_color_map()

    def create_sprite(self, g_size, position):
        self.type = np.random.randint(1, 4)
        self.size = int(np.random.randint(3, 8))
        self.size = min(self.size, g_size - position[0])
        if self.type == 1:
            return np.array(['*'] + ['-'] * (self.size - 2) + ['*']).reshape(1, self.size)
        elif self.type == 2:
            return np.array(['*'] + ['|'] * (self.size - 2) + ['*']).reshape(
                self.size, 1)
        else:
            sprite = []
            for i in range(self.size):
                sprite.append(
                    [' '] * i + ['*'] + [' '] * (self.size - i - 1)
                )
            return np.array(sprite)

    def generate_color_map(self):
        for i in range(self._sprite.shape[0]):
            for j in range(self._sprite.shape[1]):
                if self._sprite[i, j] in ['*', '-', '|']:
                    self._color_map[i, j] = '\u001b[41m'

    def on_collision(self, other):
        if other.get_pawn_type() == 8:  # Player
            if other.get_dragon_active() is True:
                self.die()
                other.set_score(other.get_score() + 20)
                other.deactivate_dragon()
            if other.get_shield_active() is True:
                self.die()
                other.set_score(other.get_score() + 20)
                return
            other.die()
            if other.get_lives() > 0:
                self.die()
                other.set_score(other.get_score() + 20)
        elif other.get_pawn_type() == 9:
            self.die()
            other.die()
            other.set_score(other.get_score() + 20)
        else:
            if np.random.random() < 0.5:
                self.die()
            else:
                other.die()


class Magnet(Pawn):
    art = np.array([['|', '|'],
                       ['-', '-']])

    def __init__(self, position, obj_number, lives=1, force_const=1.5):
        super().__init__(self.art, position, obj_number, lives=lives, pawn_type=5)
        self.force_const = force_const
        self.drag_coeff = 0
        self._is_solid = False

    def on_trigger(self, pawn):
        if pawn.get_dragon_active() is True:
            self.die()
            return pawn
        dist = np.linalg.norm(self._position - pawn.get_position())
        diff = self._position - pawn.get_position()
        if pawn.get_shield_active() is False:
            pawn_vel = pawn.get_velocity()
            y_vel = pawn_vel[0] + self.force_const *\
                    np.round(diff[0]) / (dist**1.44 + 10) 
            x_vel = pawn_vel[1] + self.force_const *\
                np.round(diff[1]) / (dist**1.44 + 10) 
            pawn.set_velocity(np.array([y_vel, x_vel]))

        return pawn


class Solid_Objects(Pawn):

    def __init__(self, position, obj_number, g_size, lives=1):
        art = self.create_sprite(g_size, position)
        super().__init__(art, position, obj_number, mass=0, pawn_type=3, lives=lives)
        self.generate_color_map()

    def create_sprite(self, g_size, position):
        self.type = np.random.randint(1, 4)
        self.size = int(np.random.randint(3, 8))
        self.size = min(self.size, g_size - position[0])
        if self.type == 1:
            return np.array([['|'] + ['-'] + ['-'] * (self.size - 2) + ['-'] + ['|'],
                             ['|'] + ['-'] + ['-'] * (self.size - 2) + ['-'] + ['|']]).reshape(2, self.size + 2)
        elif self.type == 2:
            return np.array([['-'] + ['|'] + ['|'] * (self.size - 2) + ['|'] + ['-'],
                             ['-'] + ['|'] + ['|'] * (self.size - 2) + ['|'] + ['-']]).reshape(2, self.size + 2).T
        else:
            sprite = []
            for i in range(self.size):
                sprite.append(
                    [' '] * i + ['-'] + [' '] * (self.size - i - 1)
                )
            return np.array(sprite)

    def on_collision(self, other):

        if other.get_pawn_type() == 8:
            if other.get_dragon_active() is True:
                self.die()
                other.deactivate_dragon()
            if other.get_shield_active() is True:
                self.die()
                other.set_score(other.get_score() + 20)
        elif other.get_pawn_type() == 9:
            other.die
            self.die()
            other.set_score(other.get_score() + 20)
        else:
            if np.random.random() < 0.5:
                self.die()
            else:
                other.die()

    def generate_color_map(self):
        for i in range(self._sprite.shape[0]):
            for j in range(self._sprite.shape[1]):
                if self._sprite[i, j] in ['-', '|']:
                    self._color_map[i, j] = '\u001b[46m'


class Boss_Enemy(Actor):
    art = '''(/\___   /|\\          ()==========<>_
        \_/ | \\        //|\   ______/ \)
        \_|  \\      // | \_/
            \|\/|\_   //  /\/
            (oo)\ \_//  /
            //_/\_\/ /  |
            @@/  |=\  \  |
                \_=\_ \ |
                \==\ \|\_ 
                __(\===\(  )\\
            (((~) __(_/   |
                    (((~) \  /
                    ______/ /'''.split('\n')

    def __init__(self, position, obj_number, lives):
        art = self.generate_sprite()
        super().__init__(art, position, obj_number, lives=lives)

    def generate_sprite(self):
        m = 0
        for i in self.art:
            if len(i) > m:
                m = len(i)
        b = np.array([' '] * m)
        for i in self.art:
            d = []
            for j in i:
                d.append(j)
            c = [' '] * (m - len(i))
            d += c
            d = np.array(d)
            b = np.vstack((b, d))
        b = b[1:, :]
        return np.array(b)

    def move(self, player, g_size):
        prob = 0.4
        diff = self._position - player.get_position()
        if np.random.random() < prob:
            if diff[0] > 0:
                self._position[0] -= 1
            else:
                self._position[0] += 1

            if self._position[0] < 1:
                self._position[0] = 1
            if self._position[0] + self._sprite.shape[0] >= g_size:
                self._position[0] = g_size - self._sprite.shape[0]

    def on_collision(self, other):
        if other.get_pawn_type() == 9:
            self.die()
            other.die()
            other.set_score(other.get_score() + 20)
        else:
            other.die()

    def launch_bullet(self, obj_number):
        y = np.random.randint(0, self._sprite.shape[0])
        return Boss_Bullet([self._position[0] + y, self._position[1] - 4], obj_number)


class Boss_Bullet(Pawn):
    art = np.array([['<', '-', '-', '|'],
                       ['<', '-', '-', '|']])


    def __init__(self, position, obj_number):
        super().__init__(self.art, position, obj_number, pawn_type=7, 
                         is_solid=False, lives=2)
        self._velocity[1] = - 2
        self._is_solid = False
        self._color_map = np.full(self._sprite.shape, '\u001b[40m')

    def move(self, player, g_size):
        prob = 0.1
        diff = self._position - player.get_position()
        if np.random.random() < prob:
            if diff[0] > 0:
                self._position[0] -= 1
            else:
                self._position[0] += 1

            if diff[1] > 0:
                self._position[1] -= 1
            else:
                self._position[1] += 1

            if self._position[0] < 1:
                self._position[0] = 1
            if self._position[0] + self._sprite.shape[0] >= g_size:
                self._position[0] = g_size - self._sprite.shape[0]

    def on_collision(self, other):
        if other.get_pawn_type() == 9:
            self.die()
            other.set_score(other.get_score() + 20)
        elif other.get_pawn_type() == 8:
            if other.get_dragon_active() is True:
                self.die()
                other.deactivate_dragon()
            if other.get_shield_active() is False:
                self._lives = 1
                self.die()
                other.set_score(other.get_score() + 20)
                other.die()
            else:
                self._lives = 1
                self.die()
        else:
            self._lives = 1
            self.die()
            other.die()
