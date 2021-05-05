from random import randint
import time
import numpy as np

LEFT = 1
RIGHT = -1
TOP = 1
BOTTOM = -1

class Emulator: 

    def __init__(self):
        self._data = np.array([0 for i in range(64)], dtype=int)
        # [0 for i in range(64)]
        self.hot_point_coordinate = [ 4, 4]

    def update(self):
        self.update_data()

    def update_data(self):
        i = 0
        for y in range(8):
            for x in range(8):
                self._data[i] = randint(0, 256)
                i += 1
 
    @property
    def data(self):
        return self._data

if __name__ == "__main__":
    pass