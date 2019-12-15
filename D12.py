from itertools import combinations
from math import gcd

def moons_from_text(t):
    return [[int(n.split('=')[1]) for n in m.replace('<', '').replace('>', '').split(', ')]+[0,0,0] for m in t.split('\n')]
    
def simulate_moons(moons, steps=None):
    if steps:
        for i in range(steps):
            propagate_timestep(moons)
        yield 0
    else:
        moons_start = [[moon[i] for moon in moons] for i in range(3)]
        step = 0
        while True:
            step += 1
            propagate_timestep(moons)
            for i in range(3):
                if [moon[i] for moon in moons] == moons_start[i] and [moon[i + 3] for moon in moons] == [0, 0, 0, 0]:
                    yield (i, step)

def energy(moons):
    return sum([sum([abs(n) for n in moon[:3]]) * sum([abs(n) for n in moon[3:]]) for moon in moons])

def propagate_timestep(moons):
    # Apply acceleration (gravity)
    for i in combinations([0, 1, 2, 3], 2):
        for axis in [0, 1, 2]:
            rel = moons[i[0]][axis] - moons[i[1]][axis]
            # First moon
            moons[i[0]][axis + 3] += (rel < 0) - (rel > 0)
            # Second moon
            moons[i[1]][axis + 3] += (rel > 0) - (rel < 0)
    # Apply velocity
    for i in [0, 1, 2, 3]:
        for axis in [0, 1, 2]:
            moons[i][axis] += moons[i][axis + 3]

def get_periods(moons):
    periods = {i: 0 for i in range(3)}
    period_gen = simulate_moons(moons)
    while not all(periods.values()):
        res = next(period_gen)
        if periods[res[0]] == 0:
            periods[res[0]] = res[1]
            #print(periods)
    periods = list(periods.values())
    a, b, c = periods
    return a * b * c // (gcd(a * b, c * gcd(a, b)))

# Day 12.1
print("Day 12.1")

# Test 1
print('Test 1:')
t = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""".lstrip().rstrip()
moons = moons_from_text(t)
next(simulate_moons(moons, steps=10))
out = energy(moons)
print(moons)
print(out)
print(out == 179, end='\n\n')

# Test 2
print('Test 2:')
t = """
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
""".lstrip().rstrip()
moons = moons_from_text(t)
next(simulate_moons(moons, steps=100))
out = energy(moons)
print(moons)
print(out)
print(out == 1940, end='\n\n')

# Solution
print("Solution:")
with open(__file__.replace(".py", "I.txt")) as f:
    t = f.read().rstrip()
moons = moons_from_text(t)
next(simulate_moons(moons, steps=1000))
out = energy(moons)
print(moons)
print(out, end='\n\n')

# Day 12.2
print("Day 12.2")
# Test 1
print("Test 1:")
t = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""".lstrip().rstrip()
moons = moons_from_text(t)
period = get_periods(moons)
print(period)
print(period == 2772, end='\n\n')

# Test 2
print("Test 2:")
t = """
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
""".lstrip().rstrip()
moons = moons_from_text(t)
period = get_periods(moons)
print(period)
print(period == 4686774924, end='\n\n')

# Solution
print("Solution:")
with open(__file__.replace(".py", "I.txt")) as f:
    t = f.read().rstrip()
moons = moons_from_text(t)
period = get_periods(moons)
print(period)