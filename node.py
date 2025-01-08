class Node():
    def __init__(self, x, y, name, population = 1000):
        self.name = name
        self.color = "blue"
        self.population = population
        self.connections = []
        self.x = x
        self.y = y
        self.radius = self.createSize()

    def setName(self, name):
        self.name = name
        
    def setColor(self, color):
        self.color = color
    
    def setPopulation(self, population):
        self.population = int(population)
        self.radius = int(population) * 0.07 + 40
    
    def addConnection(self, node):
        node = node.split(',')
        self.connections = node

    def createSize(self):
        return self.population * 0.07 + 40
    
    def addPosition(self, addition):
        x, y = addition
        self.x = self.x + x
        self.y = self.y + y

    def isClicked(self, pos):
        mouse_x, mouse_y = pos
        distance = ((self.x - mouse_x) ** 2 + (self.y - mouse_y) ** 2) ** 0.5
        return distance <= self.radius
    
    def getPopulationValue(self):
        PopulationValue = "{:.2f}".format(self.population)
        return PopulationValue
    
    