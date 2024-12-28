# Need Imports
import pygame
from node import Node
from button import Button
from input_box import InputBox
import helper
from states.adding import handle_adding_state
from states.edit import handle_edit_state


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

# Node List
node = []

# Game State (Normal / Adding / Delete / Editing)
gameState = "Normal"

# Test Node
node.append(Node(1500 / 2, 1000 / 2, "test 1"))
activeNode = None

# Image Generator
background , backgroundRect= helper.createImageImport('resources/background.jpg', screenSizeX / 2, screenSizeY / 2)
OptionsMenu, OptionRect = helper.createImageImport('resources/OptionsMenu.jpg', menuSize / 2, screenSizeY / 2)
DescriptionMenu, DescriptionRect = helper.createImageImport('resources/DescriptionMenu.jpg', (screenSizeX - menuSize / 2), screenSizeY / 2)
TitleImage, TitleRect = helper.createImageImport('resources/Title.png', 150, 100)

# Images for Menu
menuSquareImage, menuSquareImageRect = helper.createImageImport('resources/menuSquare.png', screenSizeX / 2, screenSizeY / 2)
menuAddingTitleImage, menuAddingTitleRect = helper.createImageImport('resources/AddingNodeTitle.png', 550 , 200)
nameAddingImage, nameAddingRect = helper.createImageImport('resources/nameBar.png', screenSizeX / 2 , 350)
populationAddingImage, populationAddingRect = helper.createImageImport('resources/PopulationBar.png', screenSizeX / 2, 510)
connectionAddingImage, connectionAddingRect = helper.createImageImport('resources/ConnectionBar.png', screenSizeX / 2, 670)

# Menu Button
CancelButtonAddingMenu = Button('resources/buttons/CancelButton.png', 'resources/buttons/CancelButtonPressed.png', 750, 830)
CancelButtonAddingMenu.preLoad()

AddNodeButtonAddingMenu = Button('resources/buttons/AddNodeButton.png', 'resources/buttons/AddNodeButtonPressed.png', 1050, 830)
AddNodeButtonAddingMenu.preLoad()

# Init all Buttons
AddNodeButton = Button('resources/buttons/AddNodeButton.png', 'resources/buttons/AddNodeButtonPressed.png', 150, 600)
AddNodeButton.preLoad()

EditNodeButton = Button('resources/buttons/EditNodeButton.png', 'resources/buttons/EditNodeButtonPressed.png', 150, 700)
EditNodeButton.preLoad()

DeleteNodeButton = Button('resources/buttons/DeleteNodeButton.png', 'resources/buttons/DeleteNodeButtonPressed.png', 150, 800)
DeleteNodeButton.preLoad()

StartButton = Button('resources/buttons/StartButton.png', 'resources/buttons/StartButtonPressed.png', 150, 900)
StartButton.preLoad()

input_boxes = [
    InputBox(screenSizeX / 3.5, 325, 250, 32, 'Insert Name'),
    InputBox(screenSizeX / 3.5, 485, 250, 32, 'Insert Population'),
    InputBox(screenSizeX / 3.5, 645, 250, 32, 'Insert Connection')
]

# Pygame Loop
while running:
    # Loads all the images for the Normal Status
    screen.blit(background, backgroundRect)
    screen.blit(OptionsMenu, OptionRect)
    screen.blit(DescriptionMenu, DescriptionRect)
    screen.blit(TitleImage, TitleRect)
    AddNodeButton.drawButton(screen=screen)
    EditNodeButton.drawButton(screen=screen)
    DeleteNodeButton.drawButton(screen=screen)
    StartButton.drawButton(screen=screen)


    # Parse all the nodes and creates a circle
    for parse in node:
        pygame.draw.circle(screen, parse.color, [parse.x, parse.y], parse.radius)

    menuSurface = pygame.Surface((1600, 1000))
    menuSurface.fill((0, 0, 0))
    menuSurface.set_alpha(150)

    # Event Manager for Normal GameState
    if gameState == "Normal":
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

    elif gameState == 'Adding':
        running, gameState = handle_adding_state(screen, screenSizeX, screenSizeY, menuSurface, menuSquareImage, menuSquareImageRect, 
                                                 menuAddingTitleImage, menuAddingTitleRect, nameAddingImage, nameAddingRect, 
                                                 populationAddingImage, populationAddingRect, connectionAddingImage, connectionAddingRect, 
                                                 AddNodeButtonAddingMenu, CancelButtonAddingMenu, input_boxes, node, gameState)            
    elif gameState == 'Editing':
        running, gameState = handle_edit_state(screen, menuSurface, gameState)
        # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        # screen.blit(menuSurface, (0, 0))
        # for event in pygame.event.get():
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if event.button == 1:
        #             gameState = "Normal"
        # # Exit
        # if event.type == pygame.QUIT:
        #     running = False

    # I still dont know why we need this but yes
    pygame.display.flip()

    # limits FPS to 60 apperantly
    dt = clock.tick(60) / 1000

# Ded
pygame.quit()