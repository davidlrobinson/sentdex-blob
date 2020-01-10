import numpy as np

class Blob:
    def __init__(self, np_random, size):
        self.np_random = np_random
        self.size = size
        self.x = self.np_random.randint(0, size)
        self.y = self.np_random.randint(0, size)
        self.pos = (self.x, self.y)
    
    def action(self, choice):
        '''
        Gives us 4 total movement options. (0,1,2,3)
        '''
        if choice == 0:
            self.move(x=1, y=1)
        elif choice == 1:
            self.move(x=-1, y=-1)
        elif choice == 2:
            self.move(x=-1, y=1)
        elif choice == 3:
            self.move(x=1, y=-1)

    def move(self, x=False, y=False):

        # if no value for x, move randomly
        if not x:
            self.x += self.np_random.randint(-1, 2)
        else:
            self.x += x

        # if no value for y, move randomly
        if not y:
            self.y += self.np_random.randint(-1, 2)
        else:
            self.y += y

        # if we are out of bounds, fix
        if self.x < 0:
            self.x = 0
        elif self.x > self.size-1:
            self.x = self.size-1
        if self.y < 0:
            self.y = 0
        elif self.y > self.size-1:
            self.y = self.size-1

        self.pos = (self.x, self.y)

    def reset(self):
        self.x = self.np_random.randint(0, self.size)
        self.y = self.np_random.randint(0, self.size)
        self.pos = (self.x, self.y)