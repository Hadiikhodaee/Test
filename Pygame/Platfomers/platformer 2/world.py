from random import choice
import pygame
from pygame.sprite import Sprite
from config import WIN_HEIGHT, TILE_SIZE
from enemy import Enemy

def draw_grid(display_surface, WIN_WIDTH):
    for line in range(14):
        pygame.draw.line(display_surface, (0, 100, 200), (0, line * TILE_SIZE), (WIN_WIDTH, line * TILE_SIZE))
    for line in range(28):
        pygame.draw.line(display_surface, (0, 100, 200), (line * TILE_SIZE, 0), (line * TILE_SIZE, WIN_WIDTH))

class Platform(Sprite):
    def __init__(self, x, y, image, direction):
        super().__init__()
        img = image
        self.image = pygame.transform.scale(img,(TILE_SIZE, TILE_SIZE / 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.tile_num = 0
        
        self.direction = direction

        if self.direction == "x":
            self.tile_num = 2
        elif self.direction == "y":
            self.tile_num = 3

        self.delta = choice([-1, 1])
        self.velocity = 1

    def update(self, tile_list, WIN_WIDTH):
        if self.direction == "x":
            self.rect.x += self.delta * self.velocity
        elif self.direction == "y":
            self.rect.y += self.delta * self.velocity

        for tile in tile_list:
            if tile[2] in [11, 0, 1, 4, 5]:
                if tile[1].colliderect(self.rect):
                    self.delta *= -1

        if self.rect.right > WIN_WIDTH or self.rect.left < 0 or self.rect.top < 0 or self.rect.bottom > WIN_HEIGHT:
            self.delta *= -1

class Coin(Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("assets/images/platforms/coin.png")
        self.image = pygame.transform.scale(img,(35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class World:
    def __init__(self, data, blob_group, platform_group, coin_group, hell_mode):

        self.reset(data, blob_group, platform_group, coin_group, hell_mode)

    def reset(self, data, blob_group, platform_group, coin_group, hell_mode):
        blob_group.empty()
        platform_group.empty()
        coin_group.empty()
        self.tile_list = []

        if not hell_mode:
            self.dirt_image = pygame.image.load("assets/images/platforms/dirt.png")
            self.grass_image = pygame.image.load("assets/images/platforms/grass.png")
            self.lava_image = pygame.image.load("assets/images/platforms/lava.png")
            self.lava_pool_image = pygame.image.load("assets/images/platforms/lava pool.png")
            self.platform_image = pygame.image.load("assets/images/platforms/platform.png")
            self.exit_door_image = pygame.image.load("assets/images/platforms/exit.png")
        if hell_mode:
            self.dirt_image = pygame.image.load("assets/images/hell images/dirt.png")
            self.grass_image = pygame.image.load("assets/images/hell images/grass.png")
            self.lava_image = pygame.image.load("assets/images/hell images/lava.png")
            self.lava_pool_image = pygame.image.load("assets/images/hell images/lava pool.png")
            self.platform_image = pygame.image.load("assets/images/hell images/platform.png")
            self.exit_door_image = pygame.image.load("assets/images/hell images/exit.png")

        self.air_image = pygame.image.load("assets/images/platforms/air.png")
        self.coin_image = pygame.image.load("assets/images/platforms/coin.png")

        self.tile_number = 0

        for row_index, row in enumerate(data):
            for col_index, col in enumerate(row):
                if col == 0:
                    img = pygame.transform.scale(self.dirt_image,(TILE_SIZE, TILE_SIZE))

                    img_rect = img.get_rect()
                    img_rect.x = col_index * TILE_SIZE
                    img_rect.y = row_index * TILE_SIZE
                    self.tile_number = 0
                    tile = (img, img_rect, self.tile_number)
                    self.tile_list.append(tile)

                if col == 1:
                    img = pygame.transform.scale(self.grass_image,(TILE_SIZE, TILE_SIZE))

                    img_rect = img.get_rect()
                    img_rect.x = col_index * TILE_SIZE
                    img_rect.y = row_index * TILE_SIZE
                    self.tile_number = 1
                    tile = (img, img_rect, self.tile_number)
                    self.tile_list.append(tile)

                if col == 2:
                    platform = Platform(col_index * TILE_SIZE, row_index * TILE_SIZE, self.platform_image, "x")
                    platform_group.add(platform)

                    tile = (platform.image, platform.rect, platform.tile_num, platform)
                    self.tile_list.append(tile)

                if col == 3:
                    platform = Platform(col_index * TILE_SIZE, row_index * TILE_SIZE, self.platform_image, "y")
                    platform_group.add(platform)

                    tile = (platform.image, platform.rect, platform.tile_num)
                    self.tile_list.append(tile)

                if col == 4:
                    img = pygame.transform.scale(self.lava_image,(TILE_SIZE, TILE_SIZE))

                    img_rect = img.get_rect()
                    img_rect.x = col_index * TILE_SIZE
                    img_rect.y = row_index * TILE_SIZE
                    self.tile_number = 4
                    tile = (img, img_rect, self.tile_number)
                    self.tile_list.append(tile)

                if col == 5:
                    img = pygame.transform.scale(self.lava_pool_image,(TILE_SIZE, TILE_SIZE))

                    img_rect = img.get_rect()
                    img_rect.x = col_index * TILE_SIZE
                    img_rect.y = row_index * TILE_SIZE
                    self.tile_number = 5
                    tile = (img, img_rect, self.tile_number)
                    self.tile_list.append(tile)

                if col == 6:
                    coin = Coin(col_index * TILE_SIZE + 7.5, row_index * TILE_SIZE + 7.5)
                    coin_group.add(coin)

                if col == 7:
                    img = pygame.transform.scale(self.exit_door_image,(TILE_SIZE, TILE_SIZE * 2))

                    img_rect = img.get_rect()
                    img_rect.x = col_index * TILE_SIZE 
                    img_rect.y = row_index * TILE_SIZE - 50
                    self.tile_number = 7
                    tile = (img, img_rect, self.tile_number)
                    self.tile_list.append(tile)

                if col == 8:
                    img = pygame.transform.scale(self.exit_door_image,(TILE_SIZE * 3, TILE_SIZE * 4))

                    img_rect = img.get_rect()
                    img_rect.x = col_index * TILE_SIZE - 25
                    img_rect.y = row_index * TILE_SIZE - 150
                    self.tile_number = 8
                    tile = (img, img_rect, self.tile_number)
                    self.tile_list.append(tile)

                if col == 9:
                    if not hell_mode:
                        blob = Enemy(col_index * TILE_SIZE, row_index * TILE_SIZE + 16)
                    else:
                        blob = Enemy(col_index * TILE_SIZE, row_index * TILE_SIZE)
                    blob_group.add(blob)

                if col == 10:
                    self.player_x = col_index * TILE_SIZE
                    self.player_y = row_index * TILE_SIZE + 50

                if col == 11:
                    img = pygame.transform.scale(self.air_image,(TILE_SIZE - 10, TILE_SIZE - 10))

                    img_rect = img.get_rect()
                    img_rect.x = col_index * TILE_SIZE + 5
                    img_rect.y = row_index * TILE_SIZE + 5
                    self.tile_number = 11
                    tile = (img, img_rect, self.tile_number)
                    self.tile_list.append(tile)

    def draw(self, display_surface):
        for thile in self.tile_list:
            display_surface.blit(thile[0], thile[1])