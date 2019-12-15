from math import gcd, atan2, pi


def text_to_dict(t):
    t = t.split('\n')
    asteroids = {}
    for y, row in enumerate(t):
        for x, column in enumerate(row):
            if column == '#':
                asteroids[(x, y)] = 0
    return asteroids


def target_list_sorted_by_angle(asteroids, coord):
    sorted_asteroids = {}
    asteroids = [(c[0] - coord[0], c[1] - coord[1]) for c in asteroids]  # Get relative coords in list
    asteroids.remove((0,0)) # Remove self
    # Sort by angle in radians (0 = up)
    asteroids.sort(key=lambda c: (
        (atan2(c[1], c[0]) + pi / 2) % (2 * pi), # First sort by angle
        c[0]**2+c[1]**2, # Then sort by relative distance
        ))
    for c in asteroids:
        angle = (atan2(c[1], c[0]) + pi / 2) % (2 * pi)
        if angle not in sorted_asteroids:
            sorted_asteroids[angle] = []
        sorted_asteroids[angle].append(c)
    asteroids = []
    while sorted_asteroids:
        for angle in sorted_asteroids:
            if sorted_asteroids[angle]:
                new_asteroid = sorted_asteroids[angle].pop(0)
                asteroids.append(
                    (new_asteroid[0] + coord[0], new_asteroid[1] + coord[1]) # Append asteroid with absolute position
                    )
        sorted_asteroids = {angle: asteroids for angle, asteroids in sorted_asteroids.items() if asteroids != []}
    return asteroids


def detect_asteroids(asteroids, coord):
    can_see = {}
    for c in asteroids:
        if coord != c:
            c = (c[0]-coord[0], c[1]-coord[1])
            ratio = (c[0] // gcd(c[1], c[0]), c[1] // gcd(c[1], c[0]))
            if ratio not in can_see:
                can_see[ratio] = 1

    return len(can_see)


def get_best_location(t):
    asteroids = text_to_dict(t)
    for coord in asteroids:
        asteroids[coord] = detect_asteroids(asteroids, coord)
    best_loc = max(asteroids, key=asteroids.get)
    return (best_loc, asteroids[best_loc])

def get_ith_vaporized(sorted_asteroids, i):
    return sorted_asteroids[i-1]

# Day 10.1
print("Day 10.2")

# Test 1:
print("Test 1:")
t = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
""" .rstrip().lstrip()
out = get_best_location(t)
print(out)
print(out == ((5, 8), 33), end="\n\n")

# Test 2
print("Test 2:")
t = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
""" .rstrip().lstrip()
out = get_best_location(t)
print(out)
print(out == ((1, 2), 35), end="\n\n")

# Test 3
print("Test 3:")
t = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
""" .rstrip().lstrip()
out = get_best_location(t)
print(out)
print(out == ((6, 3), 41), end="\n\n")

# Test 4
print("Test 4:")
t = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""" .rstrip().lstrip()
out = get_best_location(t)
print(out)
print(out == ((11, 13), 210), end="\n\n")

# Solution
print("Solution:")
with open(__file__.replace(".py", "I.txt")) as f:
    t = f.read()
out = get_best_location(t)
print(out, end="\n\n")

# Day 10.2
print("Day 10.2")

# Test 1
print("Test 1:")
t = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""" .rstrip().lstrip()
asteroids = text_to_dict(t)
best_loc = get_best_location(t)
sorted_asteroids = target_list_sorted_by_angle(asteroids, best_loc[0])
out = get_ith_vaporized(sorted_asteroids, 200)
print(out)
print(out == (8,2), end="\n\n")

# Solution
print("Solution:")
with open(__file__.replace(".py", "I.txt")) as f:
    t = f.read()
asteroids = text_to_dict(t)
best_loc = get_best_location(t)
sorted_asteroids = target_list_sorted_by_angle(asteroids, best_loc[0])
out = get_ith_vaporized(sorted_asteroids, 200)
print(out[0]*100+out[1], end="\n\n")
