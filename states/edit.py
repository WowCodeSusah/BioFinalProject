import pygame
from node import Node
from button import Button
from input_box import InputBox
FONT = pygame.font.Font(None, 32)

tempNameContainer = ''

def handle_edit_state(screen, screenSizeX, screenSizeY, menuSurface, gameState, menuSquareImage, 
                      menuSquareImageRect, menuEditingTitleImage, 
                      menuEditingTitleRect, nameAddingImage, 
                      nameAddingRect, populationAddingImage, 
                      populationAddingRect, connectionAddingImage, 
                      connectionAddingRect, EditNodeButtonEditingMenu, 
                      CancelButtonAddingMenu, input_boxes, node, selectedNode, reset_input_boxes):
    global tempNameContainer
    
    screen.blit(menuSurface, (0, 0))
    screen.blit(menuSquareImage, menuSquareImageRect)
    screen.blit(menuEditingTitleImage, menuEditingTitleRect)
    screen.blit(nameAddingImage, nameAddingRect)
    screen.blit(populationAddingImage, populationAddingRect)
    screen.blit(connectionAddingImage, connectionAddingRect)

    EditNodeButtonEditingMenu.drawButton(screen=screen)
    CancelButtonAddingMenu.drawButton(screen=screen)

    TimelineReset = False

    # Input boxes data and rendering
    if gameState == "EditPopup" and not hasattr(selectedNode, "_initialized"):
        input_boxes[0].text = selectedNode.name
        input_boxes[0].txt_surface = FONT.render(selectedNode.name, True, pygame.Color('aliceblue'))
        tempNameContainer = input_boxes[0].text
        input_boxes[1].text = str(selectedNode.population)
        input_boxes[1].txt_surface = FONT.render(str(selectedNode.population), True, pygame.Color('aliceblue'))
        input_boxes[2].text = ','.join(selectedNode.connections)
        input_boxes[2].txt_surface = FONT.render(','.join(selectedNode.connections), True, pygame.Color('aliceblue'))
        selectedNode._initialized = True

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
                        if(input_boxes[1].full_validate()):
                            # if name is changed, validate it
                            if input_boxes[0].text != tempNameContainer:
                                if not input_boxes[0].full_validate():
                                    print("Name validation failed")
                                    break

                            if(input_boxes[2].text == input_boxes[2].placeholder):
                                input_boxes[2].text = ""
                            
                            # if connection is not empty, validate it
                            if input_boxes[2].text != '':
                                if input_boxes[2].specific_validate() == False:
                                    print('Invalid input')
                                    break

                            selectedNode.setName(input_boxes[0].text)
                            selectedNode.setPopulation(int(input_boxes[1].text))  # Convert to integer
                            selectedNode.addConnection(input_boxes[2].text)  # Parse comma-separated connections

                            TimelineReset = True

                            # Update the node list
                            for i, n in enumerate(node):
                                if n == selectedNode:
                                    node[i] = selectedNode
                                    break

                            gameState = "Normal"
                    except ValueError as e:
                        print(f"Error updating node: {e}")
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
            reset_input_boxes(input_boxes)
            return False, gameState
        
    for box in input_boxes:
        box.update()
        box.draw(screen)

    return True, gameState, TimelineReset