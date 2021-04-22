import numpy as np

class Blob:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y, bound):
        self.x = np.clip(self.x + x, 0, bound)
        self.y = np.clip(self.y + y, 0, bound)

    @property
    def pos(self):
        return (self.x, self.y)

    def __repr__(self):
        return f'{self.__class__.__name__!r}(x={self.x!r}, y={self.y!r})'