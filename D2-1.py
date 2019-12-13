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


with open('day2-input.txt') as f:
    m = [int(n) for n in f.readline().split(',')]

m[1] = 12
m[2] = 2

print(run(m))
