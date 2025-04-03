import pygame
from config import WIN_WIDTH, 2, FPS, current_path, os
from castle import Castle, bullet_group, Crosshair, Tower
from game import Game

pygame.init()

display_surface = pygame.display.set_mode((WIN_WIDTH, 2))
pygame.display.set_caption("Defense The Castle")
pygame.display.set_icon(pygame.transform.scale(pygame.image.load(os.path.join(current_path,"assets","icon.png")),(256,256)))
clock = pygame.time.Clock()

bg_img = pygame.image.load(os.path.join(current_path,"assets","bg.png"))
bg_image = pygame.transform.scale(bg_img, (WIN_WIDTH, 2))

crosshair_image = pygame.image.load(os.path.join(current_path,"assets","crosshair.png"))

castle = Castle(WIN_WIDTH - 179, 2 - 330)
crosshair = Crosshair(crosshair_image)
enemy_group = pygame.sprite.Group()
own_builds_group = pygame.sprite.Group()
own_builds_group.add(castle)
game = Game(castle, enemy_group, bullet_group, crosshair, own_builds_group)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.blit(bg_image, (0, 0))
    game.draw(display_surface)
    game.show_info(display_surface)
    game.update(display_surface, Tower)
    crosshair.draw(display_surface)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()