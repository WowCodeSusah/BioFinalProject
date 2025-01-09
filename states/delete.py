import pygame
from node import Node
from button import Button
from input_box import InputBox

def handle_delete_state(screen, screenSizeX, screenSizeY, menuSurface, gameState, menuSquareImage, 
                      menuSquareImageRect, menuDeletingTitleImage, 
                      menuDeletingTitleRect, nameAddingImage, 
                      nameAddingRect, DeleteNodeButtonDeletingMenu, 
                      CancelButtonAddingMenu, input_boxes, node):
    screen.blit(menuSurface, (0, 0))
    screen.blit(menuSquareImage, menuSquareImageRect)
    screen.blit(menuDeletingTitleImage, menuDeletingTitleRect)
    screen.blit(nameAddingImage, nameAddingRect)

    DeleteNodeButtonDeletingMenu.drawButton(screen=screen)
    CancelButtonAddingMenu.drawButton(screen=screen)

    TimelineReset = False

    # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                currentX, currentY = event.pos
                if (currentX > (screenSizeX / 2 + 415) or currentX < (screenSizeX / 2 - 415)) or (currentY > (screenSizeY / 2 + 415) or currentY < (screenSizeY / 2 - 415)):
                    gameState = "Normal"
                if CancelButtonAddingMenu.isOver(event.pos):
                    gameState = 'Normal'
                if DeleteNodeButtonDeletingMenu.isOver(event.pos):
                    try:
                        # Use secondary validation, to check if the node exists
                        if(input_boxes[0].secondary_full_validate()):
                            for n in node:
                                print("Checking node with the name", input_boxes[0].text)
                                if n.name == input_boxes[0].text:
                                    print("Removing node", n.name)
                                    node.remove(n)
                                    TimelineReset = True
                                    break

                            gameState = "Normal"
                    except ValueError as e:
                        print(f"Error updating node: {e}")
                if CancelButtonAddingMenu.isOver(event.pos):
                    gameState = "Normal"

        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if CancelButtonAddingMenu.isOver(event.pos) == True or DeleteNodeButtonDeletingMenu.isOver(event.pos) == True:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        # for box in input_boxes:
        input_boxes[0].handle_event(event)

        # Exit
        if event.type == pygame.QUIT:
            return False, gameState
        
    # for box in input_boxes:
    input_boxes[0].update()
    input_boxes[0].draw(screen)
        
    return True, gameState, TimelineReset