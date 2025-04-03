import pygame
from pygame import *
from pygame.sprite import Sprite
from config import WIN_HEIGHT, WIN_WIDTH, current_path, os

class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.alive = True
        
        self.image = pygame.image.load(os.path.join(current_path, "assets", "images", "knight.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIN_WIDTH // 2
        self.rect.bottom = WIN_HEIGHT

        self.health = 5
        self.wraps = 2
        self.velocity = 8

        self.catch_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "catch.wav"))
        self.wrap_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "warp.wav"))
        self.die_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "die.wav"))

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[K_UP] or keys[K_w]) and self.rect.top > 100:
            self.rect.y -= self.velocity
        if (keys[K_DOWN] or keys[K_s]) and self.rect.bottom < WIN_HEIGHT - 100:
            self.rect.y += self.velocity
        if (keys[K_LEFT] or keys[K_a]) and self.rect.left > 0:
            self.rect.x -= self.velocity
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.right < WIN_WIDTH:
            self.rect.x += self.velocity
            
    def wrap(self):
        if self.wraps > 0:
            self.wraps -= 1
            self.wrap_sound.play()
            self.rect.bottom = WIN_HEIGHT

    def reset(self):
        self.rect.centerx = WIN_WIDTH // 2
        self.rect.bottom = WIN_HEIGHT

    def draw(self, screen):
        screen.blit(self.image, self.rect)