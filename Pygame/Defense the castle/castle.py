import math
import pygame
from pygame.sprite import Sprite
from config import 2, WIN_WIDTH, current_path, os
from game import draw_text
from game import get_distance

class Bullet(Sprite):
    def __init__(self, x ,y, angle, damage):
        super().__init__()

        img = pygame.image.load(os.path.join(current_path,"assets","bullet.png"))
        self.image = pygame.transform.scale(img, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = angle
        self.damage = damage
        self.speed = 10

        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle)) * self.speed
    
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.right < 0 or self.rect.left > WIN_WIDTH or self.rect.top > 2 or self.rect.bottom < 0:
            self.kill()

bullet_group = pygame.sprite.Group()

class Castle(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.health = 1000
        self.max_health = self.health
        self.fired = False
        img_100 = pygame.image.load(os.path.join(current_path,"assets","castle","castle_100.png"))
        img_50 = pygame.image.load(os.path.join(current_path,"assets","castle","castle_50.png"))
        img_25 = pygame.image.load(os.path.join(current_path,"assets","castle","castle_25.png"))
        self.image_100 = pygame.transform.scale(img_100, (220, 220))
        self.image_50  = pygame.transform.scale(img_50, (220, 220))
        self.image_25  = pygame.transform.scale(img_25, (220, 220))
        self.image = self.image_100
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = 25
        self.width = self.image.get_width()
        self.level = 1

        self.money = 1000

    def draw(self, display_surface):
        display_surface.blit(self.image, self.rect)

    def shoot(self):
        if self.health == self.max_health:
            self.image = self.image_100

        elif 26 <= 100 * float(self.health)/float(self.max_health) <= 50:
            self.image = self.image_50

        elif 100 * float(self.health)/float(self.max_health) <= 25:
            self.image = self.image_25

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.midleft[0] + 20
        y_dist = -(pos[1] - self.rect.midleft[1])
        self.angle = math.atan2(y_dist, x_dist)
        if pygame.mouse.get_pressed()[0] and not self.fired:
            bullet = Bullet(self.rect.midleft[0] + 20, self.rect.midleft[1], self.angle, self.damage)
            bullet_group.add(bullet)
            self.fired = True
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

    def show_info(self, display_surface):
        font = pygame.font.SysFont("Algerian Regular", 20)
        draw_text(display_surface, f"Level : {self.level}", font, (0, 0, 255), self.rect.topleft[0] + self.width / 2, self.rect.topleft[1] - 46, 1)
        draw_text(display_surface, f"HP : {self.health}", font, (0, 0, 255), self.rect.topleft[0] + self.width / 2, self.rect.topleft[1] - 34, 1)
        draw_text(display_surface, f"Max HP : {self.max_health}", font, (0, 0, 255), self.rect.topleft[0] + self.width / 2, self.rect.topleft[1] - 22, 1)
        draw_text(display_surface, f"Damage : {self.damage}", font, (0, 0, 255), self.rect.topleft[0] + self.width / 2, self.rect.topleft[1] - 10, 1)

    def repair(self):
        if self.health < self.max_health:
            if self.money >= 500:
                self.money -= 500
                self.health += self.max_health // 4
        if self.max_health < self.health:
            self.health = self.max_health

    def level_up(self):
        if self.money >= self.level * 1000:
            if self.level < 10:
                self.money -= self.level * 1000
                self.level += 1
                self.max_health += 500
                self.health += 500
                self.damage += 5

class Tower(Sprite):
    def __init__(self, x, y, castle, enemy_group):
        super().__init__()
        self.health = 500
        self.max_health = self.health
        img_100 = pygame.image.load(os.path.join(current_path,"assets","tower","tower_100.png"))
        img_50 = pygame.image.load(os.path.join(current_path,"assets","tower","tower_50.png"))
        img_25 = pygame.image.load(os.path.join(current_path,"assets","tower","tower_25.png"))
        self.image_100 = pygame.transform.scale(img_100, (50, 100))
        self.image_50 = pygame.transform.scale(img_50, (50, 100))
        self.image_25 = pygame.transform.scale(img_25, (50, 100))
        self.image = self.image_100
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        self.damage = 15
        self.castle = castle
        self.last_shoot_time = pygame.time.get_ticks()
        self.enemy_group = enemy_group
        self.width = self.image.get_width()
        self.level = 1

        self.alpha = 255

    def draw(self, display_surface):
        display_surface.blit(self.image, self.rect)

    def update(self):
        if self.health == self.max_health:
            self.image = self.image_100

        elif 26 <= 100 * float(self.health)/float(self.max_health) <= 50:
            self.image = self.image_50

        elif 100 * float(self.health)/float(self.max_health) <= 25:
            self.image = self.image_25

        self.shoot()

        if self.health == 0:
            self.alpha -= 5
            self.image.set_alpha(self.alpha)
            if self.alpha <= 0:
                self.kill()

    def shoot(self):
        for enemy in self.enemy_group:
            enemy_distance = get_distance(self.rect, enemy.rect)
            for enemy2 in self.enemy_group:
                enemy_distance2 = get_distance(self.rect, enemy2.rect)
                if enemy_distance < enemy_distance2:
                    x_dist = enemy.rect.x - (self.rect.topleft[0] - self.width / 2)
                    y_dist = -(enemy.rect.y - (self.rect.topleft[1] - self.width / 2))
                    self.angle = math.atan2(y_dist, x_dist)
                    if pygame.time.get_ticks() - self.last_shoot_time >= 1000:
                        self.last_shoot_time = pygame.time.get_ticks()
                        bullet = Bullet(self.rect.topleft[0] - self.width / 2, self.rect.topleft[1] - self.width / 2, self.angle, self.damage)
                        bullet_group.add(bullet)

    def show_info(self, display_surface):
        font = pygame.font.SysFont("Algerian Regular", 20)
        draw_text(display_surface, f"Level : {self.level}", font, (0, 0, 255), self.rect.topleft[0] + self.width / 2, self.rect.topleft[1] - 46, 1)
        draw_text(display_surface, f"HP : {self.health}", font, (0, 0, 255), self.rect.topleft[0] + self.width / 2, self.rect.topleft[1] - 34, 1)
        draw_text(display_surface, f"max HP : {self.max_health}", font, (0, 0, 255), self.rect.topleft[0] + self.width / 2, self.rect.topleft[1] - 22, 1)
        draw_text(display_surface, f"Damage : {self.damage}", font, (0, 0, 255), self.rect.topleft[0] + self.width / 2, self.rect.topleft[1] - 10, 1)

    def repair(self):
        if self.health < self.max_health:
            if self.castle.money >= 250:
                self.castle.money -= 250
                self.health += self.max_health // 4
        if self.max_health < self.health:
            self.health = self.max_health

    def level_up(self):
        if self.castle.money >= self.level * 500:
            if self.level < 5:
                self.castle.money -= self.level * 500
                self.level += 1
                self.max_health += 150
                self.health += 150
                self.damage += 2.5

class Crosshair:
    def __init__(self, image):
        img = image
        self.image = pygame.transform.scale(img, (35, 35))
        self.rect = self.image.get_rect()

        pygame.mouse.set_visible(False)

    def draw(self, display_surface):
        self.rect.center = pygame.mouse.get_pos()
        display_surface.blit(self.image, self.rect)