import helper
import pygame

class Button():
    def __init__(self, buttonFile, buttonPressedFile, x, y):
        self.buttonFile = buttonFile
        self.buttonPressedFile = buttonPressedFile
        self.x = x
        self.y = y
        self.height = 49
        self.width = 130
        self.buttonImage = None
        self.buttonRect = None
        self.buttonPressedImage = None
        self.buttonPressedRect = None
        self.preLoadStatus = False
        self.mouseOnTop = False

    def preLoad(self):
        self.buttonImage, self.buttonRect = helper.createImageImport(self.buttonFile, self.x, self.y)
        self.buttonPressedImage, self.buttonPressedRect =  helper.createImageImport(self.buttonPressedFile, self.x, self.y)
        self.preLoadStatus = True

    def drawButton(self, screen):
        if self.preLoadStatus == False:
            print("Haven't been Preloaded")
        elif self.preLoadStatus == True and self.mouseOnTop == False:
            screen.blit(self.buttonImage, self.buttonRect)
        elif self.preLoadStatus == True and self.mouseOnTop == True:
            screen.blit(self.buttonPressedImage, self.buttonPressedRect)
        
    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x - self.width and pos[0] < self.x + self.width:
            if pos[1] > self.y - self.height and pos[1] < self.y + self.height:
                self.mouseOnTop = True
                return True
        self.mouseOnTop = False
        return False