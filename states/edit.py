import pygame
from node import Node
from button import Button
from input_box import InputBox

def handle_edit_state(screen, screenSizeX, screenSizeY, menuSurface, gameState, menuSquareImage, 
                      menuSquareImageRect, menuAddingTitleImage, 
                      menuAddingTitleRect, nameAddingImage, 
                      nameAddingRect, populationAddingImage, 
                      populationAddingRect, connectionAddingImage, 
                      connectionAddingRect, EditNodeButtonEditingMenu, 
                      CancelButtonAddingMenu, input_boxes, node, selectedNode):
    screen.blit(menuSurface, (0, 0))
    screen.blit(menuSquareImage, menuSquareImageRect)
    screen.blit(menuAddingTitleImage, menuAddingTitleRect)
    screen.blit(nameAddingImage, nameAddingRect)
    screen.blit(populationAddingImage, populationAddingRect)
    screen.blit(connectionAddingImage, connectionAddingRect)

    EditNodeButtonEditingMenu.drawButton(screen=screen)
    CancelButtonAddingMenu.drawButton(screen=screen)

    # Input boxes data and rendering
    if gameState == "EditPopup" and not hasattr(selectedNode, "_initialized"):
        input_boxes[0].text = selectedNode.name
        input_boxes[1].text = str(selectedNode.population)
        input_boxes[2].text = ','.join(selectedNode.connections)
        selectedNode._initialized = True
    # input_boxes[0].text = selectedNode.name
    # input_boxes[1].text = str(selectedNode.population)
    # input_boxes[2].text = ','.join(selectedNode.connections)

    # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                currentX, currentY = event.pos
                if (currentX > (screenSizeX / 2 + 415) or currentX < (screenSizeX / 2 - 415)) or (currentY > (screenSizeY / 2 + 415) or currentY < (screenSizeY / 2 - 415)):
                    gameState = "Normal"
                if CancelButtonAddingMenu.isOver(event.pos):
                    gameState = 'Normal'
                if EditNodeButtonEditingMenu.isOver(event.pos):
                    try:
                        selectedNode.setName(input_boxes[0].text)
                        selectedNode.setPopulation(int(input_boxes[1].text))  # Convert to integer
                        selectedNode.addConnection(input_boxes[2].text)  # Parse comma-separated connections

                        # Update the node list
                        for i, n in enumerate(node):
                            if n == selectedNode:
                                node[i] = selectedNode
                                break

                        gameState = "Normal"
                    except ValueError as e:
                        print(f"Error updating node: {e}")
                    # selectedNode.setName(input_boxes[0].text)
                    # selectedNode.setPopulation(input_boxes[1].text)
                    # selectedNode.addConnection(input_boxes[2].text)

                    # for i, n in enumerate(node):
                    #     if n == selectedNode:  # Identify the node in the array
                    #         node[i] = selectedNode
                    #         break  # Exit loop after updating

                    # gameState = "Normal"
                if CancelButtonAddingMenu.isOver(event.pos):
                    gameState = "Normal"

        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if CancelButtonAddingMenu.isOver(event.pos) == True or EditNodeButtonEditingMenu.isOver(event.pos) == True:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        for box in input_boxes:
            box.handle_event(event)

        # Exit
        if event.type == pygame.QUIT:
            return False, gameState
        
    for box in input_boxes:
        box.update()
        box.draw(screen)
        
    if gameState == "Normal" and hasattr(selectedNode, "_initialized"):
        del selectedNode._initialized

    return True, gameState