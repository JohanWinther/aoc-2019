class Body:
    body_dict = {}

    def __init__(self, name, parent):
        self.name = name

        if Body.bodyExists(parent):
            self.parent = Body.body_dict[parent]
        else:
            self.parent = parent
        
        Body.body_dict[name] = self
    
    def body(name):
        return Body.body_dict[name]

    def bodyExists(name):
        return (name in Body.body_dict)

    def addBodiesFromList(orbits):
        Body('COM', None)
        for o in orbits:
            Body(o[1], o[0])
        for key in Body.body_dict:
            if Body.body(key).parent is not None and type(Body.body(key).parent) is not Body:
                Body.body(key).parent = Body.body_dict[Body.body(key).parent]
    
    def getNumberOfOrbits(self):
        if self.parent is not None:
            return 1 + self.parent.getNumberOfOrbits()
        else:
            return 0

    def getTotalNumberOfOrbits():
        return sum([Body.body(key).getNumberOfOrbits() for key in Body.body_dict])

    def getOrbitalTransfers(self, body2):
        path1 = [self.parent]
        while (path1[len(path1) - 1].parent is not None):
            path1.append(path1[len(path1) - 1].parent)
        path2 = [body2.parent]
        while (path2[len(path2) - 1].parent is not None):
            path2.append(path2[len(path2) - 1].parent)
        
        steps = 0
        for p in path1:
            if p in path2: # Go to common parent and count steps from self
                for p2 in path2:
                    if p2 in path1:  # Go to common parent and count steps from body2
                        return (p, steps)
                    steps += 1
            steps += 1

# Load orbits into variable
with open('D6I.txt') as f:
    t = f.read().rstrip('\n')
orbits = [o.split(')') for o in t.split('\n')]

Body.addBodiesFromList(orbits)
# Task 1
print(Body.getTotalNumberOfOrbits())

# Task 2
p = Body.body('YOU').getOrbitalTransfers(Body.body('SAN'))
print(p[0].name, p[1])