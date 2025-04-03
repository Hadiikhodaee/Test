import pygame
from pygame.sprite import Sprite
from config import WIN_HEIGHT, WIN_WIDTH, TILE_SIZE

class Bullet(Sprite):
    def __init__(self, x ,y, bullet_group, direction, source, target):
        super().__init__()

        self.image = pygame.image.load("assets/img/icons/bullet.png")
        self.rect = self.image.get_rect(center= (x, y))
        self.speed = 10
        self.direction = direction
        self.source = source
        self.target = target

        self.bullet_group = bullet_group

        self.bullet_group.add(self)
    
    def update(self, tile_list, screen_scroll):
        self.rect.x += screen_scroll
        for tile in tile_list:
            if tile[2] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
                if tile[1].colliderect(self.rect):
                    self.kill()
            if tile[2] in [12, 13]:
                if tile[1].colliderect(self.rect):
                    self.speed = 5
        self.rect.x += self.speed * self.direction

        if self.rect.right < 0 or self.rect.left > WIN_WIDTH or self.rect.top > WIN_HEIGHT or self.rect.bottom < 0:
            self.kill()

        if type(self.target) != pygame.sprite.Group:
            if self.target.alive:
                if pygame.sprite.spritecollide(self.target, self.source.bullet_group, True):
                    self.target.health -= 15
        else:
            collid_dict = pygame.sprite.groupcollide(self.target, self.source.bullet_group, False, False)
            if collid_dict:
                t = list(collid_dict.keys())[0]
                if t.alive:
                    collid_dict = pygame.sprite.groupcollide(self.target, self.source.bullet_group, False, True)
                    t.health -= 15

        if self.rect.y > WIN_HEIGHT:
            self.kill()

class Explosion(Sprite):
    def __init__(self, x, y, explosion_group):
        super().__init__()

        self.images = []
        for i in range(1, 6):
            image = pygame.image.load(f"assets/img/explosion/exp{i}.png")
            self.images.append(image)

        self.frame_index = 0
        self.counter = 0

        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect(center = (x, y))

        explosion_group.add(self)

    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        EXPLOSION_COLDOWN = 5
        self.counter += 1

        if self.counter >= EXPLOSION_COLDOWN:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]

class Grenade(Sprite):
    def __init__(self, x, y, grenade_group, direction=1):
        super().__init__()
        self.image = pygame.image.load("assets/img/icons/grenade.png")
        self.rect = self.image.get_rect(center = (x, y))

        self.vel_y = -11
        self.gravity = 0.8
        self.direction = direction
        self.vel_x = 7

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.explosion_sound = pygame.mixer.Sound("assets/audio/grenade.wav")

        self.timer = 100

        grenade_group.add(self)

    def update(self, explosion_group, player, enemy_group, tile_list, screen_scroll):
        self.rect.x += screen_scroll
        self.vel_y += self.gravity

        dx = self.vel_x * self.direction
        dy = self.vel_y

        for tile in tile_list:
            if tile[2] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    self.direction *= -1
                    dx = self.vel_x * self.direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.vel_x = 0

        self.rect.x += dx
        self.rect.y += dy
        self.timer -= 1

        if self.timer <= 0:
            self.kill()
            Explosion(self.rect.x, self.rect.y, explosion_group)
            self.explosion_sound.play()
            if abs(self.rect.centerx - player.rect.centerx) < 1 * TILE_SIZE and abs(self.rect.centery - (player.rect.centery + 20)) < 1 * TILE_SIZE:
                player.health -= 100
            elif abs(self.rect.centerx - player.rect.centerx) < 2 * TILE_SIZE and abs(self.rect.centery - (player.rect.centery + 20)) < 2 * TILE_SIZE:
                player.health -= 50
            elif abs(self.rect.centerx - player.rect.centerx) < 3 * TILE_SIZE and abs(self.rect.centery - (player.rect.centery + 20)) < 3 * TILE_SIZE:
                player.health -= 25

            for enemy in enemy_group:
                if enemy.alive:
                    if abs(self.rect.centerx - enemy.rect.centerx) < 1 * TILE_SIZE and abs(self.rect.centery - (enemy.rect.centery + 20)) < 1 * TILE_SIZE:
                        enemy.health -= 100
                    elif abs(self.rect.centerx - enemy.rect.centerx) < 2 * TILE_SIZE and abs(self.rect.centery - (enemy.rect.centery + 20)) < 2 * TILE_SIZE:
                        enemy.health -= 50
                    elif abs(self.rect.centerx - enemy.rect.centerx) < 3 * TILE_SIZE and abs(self.rect.centery - (enemy.rect.centery + 20)) < 3 * TILE_SIZE:
                        enemy.health -= 25