from intcode import Intcode
from screen import Screen
import time

class Arcade():
    def __init__(self):
        with open(__file__.replace(".py", "I.txt")) as f:
            t = f.read().rstrip()
        self.brain = Intcode([int(n) for n in t.split(',')])
        self.grid = {}
        self.screen = None
        self.grid_drawn = False
        self.paddle = (0, 0)
        self.ball = (0, 0)

    def start(self):
        self.brain.m[0] = 2
        di = self.drawing_instruction()
        while not self.brain.completed:
            instruction = next(di)
            if instruction:
                self.draw(instruction)
                self.screen.send_message(','.join([str(n) for n in instruction]))

                if instruction[2] == 3:
                    self.paddle = (instruction[0], instruction[1])
                elif instruction[2] == 4:
                    self.ball = (instruction[0], instruction[1])
                if instruction[2] == 4:
                    direction = (self.paddle[0] < self.ball[0]) - (self.paddle[0] > self.ball[0])
                    self.brain.set_input(direction)
                    #time.sleep(60/124)

    def drawing_instruction(self):
        while True:
            out = []
            for i in range(3):
                self.brain.run_until_output()
                if not self.brain.completed:
                    out.append(self.brain.output_buffer.popleft())
            yield out

    def draw(self, instruction):
        self.grid[(instruction[0], instruction[1])] = instruction[2]

    def print_grid(self):
        for y in range(max(self.grid, key=lambda x: x[1])[1]+1):
            for x in range(max(self.grid)[0] + 1):
                print(str(self.grid[(x, y)]), end='')
            print('\n', end='')

    def num_of_tiles(self, tile_id):
        tiles = 0
        for y in range(max(self.grid, key=lambda x: x[1])[1]+1):
            for x in range(max(self.grid)[0] + 1):
                if self.grid[(x, y)] == tile_id:
                    tiles += 1
        return tiles

#machine = Arcade()
#machine.start()
# Day 13.1
#print(machine.num_of_tiles(2))

screen = Screen()
arcade = Arcade()
arcade.screen = screen
#screen.arcade = arcade
screen.run()
time.sleep(2)
arcade.start()
