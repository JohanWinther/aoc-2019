from intcode import Intcode
from itertools import permutations

def calculate_thrust(amps, phases):
    for amp, phase in zip(amps, phases):
        amp.reset()
        amp.set_input(phase)
        amp.run_step()
    
    amps[0].set_input(0)
    for amp in amps:
        amp.run_until_output()
    return amps[-1].output_buffer[0]


with open('D7I.txt') as f:
    t = f.read().rstrip('\n')
#t = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
#t = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
#t = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
m = [int(n) for n in t.split(',')]

amps = ['A', 'B', 'C', 'D', 'E']
amps = [Intcode(m, name=f'Amp {amp}') for amp in amps]
for i, amp in enumerate(amps):
    amp.set_previous(amps[(i-1) % len(amps)])

max_thrust = 0
for phases in map(list, permutations(range(4))):
    new_thrust = calculate_thrust(amps, phases)
    if new_thrust > max_thrust:
        max_thrust = new_thrust
        max_phase = phases

print(max_thrust, max_phase)
