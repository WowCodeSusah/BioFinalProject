import pygame
from node import Node
from button import Button
from input_box import InputBox

def handle_adding_state(screen, screenSizeX, screenSizeY, menuSurface, menuSquareImage, menuSquareImageRect, 
                        menuAddingTitleImage, menuAddingTitleRect, nameAddingImage, nameAddingRect, 
                        populationAddingImage, populationAddingRect, connectionAddingImage, connectionAddingRect, 
                        AddNodeButtonAddingMenu, CancelButtonAddingMenu, input_boxes, node, gameState):
    screen.blit(menuSurface, (0, 0))
    screen.blit(menuSquareImage, menuSquareImageRect)
    screen.blit(menuAddingTitleImage, menuAddingTitleRect)
    screen.blit(nameAddingImage, nameAddingRect)
    screen.blit(populationAddingImage, populationAddingRect)
    screen.blit(connectionAddingImage, connectionAddingRect)

    AddNodeButtonAddingMenu.drawButton(screen=screen)
    CancelButtonAddingMenu.drawButton(screen=screen)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                currentX, currentY = event.pos
                if (currentX > (screenSizeX / 2 + 415) or currentX < (screenSizeX / 2 - 415)) or (currentY > (screenSizeY / 2 + 415) or currentY < (screenSizeY / 2 - 415)):
                    gameState = "Normal"
                if CancelButtonAddingMenu.isOver(event.pos):
                    gameState = 'Normal'
                if AddNodeButtonAddingMenu.isOver(event.pos):
                    node_name = input_boxes[0].text
                    node_population = input_boxes[1].text
                    node_connections = input_boxes[2].text
                    
                    newNode = Node(screenSizeX / 2, screenSizeY / 2, node_name)
                    newNode.setPopulation(node_population)
                    newNode.addConnection(node_connections)

                    node.append(newNode)

                    print('Node Added')

                    gameState = 'Normal'

        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if CancelButtonAddingMenu.isOver(event.pos) == True or AddNodeButtonAddingMenu.isOver(event.pos) == True:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        for box in input_boxes:
            box.handle_event(event)

        if event.type == pygame.QUIT:
            return False, gameState
    
    for box in input_boxes:
        box.update()
        box.draw(screen)
    
    return True, gameState