import pygame
from pygame.sprite import Sprite
from config import 2, WIN_WIDTH, current_path, os
import math

class Bullet(Sprite):
    def __init__(self, x ,y, angle):
        super().__init__()

        img = pygame.image.load(os.path.join(current_path,"defense_game","assets","bullet.png"))
        self.image = pygame.transform.scale(img, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = angle
        self.speed = 10

        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle)) * self.speed
    
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.right < 0 or self.rect.left > WIN_WIDTH or self.rect.top > 2 or self.rect.bottom < 0:
            self.kill()