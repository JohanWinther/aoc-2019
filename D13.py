from intcode import Intcode

class Arcade():
    def __init__(self):
        with open(__file__.replace(".py", "I.txt")) as f:
            t = f.read().rstrip()
        self.brain = Intcode([int(n) for n in t.split(',')])
        self.grid = {}
        self.tiles = {
            0: '  ',
            1: '⬛ ',
            2: '⬜ ',
            3: '➖ ',
            4: '⚽ ',
        }

    def start(self):
        di = self.drawing_instruction()
        while not self.brain.completed:
            instruction = next(di)
            if instruction:
                self.draw(instruction)
                if instruction[0] == 36 and instruction[1] == 25:
                    self.print_grid()

    def drawing_instruction(self):
        while True:
            out = []
            for i in range(3):
                self.brain.run_until_output()
                if not self.brain.completed:
                    out.append(self.brain.output_buffer.pop(0))
            yield out

    def draw(self, instruction):
        self.grid[(instruction[0], instruction[1])] = instruction[2]

    def print_grid(self):
        for y in range(max(self.grid, key=lambda x: x[1])[1]+1):
            for x in range(max(self.grid)[0] + 1):
                print(self.tiles[self.grid[(x, y)]], end='')
            print('\n', end='')

    def num_of_tiles(self, tile_id):
        tiles = 0
        for y in range(max(self.grid, key=lambda x: x[1])[1]+1):
            for x in range(max(self.grid)[0] + 1):
                if self.grid[(x, y)] == tile_id:
                    tiles += 1
        return tiles

machine = Arcade()
machine.start()
# Day 13.1
print(machine.num_of_tiles(2))