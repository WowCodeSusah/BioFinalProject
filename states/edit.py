import pygame
from node import Node
from button import Button
from input_box import InputBox

def handle_edit_state(screen, menuSurface, gameState):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    screen.blit(menuSurface, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                gameState = "Normal"
        # Exit
        if event.type == pygame.QUIT:
            return False, gameState
        
    return True, gameState