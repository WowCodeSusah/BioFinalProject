class Node():
    def __init__(self, x, y, name):
        self.name = name
        self.color = "blue"
        self.population = 10
        self.connections = []
        self.x = x
        self.y = y
        self.radius = self.createSize()
        
    def setColor(self, color):
        self.color = color
    
    def setPopulation(self, population):
        self.population = population
    
    def addConnection(self, node):
        self.connections.append(node)

    def createSize(self):
        return self.population * 3
    
    def addPosition(self, addition):
        x, y = addition
        self.x = self.x + x
        self.y = self.y + y
    
    