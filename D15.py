from intcode import Intcode
from time import sleep
import collections

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.appendleft(x)
    
    def get(self):
        return self.elements.popleft()

class SimpleGraph:
    def __init__(self):
        self.edges = {}
    
    def neighbors(self, id):
        return self.edges[id]

class RepairRobot():
    def __init__(self, brain, hull={(0,0):1}):
        self.brain = brain
        self.hull = hull
        self.hull_graph = SimpleGraph()
        self.hull_graph_doubly = SimpleGraph()
        self.x = 0
        self.y = 0
        self.rd = {
            1: 2,
            2: 1,
            3: 4,
            4: 3,
        }
        self.move_history = []
        self.oxygen = None

    @staticmethod    
    def get_adj(c):
        x, y = c
        return([
            (x, y - 1),
            (x, y + 1),
            (x - 1, y),
            (x + 1, y),
        ])

    def step(self, direction):
        self.brain.set_input(direction)
        self.brain.run_until_output()
        if direction < 3:
            coord = (self.x, self.y + (direction * 2 - 3))
        else:
            coord = (self.x + (direction * 2 - 7), self.y)
        out = self.brain.output_buffer.pop(0)
        self.hull[coord] = out
        if out == 2 and not self.oxygen:
            print(f'Oxygen system found at {coord}')
            print(f'Steps: {len(self.move_history) + 1}')
            input()
            self.oxygen = coord
        if out:
            if (self.x, self.y) not in self.hull_graph.edges:
                self.hull_graph.edges[(self.x, self.y)] = []
                self.hull_graph_doubly.edges[(self.x, self.y)] = []
            if coord not in self.hull_graph.edges:
                self.hull_graph.edges[(self.x, self.y)].append(coord)
            if coord not in self.hull_graph_doubly.edges[(self.x, self.y)]:
                self.hull_graph_doubly.edges[(self.x, self.y)].append(coord)

        self.x = coord[0] if out else self.x
        self.y = coord[1] if out else self.y
        return out
    
    def loc_in_path(self, loc, path):
        if loc in self.hull_graph.edges[path]:
            return True
        else:
            r = False
            for p in self.hull_graph.edges[path]:
                r = self.loc_in_path(loc, p)
                if r:
                    return True

    def explore(self):
        frontier = Queue()
        start = (self.x, self.y)
        frontier.put(start)
        visited = {}
        visited[start] = True
        
        while not frontier.empty():
            current = frontier.get()
            if (self.x, self.y) != current:
                try:
                    direction = self.get_adj((self.x, self.y)).index(current) + 1
                    self.step(direction)
                    self.print_hull()
                    self.move_history.append(direction)
                except:
                    while not self.loc_in_path(current, (self.x, self.y)):
                        self.step(self.rd[self.move_history.pop()])
                        self.print_hull()
                    direction = self.get_adj((self.x, self.y)).index(current) + 1
                    self.step(direction)
                    self.move_history.append(direction)
            for i, c in enumerate(self.get_adj(current)):
                if self.step(i + 1):
                    self.step(self.rd[i + 1])
            for n in self.hull_graph.neighbors(current):
                if n not in visited:
                    frontier.put(n)
                    visited[n] = True
        self.print_hull()
    
    def longest_path_from_loc(self, loc):
        path_length = [0, []]
        start = loc
        frontier = Queue()
        frontier.put(loc)
        visited = {}
        history = []
        visited[start] = True

        all_visited = False
        while not frontier.empty():
            current = frontier.get()
            if all_visited:
                while current not in self.hull_graph_doubly.neighbors(history.pop()):
                    if history:
                        self.x = history[-1][0]
                        self.y = history[-1][1]
                        pass
                    else:
                        break
                history.append((self.x, self.y))
            history.append(current)
            self.x = history[-1][0]
            self.y = history[-1][1]
            #self.print_hull()
            if len(history)-1 > path_length[0]:
                path_length[0] = len(history)-1
                path_length[1] = history.copy()
            all_visited = True
            for n in self.hull_graph_doubly.neighbors(current):
                if n not in visited:
                    frontier.put(n)
                    visited[n] = True
                    all_visited = False
        for loc in path_length[1]:
            self.hull[loc] = 2
        self.print_hull()
        return path_length

    def print_hull(self):
        print('---')
        if not self.hull:
            print('🤖 ')
            print('---')
            return
        edges = (
            min(self.hull)[0], min(self.hull, key=lambda x: x[1])[1],
            max(self.hull)[0], max(self.hull, key=lambda x: x[1])[1]
            )
        absolute_hull = {(k[0] - edges[0], k[1] - edges[1]): v for k, v in self.hull.items()}
        for y in range(edges[3] - edges[1] + 1):
            for x in range(edges[2] - edges[0] + 1):
                c = (x, y)
                t = "⬛ "
                if c in absolute_hull:
                    if x == -edges[0] and y == -edges[1]:
                        t = '🔶 '
                    elif absolute_hull[c] == 2:
                        t = '⚪ '
                    elif absolute_hull[c]:
                        t = "  "
                    else:
                        t = "⏹️ "
                if t != '⚪ ' and c == (self.x - edges[0], self.y - edges[1]):
                    t = "🤖 "
                print(t, end='')
            print('\n', end='')
        print('---')
        sleep(0.005)

# Day 11.1
print("Day 11.1")
with open(__file__.replace(".py", "I.txt")) as f:
    t = f.read()
m = [int(n) for n in t.split(',')]
robot = RepairRobot(Intcode(m))
robot.print_hull()
directions = {
    'w': 1,
    'a': 3,
    's': 2,
    'd': 4,
}

robot.explore()
sleep(2)
path_length = robot.longest_path_from_loc((18, -18))

# Day 11.2
print("Day 11.2")
# Solution
print("Solution:")
print(path_length[0])