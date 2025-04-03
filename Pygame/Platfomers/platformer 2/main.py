import pygame
from pygame.locals import *
from config import WIN_WIDTH, WIN_HEIGHT, FPS, TILE_SIZE
from world import World, draw_grid
from player import Player
from button import Button
import pickle

with open("levels/level0_data.py", "rb") as f:
    world_data = pickle.load(f)

pygame.init()

display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("platformer")
clock = pygame.time.Clock()
main_menu = True

bg_img = pygame.image.load("assets/images/sky.png")
bg_image = pygame.transform.scale(bg_img, (WIN_WIDTH, WIN_HEIGHT))
sun_image = pygame.image.load("assets/images/sun.png")
start_image = pygame.transform.scale(pygame.image.load("assets/images/editors/start_btn.png"), (TILE_SIZE * 4, TILE_SIZE * 2))
restart_image = pygame.transform.scale(pygame.image.load("assets/images/editors/restart_btn.png"), (TILE_SIZE * 4, TILE_SIZE * 2))
exit_image = pygame.transform.scale(pygame.image.load("assets/images/editors/exit_btn.png"), (TILE_SIZE * 4, TILE_SIZE * 2))
pygame.mixer.music.load('assets/sounds/music.wav')
pygame.mixer.music.play(-1)

blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
world = World(world_data, blob_group, platform_group, coin_group, False)
player = Player(world.player_x, world.player_y)
start_button = Button(100, 300, start_image)
restart_button = Button(100, 300, restart_image)
exit_button = Button(WIN_WIDTH - 300, 300, exit_image)

level_number = 0
hell_mode = False

big_font = pygame.font.SysFont("terminal", 250)
small_font = pygame.font.SysFont("terminal", 22)

def next_level():
    global level_number, hell_mode
    with open(f"levels/level{level_number}_data.py", "rb") as f:
        world_data = pickle.load(f)
    if level_number in [5, 10]:
        hell_mode = True
    else:
        hell_mode = False
    world.reset(world_data, blob_group, platform_group, coin_group, hell_mode)
    player.reset(world.player_x, world.player_y)
    return world_data

change_screen = True
lose = False
lives = player.livies
game_over = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.jump()

    display_surface.fill((0, 0, 0))
    display_surface.blit(bg_image, (0, 0))
    if not hell_mode:
        display_surface.blit(sun_image, (100, 100))

    if main_menu and game_over == 0:
        if level_number == 0:
            if not lose:
                level_text = big_font.render("Welcome", True, (0, 0, 0))
            else:
                level_text = big_font.render("You lose", True, (255, 0, 0))
        else:
            level_text = big_font.render(f"level {level_number}", True, (0, 255, 0))
        if start_button.draw(display_surface):
            main_menu = False
            just_start = False
        if exit_button.draw(display_surface):
            running = False
        level_rect = level_text.get_rect()
        level_rect.centerx = WIN_WIDTH / 2
        level_rect.centery = 150
        display_surface.blit(level_text, level_rect)

    else:
        if level_number == 0:
            hint_text1 = small_font.render("come on the door and press", True, (0, 0, 0))
            hint_text1_rect = hint_text1.get_rect()
            hint_text1_rect.centerx = 500
            hint_text1_rect.centery = 250
            hint_text2 = small_font.render(" 'Enter' to go next level", True, (0, 0, 0))
            hint_text2_rect = hint_text2.get_rect()
            hint_text2_rect.centerx = 500
            hint_text2_rect.centery = 270
            display_surface.blit(hint_text1, hint_text1_rect)
            display_surface.blit(hint_text2, hint_text2_rect)
        if change_screen:
            if level_number in [5, 10]:
                WIN_WIDTH = 1400
                hell_mode = True
                display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
                bg_img = pygame.image.load("assets/images/hell.gif")
                bg_image = pygame.transform.scale(bg_img, (WIN_WIDTH, WIN_HEIGHT))
                change_screen = False
                exit_button = Button(WIN_WIDTH - 300, 300, exit_image)
            else:
                WIN_WIDTH = 1000
                hell_mode = False
                display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
                bg_img = pygame.image.load("assets/images/sky.png")
                bg_image = pygame.transform.scale(bg_img, (WIN_WIDTH, WIN_HEIGHT))
                change_screen = False
                exit_button = Button(WIN_WIDTH - 300, 300, exit_image)
        world.draw(display_surface)
        blob_group.draw(display_surface)
        blob_group.update(world.tile_list, player.rect, game_over, hell_mode, WIN_WIDTH)
        coin_group.draw(display_surface)
        platform_group.draw(display_surface)
        platform_group.update(world.tile_list, WIN_WIDTH)
        game_over = player.update(display_surface, world.tile_list, blob_group, coin_group, game_over, WIN_WIDTH)

    if game_over == 1:
        level_number += 1
        game_over = 0
        main_menu = True
        change_screen = True
        next_level()

    if game_over == -1:
        if restart_button.draw(display_surface):
            game_over = 0
            player.reset(world.player_x, world.player_y)
            world.reset(next_level(), blob_group, platform_group, coin_group, hell_mode)
        if exit_button.draw(display_surface):
            running = False

    if game_over == -2:
        level_number = 0
        lose = True
        main_menu = True
        change_screen = True
        player.reset(world.player_x, world.player_y)
        world.reset(next_level(), blob_group, platform_group, coin_group, hell_mode)
        player.livies = lives
        player.coin_goten = 0
        game_over = 0
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()