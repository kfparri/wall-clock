import pygame

class Button:
    "This is a generic button class"

    # image_to_use - this is a png image to display on the screen
    # x_position - 
    # y_position - 
    def __init__(self, image_to_use, x_position, y_position, rect = None, color = None):
        self.image = image_to_use
        self.x = x_position
        self.y = y_position
        if (rect == None):
            self.rect = self.image.get_rect()
        else:
            self.rect = rect
        
        self.color = color
        self.rect.x = self.x
        self.rect.y = self.y

    def collides_with(self, x, y):
        if (self.color == None):
            self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        return self.rect.collidepoint(x,y)

    def update(self, screen, color = None):
        # Make sure the rect x and y are in the correct position
        self.rect.x = self.x
        self.rect.y = self.y

        if (not self.color == None):
            if(not color == None):
                self.color = color

            pygame.draw.rect(screen, self.color, self.rect)
        else:
            screen.blit(self.image, self.rect)

