from math import gcd
# Day 10.1

def text_to_dict(t):
    t = t.split('\n')
    asteroids = {}
    for y, row in enumerate(t):
        for x, column in enumerate(row):
            if column == '#':
                asteroids[(x, y)] = 0
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


# Test 2
print("Test 2")
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
print(out == ((5,8), 33), end="\n\n")

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

# Day 10.1
print("Day 10.1")
with open(__file__.replace(".py", "I.txt")) as f:
    t = f.read()
out = get_best_location(t)
print(out)
