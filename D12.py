from itertools import combinations

def moons_from_text(t):
    return [[int(n.split('=')[1]) for n in m.replace('<', '').replace('>', '').split(', ')]+[0,0,0] for m in t.split('\n')]
    
def simulate_moons(moons, steps=None):
    if steps:
        for i in range(steps):
            propagate_timestep(moons)
        yield 0
    else:
        moons_start = [m.copy() for m in moons.copy()]
        step = 0
        while True:
            step += 1
            propagate_timestep(moons)
            for i in range(len(moons)):
                if moons[i] == moons_start[i]:
                    yield (i, step)
    #    for i in [0, 1, 2, 3]:
    #        for axis in [0, 1, 2]:
    #            moons_position_list[i][axis].append(moons_position[i][axis])
    #return moons_position_list

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
    #return [moon[:3] for moon in moons]

def frequency(signal):
    frequency = 0
    
    return frequency
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
print(out, ends='\n\n')

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
step = simulate_moons(moons, 3000)
print(step)
print(step == 2772, end='\n\n')

# Test 2
print("Test 2:")
t = """
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
""".lstrip().rstrip()
moons = moons_from_text(t)
step = simulate_moons(moons, 3000)
print(step)
print(step == 4686774924, end='\n\n')

# Solution
#print("Solution:")
#t = """
#<x=-1, y=0, z=2>
#<x=2, y=-10, z=-7>
#<x=4, y=-8, z=8>
#<x=3, y=5, z=-1>
#""".lstrip().rstrip()
#moons = moons_from_text(t)
#step = simulate_moons(moons, 3000)
#print(step)
#fig = plt.figure(figsize=(4*10,3*10))
#ax = fig.add_subplot(111, projection='3d')
#for m in moons_positons[:1]:
#    ax.plot([m[0][0]], [m[1][0]], [m[2][0]], '*k')
#    ax.plot(m[0], m[1], m[2])
#    ax.plot([m[0][-1]], [m[1][-1]], [m[2][-1]], '*r')
#for m in range(4):
#    for i in range(3):
#        ax = fig.add_subplot(3,4,m*3+i+1)
#        ax.plot(moons_positons[m][i])
#ax = fig.add_subplot(111)
#x = moons_positons[0][1]
#w = np.fft.rfft(x)
#freqs = np.fft.rfftfreq(len(x))*len(x)
#ax.plot(freqs, w)
##for coef,freq in zip(w,freqs):
##    if coef:
##        print('{c:>6} * exp(2 pi i t * {f})'.format(c=coef,f=freq))
#
#print(freqs)
#fig.savefig('moons.png')