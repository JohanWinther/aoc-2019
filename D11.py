from intcode import Intcode
from cmath import exp, pi

class HullPaintingRobot():
    def __init__(self, brain, hull={}):
        self.brain = brain
        self.hull = hull
        self.x = 0
        self.y = 0
        self.direction = 0
        self.painted_panels = 0

    def step(self):
        # Read panel
        coord = (self.x, self.y)
        panel_painted_before = True
        if coord not in self.hull:
            self.hull[coord] = 0
            panel_painted_before = False
        if self.painted_panels:
            self.brain.set_input(self.hull[coord])
        else:
            self.brain.set_input(1)
        self.brain.run_until_output()
        if self.brain.completed:
            return
        # Draw panel
        self.hull[coord] = self.brain.output_buffer.pop(0)
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

    def print_hull(self):
        edges = (
            min(self.hull)[0], min(self.hull, key=lambda x: x[1])[1],
            max(self.hull)[0], max(self.hull, key=lambda x: x[1])[1]
            )
        absolute_hull = {(k[0] - edges[0], k[1] - edges[1]): v for k, v in self.hull.items()}
        for y in range(edges[3] - edges[1] + 1):
            for x in range(edges[2] - edges[0] + 1):
                c = (x, y)
                t = "⬛ "
                if c in absolute_hull:
                    if absolute_hull[c]:
                        t = "⬜ "
                print(t, end='')
            print('\n', end='')
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

# Day 11.2
print("Day 11.2")
# Solution
print("Solution:")
robot = HullPaintingRobot(Intcode(m))
robot.start()
robot.print_hull()
