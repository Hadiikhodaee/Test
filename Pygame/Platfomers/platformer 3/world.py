import pygame
from config import WIN_HEIGHT, WIN_WIDTH, TILE_SIZE
from soldier import Enemy
from item_box import Item_box
        
class World:
    def __init__(self, data, player, enemy_group, item_box_group, enemy_bullet_group, granade_group, explosion_group):
        
        self.reset(data, player, enemy_group, item_box_group, enemy_bullet_group, granade_group, explosion_group)

    def reset(self, data, player, enemy_group, item_box_group, enemy_bullet_group, granade_group, explosion_group):
        enemy_group.empty()
        explosion_group.empty()
        item_box_group.empty()
        enemy_bullet_group.empty()
        player.reset()

        self.tile_list = []

        self.img_list = []
        for i in range(24):
            img = pygame.image.load(f"assets/img/tile/{i}.png")
            tile_img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.img_list.append(tile_img)
        air = pygame.transform.scale(pygame.image.load("assets/img/tile/25.png"), (TILE_SIZE, TILE_SIZE))
        self.img_list.append(air)

        for row_index, row in enumerate(data):
            for col_index, col in enumerate(row):
                if 25 > col > -1:
                    if col == 18:
                        player.rect.x = col_index * TILE_SIZE
                        player.rect.y = row_index * TILE_SIZE

                    elif col == 19:
                        Enemy(col_index * TILE_SIZE, row_index * TILE_SIZE, enemy_group, player, enemy_bullet_group, granade_group, explosion_group, 1.65)

                    elif col == 20:
                        Item_box(col_index * TILE_SIZE, row_index * TILE_SIZE, "AMMO", item_box_group)

                    elif col == 21:
                        Item_box(col_index * TILE_SIZE, row_index * TILE_SIZE, "GRENAMDE", item_box_group)

                    elif col == 22:
                        Item_box(col_index * TILE_SIZE, row_index * TILE_SIZE, "HEALTH", item_box_group)

                    else:
                        img = self.img_list[col]

                        img_rect = img.get_rect()
                        img_rect.x = col_index * TILE_SIZE
                        img_rect.y = row_index * TILE_SIZE
                        tile_number = col
                        tile = (img, img_rect, tile_number)

                        self.tile_list.append(tile)

    def draw(self, screen, screen_scroll):
        for tile in self.tile_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])