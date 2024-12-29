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

# Game State (Normal / Adding / Delete / Editing/ EditPopup)
gameState = "Normal"

# Test Node
node.append(Node(1500 / 2, 1000 / 2, "test 1"))
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
        return True;
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
        screenSizeX / 3.5, 325, 250, 32, 'e.g. Fish', 
        validation_func=check_node_double, 
        secondary_validation_func=check_node_exists,
        custom_error_message='Node already exists',
        secondary_custom_error_message='Node does not exist'
    ),
    InputBox(
        screenSizeX / 3.5, 485, 250, 32, 'e.g. 100', 
        validation_func=is_number,
        custom_error_message='Input should be numeric'
    ),
    InputBox(screenSizeX / 3.5, 645, 250, 32, 'e.g. Cat:eater, Bear:eater, Plankton:food, Shrimp:food', 
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
        # Draw the circle
        pygame.draw.circle(screen, parse.color, [parse.x, parse.y], parse.radius)

        # Render the name
        name_text = font.render(parse.name, True, (255, 255, 255))  # White text
        name_rect = name_text.get_rect(center=(parse.x, parse.y - parse.radius - 10))  # Position above the node
        screen.blit(name_text, name_rect)

        # Render the population
        population_text = font.render(str(parse.population), True, (255, 255, 255))  # White text
        population_rect = population_text.get_rect(center=(parse.x, parse.y))  # Position at the center of the node
        screen.blit(population_text, population_rect)

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
                    if DeleteNodeButton.isOver(event.pos):
                        gameState = 'Deleting'

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
        running, gameState = handle_edit_state(screen, screenSizeX, screenSizeY, menuSurface, gameState, menuSquareImage, 
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
        running, gameState = handle_delete_state(screen, screenSizeX, screenSizeY, menuSurface, gameState, menuSquareImage, 
                      menuSquareImageRect, menuDeletingTitleImage, 
                      menuDeletingTitleRect, nameAddingImage, 
                      nameAddingRect, DeleteNodeButtonDeletingMenu, 
                      CancelButtonAddingMenu, input_boxes, node)
        if gameState == "Normal":
            reset_input_boxes(input_boxes)

    # I still dont know why we need this but yes
    pygame.display.flip()

    # limits FPS to 60 apperantly
    dt = clock.tick(60) / 1000

# Ded
pygame.quit()