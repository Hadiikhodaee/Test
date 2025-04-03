import math
import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    def __init__(self, health, damage, animation_list, x, y, enemy_group):
        super().__init__()
        self.max_health = health
        self.health = health
        self.animation_list = animation_list
        self.damage = damage
        self.action = 0
        self.frame_index = 0
        self.attack_coldown = 1000
        self.alive = True
        self.last_attack = pygame.time.get_ticks()

        self.angle = 0

        self.hithp = health 

        self.update_time = pygame.time.get_ticks()

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.started_y = self.rect.y

        self.width = self.image.get_width()

        self.do_kill = True
        self.alpha = 255

        self.show = False
        self.show_time = 60 * 2

        self.target = None

        enemy_group.add(self)

    def animate(self):
        ANIMATION_COLDOWN = 60

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COLDOWN:
            self.frame_index += 1
            self.image = self.animation_list[self.action][self.frame_index]
            self.update_time = pygame.time.get_ticks()

            if self.frame_index >= len(self.animation_list[self.action]) - 1:
                if self.action == 2:
                    self.frame_index = len(self.animation_list[self.action]) - 2
                else:
                    self.frame_index = 0

    def update(self, castle, bullet_group, display_surface, own_build_group):
        if self.action == 0:
            if len(own_build_group) == 1:
                self.rect.x += 1
                if self.rect.y != self.started_y:
                    if self.rect.y > self.started_y:
                        self.rect.y -= 1
                    if self.rect.y < self.started_y:
                        self.rect.y += 1
            else:
                self.dx = math.cos(self.angle) * 1
                self.dy = -(math.sin(self.angle)) * 1

                self.rect.x += self.dx
                self.rect.y += self.dy

        self.animate()

        for bullet in bullet_group:
            if pygame.sprite.spritecollide(self, bullet_group, self.do_kill):
                self.health -= bullet.damage

        if self.health <= 0:
            self.alive = False
            self.action = 2
            self.do_kill = False
            if self.frame_index == len(self.animation_list[self.action]) - 2:
                self.image.set_alpha(self.alpha)
                self.alpha -= 5
                if self.alpha <= 0:
                    castle.money += self.max_health
                    self.kill()

        if self.action == 1:
            if pygame.time.get_ticks() - self.last_attack >= self.attack_coldown and self.frame_index == 10:
                self.target.health -= self.damage
                self.last_attack = pygame.time.get_ticks()
            if self.target.health < 0:
                self.target.health = 0
        if self.alive:
            enemy_hp_persent = self.width / 2 * float(self.health)/float(self.max_health)
            x = self.rect.topleft[0] + 5
            y = self.rect.topleft[1] + 5
            if self.hithp > self.health:
                self.show = True
                self.hithp = self.health
            if self.show:
                pygame.draw.rect(display_surface, (0, 0, 0), (x, y, self.width / 2, 5))
                pygame.draw.rect(display_surface, (255, 0, 0), (x, y, enemy_hp_persent, 5))
                self.show_time -= 1
            if self.show_time <= 0:
                self.show_time = 60 * 2
                self.show = False