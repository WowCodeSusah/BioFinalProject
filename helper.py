import pygame

def createImageImport(link, x, y):
    image = pygame.image.load(link).convert_alpha()
    rect = image.get_rect()
    rect.center = (x, y)
    return (image, rect)