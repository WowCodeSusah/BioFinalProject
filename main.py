# Need Imports
import pygame
from node import Node
from button import Button
from input_box import InputBox
import helper
from states.adding import handle_adding_state
from states.edit import handle_edit_state
from states.delete import handle_delete_state

# Settings
menuSize = 300
screenSizeX = 1600
screenSizeY = 1000

# pygame setup
pygame.init()
screen = pygame.display.set_mode((screenSizeX, screenSizeY))
clock = pygame.time.Clock()
pygame.display.set_caption("Food Web Simulator")
running = True
dt = 0
font = pygame.font.Font(None, 24)

# Node List
node = []

# Day Lists
currentDay = 0
NodeDaysPopulation = []

# Game State (Normal / Adding / Delete / Editing/ EditPopup)
gameState = "Normal"

# Test Node
def DefaultNode(node):
    node.append(Node(1500 / 2, 300, "Fox", 10))
    node[0].addConnection("Chicken,Snake")

    node.append(Node(1500 * 4 / 10, 400, "Chicken", 50))
    node[1].addConnection("Worm,GrassHooper")

    node.append(Node(1500 * 6 / 10 , 400, "Snake", 50))
    node[2].addConnection("Mouse")

    node.append(Node(1500 * 7 / 10, 600, "Mouse", 500))
    node.append(Node(1500 * 5 / 10, 600, "Worm", 250))
    node.append(Node(1500 * 3 / 10, 600, "GrassHooper", 250))

    return node

def CustomNode(node):
    node.append(Node(600, 1000 / 2, "Example 1", 100))
    node[0].addConnection("Example 2")

    node.append(Node(800, 1000 / 2, "Example 2", 1000))

    return node

NodeDaysPopulation.append(helper.getPopulation(node))

activeNode = None
selectedNode = None

# Image Generator
background , backgroundRect= helper.createImageImport('resources/background.jpg', screenSizeX / 2, screenSizeY / 2)
OptionsMenu, OptionRect = helper.createImageImport('resources/OptionsMenu.jpg', menuSize / 2, screenSizeY / 2)
DescriptionMenu, DescriptionRect = helper.createImageImport('resources/DescriptionMenu.jpg', (screenSizeX - menuSize / 2), screenSizeY / 2)
TitleImage, TitleRect = helper.createImageImport('resources/Title.png', 150, 100)

# Images for Menu
menuSquareImage, menuSquareImageRect = helper.createImageImport('resources/menuSquare.png', screenSizeX / 2, screenSizeY / 2)

# Modal titles
menuAddingTitleImage, menuAddingTitleRect = helper.createImageImport('resources/AddingNodeTitle.png', 550 , 200)
menuEditingTitleImage, menuEditingTitleRect = helper.createImageImport('resources/EditingNodeTitle.png', 550 , 200)
menuDeletingTitleImage, menuDeletingTitleRect = helper.createImageImport('resources/DeletingNodeTitle.png', 550 , 200)

# Field Names
nameAddingImage, nameAddingRect = helper.createImageImport('resources/nameBar.png', screenSizeX / 2 , 350)
populationAddingImage, populationAddingRect = helper.createImageImport('resources/PopulationBar.png', screenSizeX / 2, 510)
connectionAddingImage, connectionAddingRect = helper.createImageImport('resources/ConnectionBar.png', screenSizeX / 2, 670)

# Menu Button to Cancel (Exit modal)
CancelButtonAddingMenu = Button('resources/buttons/CancelButton.png', 'resources/buttons/CancelButtonPressed.png', 750, 830)
CancelButtonAddingMenu.preLoad()

# Cancel Button for Start Sequence
CancelButtonStart = Button('resources/buttons/CancelButton.png', 'resources/buttons/CancelButtonPressed.png', 1450, 900)
CancelButtonStart.preLoad()

# Day Control Menu
DayControlMenu, DayControlMenuRect = helper.createImageImport('resources/DayControlTitle.png', 1450 , 100)

# Start Day Buttons
PlusButton = Button('resources/buttons/PlusButton.png', 'resources/buttons/PlusButtonPressed.png', 1540, 230, 49, 49)
PlusButton.preLoad()

MinusButton = Button('resources/buttons/MinusButton.png', 'resources/buttons/MinusButtonPressed.png', 1360, 230, 49, 49)
MinusButton.preLoad()

# Menu Buttons for Adding, Editing and Deleting (In the Modal)
AddNodeButtonAddingMenu = Button('resources/buttons/AddNodeButton.png', 'resources/buttons/AddNodeButtonPressed.png', 1050, 830)
AddNodeButtonAddingMenu.preLoad()
EditNodeButtonEditingMenu = Button('resources/buttons/EditNodeButton.png', 'resources/buttons/EditNodeButtonPressed.png', 1050, 830)
EditNodeButtonEditingMenu.preLoad()
DeleteNodeButtonDeletingMenu = Button('resources/buttons/DeleteNodeButton.png', 'resources/buttons/DeleteNodeButtonPressed.png', 1050, 830)
DeleteNodeButtonDeletingMenu.preLoad()

# Main menu buttons
AddNodeButton = Button('resources/buttons/AddNodeButton.png', 'resources/buttons/AddNodeButtonPressed.png', 150, 600)
AddNodeButton.preLoad()
EditNodeButton = Button('resources/buttons/EditNodeButton.png', 'resources/buttons/EditNodeButtonPressed.png', 150, 700)
EditNodeButton.preLoad()
DeleteNodeButton = Button('resources/buttons/DeleteNodeButton.png', 'resources/buttons/DeleteNodeButtonPressed.png', 150, 800)
DeleteNodeButton.preLoad()
StartButton = Button('resources/buttons/StartButton.png', 'resources/buttons/StartButtonPressed.png', 150, 900)
StartButton.preLoad()

# Title Screen Buttons
DefaultNodeButton = Button('resources/buttons/DefaultButton.png', 'resources/buttons/DefaultButtonPressed.png', 650, 725)
DefaultNodeButton.preLoad()
CustomNodeButton = Button('resources/buttons/CustomButton.png', 'resources/buttons/CustomButtonPressed.png', 1100, 725)
CustomNodeButton.preLoad()

# name validation function
def check_node_double(node_name):
    for n in node:
        if n.name == node_name:
            return False
    return True

# backup validation function for name, used only for when deleting
def check_node_exists(node_name):
    for n in node:
        if n.name == node_name:
            return True
    return False

# population validation function
def is_number(text):
    return text.isdigit()

# connection validation function
def check_connection(node_name):
    if len(node) == 0:
        return True
    else:
        node_names = node_name.split(',')
        for name in node_names:
            if name == '':
                continue
            name = name.strip() 
            for n in node:
                if n.name == name:
                    return True
        return False

input_boxes = [
    InputBox(
        screenSizeX / 3.5, 325, 500, 32, 'e.g. Fish', 
        validation_func=check_node_double, 
        secondary_validation_func=check_node_exists,
        custom_error_message='Node already exists',
        secondary_custom_error_message='Node does not exist'
    ),
    InputBox(
        screenSizeX / 3.5, 485, 500, 32, 'e.g. 100', 
        validation_func=is_number,
        custom_error_message='Input should be numeric'
    ),
    InputBox(
        screenSizeX / 3.5, 645, 500, 32, 'e.g. Cat:eater, Bear:eater, Plankton:food, Shrimp:food', 
        validation_func=check_connection,
        custom_error_message='Connection does not exist'
    )
]

def reset_input_boxes(input_boxes):
    print("Resetting input boxes")
    input_boxes[0].reset()
    input_boxes[1].reset()
    input_boxes[2].reset()

def reInitialize(selectedNode): 
    print("Reinitializing selected node")
    if hasattr(selectedNode, "_initialized"):
        del selectedNode._initialized

menuState = True

# Menu Imports
connectionAddingImage, connectionAddingRect = helper.createImageImport('resources/ConnectionBar.png', screenSizeX / 2, 670)
menuScreenBackground, menuScreenBackgroundRect = helper.createImageImport('resources/menuScreen.png', screenSizeX / 2, screenSizeY / 2)
menuScreenBackground = pygame.transform.scale(menuScreenBackground, (1600, 1000))

screen.blit(menuScreenBackground, menuScreenBackgroundRect)

# Cover Animations
RightCover = pygame.image.load('resources/CoverRight.png')
LeftCover = pygame.image.load('resources/CoverLeft.png')
animationRunning = False
animationRunningTwo = False
frameCount = 0
TimelineReset = False

# Pygame Loop
while running:
    if TimelineReset == True:
        currentDay = 0
        NodeDaysPopulation = []
        NodeDaysPopulation.append(helper.getPopulation(node))
        activeNode = None
        selectedNode = None
        TimelineReset = False
    # Menu State and Animations  
    if menuState == True and animationRunning == False:
        screen.blit(menuScreenBackground, menuScreenBackgroundRect)
        DefaultNodeButton.drawButton(screen=screen)
        CustomNodeButton.drawButton(screen=screen)
        for event in pygame.event.get():
        # Finds the cursor when it clicks down and checks for circle colision
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        currentX, currentY = event.pos
                        for num, parse in enumerate(node):
                            if currentX < (parse.x + parse.radius) and currentY < (parse.y + parse.radius):
                                if currentX > (parse.x - parse.radius) and currentY > (parse.y - parse.radius):
                                    activeNode = num
                        if DefaultNodeButton.isOver(event.pos):
                            node = []
                            currentDay = 0
                            NodeDaysPopulation = []
                            node = DefaultNode(node)
                            NodeDaysPopulation.append(helper.getPopulation(node))
                            activeNode = None
                            selectedNode = None
                            animationRunning = True

                        if CustomNodeButton.isOver(event.pos):
                            node = []
                            currentDay = 0
                            NodeDaysPopulation = []
                            node = CustomNode(node)
                            NodeDaysPopulation.append(helper.getPopulation(node))
                            activeNode = None
                            selectedNode = None
                            animationRunning = True
                
            if event.type == pygame.MOUSEMOTION:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    if DefaultNodeButton.isOver(event.pos) == True or CustomNodeButton.isOver(event.pos) == True:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if event.type == pygame.QUIT:
                    running = False

    elif menuState == True and animationRunning == True:
        if frameCount <= 800:
                screen.blit(RightCover, (frameCount - 800, 0))
                screen.blit(LeftCover, (800 - frameCount, 0))
                frameCount = frameCount + 16
        else:
                pygame.time.delay(1000)
                menuState = False
                animationRunning = False
                animationRunningTwo = True
    else:
        # Loads all the images for the Normal Status
        screen.blit(background, backgroundRect)
        screen.blit(OptionsMenu, OptionRect)
        screen.blit(DescriptionMenu, DescriptionRect)
        screen.blit(TitleImage, TitleRect)
        AddNodeButton.drawButton(screen=screen)
        EditNodeButton.drawButton(screen=screen)
        DeleteNodeButton.drawButton(screen=screen)
        StartButton.drawButton(screen=screen)

        # Drawing the individual Lines
        if gameState == 'Start':
            for individual_node in node:
                if len(individual_node.connections) >= 1:
                    for connection in individual_node.connections:
                        for individual_node_2 in node:
                            if individual_node_2.name == connection:
                                pygame.draw.line(screen, "black", (individual_node.x, individual_node.y), (individual_node_2.x, individual_node_2.y), 2)

        # Parse all the nodes and creates a circle
        for parse in node:
            # Draw the circle
            pygame.draw.circle(screen, parse.color, [parse.x, parse.y], parse.radius)

            # Render the name
            name_text = font.render(parse.name, True, (255, 255, 255))  # White text
            name_rect = name_text.get_rect(center=(parse.x, parse.y - parse.radius - 10))  # Position above the node
            screen.blit(name_text, name_rect)

            # Render the population
            population_text = font.render(str(parse.getPopulationValue()), True, (255, 255, 255))  # White text
            population_rect = population_text.get_rect(center=(parse.x, parse.y))  # Position at the center of the node
            screen.blit(population_text, population_rect)

        menuSurface = pygame.Surface((1600, 1000))
        menuSurface.fill((0, 0, 0))
        menuSurface.set_alpha(150)

        # Event Manager for Normal GameState
        if gameState == "Normal" and animationRunningTwo == False:
            for event in pygame.event.get():
                # Finds the cursor when it clicks down and checks for circle colision
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        currentX, currentY = event.pos
                        for num, parse in enumerate(node):
                            if currentX < (parse.x + parse.radius) and currentY < (parse.y + parse.radius):
                                if currentX > (parse.x - parse.radius) and currentY > (parse.y - parse.radius):
                                    activeNode = num
                        if EditNodeButton.isOver(event.pos):
                            gameState = 'Editing'
                        if AddNodeButton.isOver(event.pos):
                            gameState = 'Adding'
                        if DeleteNodeButton.isOver(event.pos):
                            gameState = 'Deleting'
                        if StartButton.isOver(event.pos):
                            gameState = 'Start'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menuState = True
                        screen.blit(menuScreenBackground, menuScreenBackgroundRect)

                # Stops the circle colision
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        activeNode = None

                # Moves the circle around and stops it at the menu rect
                if event.type == pygame.MOUSEMOTION:
                    currentX, currentY = event.pos
                    if activeNode != None and (menuSize + node[activeNode].radius) < currentX and (screenSizeX - menuSize - node[activeNode].radius) > currentX:
                        node[activeNode].addPosition(event.rel)
                    if activeNode != None and (menuSize + node[activeNode].radius) > currentX:
                        node[activeNode].x = menuSize + node[activeNode].radius
                    if activeNode != None and (screenSizeX - menuSize - node[activeNode].radius) < currentX:
                        node[activeNode].x = screenSizeX - menuSize - node[activeNode].radius

                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    if AddNodeButton.isOver(event.pos) == True or EditNodeButton.isOver(event.pos) == True or DeleteNodeButton.isOver(event.pos) == True or StartButton.isOver(event.pos) == True:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if event.type == pygame.QUIT:
                running = False

        elif gameState == "Normal" and animationRunningTwo == True:
            if frameCount > 0:
                screen.blit(RightCover, (frameCount - 800, 0))
                screen.blit(LeftCover, (800 - frameCount, 0))
                frameCount = frameCount - 16
            else:
                frameCount = 0
                animationRunningTwo = False

        elif gameState == 'Adding':
            running, gameState, TimelineReset = handle_adding_state(screen, screenSizeX, screenSizeY, menuSurface, menuSquareImage, menuSquareImageRect, 
                                                    menuAddingTitleImage, menuAddingTitleRect, nameAddingImage, nameAddingRect, 
                                                    populationAddingImage, populationAddingRect, connectionAddingImage, connectionAddingRect, 
                                                    AddNodeButtonAddingMenu, CancelButtonAddingMenu, input_boxes, node, gameState)
            if gameState == "Normal":
                reset_input_boxes(input_boxes)
            
        elif gameState == 'Editing':
            title_text = font.render('Choose Node to Edit', True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(screenSizeX // 2, 50))

            node_clicked = False
        
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    current_pos = event.pos

                    for n in node:
                        if n.isClicked(current_pos):
                            print("clicked on node:", n.name)
                            selectedNode = n
                            gameState = "EditPopup"
                            node_clicked = True
                            break  # Exit the node loop

                    if not node_clicked:
                        print("clicked on background")
                        gameState = "Normal"
                    
                    break  # Exit the event loop once a node is selected
                elif event.type == pygame.QUIT:
                    running = False

            screen.blit(title_text, title_rect)
            pygame.display.flip()

        elif gameState == 'EditPopup':
            running, gameState, TimelineReset = handle_edit_state(screen, screenSizeX, screenSizeY, menuSurface, gameState, menuSquareImage, 
                        menuSquareImageRect, menuEditingTitleImage, 
                        menuEditingTitleRect, nameAddingImage, 
                        nameAddingRect, populationAddingImage, 
                        populationAddingRect, connectionAddingImage, 
                        connectionAddingRect, EditNodeButtonEditingMenu, 
                        CancelButtonAddingMenu, input_boxes, node, selectedNode, reset_input_boxes)
            if gameState == "Normal":
                reset_input_boxes(input_boxes)
                reInitialize(selectedNode)

        elif gameState == 'Deleting':
            running, gameState, TimelineReset = handle_delete_state(screen, screenSizeX, screenSizeY, menuSurface, gameState, menuSquareImage, 
                        menuSquareImageRect, menuDeletingTitleImage, 
                        menuDeletingTitleRect, nameAddingImage, 
                        nameAddingRect, DeleteNodeButtonDeletingMenu, 
                        CancelButtonAddingMenu, input_boxes, node)
            if gameState == "Normal":
                reset_input_boxes(input_boxes)

        elif gameState == 'Start':
            screen.blit(DayControlMenu, DayControlMenuRect)
            CancelButtonStart.drawButton(screen=screen)
            PlusButton.drawButton(screen=screen)
            MinusButton.drawButton(screen=screen)

            for event in pygame.event.get():
                # Finds the cursor when it clicks down and checks for circle colision
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        currentX, currentY = event.pos
                        for num, parse in enumerate(node):
                            if currentX < (parse.x + parse.radius) and currentY < (parse.y + parse.radius):
                                if currentX > (parse.x - parse.radius) and currentY > (parse.y - parse.radius):
                                    activeNode = num
                        if CancelButtonStart.isOver(event.pos):
                            gameState = 'Normal'
                        if PlusButton.isOver(event.pos):
                            if (currentDay + 1) == len(NodeDaysPopulation):
                                currentDay = currentDay + 1
                                node = helper.createDay(node)
                                NodeDaysPopulation.append(helper.getPopulation(node))
                            else:
                                currentDay = currentDay + 1
                                node = helper.setPopulation(node ,NodeDaysPopulation[currentDay])

                        if MinusButton.isOver(event.pos):
                            if currentDay > 0:
                                node = helper.setPopulation(node, NodeDaysPopulation[currentDay])
                                currentDay = currentDay - 1
                            else:
                                # Add So that the Minus Button Doesnt Work here
                                node = helper.setPopulation(node, NodeDaysPopulation[0])

                # Stops the circle colision
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        activeNode = None

                # Moves the circle around and stops it at the menu rect
                if event.type == pygame.MOUSEMOTION:
                    currentX, currentY = event.pos
                    if activeNode != None and (menuSize + node[activeNode].radius) < currentX and (screenSizeX - menuSize - node[activeNode].radius) > currentX:
                        node[activeNode].addPosition(event.rel)
                    if activeNode != None and (menuSize + node[activeNode].radius) > currentX:
                        node[activeNode].x = menuSize + node[activeNode].radius
                    if activeNode != None and (screenSizeX - menuSize - node[activeNode].radius) < currentX:
                        node[activeNode].x = screenSizeX - menuSize - node[activeNode].radius

                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    if CancelButtonStart.isOver(event.pos) == True or PlusButton.isOver(event.pos) == True or MinusButton.isOver(event.pos) == True:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if event.type == pygame.QUIT:
                running = False

    # I know why now, it updates the entire screen
    pygame.display.flip()

    # limits FPS to 60 apperantly
    dt = clock.tick(60) / 1000

# Ded
pygame.quit()