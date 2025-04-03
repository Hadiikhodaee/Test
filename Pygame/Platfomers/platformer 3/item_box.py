import pygame
from pygame.sprite import Sprite
from config import TILE_SIZE

HEALTH_BOX_IMAGE = pygame.image.load("assets/img/icons/health_box.png")
AMMO_BOX_IMAGE = pygame.image.load("assets/img/icons/ammo_box.png")
GRENADE_BOX_IMAGE = pygame.image.load("assets/img/icons/grenade_box.png")

item_boxes = {
    "HEALTH":HEALTH_BOX_IMAGE,
    "AMMO":AMMO_BOX_IMAGE,
    "GRENAMDE":GRENADE_BOX_IMAGE
}

class Item_box(Sprite):
    def __init__(self, x, y, type, group):
        super().__init__()

        self.item_type = type
        img = item_boxes[self.item_type]
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft = (x, y))

        group.add(self)

    def update(self, player, screen_scroll):
        self.rect.x += screen_scroll
        if player.alive:
            if self.rect.colliderect(player.rect):
                self.kill()
                if self.item_type == "HEALTH":
                    player.health += 25
                    if player.health > player.MAX_HEALTH:
                        player.health = player.MAX_HEALTH
                if self.item_type == "AMMO":
                    player.ammo += 15
                    if player.ammo > 50:
                        player.ammo = 50
                if self.item_type == "GRENAMDE":
                    player.grenade += 3
                    if player.grenade > 9:
                        player.grenade = 9