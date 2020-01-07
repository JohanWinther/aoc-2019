def print_signal(signal, l=None):
    if l:
        s = signal[:l]
    else:
        s = signal
    print("".join([str(n) for n in s]))

def transform_phases(signal):
    new_signal = signal.copy()
    for i, v in enumerate(signal):
        c = 1
        s = 0
        j = i
        k = 0
        while j < len(signal):
            s += signal[j] * c
            if k == i:
                c *= - 1
                k = 0
                j += i + 1
            else:
                k += 1
            j += 1
        new_signal[i] = abs(s) % 10
    return new_signal



def transform_phases_over_half_idx(signal):
    new_signal = signal[:]
    l = len(new_signal)
    for i in reversed(range(l-1)):
        new_signal[i] = (new_signal[i]+new_signal[i+1]) % 10
    return new_signal

with open(__file__.replace(".py", "I.txt")) as f:
    sig = f.read().rstrip().lstrip()
m = [int(n) for n in sig]
for i in range(100):
    m = transform_phases(m)
print_signal(m, 8)

m = [int(n) for n in sig] * 10000
idx = int("".join([str(n) for n in m[:7]]))
m = m[idx:]
for i in range(100):
    m = transform_phases_over_half_idx(m)
print_signal(m[:8])