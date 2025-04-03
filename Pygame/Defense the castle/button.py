import pygame

class Button:
    def __init__(self, x,y, image, rect_point=0):
        img = image
        self.image = pygame.transform.scale(img, (40, 40))
        self.startx = x
        self.starty = y
        self.rect = self.image.get_rect()
        if rect_point == 0:
            self.rect.topleft = (x, y)
        elif rect_point == 1:
            self.rect.centerx = x
            self.rect.centery = y
        elif rect_point == 2:
            self.rect.topright = (x, y)

    def draw(self, display_surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                action = True

        display_surface.blit(self.image, self.rect)
        return action