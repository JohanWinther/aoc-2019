from math import ceil

def rx_in_rx_list(rx, rx_list):
    for r in rx_list:
        for i in rx_list[r][1]:
            if i[0] == rx:
                return True
    return False

t ='''
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
''' .lstrip().rstrip()
with open(__file__.replace(".py", "I.txt")) as f:
    t = f.read().rstrip().lstrip()
rxs_txt = t.split('\n')
rxs = {}

for l in rxs_txt:
    inputs, output = l.split('=>')
    output = output.lstrip().rstrip().split(' ')
    output[0] = int(output[0])
    inputs = [[inp.split(' ')[1], int(inp.split(' ')[0])] for inp in inputs.lstrip().rstrip().split(', ')]
    rxs[output[1]] = (output[0],inputs)

def number_of_ores(rxs, fuel=1):
    s = [['FUEL',fuel]]
    while len(rxs):
        k = 0
        for i, v in enumerate(s):
            if not rx_in_rx_list(v[0], rxs):
                k = i
                break
        ratio = ceil(s[k][1] / rxs[s[k][0]][0])
        for r in rxs[s[k][0]][1]:
            s_keys = [i[0] for i in s]
            if r[0] not in s_keys:
                s.append([r[0], r[1]*ratio])
            else:
                s[s_keys.index(r[0])][1] += r[1] * ratio
        del (rxs[s[k][0]])
        s.pop(k)

    return s[0][1]

# Day 14.1
n = number_of_ores(rxs.copy())
print(n)

# Day 14.2
N = 1000000000000
l = []
for i in range(1,10000):
    l.append(number_of_ores(rxs.copy(), fuel=i)//i)
k = sum(l) // len(l) - 2
k += 10

f_guess = N // k
print(f'Start guess: {f_guess}')
ore = number_of_ores(rxs.copy(), fuel=f_guess)
while abs(ore - N) > n//2:
    if ore > N:
        direction = -1
    else:
        direction = 1
    f_guess += direction
    ore = number_of_ores(rxs.copy(), fuel=f_guess)
fuel = f_guess + direction - (1 if direction == 1 else 0)

for i in range(9):
    if i == 4:
        print(fuel, number_of_ores(rxs.copy(), fuel=fuel), '*')
    else:
        print(fuel+i-4, number_of_ores(rxs.copy(), fuel=fuel+i-4))
