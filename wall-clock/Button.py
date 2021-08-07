class Button:
    "This is a generic button class"

    # image_to_use - this is a png image to display on the screen
    # x_position - 
    # y_position - 
    def __init__(self, image_to_use, x_position, y_position):
        self.image = image_to_use
        self.x = x_position
        self.y = y_position
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def collides_with(self, x, y):
        rect = self.image.get_rect()
        return rect.collidepoint(x,y)

    def update(self, screen):
        screen.blit(self.image, self.rect)

