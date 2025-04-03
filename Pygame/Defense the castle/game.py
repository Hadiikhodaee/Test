import math
import random
import pygame
from config import WIN_HEIGHT, WIN_WIDTH, current_path, os
from enemy import Enemy
from button import Button

def get_distance(rect1, rect2):
    x1, y1 = rect1.topleft
    x1b, y1b = rect1.bottomright
    x2, y2 = rect2.topleft
    x2b, y2b = rect2.bottomright
    left = x2b < x1
    right = x1b < x2
    top = y2b < y1
    bottom = y1b < y2
    if bottom and left:
        return math.hypot(x2b-x1, y2-y1b)
    elif left and top:
        return math.hypot(x2b-x1, y2b-y1)
    elif top and right:
        return math.hypot(x2-x1b, y2b-y1)
    elif right and bottom:
        return math.hypot(x2-x1b, y2-y1b)
    elif left:
        return x1 - x2b
    elif right:
        return x2 - x1b
    elif top:
        return y1 - y2b
    elif bottom:
        return y2 - y1b
    else:
        return 0

def draw_text(display_surface, text, font, color, x, y, rect_point=0):
    text = font.render(text, True, color)
    rect = text.get_rect()
    if rect_point == 0:
        rect.topleft = (x, y)
    elif rect_point == 1:
        rect.centerx = x
        rect.centery = y
    elif rect_point == 2:
        rect.topright = (x, y)
    elif rect_point == 3:
        rect.bottomleft = (x, y)
    elif rect_point == 4:
        rect.bottomright = (x, y)
    display_surface.blit(text, rect)

enemy_animations = []

enemy_types = ["goblin", "knight", "purple_goblin", "red_goblin"]
animation_types = ["walk", "attack", "death"]
enemy_health = [75, 100, 150, 200]
enemy_damage = [10, 15, 20, 25]

for enemy in enemy_types:
    animation_list = []
    for animation in animation_types:
        temp_list = []
        for i in range(20):
            img = pygame.image.load(os.path.join(current_path,"assets","enemies",enemy,animation,f"{i}.png"))
            img = pygame.transform.scale(img, (64, 64))
            temp_list.append(img)
        animation_list.append(temp_list)
    enemy_animations.append(animation_list)

class Game:
    def __init__(self, castle, enemy_group, bullet_group, crosshair, own_builds_group):
        self.castle = castle
        self.enemy_group = enemy_group
        self.bullet_group = bullet_group
        self.crosshair = crosshair
        self.own_builds_group = own_builds_group

        self.mouse_job_number = 0 #0 -> shoot    1 -> repair    2 -> armour    3 ->    tower
        self.mouse_clicked = False
        self.tower_cost = 5000

        self.level_number = 1
        self.level_difficulty = 0
        self.target_difficulty = 1000
        self.DIFFICULTY_MULTIPLIER = 1.3

        self.small_font = pygame.font.SysFont("Algerian Regular", 28)
        self.big_font = pygame.font.SysFont("Algerian Regular", 84)

        self.crosshair_image = pygame.image.load(os.path.join(current_path,"assets","crosshair.png"))
        self.repair_image = pygame.image.load(os.path.join(current_path,"assets","repair.png"))
        self.armour_image = pygame.image.load(os.path.join(current_path,"assets","armour.png"))
        self.tower_image = pygame.image.load(os.path.join(current_path,"assets","tower.png"))

        self.repair_button = Button(500, 50, self.repair_image)
        self.armour_button = Button(600, 50, self.armour_image)
        self.tower_button = Button(700, 50, self.tower_image)

        self.enemies_alive = 0
        self.last_enemy = pygame.time.get_ticks()
        self.spawn_coldown = 1000
        self.game_over = False
        self.win = False

    def update(self, display_surface, tower):
        if not self.game_over:
            if not self.win:
                if self.level_difficulty < self.target_difficulty:
                    if pygame.time.get_ticks() - self.last_enemy > self.spawn_coldown:
                        self.last_enemy = pygame.time.get_ticks()
                        e = random.randint(0, len(enemy_types)-1)
                        e_y = random.randint(290, 460)
                        enemy = Enemy(enemy_health[e], enemy_damage[e], enemy_animations[e], -10, e_y, self.enemy_group)
                        self.enemy_group.add(enemy)
                        self.level_difficulty += enemy_health[e]

            for enemy in self.enemy_group:
                for build in self.own_builds_group:
                    build_distance = get_distance(enemy.rect, build.rect)
                    for build2 in self.own_builds_group:
                        build_distance2 = get_distance(enemy.rect, build2.rect)
                        if build_distance < build_distance2:
                            x_dist = (build.rect.midleft[0] + 30) - enemy.rect.midright[0]
                            y_dist = -(build.rect.midleft[1] - enemy.rect.midright[1])
                            angle = math.atan2(y_dist, x_dist)

                            enemy.angle = angle

            for enemy in self.enemy_group:
                for build in self.own_builds_group:
                    if enemy.rect.colliderect(build.rect) and enemy.rect.right > build.rect.left + 30:
                        enemy.target = build
                        enemy.action = 1
                    if enemy.health <= 0:
                        enemy.action = 2
                    if build.health == 0:
                        enemy.action = 0
                        enemy.target = None

            if self.level_difficulty >= self.target_difficulty:
                enemies_alive = 0
                for enemy in self.enemy_group:
                    if enemy.alive:
                        enemies_alive += 1
                if not self.enemy_group:
                    enemies_alive = 0

                if enemies_alive == 0:
                    self.new_level(display_surface)

            self.own_builds_group.update()
            self.bullet_group.update()
            if self.repair_button.draw(display_surface):
                self.crosshair.image = pygame.transform.scale(self.repair_image, (35, 35))
                self.mouse_job_number = 1
                self.mouse_clicked = True
            if self.armour_button.draw(display_surface):
                self.crosshair.image = pygame.transform.scale(self.armour_image, (35, 35))
                self.mouse_job_number = 2
                self.mouse_clicked = True
            if self.tower_button.draw(display_surface):
                self.crosshair.image = pygame.transform.scale(self.tower_image, (35, 35))
                self.mouse_job_number = 3
                self.mouse_clicked = True
            if pygame.mouse.get_pressed()[2]:
                self.crosshair.image = pygame.transform.scale(self.crosshair_image, (35, 35))
                self.mouse_job_number = 0
            if self.mouse_job_number == 0:
                self.castle.shoot()

            for build in self.own_builds_group:
                pos = pygame.mouse.get_pos()
                if build.rect.collidepoint(pos):
                    build.show_info(display_surface)
                    if pygame.mouse.get_pressed()[0]:
                        if self.mouse_job_number == 1 and not self.mouse_clicked:
                            build.repair()
                            self.mouse_clicked = True
                        elif self.mouse_job_number == 2 and not self.mouse_clicked:
                            build.level_up()
                            self.mouse_clicked = True
                    if not pygame.mouse.get_pressed()[0]:
                        self.mouse_clicked = False
            if pygame.mouse.get_pressed()[0]:
                if self.mouse_job_number == 3 and not self.mouse_clicked:
                    pos_towr = pygame.mouse.get_pos()
                    if pos[0] > 0 and pos[0] <= 585 and pos[1] <= 2 and pos[1] >= 306:
                        if self.castle.money >= self.tower_cost:
                            self.castle.money -= self.tower_cost
                            tower = tower(pos_towr[0], pos_towr[1], self.castle, self.enemy_group)
                            self.own_builds_group.add(tower)
                            self.mouse_clicked = True
            if not pygame.mouse.get_pressed()[0]:
                self.mouse_clicked = False

        if self.castle.health == 0:
                self.lose(display_surface)
                
        self.enemy_group.update(self.castle, self.bullet_group, display_surface, self.own_builds_group)

    def draw(self, display_surface):
            castle_hp_persent = 100 * float(self.castle.health)/float(self.castle.max_health)
            pygame.draw.rect(display_surface, (0, 0, 0), (10, 5, 780, 35))
            pygame.draw.rect(display_surface, (0, 255, 0), (10, 5, castle_hp_persent * 8 - 20, 35))
            self.repair_button.draw(display_surface)
            self.armour_button.draw(display_surface)
            self.tower_button.draw(display_surface)
            self.own_builds_group.draw(display_surface)
            self.enemy_group.draw(display_surface)
            self.bullet_group.draw(display_surface)

    def show_info(self, display_surface):
        draw_text(display_surface, f"Castle health : {self.castle.health} / {100 * self.castle.health//self.castle.max_health}%", self.small_font, (255, 255, 255), 12, 14)
        draw_text(display_surface, f'Money:{self.castle.money}$', self.small_font, (10,10,40), 12, 45)
        draw_text(display_surface, f'level:{self.level_number}', self.small_font, (10,10,40), 12, 65)

    def new_level(self, display_surface):
        if not self.win:
            self.rest_time = pygame.time.get_ticks()
        draw_text(display_surface, f"LEVEL {self.level_number} COMPLETE", self.big_font, (0, 255, 0), WIN_WIDTH / 2, 2 / 2, 1)
        draw_text(display_surface, f"{5 - (pygame.time.get_ticks() - self.rest_time) // 1000}", self.big_font, (0, 255, 0), WIN_WIDTH / 2, 2 / 2 + 60, 1)
        self.win = True
        if pygame.time.get_ticks() - self.rest_time > 5000:
            if self.spawn_coldown >= 300:
                self.spawn_coldown - 50
            self.rest_time = pygame.time.get_ticks()
            self.level_number += 1
            self.level_difficulty = 0
            self.target_difficulty *= self.DIFFICULTY_MULTIPLIER
            self.win = False

    def lose(self, display_surface):
        draw_text(display_surface, "You lose", self.big_font, (255, 0, 0), WIN_WIDTH / 2, 2 / 2, 1)
        self.game_over = True