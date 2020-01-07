from intcode import Intcode
from collections import deque

import sys

class ASCII():
    def __init__(self):
        with open(__file__.replace(".py", "I.txt")) as f:
            t = f.read()
        self.computer = Intcode(m=[int(n) for n in t.split(',')])
        self.image = ""
        self.grid = []
        self.directions = [">","v","<","^",]
        self.robot = [0,0,0]
    
    def get_image(self):
        self.image = ""
        self.computer.run()

        x = y = 0
        while self.computer.output_buffer:
            char = chr(self.computer.output_buffer.popleft())
            self.image += char
            if char in self.directions:
                self.robot = [x, y, self.directions.index(char)]
            if char == '\n':
                y += 1
                x = 0
            else:
                x += 1
        self.image = self.image.rstrip().lstrip()
        self.grid = [[(1 if x == "#" else 0) for x in y] for y in self.image.split('\n')]

    def print_image(self):
        sysout = sys.stdout
        sys.stdout = open('D17-camera.txt', 'w')
        self.image = (self.image 
            .replace('.', ' ')
            .replace('#', "■")
            #.replace(">", "➡")
            #.replace("v", "🠻")
            #.replace("^", "🠹")
            #.replace("<", "🠸")
        )
        print(self.image)
        sys.stdout = sysout

    def get_intersections(self):
        for y in range(1, len(self.grid) - 1):
            for x in range(1, len(self.grid[y]) - 1):
                if self.grid[y][x] and all([
                    self.grid[y][x+1],
                    self.grid[y+1][x],
                    self.grid[y][x-1],
                    self.grid[y-1][x],
                ]):
                    yield [x, y]

    def get_alignment_params(self):
        return sum([i[0] * i[1] for i in self.get_intersections()])

camera = ASCII()
camera.get_image()
camera.print_image()
print(camera.get_alignment_params())
