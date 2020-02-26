from itertools import combinations
from intcode import Intcode
from pprint import pprint

def bool_to_sc(bool_expr, end="WALK"):
    sc_bool = bool_expr.split(" ")
    sc = ''
    for i, v in enumerate(sc_bool):
        if i == 0:
            if v[0] == '!':
                sc += f'NOT {v[1]} J\n'
            else:
                sc += f'NOT {v[0]} T\nNOT T J\n'
        elif i % 2 == 1:
            current_operator = "AND" if v == '&' else 'OR'
        elif i % 2 == 0:
            if v[0] == '!':
                sc += f'NOT {v[1]} T\n{current_operator} T J\n'
            else:
                sc += f'{current_operator} {v[0]} J\n'
    sc += end+'\n'
    return sc

with open(__file__.replace(".py", "I.txt")) as f:
    t = f.read()
m = [int(n) for n in t.split(',')]
computer = Intcode(m)

sc_bool = "D & !C | !A"
sc = bool_to_sc(sc_bool)

out = 0
while out != 10:
    computer.run_until_output()
    out = computer.output_buffer.popleft()
    print(chr(out), end='')

for c in sc:
    computer.set_input(ord(c))
print("\n".join(["{:2d} ".format(idx + 1) + instruction for idx,
                 instruction in enumerate(sc.split("\n")[:-2])]))

computer.run()

print("".join([chr(c) if c < 0x110000 else str(c) for c in list(computer.output_buffer)]))


computer.reset()

# Part 2
sc = ('''
NOT A J
AND D J
NOT B T
AND D T
AND H T
OR  T J
NOT C T
AND D T
AND E T
OR  T J
NOT C T
AND D T
AND H T
OR  T J
RUN
''')[1:]

out = 0
while out != 10:
    computer.run_until_output()
    out = computer.output_buffer.popleft()
    print(chr(out), end='')

for c in sc:
    computer.set_input(ord(c))
print("\n".join(["{:2d} ".format(idx + 1) + instruction for idx,
                 instruction in enumerate(sc.split("\n")[:-2])]))

computer.run()

print("".join([chr(c) if c < 0x110000 else str(c)
               for c in list(computer.output_buffer)]))
