from random import shuffle
from time import sleep
from collections import deque

def adj(c, d):
    offset = [1, 0, -1, 0]
    return (c[0] + offset[d], c[1] + offset[(d - 1) % 4])

def neighbors(t, c):
    x, y = c
    return [
        t[y][x + 1],
        t[y + 1][x],
        t[y][x - 1],
        t[y - 1][x],
    ]

def find_letter(t, l, exclude=None):
    for y in range(1, len(t) - 1):
        for x in range(1, len(t[y]) - 1):
            n = neighbors(t, (x, y))
            if t[y][x] == l[1] and n.count(l[0]) == 1 and n.count('.') == 1:
                d = n.index('.')
                if exclude != (x, y):
                    return adj((x, y), d)

def find_pair(t, l, exclude=None):
    pair = find_letter(t, l[1] + l[0])
    if not pair:
        pair = find_letter(t, l, exclude=exclude)
    return pair

def is_letter(x):
    return x != '#' and x != ' ' and x != '.'

def print_out():
    print("\n".join(["".join(y).replace('.',' ') for y in out]))

def dfs(t, v, pr=False):
    visited[v] = True
    if v not in edges:
        edges[v] = []
    if pr:
        out[v[1]][v[0]] = '·'
        print_out()
        sleep(0.01)
    n = neighbors(t, v)
    R = list(range(4))
    shuffle(R)
    for r in R:
        w = adj(v, r)
        add_node = False
        if n[r] == '.' and w not in visited:
            add_node = True
        elif is_letter(n[r]):
            ln = neighbors(t, w)
            for d, n2 in enumerate(ln):
                if is_letter(n2):
                    l = n2 + n[r]
                    break
            w = find_pair(t, l, exclude=w)
            if w not in visited:
                add_node = True
        if add_node:
            if v not in edges:
                edges[v] = []
            edges[v].append(w)
            dfs(t, w)

def bfs(t, v, pr=False):
    Q = deque()
    visited[v] = True
    Q.append(v)

    while Q:
        v = Q.popleft()
        if v not in edges:
            edges[v] = []
        if pr:
            out[v[1]][v[0]] = 'x'
            print_out()
            sleep(0.01)
        for d, n in enumerate(neighbors(t, v)):
            w = adj(v, d)
            add_node = False
            if n == '.' and w not in visited:
                add_node = True
            elif is_letter(n):
                ln = neighbors(t, w)
                for d2, n2 in enumerate(ln):
                    if is_letter(n2):
                        l = n2 + n
                        break
                w = find_pair(t, l, exclude=w)
                if w not in visited:
                    add_node = True
            if add_node:
                Q.append(w)
                visited[w] = True
                edges[v].append(w)
        if pr:
            out[v[1]][v[0]] = '·'
            print_out()

def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visit = set()
    
    while current_node != end:
        visit.add(current_node)
        destinations = edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = 1 + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visit}
        if not next_destinations:
            return []
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path

t =(
'''
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
''')[1:-1].split('\n')

t = (
'''
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               
''')[1:-1].split('\n')

with open(__file__.replace(".py", "I.txt")) as f:
    t = f.read().split('\n')[:-1]

visited = {}
edges = {}
out = [[x for x in y] for y in t]

bfs(t, find_letter(t, 'AA'))
#dfs(t, find_letter(t, 'AA'))
path = dijsktra(edges, find_letter(t, 'AA'), find_letter(t, 'ZZ'))


out = [[x for x in y] for y in t]
for p in path:
    out[p[1]][p[0]] = '·'
print_out()
print(f"Shortest path: {len(path)-1}")