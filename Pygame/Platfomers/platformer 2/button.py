import pygame

class Button:
    def __init__(self, x, y, image, scale:tuple=None):
        if scale == None:
            self.image = image
        else:
            self.image = pygame.transform.scale(image, scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, display_surface):

        klicked = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                klicked = True

        display_surface.blit(self.image, self.rect)
        return klicked