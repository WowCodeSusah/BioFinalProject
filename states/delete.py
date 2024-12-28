import pygame
from node import Node
from button import Button
from input_box import InputBox

def handle_delete_state(screen, menuSurface, gameState, menuSquareImage, 
                      menuSquareImageRect, menuAddingTitleImage, 
                      menuAddingTitleRect, nameAddingImage, 
                      nameAddingRect, populationAddingImage, 
                      populationAddingRect, connectionAddingImage, 
                      connectionAddingRect, DeleteNodeButtonDeletingMenu, 
                      CancelButtonAddingMenu):
    screen.blit(menuSurface, (0, 0))
    screen.blit(menuSquareImage, menuSquareImageRect)
    screen.blit(menuAddingTitleImage, menuAddingTitleRect)
    screen.blit(nameAddingImage, nameAddingRect)
    screen.blit(populationAddingImage, populationAddingRect)
    screen.blit(connectionAddingImage, connectionAddingRect)

    DeleteNodeButtonDeletingMenu.drawButton(screen=screen)
    CancelButtonAddingMenu.drawButton(screen=screen)

    # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                gameState = "Normal"
        # Exit
        if event.type == pygame.QUIT:
            return False, gameState
        
    return True, gameState