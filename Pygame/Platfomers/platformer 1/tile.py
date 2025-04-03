import pygame.sprite
from config import current_path, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image_int, main_group, sub_group=""):
        super().__init__()

        if image_int == 1:
            self.image = pygame.image.load(os.path.join(current_path, "assets", "dirt.png"))
        elif image_int == 2:
            self.image = pygame.image.load(os.path.join(current_path, "assets", "grass.png"))
            sub_group.add(self)
        else:
            self.image = pygame.image.load(os.path.join(current_path, "assets", "water.png"))
            sub_group.add(self)

        main_group.add(self)
        self.rect = self.image.get_rect ()
        self.rect.topleft = (x, y)