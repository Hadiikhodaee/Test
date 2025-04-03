from random import choice
import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/images/characters/blob.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.dx = choice([-1, 1])
        self.velocity = 2

        self.die_sound = pygame.mixer.Sound("assets/sounds/blob_die.wav")
        self.die_sound.set_volume(0.3)

    def update(self, tile_list, player_rect, game_over, hell_mode, WIN_WIDTH):
        self.rect.x += self.dx * self.velocity

        for tile in tile_list:
            if tile[2] in [0, 1, 2, 3, 4, 5, 11]:
                if tile[1].colliderect(self.rect.x, self.rect.y - 5, self.width, self.height):
                    self.dx *= -1

        if self.rect.right > WIN_WIDTH or self.rect.left < 0:
            self.dx *= -1

        if hell_mode:
            self.image = pygame.image.load("assets/images/hell images/hell_blob.png")

        else:
            if player_rect.colliderect(self.rect.x + 11, self.rect.y - 2, self.width - 22, self.height - 28) and game_over != -1:
                self.kill()
                self.die_sound.play()