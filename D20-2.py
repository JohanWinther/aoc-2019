from random import shuffle
from time import sleep
from collections import deque
import sys


def is_letter(symbol):
    return symbol in list(map(chr, range(65, 91)))


def adj(c, d):
    offset = [1, 0, -1, 0]
    return (c[0] + offset[d], c[1] + offset[(d - 1) % 4], c[2])


def set_z(c, lev):
    return (c[0], c[1], lev)


def neighbors(t, c):
    x, y = c[:2]
    return [
        t[y][x + 1],
        t[y + 1][x],
        t[y][x - 1],
        t[y - 1][x],
    ]


def opp(d):
    return (d + 2) % 4


def taxicab(c, goal):
    return abs(c[0] - goal[0]) + abs(c[1] - goal[1])


def find_portals(t):
    coords = {}
    portals = {}
    for y in range(1, len(t) - 1):
        for x in range(1, len(t[y]) - 1):
            c = (x, y, 0)
            l = t[y][x]
            n = neighbors(t, c)
            if is_letter(l) and n.count('.') == 1:
                d = n.index('.')
                c = adj(c, d)  # Portal entrance
                d2 = opp(d)
                c2 = adj(adj(c, d2), d2)
                l2 = t[c2[1]][c2[0]]

                if d2 == 0:
                    outer = (c2[0] == len(t[0])-1)
                    letter = l + l2
                elif d2 == 1:
                    outer = (c2[1] == len(t)-1)
                    letter = l + l2
                elif d2 == 2:
                    outer = c2[0] == 0
                    letter = l2 + l
                elif d2 == 3:
                    outer = c2[1] == 0
                    letter = l2 + l

                coords[c] = (2 * int(outer) - 1)
                if letter not in portals:
                    portals[letter] = []
                if outer:
                    portals[letter].append(c)
                else:
                    portals[letter].insert(0, c)
    for p in portals:
        if len(portals[p]) > 1:
            coords[portals[p][0]] = (portals[p][1], coords[portals[p][0]], p)
            coords[portals[p][1]] = (portals[p][0], coords[portals[p][1]], p)
        else:
            coords[portals[p][0]] = None
    return coords


def find_letter(t, l, exclude=None):
    if exclude:
        exclude = (exclude[0], exclude[1])
    for y in range(1, len(t) - 1):
        for x in range(1, len(t[y]) - 1):
            n = neighbors(t, (x, y, 0))
            if t[y][x] == l[0] and n.count(l[1]) == 1 and n.count('.') == 1:
                d = n.index('.')
                if exclude != (x, y):
                    return adj((x, y, 0), d)


def is_letter(x):
    return x in list(map(chr, range(65, 91)))


def bfs(t, start, goal=None):
    edges = {}
    Q = deque()
    visited = set(start)
    Q.append(start)
    v = start

    while Q:
        v = Q.popleft()
        if goal and v == goal:
            return edges
        if v not in edges:
            edges[v] = []
        for d, n in enumerate(neighbors(t, v)):
            w = adj(v, d)
            if n == '.' and w not in visited:
                Q.append(w)
                visited.add(w)
                edges[v].append(w)
    return edges


def a_star_coords(graph, start, goal, h=lambda c, g: 0):

    openSet = set([start])

    gScore = {}
    gScore[start] = 0

    fScore = {}
    fScore[start] = h(start, goal)

    while openSet:
        current = None
        for node in openSet:
            if node in fScore and (current not in fScore or fScore[node] < fScore[current]):
                current = node
        if current == goal:
            return gScore[current]

        openSet.remove(current)
        for neighbor in graph[current]:
            # d(current, neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tentative_gScore = gScore[current] + 1  # d(current, neighbor)
            if neighbor not in gScore or tentative_gScore < gScore[neighbor]:
                # This path to neighbor is better than any previous one. Record it!
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + h(neighbor, goal)
                if neighbor not in openSet:
                    openSet.add(neighbor)

    # Open set is empty but goal was never reached
    return None


def shorten_graph(g, start, end_nodes):
    G = {}
    for portal_entrance in set(end_nodes).intersection(g):
        if portal_entrance != start:
            if start not in G:
                G[start] = []
            if portal_coords[portal_entrance]:
                portal_exit, level, _ = portal_coords[portal_entrance]
                G[start].append(
                    (portal_exit, a_star_coords(g, start, portal_entrance, h=taxicab) + 1))
            else:
                G[start].append(
                    (portal_entrance, a_star_coords(g, start, portal_entrance, h=taxicab)))
    return G


def create_portal_graph(t, portal_coords):
    G = {}
    for p in portal_coords:
        #out = [[x for x in y] for y in t]
        g = bfs(t, p)
        g = shorten_graph(g, p, portal_coords)
        G.update(g)
    return G


def a_star_portals(graph, portal_coords, start, goal, h=lambda c, g: 0):

    openSet = set([start])
    cameFrom = {}
    gScore = {}
    gScore[start] = 0

    fScore = {}
    fScore[start] = h(start, goal)

    while openSet:
        current = None
        for node in openSet:
            if node in fScore and (current not in fScore or fScore[node] < fScore[current]):
                current = node
        if current == goal:
            return (gScore[current], reconstruct_path(cameFrom, current))

        openSet.remove(current)
        for portal, weight in graph[set_z(current, 0)]:
            level_direction = 0
            add_portal = True
            if portal == start:
                add_portal = False
            elif portal_coords[set_z(portal, 0)]:
                _, level_direction, name = portal_coords[set_z(portal, 0)]
                add_portal = not (current[2] == 0 and level_direction == -1)
            portal = set_z(portal, current[2] + level_direction)

            tentative_gScore = gScore[current] + weight
            if add_portal and (portal not in gScore or tentative_gScore < gScore[portal]):
                cameFrom[portal] = current
                # This path to neighbor is better than any previous one. Record it!
                gScore[portal] = tentative_gScore
                fScore[portal] = gScore[portal] + h(portal, goal)
                if portal not in openSet:
                    openSet.add(portal)

    return None


def reconstruct_path(cameFrom, current):
    total_path = []
    while current in cameFrom:
        total_path.insert(0, current)
        current = cameFrom[current]
    total_path.insert(0, current)
    return total_path


def print_path(path):
    i = 0
    for p in path:
        k = portal_coords[set_z(p, 0)]
        if not k:
            k = [None, None, 'AA']
        b = ' => ' if i % 2 == 0 else f'\n'
        print(k[2], p[2], end=b)
        i += 1


t = (
    '''
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     
''')[1:-1].split('\n')

with open(__file__.replace("-2.py", "I.txt")) as f:
   t = f.read().split('\n')[:-1]

portal_coords = find_portals(t)
G = create_portal_graph(t, portal_coords)
l, path = a_star_portals(
    G,
    portal_coords,
    find_letter(t, 'AA'),
    find_letter(t, 'ZZ')
)
print_path(path)
print(f"Length: {l}")
