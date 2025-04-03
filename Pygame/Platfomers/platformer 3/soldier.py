import os
import random
from pygame.sprite import Sprite
import pygame
from config import WIN_HEIGHT, WIN_WIDTH, TILE_SIZE
from weapons import Bullet, Grenade

SCROLL_THRESH = 200

def draw_text(text, text_col, font, screen, x, y):
	text = font.render(text, True, text_col)
	screen.blit(text, (x, y))

class Soldier(Sprite):
    def __init__(self, x, y, enemy_group, bullet_group, grenade_group, explosion_group, scale, char_type="enemy"):
        super().__init__()
        self.char_type = char_type
        self.win = False

        self.alive = True
        self.MAX_HEALTH = 100
        self.health = self.MAX_HEALTH

        self.direction = 1
        self.flip = False
        self.frame_index = 0
        self.action = 0
        self.animation_list = []

        self.speed = 5
        self.vel_y = 0
        self.START_AMMO = 15
        self.ammo = self.START_AMMO
        self.START_GRENADE = 3
        self.grenade = self.START_GRENADE

        self.jumped = False
        self.shoot_bullet = True
        self.shoot_grenade = False

        self.bullet_group = bullet_group
        self.grenade_group = grenade_group
        self.explosion_group = explosion_group
        self.enemy_group = enemy_group

        self.update_time = pygame.time.get_ticks()
        animation_types = ['Idle', 'Run', 'Jump', 'Death']

        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'assets/img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'assets/img/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=(x,y))
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.jump_sound = pygame.mixer.Sound("assets/audio/jump.wav")
        self.jump_sound.set_volume(0.3)
        self.shoot_sound = pygame.mixer.Sound("assets/audio/shoot.wav")

        self.ammo_image = pygame.image.load("assets/img/icons/bullet.png")
        self.grenade_image = pygame.image.load("assets/img/icons/grenade.png")
        self.font = pygame.font.SysFont("terminal", 30)

    def draw(self,screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def animate(self):
        ANIMATION_COOLDOWN = 100

        self.image= self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update(self, tile_list, bg_scroll):
        screen_scroll = 0

        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()
        if self.alive:
            if self.jumped:
                self.update_action(2)
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx -= self.speed
                if not self.jumped:
                    self.update_action(1)
                self.direction = -1
                self.flip = True
                move_rigth = True
            else:
                move_rigth = False
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx += self.speed
                self.direction = 1
                if not self.jumped:
                    self.update_action(1)
                self.flip = False
                move_left = True
            else:
                move_left = False
    
            if not move_rigth and not move_left and not self.jumped:
                self.update_action(0)
    
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy = self.vel_y

            for tile in tile_list:
                if tile[2] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                        elif self.vel_y >= 0:
                            dy = tile[1].top - self.rect.bottom
                            self.jumped = False
                        self.vel_y = 0
                if tile[2] in [12, 13]:
                    if tile[1].colliderect(self.rect):
                        self.health = 0

            if self.rect.left + dx < 0 or self.rect.right + dx > WIN_WIDTH:
                dx = 0
    
            self.rect.x += dx
            self.rect.y += dy
    
            if pygame.mouse.get_pressed()[0] or keys[pygame.K_LSHIFT]:
                self.shoot()
            else:
                self.shoot_bullet = False
    
            if pygame.mouse.get_pressed()[2] or keys[pygame.K_q]:
                self.throw_grenade()
            else:
                self.shoot_grenade = False

            self.jump()
        
        self.animate()

        if (self.rect.right > WIN_WIDTH - SCROLL_THRESH and bg_scroll < (150 * TILE_SIZE) - WIN_WIDTH) or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
            self.rect.x -= dx
            screen_scroll = -dx

        if self.rect.y > WIN_HEIGHT:
            self.health = 0
            self.vel_y = 0
            dy = 0

        return screen_scroll

    def shoot(self):
        if not self.shoot_bullet and self.ammo > 0:
            self.shoot_sound.play()
            if self.direction == 1:
                Bullet(self.rect.midright[0] + 2, self.rect.midleft[1] + 2, self.bullet_group, self.direction, self, self.enemy_group)
            if self.direction == -1:
                Bullet(self.rect.midleft[0] - 2, self.rect.midleft[1] + 2, self.bullet_group, self.direction, self, self.enemy_group)
            self.ammo -= 1
            self.shoot_bullet = True
    
    def throw_grenade(self):
        if not self.shoot_grenade and self.grenade > 0:
            if self.direction == 1:
                Grenade(self.rect.topright[0] - 15, self.rect.topright[1] - 5, self.grenade_group, self.direction)
            if self.direction == -1:
                Grenade(self.rect.topleft[0] + 15, self.rect.topleft[1] - 5, self.grenade_group, self.direction)
            self.grenade -= 1
            self.shoot_grenade = True

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(3)
        return self.alive

    def jump(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not self.jumped:
                self.jump_sound.play()
                self.vel_y = 0
                self.vel_y -= 15
                self.jumped = True

    def show_info(self, screen):
        hp_persent = 100 * float(self.health)/float(self.MAX_HEALTH)
        pygame.draw.rect(screen, (0, 0, 0), (6, 6, 200, 20))
        pygame.draw.rect(screen, (255, 0, 0), (8, 8, 196, 16))
        pygame.draw.rect(screen, (0, 255, 0), (8, 8, hp_persent * 2 - 4, 16))

        draw_text('AMMO: ', (255, 255, 255), self.font, screen, 10, 35)
        for x in range(self.ammo):
            screen.blit(self.ammo_image, (90 + (x * 10), 40))

        draw_text('GRENADES: ', (255, 255, 255), self.font, screen, 10, 60)
        for x in range(self.grenade):
            screen.blit(self.grenade_image, (135 + (x * 15), 60))

    def reset(self):
        self.ammo = self.START_AMMO
        self.grenade = self.START_GRENADE
        self.health = self.MAX_HEALTH
        self.alive = True
        self.direction = 1
        self.flip = False
            
class Enemy(Soldier):
    def __init__(self, x, y, enemy_group, player, bullet_group, grenade_group, explosion_group, scale, char_type="enemy"):
        super().__init__(x, y, enemy_group, bullet_group, grenade_group, explosion_group, scale, char_type)

        self.player = player
        self.shoot_cooldown = 20
        self.speed = 4

        self.jumped = False

        self.move_counter = 0
        self.vision = pygame.Rect(x, y, 400, 20)
        self.grenade_vision = pygame.Rect(x, y, 250, 20)
        self.idling = False
        self.idling_counter = 0

        enemy_group.add(self)

    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        self.animate()
        self.check_alive()

    def ai_movement(self, moving_left, moving_right, tile_list):
        self.dx = 0
        self.dy = 0

        if moving_left:
            self.dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            self.dx = self.speed
            self.flip = False
            self.direction = 1

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        self.dy = self.vel_y

        list_for_check = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        for tile in tile_list:
            if tile[2] in list_for_check:
                if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
                    if self.vel_y < 0:
                        self.dy = tile[1].bottom - self.rect.top
                    elif self.vel_y >= 0:
                        self.dy = tile[1].top - self.rect.bottom
            if tile[2] in list_for_check or tile[2] == 24:
                if tile[1].colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
                    self.direction *= -1

        self.rect.x += self.dx
        self.rect.y += self.dy

    def ai(self, tile_list):
        if self.alive and self.player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                self.idling_counter = 50
            if self.vision.colliderect(self.player.rect):
                self.update_action(0)#0: idle
                if self.grenade_vision.colliderect(self.player.rect) and random.randint(1, 200) == 1:
                    self.throw_grenade()
                else:
                    self.shoot()
                    self.shoot_grenade = False
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.ai_movement(ai_moving_left, ai_moving_right, tile_list)
                    self.update_action(1)#1: run
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 180 * self.direction, self.rect.centery)
                    self.grenade_vision.center = (self.rect.centerx + 120 * self.direction, self.rect.centery)
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

    def shoot(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            if self.direction == 1:
                Bullet(self.rect.midright[0] + 2, self.rect.midleft[1] + 2, self.bullet_group, self.direction, self, self.player)
            if self.direction == -1:
                Bullet(self.rect.midleft[0] - 2, self.rect.midleft[1] + 2, self.bullet_group, self.direction, self, self.player)
            self.ammo -= 1