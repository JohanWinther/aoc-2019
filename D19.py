from intcode import Intcode
from math import floor
import sys

with open(__file__.replace(".py", "I.txt")) as f:
    t = f.read().split(',')
comp = Intcode(m=[int(n) for n in t])

def print_beam(x_range=(0, 50), y_range=(0, 50)):
    stdout = sys.stdout
    sys.stdout = open('D19-output.txt','w')
    s = 0
    t = ''
    for y in range(y_range[0],y_range[1]):
        for x in range(x_range[0],x_range[1]):
            comp.reset()
            comp.set_input(x)
            comp.set_input(y)
            comp.run()
            n = comp.output_buffer.pop()
            if n:
                print('#', end='')
            else:
                print('.', end='')
            s += n
        print('\n', end='')
    sys.stdout = stdout
    print(s)

def is_in_beam(x, y):
    comp.reset()
    comp.set_input(x)
    comp.set_input(y)
    comp.run()
    return comp.output_buffer.pop()

# Part 1
#print_beam()

# Part 2
def get_lower_k(y=100, x=100):
    t = 0
    while t == 0:
        comp.reset()
        comp.set_input(x)
        comp.set_input(y)
        comp.run()
        t = comp.output_buffer.pop()
        x += 1
    return x / y


def coord(start, end=0):
    n = 1
    y = start
    while n:
        x = floor(lower_k * y)
        n = is_in_beam(x, y)
        if n:
            while is_in_beam(x, y):
                x -= 1
            x += 1
        else:
            while not is_in_beam(x, y):
                x += 1
        yield((x, y))
        y += 1
        if end > 0 and y > end:
            n = 0

lower_k = get_lower_k()
gen = coord(1000)
in_beam = False
while not in_beam:
    c = next(gen)
    in_beam = is_in_beam(c[0] + 99, c[1] - 99)
closest = (c[0], c[1]-99)
print(closest)
print(10000*closest[0] + closest[1])
#print_beam((c[0], c[0] + 100), (c[1] - 100, c[1]))
