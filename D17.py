from intcode import Intcode
from collections import deque
from time import sleep
import sys

class ASCII():
    def __init__(self, wakeup=False):
        with open(__file__.replace(".py", "I.txt")) as f:
            t = f.read()
        m = [int(n) for n in t.split(',')]
        if wakeup:
            m[0] = 2
        self.computer = Intcode(m)
        self.image = ""
        self.grid = []
        self.directions = [">","v","<","^",]
        self.robot = [0, 0, 0]
        self.dust = 0

    def get_image(self):
        self.image = ""
        x = y = 0
        while not self.computer.completed:
            self.computer.run_until_output()
            if self.computer.output_buffer:
                num = self.computer.output_buffer.popleft()
                if num > 127:
                    self.dust = num
                    break
                else:
                    char = chr(num)
                    self.image += char
                    if self.image[-2:] == '\n\n':
                        break
                if char in self.directions:
                    self.robot = [x, y, self.directions.index(char)]
                if char == '\n':
                    y += 1
                    x = 0
                else:
                    x += 1
        if self.image and (self.image[0] == "#" or self.image[0] == "."):
            self.grid = [[(1 if x != "." else 0) for x in y] for y in self.image.rstrip().lstrip().split('\n')]

    def print_image(self):
        if self.image and (self.image[0] == "#" or self.image[0] == "."):
            sysout = sys.stdout
            sys.stdout = open('D17-camera.txt', 'w')
            print(self.image.replace('.', ' ').replace('#', "■"))
            sys.stdout = sysout

    def get_intersections(self):
        for y in range(1, len(self.grid) - 1):
            for x in range(1, len(self.grid[y]) - 1):
                if self.grid[y][x] and all(self.get_neighbors(x, y)):
                    yield [x, y]

    def get_alignment_params(self):
        return sum([i[0] * i[1] for i in self.get_intersections()])

    def movement(self, instr_str):
        for i in instr_str:
            self.computer.input_buffer.append(ord(i))

    def get_neighbors(self, x, y):
        return [
            self.grid[y][x+1] if x < len(self.grid[0])-1 else 0,
            self.grid[y+1][x] if y < len(self.grid)-1 else 0,
            self.grid[y][x-1] if x > 0 else 0,
            self.grid[y-1][x] if y > 0 else 0,
        ]

    def get_path(self):
        x = self.robot[0]
        y = self.robot[1]
        d = self.robot[2]
        movements = []
        offsets = [1,0,-1,0]
        neighbors = self.get_neighbors(x, y)

        while sum(neighbors) > 1 or len(movements) < 2:
            if neighbors[d]:
                if isinstance(movements[-1], int):
                    movements[-1] += 1
                else:
                    movements.append(1)
                x += offsets[d]
                y += offsets[(d - 1) % 4]
            else:
                neighbors[(d + 2) % 4] = 0
                td = neighbors.index(1)
                movements.append('L' if (td - d) == -1 or (td - d) == 3 else 'R')
                d = td
            neighbors = self.get_neighbors(x, y)
        return movements

    def get_instructions(self):
        moves = ",".join([str(n) for n in self.get_path()])
        funs = ['A', 'B', 'C']
        mov = []
        k = 0
        for f in funs:
            while moves[k] in funs:
                k += 2
            for i in reversed(range(k, 20 + k)):
                pattern = moves[k:i+1].split('A')[0].split('B')[0].split('C')[0]
                if moves.count(pattern) > 1:
                    mov.append(pattern[:-1])
                    moves = moves.replace(pattern[:-1], f)
                    break
        mov.insert(0, moves)
        return "\n".join(mov)

    def start(self, cont='n'):
        camera.get_image()
        camera.print_image()
        sleep(2)
        self.movement(self.get_instructions() + f'\n{cont}\n')
        while self.image:
            self.get_image()
            self.print_image()
        return self.dust
# Part 1
camera = ASCII()
camera.get_image()
camera.print_image()
print(camera.get_alignment_params())

# Part 2
camera = ASCII(wakeup=True)
dust = camera.start()
print(dust)