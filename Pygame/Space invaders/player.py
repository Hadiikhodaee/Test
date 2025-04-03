import pygame
from pygame import *
from pygame.sprite import Sprite
from config import WIN_HEIGHT, WIN_WIDTH, current_path, os

class Player(Sprite):
    def __init__(self, bullet_group):
        super().__init__()

        img = pygame.transform.scale(pygame.image.load(os.path.join(current_path, "assets", "images", "spaceship_yellow.png")), (64, 64))
        self.image = pygame.transform.flip(img, False, True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIN_WIDTH / 2
        self.rect.centery = WIN_HEIGHT - 38

        self.lives = 5
        self.velocity = 10
        self.laser_limit = 2

        self.bullet_group = bullet_group

        self.shot_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "player_fire.wav"))

    def fire(self):
        if len(self.bullet_group) < self.laser_limit:
            self.shot_sound.play()
            Player_bullet(self.rect.centerx, self.rect.top, self.bullet_group)

    def update(self):
        keys = pygame.key.get_pressed()
        
        if (keys[K_d] or keys[K_RIGHT]) and self.rect.right < WIN_WIDTH:
            self.rect.x += self.velocity
        elif (keys[K_a] or keys[K_LEFT]) and self.rect.left > 0:
            self.rect.x -= self.velocity

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Player_bullet(Sprite):
    def __init__(self, x, y, bullet_group):
        super().__init__()

        self.image = pygame.image.load(os.path.join(current_path, "assets", "images", "green_laser.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        self.rect.y -= self.velocity

        if self.rect.bottom < 0:
            self.kill()