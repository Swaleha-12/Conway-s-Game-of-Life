import time
from tkinter import *
import copy
import math

import random


w = 32

'''Linear Probing Implementation'''


class LinearDict:
    def __init__(self):
        self.randomInt = random.randrange(1, 101, 2)
        self.width = 1
        self.data = 0
        self.nonNone = 0
        self.table = [()] * 2**self.width

    def __setitem__(self, key, value):
        if 2 * (self.nonNone + 1) > 2**self.width:
            self.resize()
        hashIndex = hashFunction(self.randomInt, key, self.width)
        while self.table[hashIndex] != () and self.table[hashIndex] != "" and self.table[hashIndex][0] != key:
            hashIndex = (hashIndex + 1) % 2**self.width
        if self.table[hashIndex] == ():
            self.nonNone += 1
            self.data += 1
        self.table[hashIndex] = (key, value)

    def get(self, coord, defaultVal):
        hashIndex = hashFunction(self.randomInt, coord, self.width)
        while self.table[hashIndex] != ():
            if coord == self.table[hashIndex][0]:
                return self.table[hashIndex][1]
            hashIndex = (hashIndex + 1) % 2**self.width
        return defaultVal

    def items(self):
        for i in self.table:
            if len(i) != 0:
                yield i

    def __iter__(self):
        for i in self.table:
            if len(i) != 0:
                yield i

    def clear(self):
        self.randomInt = random.randrange(1, 101, 2)
        self.width = 1
        self.data = 0
        self.nonNone = 0
        self.table = [()] * 2**self.width

    def resize(self):
        self.width = int(math.log2(3*self.data))
        self.width += 1
        table = self.table
        self.table = [()] * 2**self.width
        self.nonNone = self.data
        for coord in table:
            if coord != "" and coord != ():
                hashIndex = hashFunction(self.randomInt, coord[0], self.width)
                while self.table[hashIndex] != ():
                    hashIndex = (hashIndex + 1) % 2**self.width
                self.table[hashIndex] = coord


class LinearSet:
    def __init__(self, state):
        self.randomInt = random.randrange(1, 101, 2)
        self.width = 1
        self.data = 0
        self.nonNone = 0
        self.table = [None] * 2**self.width
        for i in state:
            self.add(i)

    def add(self, coord):
        if self.find(coord) != None:
            return False
        if 2 * (self.nonNone + 1) > 2**self.width:
            self.resize()
        hashIndex = hashFunction(self.randomInt, coord, self.width)
        while self.table[hashIndex] != None and self.table[hashIndex] != "":
            hashIndex = (hashIndex + 1) % 2**self.width
        if self.table[hashIndex] == None:
            self.nonNone += 1
        self.data += 1
        self.table[hashIndex] = coord
        return True

    def find(self, coord):
        hashIndex = hashFunction(self.randomInt, coord, self.width)
        while self.table[hashIndex] != None:
            if self.table[hashIndex] != "" and coord == self.table[hashIndex]:
                return self.table[hashIndex]
            hashIndex = (hashIndex + 1) % 2**self.width

    def discard(self, coord):
        hashIndex = hashFunction(self.randomInt, coord, self.width)
        while self.table[hashIndex] != None:
            y = self.table[hashIndex]
            if y != "" and coord == y:
                self.table[hashIndex] = ""
                self.data -= 1
                if 8 * self.data < 2**self.width:
                    self.resize()
                return y
            hashIndex = (hashIndex + 1) % 2**self.width
        return None

    def __iter__(self):
        for i in self.table:
            if i != None and i != "":
                yield i

    def resize(self):
        self.width = int(math.log2(3*self.data))
        self.width += 1
        table = self.table
        self.table = [None] * 2**self.width
        self.nonNone = self.data
        for coord in table:
            if coord != "" and coord != None:
                hashIndex = hashFunction(self.randomInt, coord, self.width)
                while self.table[hashIndex] != None:
                    hashIndex = (hashIndex + 1) % 2**self.width
                self.table[hashIndex] = coord


def hashFunction(randomInt, coord, d):
    return ((randomInt*hash(coord)) % 2**(32)) >> (32 - d)


"""A Set implementation that uses hashing with chaining"""


class ChainedSet:
    def __init__(self, state):
        self.d = 1
        self.t = self._alloc_table((1 << self.d))
        self.z = self._random_odd_int()
        self.n = 0
        for i in state:
            self.add(i)

    def _random_odd_int(self):
        return random.randrange(1 << w) | 1

    def _alloc_table(self, s):
        return [[] for _ in range(s)]

    def _resize(self):
        temp = self.t
        self.t = []
        self.d = int(math.log2(3*self.n))
        if self.d < 1:
            self.d = 1
        self.t = self._alloc_table(2**self.d)
        self.n = 0
        for i in temp:
            for coord in i:
                self.add(coord)

    def _hash(self, x):
        return ((self.z * hash(x)) % (2 ** w)) >> (w-self.d)

    def add(self, x):
        if self.find(x) is not None and self.find(x) != []:
            return False
        if self.n+1 >= 2**self.d:
            self._resize()
        self.t[self._hash(x)].append(x)
        self.n += 1
        return True

    def discard(self, x):
        index = self._hash(x)
        for y in self.t[index]:
            if y == x:
                self.t[index].remove(y)
                self.n -= 1
                if (3*self.n) < 2**self.d:
                    self._resize()
                return y
        return None

    def find(self, x):
        for y in self.t[self._hash(x)]:
            if y == x:
                return y
        return None

    def __iter__(self):
        for ell in self.t:
            for x in ell:
                yield x


class ChainedDict():

    def __init__(self, iterable=[]):
        self.d = 1
        self.t = self._alloc_table((1 << self.d))
        self.z = self._random_odd_int()
        self.n = 0

    def _random_odd_int(self):
        return random.randrange(1 << w) | 1

    def clear(self):
        self.d = 1
        self.t = self._alloc_table((1 << self.d))
        self.n = 0

    def _alloc_table(self, s):
        return [[] for _ in range(s)]

    def _resize(self):
        old_t = self.t
        self.d = int(math.log2(3*self.n))
        if self.d < 1:
            self.d = 1
        self.t = self._alloc_table(2**self.d)
        self.n = 0
        for i in old_t:
            for key, neigh in i:
                self.add((key, neigh))

    def _hash(self, x):
        return ((self.z * hash(x)) % (2 ** w)) >> (w-self.d)

    def add(self, x, neighbour=0):
        if self.find(x) is not None:
            return False
        if self.n+1 >= len(self.t):
            self._resize()
        self.t[self._hash(x)].append((x, neighbour))
        self.n += 1
        return True

    def find(self, x):
        for y in self.t[self._hash(x)]:
            if y[0] == x:
                return y
        return None

    def __iter__(self):
        for ell in self.t:
            for x in ell:
                yield x
                
    def get(self, key, defaultValue) -> int:
        hashedIndex = self._hash(key)
        for i in range(len(self.t[hashedIndex])):
            if self.t[hashedIndex][i][0] == key:
                return self.t[hashedIndex][i][1]
        self.add(key)
        return defaultValue

    def __setitem__(self, key, value):
        index = self._hash(key)
        for i in range(len(self.t[index])):
            if self.t[index][i][0] == key:
                self.t[index][i] = (key, value)

    def items(self):
        for i in self.t:
            for j in i:
                yield j


# An implementation of Conway's Game of Life
#
# Adapted from code by Abdullah Zafar


class Config:
    """Config class.
    Contains game configurations .
    """

    # Some starting configurations.
    glider = [(20, 40), (21, 40), (22, 40),
              (22, 41), (21, 42)]  # simple glider
    dense = [(21, 40), (21, 41), (21, 42), (22, 41),
             (20, 42)]  # explodes into a dense network
    oscillator = [(1, 4), (2, 4), (3, 4)]  # oscillator
    block = [(4, 4), (5, 4),
             (4, 5), (5, 5)]  # Block

    def __init__(self) -> None:
        """Provides a default configuration.
        Args:
        - self: automatic object reference.
        Returns:
        none
        """
        # ===== Life parameters
        self.start = Config.glider  # starting shape
        self.rounds = 5000  # number of rounds of the game

        # ===== Animation parameters
        self.animate: bool = False  # switch animation on or off
        # Screen dimensions
        self.width: int = 800
        self.height: int = 800
        # HU colors
        self.bg_color = '#e6d19a'
        self.cell_color = '#580f55'
        # Cell size. Cells are drawn at resolution CELL_SIZE x CELL_SIZE pixels.
        self.cell_size: int = 10
        # Animation speed. Positive integers, bigger is faster animation.
        self.speed: int = 1


class Life:
    """Life class.
    The state of the game.
    """

    def __init__(self, state: [(int, int)], chain: bool = True) -> None:
        """Initializes game state and internal variables.
        Args:
        - self: automatic object reference.
        - state: initial congifuration - (x,y) coordinates of live cells
        - chain: controls whether to use chaining (True) or linear probiing (False)
        Returns:
        none
        """
        # USet implementations.
        self._alive = None  # intial config: (x, y) coordinates of alive cells.
        self._nbr_count = None  # stores count of live neighbors for cells.

        if chain:
            self._alive: ChainedSet = ChainedSet(state)
            self._nbr_count: ChainedDict = ChainedDict()
        else:
            self._alive: LinearSet = LinearSet(state)
            self._nbr_count: LinearDict = LinearDict()

    def step(self) -> None:
        """One iteration of the game.
        Applies game rules on current live cells in order to compute the next state of the game.
        Args:
        - self: automatic object reference.
        Returns:
        none
        """
        # Compute neighbors of current live cells.
        deltas = [(-1, -1), (0, -1), (1, -1),
                  (-1,  0),          (1,  0),
                  (-1,  1), (0,  1), (1,  1)]
        neighbors = [(x+dx, y+dy) for x, y in self._alive
                     for dx, dy in deltas]
        # Collect the number of times each coordinate appears as a
        # neighbor. That provides a count of the number of live neighbors of
        # these cells.
        for coord in neighbors:
            self._nbr_count[coord] = self._nbr_count.get(coord, 0) + 1
        # Apply rules based on numberof neighbors.
        for coord, count in self._nbr_count.items():
            # Alive cells with too few or too many alive neighbors die.
            if count == 1 or count > 3:
                self._alive.discard(coord)
            # Cells with 3 alive neighbors come alive.
            elif count == 3:
                self._alive.add(coord)
            # All other live cells survive.
        # Clear for next iteration.
        self._nbr_count.clear()

    def state(self) -> [(int, int)]:
        """Returns the current state of the game.
        Args:
        - self: automatic object reference.
        Returns:
        Coordinates of live cells .
        """
        # self._alive must be iterable, https://stackoverflow.com/a/37639615/1382487
        return list(self._alive)


class Game:
    def run(life, config) -> None:
        """Runs the game as per config.
        Args:
        - life: the instance to run.
        - config: contains game configurations.
        Returns:
        nothing.
        """
        # Set up animation if required.
        if config.animate:
            # Use tkinter. Set up the rendering window.
            tk = Tk()
            canvas = Canvas(tk, width=config.width, height=config.height)
            tk.title("Game of Life")
            canvas.configure(background=config.bg_color)
            # Indicate that rendering will be in cells.
            canvas.pack()
            # Number of rendered cells in each direction.
            cells_x = config.width // config.cell_size
            cells_y = config.height // config.cell_size

        # Make the required number of iterations.
        for i in range(config.rounds):
            # Animate if specified.
            if config.animate:
                # Clear canvas and add cells as per current state.
                canvas.delete('all')
                for x, y in life.state():
                    # Wrap cell around screen boundaries. Comment for no wrap.
                    x %= cells_x
                    y %= cells_y
                    # Add cell to canvas.
                    x1, y1 = x * config.cell_size, y * config.cell_size
                    x2, y2 = x1 + config.cell_size, y1 + config.cell_size
                    canvas.create_rectangle(
                        x1, y1, x2, y2, fill=config.cell_color)
                # Render cells, pause for next iteration.
                tk.update()
                time.sleep(0.1 / config.speed)
            # Advanmce the game by one step.
            life.step()


def main():
    config = Config()
    config.animate = True
    config.rounds = 1000
    config.start = Config.glider
    config.speed = 5
    life = Life(config.start, False)
    Game.run(life, config)


if __name__ == '__main__':
    main()
