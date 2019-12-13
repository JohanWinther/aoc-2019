
def init(m, noun, verb):
    m[1] = noun
    m[2] = verb

def run(m):
    oci = 0
    oc = m[oci]
    while (oc != 99):
        if oc == 1:
            m[m[oci+3]] = m[m[oci+1]]+m[m[oci+2]]
        elif oc == 2:
            m[m[oci+3]] = m[m[oci+1]]*m[m[oci+2]]
        else:
            break
        oci += 4
        oc = m[oci]
    return m

def find(m, output):
    for noun in range(99):
        for verb in range(99):
            tm = m.copy()
            init(tm, noun, verb)
            run(tm)
            if (tm[0] == output):
                return 100 * noun + verb

with open('day2-input.txt') as f:
    m = [int(n) for n in f.readline().split(',')]

ans = find(m, 19690720)
print(ans)