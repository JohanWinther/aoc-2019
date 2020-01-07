from intcode import Intcode

with open(__file__.replace(".py", "I.txt")) as f:
    t = f.read().split(',')
comp = Intcode(m=[int(n) for n in t])

# Part 1
s = 0
for x in range(50):
    for y in range(50):
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
print(s)

# Part 2