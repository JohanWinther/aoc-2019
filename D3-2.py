def distance(p1, p2):
    return abs(p2[1]-p1[1])+abs(p2[0]-p1[0])

def wires_from_text(t):
    return [ [ (move[0], int(move[1:])) for move in wire.split(',')] for wire in t.split('\n') ]

def wire_list(wire):
    w = []
    p = (0, 0)
    w.append(p)
    for move in wire:
        if move[0] == 'R':
            d = (1, 0)
        elif move[0] == 'L':
            d = (-1, 0)
        elif move[0] == 'U':
            d = (0, -1)
        elif move[0] == 'D':
            d = (0, 1)
        else:
            d = (0, 0)
        for steps in range(move[1]):
            p = (p[0]+d[0], p[1]+d[1])
            w.append(p)
    return w

def wires_to_grid(wires):
    gz = grid_size(wires)
    g = []
    for i in range(gz[3]):
        g.append([0] * gz[2])
    for (n, wire) in enumerate(wires):
        for p in wire:
            g[p[1]][p[0]] += n+1
    return g

def print_grid(grid):
    with open('output.txt', 'w') as f:
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if grid[r][c] == 0:
                    f.write(' ')
                else:
                    f.write(str(grid[r][c]))
            f.write('\n')

def grid_size(wires):
    min_x = max_x = max_y = min_y = 0
    for wire in wires:
        for p in wire:
            min_x = min(p[0], min_x)
            max_x = max(p[0], max_x)
            min_y = min(p[1], min_y)
            max_y = max(p[1], max_y)
    return (min_x, min_y, max_x+1, max_y+1)

def shift_wires(wires):
    grid_edges = grid_size(wires)
    return [[(p[0]-grid_edges[0], p[1]-grid_edges[1]) for p in wire] for wire in wires]

def least_steps_to_intersections(wires, intersections):
    steps_list = []
    for wire in wires:
        steps = 0
        for step, p in enumerate(wire):
            if p in intersections:
                steps_list.append((step, p))

    d = {x: 0 for _, x in steps_list}
    for n, p in steps_list:
        d[p] += n
    return min(d.values())

with open('D3I.txt') as f:
    wires = f.read().rstrip('\n')

#wires = "R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83"
#wires = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
wires = wires_from_text(wires)
wires = [wire_list(w) for w in wires]
#wires = shift_wires(wires)
origin = wires[0][0]
#grid = wires_to_grid(wires)
#print_grid(grid)
intersections = list(set(wires[0][1:]).intersection(wires[1][1:]))
print(least_steps_to_intersections(wires, intersections))
