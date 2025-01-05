import pygame as pg
import time

pg.init()
COLOR_INACTIVE = pg.Color('aqua')
COLOR_ACTIVE = pg.Color('aliceblue')
COLOR_INVALID = pg.Color('red')
FONT = pg.font.Font(None, 32)

class InputBox:

    def __init__(self, x, y, w, h, placeholder='', validation_func=None, secondary_validation_func=None, custom_error_message='', secondary_custom_error_message=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = ''
        self.placeholder = placeholder  # Store the placeholder text
        self.txt_surface = FONT.render(self.placeholder, True, self.color)
        self.active = False
        self.validation_func = validation_func
        self.secondary_validation_func = secondary_validation_func # backup validation for specific cases
        self.error_message = ''
        self.custom_error_message = custom_error_message
        self.secondary_custom_error_message = secondary_custom_error_message
        self.txt_rect = self.txt_surface.get_rect()
        self.cursor = pg.Rect(self.txt_rect.topright, (3, self.txt_rect.height + 2))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                if self.active:
                    if self.text == self.placeholder:
                        self.text = ''  # Clear the text when activated
                else:
                    if self.text == '':
                        self.text = self.placeholder  # Reset to placeholder if empty
            else:
                self.active = False
                if self.text == '':
                    self.text = self.placeholder  # Reset to placeholder if empty
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            # Re-render the text.
            self.txt_surface = FONT.render(self.text, True, self.color)
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # pg.draw.rect(screen, self.color, self.rect, 2)
        if self.active:
            if time.time() % 1 > 0.5:

                # bounding rectangle of the text
                text_rect = self.txt_surface.get_rect(topleft = (self.rect.x + 5, self.rect.y + 5))

                # set cursor position
                self.cursor.midleft = text_rect.midright

                pg.draw.rect(screen, self.color, self.cursor)

        if self.error_message:
            error_surface = FONT.render(self.error_message, True, (255, 0, 0))
            screen.blit(error_surface, (self.rect.x, self.rect.y - 25))

    def reset(self):
        self.text = ''
        self.txt_surface = FONT.render(self.placeholder, True, self.color)
        self.error_message = ''

    def specific_validate(self):
        if self.validation_func and not self.validation_func(self.text):
            if self.custom_error_message != '':
                self.error_message = self.custom_error_message
            else:  
                self.error_message = "Invalid input"
            self.color = COLOR_INVALID
            return False
        self.error_message = ''
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        return True
    
    def full_validate(self):
        if not self.text or self.text == self.placeholder:
            self.error_message = "Input cannot be empty"
            self.color = COLOR_INVALID
            return False
        if self.validation_func and not self.validation_func(self.text):
            if self.custom_error_message != '':
                self.error_message = self.custom_error_message
            else: 
                self.error_message = "Invalid input"
            self.color = COLOR_INVALID
            return False
        self.error_message = ''
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        return True
    
    def secondary_full_validate(self):
        if not self.text or self.text == self.placeholder:
            self.error_message = "Input cannot be empty"
            self.color = COLOR_INVALID
            return False
        if self.secondary_validation_func and not self.secondary_validation_func(self.text):
            if self.secondary_custom_error_message != '':
                self.error_message = self.secondary_custom_error_message
            else: 
                self.error_message = "Invalid input"
            self.color = COLOR_INVALID
            return False
        self.error_message = ''
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        return True