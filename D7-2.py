from intcode import Intcode


def get_thruster_input(amps, phases):
    for amp, phase in zip(amps, phases):
        amp.set_input(phase)
        amp.run_step()

    amps[0].set_input(0)
    while not amps[-1].completed:
        for i in range(len(amps)):
            if not amps[i].completed:
                amps[i].run_step()
    return amps[-1].output_buffer[0]

def num_to_array(p, l):
    a = []
    while p > 0:
        a.insert(0, p % 10)
        p //= 10
    while len(a) < l:
        a.insert(0, 0)
    return a


with open('D7I.txt') as f:
    t = f.read().rstrip('\n')
#t = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
t = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
m = [int(n) for n in t.split(',')]

amps = ['A', 'B', 'C', 'D', 'E']
amps = [Intcode(m, name=f'Amp {amp}') for amp in amps]
#for i in range(len(amps)):
#    amps[i].set_next(amps[(i+1) % len(amps)])


max_thrust = 0
#for phases in range(55555, 99999 + 1):
for phases in [98765, 97856]:
    for i, amp in enumerate(amps):
        amps[i].set_previous(amps[(i-1) % len(amps)])
        amp.reset()
    phases = num_to_array(phases, 5)
    if len(list(set(phases))) == 5:
        new_thrust = get_thruster_input(amps, phases)
        if new_thrust > max_thrust:
            max_thrust = new_thrust
            max_phase = phases

print(max_thrust, max_phase)
