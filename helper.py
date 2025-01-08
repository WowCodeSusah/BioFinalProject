import pygame
import random

def createImageImport(link, x, y):
    image = pygame.image.load(link).convert_alpha()
    rect = image.get_rect()
    rect.center = (x, y)
    return (image, rect)

# Algorithm for Nodes
def createDay(listOfNodes):
    # Find the top Node and Sort them From Top to Bottom
    TopNode = None

    # Find the top of the totem (Does not have connections from the bottom)
    notTopNames = []
    for nodes in listOfNodes:
        for names in nodes.connections:
            notTopNames.append(names)

    # Search List
    for nodes in listOfNodes:
        if nodes.name not in notTopNames:
            TopNode = nodes

    # After getting the top parse throught its connections to gather the rest of the tree
    setNewPopulation(TopNode, 1, 1, listOfNodes)

    return listOfNodes 

def setNewPopulation(node, currentPosition, NumberOfConnection, NodeList):
    currentNode = []
    for nodes in node.connections:
        for nodeFromNodeList in NodeList:
            if nodeFromNodeList.name == nodes:
                currentNode.append(nodeFromNodeList)
        
    totalPreyPopulation = 0
    for total in currentNode:
        totalPreyPopulation = totalPreyPopulation + total.population    

    if totalPreyPopulation > 0:
        populationEquation = (((totalPreyPopulation / 10) - node.population) / 10)
        node.setPopulation(node.population + populationEquation)
    else:
        populationEquation = random.randint(int(-(node.population / 10)), int(node.population / 10))
        node.setPopulation(node.population + populationEquation)

    if len(node.connections) == 0:
        return False
    else:
        for nodes in node.connections:
            currentNode = None
            for nodeFromNodeList in NodeList:
                if nodeFromNodeList.name == nodes:
                    currentNode = nodeFromNodeList
            setNewPopulation(currentNode, currentPosition + 1, len(node.connections), NodeList)

def getPopulation(NodeList):
    PopulationList = []
    for nodes in NodeList:
        PopulationList.append(nodes.population)
    return PopulationList

def setPopulation(NodeList, Population):
    if len(NodeList) == len(Population):
        for count, nodes in enumerate(NodeList):
            nodes.setPopulation(Population[count])
    return NodeList
