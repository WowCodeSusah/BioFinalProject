class Node():
    def __init__(self, x, y, name):
        self.name = name
        self.color = "blue"
        self.population = 10
        self.connections = []
        self.x = x
        self.y = y
        self.radius = self.createSize()

    def setName(self, name):
        self.name = name
        
    def setColor(self, color):
        self.color = color
    
    def setPopulation(self, population):
        self.population = population
        self.radius = population * 5
    
    def addConnection(self, node):
        self.connections.append(node)

    def createSize(self):
        return self.population * 5
    
    def addPosition(self, addition):
        x, y = addition
        self.x = self.x + x
        self.y = self.y + y

    def isClicked(self, pos):
        mouse_x, mouse_y = pos
        distance = ((self.x - mouse_x) ** 2 + (self.y - mouse_y) ** 2) ** 0.5
        return distance <= self.radius
    
    