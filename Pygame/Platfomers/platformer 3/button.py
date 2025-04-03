import pygame

class Button():
    def __init__(self, x, y, img, scale):
        self.image = pygame.transform.scale(img, scale)
        self.rect = self.image.get_rect(topleft=(x, y))
        clicked = False

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True
        if not pygame.mouse.get_pressed()[0]:
                self.clicked = False


        screen.blit(self.image, self.rect)

        return action