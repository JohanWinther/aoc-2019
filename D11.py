from intcode import Intcode
from cmath import exp, pi

class HullPaintingRobot():
    def __init__(self, brain, wall={}):
        self.brain = brain
        self.wall = wall
        self.x = 0
        self.y = 0
        self.direction = 0
        self.painted_panels = 0

    def step(self):
        # Read panel
        coord = (self.x, self.y)
        panel_painted_before = True
        if coord not in self.wall:
            self.wall[coord] = 0
            panel_painted_before = False
        self.brain.set_input(self.wall[coord])
        self.brain.run_until_output()
        if self.brain.completed:
            return
        # Draw panel
        self.wall[coord] = self.brain.output_buffer.pop(0)
        if not panel_painted_before:
            self.painted_panels += 1
        # Turn
        self.brain.run_until_output()
        self.direction = (self.direction + (self.brain.output_buffer.pop(0) * 2 - 1)) % 4
        # Move
        c = exp(1j * pi / 2 * (self.direction - 1))
        self.x += round(c.real)
        self.y += round(c.imag)

    def start(self):
        while not self.brain.completed:
            self.step()

# Day 11.1
print("Day 11.1")
# Solution
print("Solution:")
with open(__file__.replace(".py", "I.txt")) as f:
    t = f.read()
m = [int(n) for n in t.split(',')]
robot = HullPaintingRobot(Intcode(m))
robot.start()
out = robot.painted_panels
print(out)