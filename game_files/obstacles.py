import numpy as np
from pawn import Pawn, Actor


class Firebeam(Pawn):
    def __init__(self, position, obj_number, g_size, lives=1):
        sprite = self.create_sprite(g_size, position)
        super().__init__(sprite, position, obj_number, mass=0, pawn_type=4, lives=lives)

    def create_sprite(self, g_size, position):
        self.type = np.random.randint(1, 4)
        self.size = int(np.random.randint(3, 8))
        self.size = min(self.size, g_size - position[0])
        if self.type == 1:
            # print("E1")
            return np.array(['*'] + ['-'] * (self.size - 2) + ['*']).reshape(1, self.size)
        elif self.type == 2:
            # print("E2")
            return np.array(['*'] + ['|'] * (self.size - 2) + ['*']).reshape(
                self.size, 1)
        else:
            sprite = []
            for i in range(self.size):
                sprite.append(
                    [' '] * i + ['*'] + [' '] * (self.size - i - 1)
                )
            return np.array(sprite)

    def on_collision(self, other):
        if other.pawn_type == 8:  # Player
            other.die()
            if other.lives > 0:
                self.die()
        elif other.pawn_type == 9:
            self.die()
            other.die()
        else:
            if np.random.random() < 0.5:
                self.die()
            else:
                other.die()


class Magnet(Pawn):
    sprite = np.array([['|', '|'],
                       ['-', '-']])

    def __init__(self, position, obj_number, lives=1, force_const=1.5):
        super().__init__(self.sprite, position, obj_number, lives=lives, pawn_type=5)
        self.force_const = force_const
        # self.velocity[1] = 0.5
        self.drag_coeff = 0
        self.is_solid = False

    def on_trigger(self, pawn):
        # print("Entered here")
        dist = np.linalg.norm(self.position - pawn.position)
        diff = self.position - pawn.position
        if pawn.shield_active is False:
            pawn.velocity[0] += self.force_const *\
                    np.round(diff[0]) / (dist**1.44 + 10)
            
            # if diff[0] > 0:
            #     pawn.velocity[0] += min(self.force_const *\
            #         np.round(diff[0]) / (dist**1.8 + 10), 0.5)
            # else: 
            #     pawn.velocity[0] += max(self.force_const *\
            #         np.round(diff[0]) / (dist**1.5 + 10), -0.5)
            pawn.velocity[1] += self.force_const *\
                np.round(diff[1]) / (dist**1.44 + 10)
            # print(dist, "dist")
            # print(self.force_const * int(self.position[1] - pawn.position[1]) / (dist**2 + 1), "X")
            # print(self.force_const * int(np.round(self.position[0] - pawn.position[0])) / (dist**2 + 1), "Y")
            # print(pawn)
        return pawn

# Maybe try to reduce the velocity of the player by a constant times norm
# of the distance between them for each successive frame
# 1/r effectively


class Solid_Objects(Pawn):

    def __init__(self, position, obj_number, g_size, lives=1):
        sprite = self.create_sprite(g_size, position)
        super().__init__(sprite, position, obj_number, mass=0, pawn_type=3, lives=lives)

    def create_sprite(self, g_size, position):
        self.type = np.random.randint(1, 4)
        self.size = int(np.random.randint(3, 8))
        self.size = min(self.size, g_size - position[0])
        if self.type == 1:
            # print("E1")
            return np.array([['|'] + ['-'] + ['-'] * (self.size - 2) + ['-'] + ['|'],
                             ['|'] + ['-'] + ['-'] * (self.size - 2) + ['-'] + ['|']]).reshape(2, self.size + 2)
        elif self.type == 2:
            # print("E2")
            # return np.array(['|'] + ['|'] * (self.size - 2) + ['|']).reshape(
            #     self.size, 1).T
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

        if other.pawn_type == 8:
            if other.shield_active is True:
                self.die()
        elif other.pawn_type == 9:
            other.die
            self.die()
        else:
            if np.random.random() < 0.5:
                self.die()
            else:
                other.die()


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
        sprite = self.generate_sprite()
        super().__init__(sprite, position, obj_number, lives=lives)
        print(sprite.shape)

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
        diff = self.position - player.position
        if np.random.random() < prob:
            if diff[0] > 0:
                self.position[0] -= 1
            else:
                self.position[0] += 1

            if self.position[0] < 1:
                self.position[0] = 1
            if self.position[0] + self.sprite.shape[0] >= g_size:
                self.position[0] = g_size - self.sprite.shape[0]

    def on_collision(self, other):
        if other.pawn_type == 9:
            self.die()
            other.die()
        else:
            other.die()

    def launch_bullet(self, obj_number):
        y = np.random.randint(0, self.sprite.shape[0])
        return Boss_Bullet([self.position[0] + y, self.position[1] - 4], obj_number)


class Boss_Bullet(Pawn):
    sprite = np.array([['<', '-', '-', '|'],
                       ['<', '-', '-', '|']])

    def __init__(self, position, obj_number):
        super().__init__(self.sprite, position, obj_number, pawn_type=7, 
                         is_solid=False, lives=2)
        self.velocity[1] = - 2
        self.is_solid = False

    def move(self, player, g_size):
        prob = 0.1
        diff = self.position - player.position
        if np.random.random() < prob:
            if diff[0] > 0:
                self.position[0] -= 1
            else:
                self.position[0] += 1

            if diff[1] > 0:
                self.position[1] -= 1
            else:
                self.position[1] += 1

            if self.position[0] < 1:
                self.position[0] = 1
            if self.position[0] + self.sprite.shape[0] >= g_size:
                self.position[0] = g_size - self.sprite.shape[0]

    def on_collision(self, other):
        if other.pawn_type == 9:
            self.die()
        elif other.pawn_type == 8:
            if other.shield_active is False:
                self.lives = 1
                self.die()
                other.die()
            else:
                self.lives = 1
                self.die()
        else:
            self.lives = 1
            self.die()
            other.die()
