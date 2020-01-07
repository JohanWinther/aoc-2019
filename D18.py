
from collections import deque

class Area():

    key_list = list(map(chr, range(97, 123)))
    door_list = list(map(chr, range(65, 91)))
    offset = [0, 1, 0, -1]

    def __init__(self, area=''):
        if not area:
            with open(__file__.replace(".py", "I.txt")) as f:
                area = f.read().rstrip().lstrip()
        self.area = [[(x if x != '#' and x != '.' else (0 if x != '.' else 1)) for x in y] for y in area.split('\n')]
        self.moves = 0
        self.graph = {}
        self.keys = {}
        self.doors = {}
        for y in range(1,len(self.area)-1):
            for x in range(1, len(self.area[y]) - 1):
                symbol = self.area[y][x]
                if symbol == '@':
                    self.loc = [x, y]
                elif symbol in Area.door_list:
                    self.doors[symbol] = (x, y)
                #elif symbol in Area.key_list:
                #    self.keys[symbol] = (x, y)
                for i in range(4):
                    if self.area[y + Area.offset[i]][x + Area.offset[(i + 1) % 4]]:
                        if (x,y) not in self.graph:
                            self.graph[(x, y)] = []
                        self.graph[(x, y)].append((x + Area.offset[(i + 1) % 4], y + Area.offset[i]))

    def get_bfs_graph(self):
        graph = {}
        Q = deque()
        visited = {}

        start = (self.loc[0], self.loc[1])
        graph[start] = None
        visited[start] = True
        Q.append(start)

        
        while Q:
            current = Q.popleft()
            symbol = self.area[current[1]][current[0]]
            if symbol in Area.key_list:
                self.keys[symbol] = current
            elif symbol in Area.door_list:
                #self.area[self.doors[symbol.upper()][1]][self.doors[symbol.upper()][0]] = 1
                return graph
            for n in self.graph[current]:
                if n not in visited:
                    visited[n] = True
                    graph[n] = current
                    Q.append(n)
        return graph

    def key_distance(self, k, bfs_graph):
        d = 0
        if k in self.keys:
            node = self.keys[k]
            while bfs_graph[node]:
                node = bfs_graph[node]
                d += 1
        return d

    def get_key_distances(self):
        g = self.get_bfs_graph()
        return {k:self.key_distance(k, g) for k in self.keys}
    

    def print_area(self):
        for y in self.area:
            for x in y:
                if x==0:
                    t = '#'
                elif x==1:
                    t = ' '
                else:
                    t = str(x)
                print(t, end='')
            print('\n', end='')

area='''
#################
#b.A....@..c.a.B#
#################
''' .lstrip().rstrip()

a = Area(area)

kg = a.get_key_distances()

print(0)