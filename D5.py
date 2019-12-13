
op_params = [
    0,  # undefined
    3,  # add
    3,  # multiply
    1,  # input
    1,  # output
    2,  # jump-if-true
    2,  # jump-if-false
    3,  # less than
    3,  # equals
    ]

def run(inp=None):
    global m, ip

    oc = (m[ip] % 100, m[ip]//100)
    while (oc[0] != 99):
        opcode(oc, m[ip+1:ip+1+op_params[oc[0]]], inp)
        oc = (m[ip] % 100, m[ip]//100)

def opcode(oc, params, inp):
    global m, ip
    values = [m[p] if oc[1]//10**i % 10 == 0 else p
                                    for i, p in enumerate(params)]
    if oc[0] == 1:
        m[params[2]] = values[0] + values[1]
    elif oc[0] == 2:
        m[params[2]] = values[0] * values[1]
    elif oc[0] == 3:
        m[params[0]] = inp
    elif oc[0] == 4:
        print(values[0])
    elif oc[0] == 5:
        if values[0]:
            ip = values[1]
            return
    elif oc[0] == 6:
        if values[0] == 0:
            ip = values[1]
            return
    elif oc[0] == 7:
        m[params[2]] = int(values[0] < values[1])
    elif oc[0] == 8:
        m[params[2]] = int(values[0] == values[1])
    else:
        raise ValueError('Unkown opcode.')
    ip += len(params)+1

global m, ip
m = []
ip = 0

with open('D5I.txt') as f:
    t = f.read().rstrip('\n')
#t = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"
#t = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
m = [int(n) for n in t.split(',')]

run(5)