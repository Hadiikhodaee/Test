import pygame, random
from pygame.sprite import Sprite
from config import WIN_HEIGHT, current_path, os

class Alien(Sprite):
    def __init__(self, x, y, velocity, alien_group, bullet_group):
        super().__init__()

        self.image = pygame.image.load(os.path.join(current_path, "assets", "images", "alien.png"))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.direction = 1
        self.velocity = velocity
        self.bullet_group = bullet_group

        alien_group.add(self)

        self.shoot_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "alien_fire.wav"))

    def fire(self):
        self.shoot_sound.play()
        Alien_bullet(self.rect.centerx, self.rect.bottom, self.bullet_group)

    def update(self):
        self.rect.x += self.velocity * self.direction

        if random.randint(0, 2000) > 1999:
            self.fire()

class Alien_bullet(Sprite):
    def __init__(self, x, y, bullet_group):
        super().__init__()

        self.image = pygame.image.load(os.path.join(current_path, "assets", "images", "red_laser.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        self.rect.y += self.velocity

        if self.rect.top > WIN_HEIGHT:
            self.kill()