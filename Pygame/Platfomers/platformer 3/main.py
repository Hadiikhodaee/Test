import csv, pickle
import pygame
from config import WIN_WIDTH, WIN_HEIGHT, TILE_SIZE, FPS
from button import Button
from soldier import Soldier
from world import World

pygame.init()

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Platformer 3")
clock = pygame.time.Clock()

pygame.mixer.music.load("assets/audio/music2.mp3")
pygame.mixer.music.play(-1, 0.0, 5000)

start_button_image = pygame.image.load("assets/img/start_btn.png")
exit_button_image = pygame.image.load("assets/img/exit_btn.png")
restart_button_image = pygame.image.load("assets/img/restart_btn.png")

start_button = Button(80, WIN_HEIGHT / 2 - 40, start_button_image, (TILE_SIZE * 4, TILE_SIZE * 2))
exit_button = Button(WIN_WIDTH - 160 - 80, WIN_HEIGHT / 2 - 40, exit_button_image, (TILE_SIZE * 4, TILE_SIZE * 2))
restart_button = Button(80, WIN_HEIGHT / 2 - 40, restart_button_image, (TILE_SIZE * 4, TILE_SIZE * 2))

player_bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
granade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

player = Soldier(600, 250, enemy_group, player_bullet_group, granade_group, explosion_group, 1.65, "player")

ROWS = 16
COLS = 150
screen_scroll = 0
bg_scroll = 0
main_menu = True
start_intro = False

level = 1
world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)

with open(f"levels\level{level}.csv", "r", newline="") as csv_file:
    reader = list(csv.reader(csv_file, delimiter=","))
    for i in range(len(reader)):
        for j in range(len(reader[i])):
            world_data[i][j] = int(reader[i][j])

pine1_img = pygame.image.load("assets/img/background/pine1.png")
pine2_img = pygame.image.load("assets/img/background/pine2.png")
mountain_img = pygame.image.load("assets/img/background/mountain.png")
sky_img = pygame.image.load("assets/img/background/sky_cloud.png")
width = sky_img.get_width()

def draw_bg():
    for i in range(5):
        screen.blit(sky_img, ((i * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((i * width) - bg_scroll * 0.6, WIN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((i * width) - bg_scroll * 0.7, WIN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((i * width) - bg_scroll * 0.8, WIN_HEIGHT - pine2_img.get_height()))

world = World(world_data, player, enemy_group, item_box_group, enemy_bullet_group, granade_group, explosion_group)

def restart():
    global bg_scroll, start_intro
    world.reset(world_data, player, enemy_group, item_box_group, enemy_bullet_group, granade_group, explosion_group)
    player.reset()
    start_intro = True
    for enemy in enemy_group:
        enemy.reset()
    bg_scroll = 0

def next_level():
    global level, world, world_data
    level += 1
    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS
        world_data.append(r)

    with open(f"levels\level{level}.csv", "r") as csv_file:
        reader = list(csv.reader(csv_file, delimiter=","))
        for i in range(len(reader)):
            for j in range(len(reader[i])):
                world_data[i][j] = int(reader[i][j])
    restart()
    world = World(world_data, player, enemy_group, item_box_group, enemy_bullet_group, granade_group, explosion_group)

class ScreenFade():
	def __init__(self, direction, colour, speed):
		self.direction = direction
		self.colour = colour
		self.speed = speed
		self.fade_counter = 0

	def fade(self):
		fade_complete = False
		self.fade_counter += self.speed
		if self.direction == 1:#whole screen fade
			pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, WIN_WIDTH // 2, WIN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (WIN_WIDTH // 2 + self.fade_counter, 0, WIN_WIDTH, WIN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, WIN_WIDTH, WIN_HEIGHT // 2))
			pygame.draw.rect(screen, self.colour, (0, WIN_HEIGHT // 2 +self.fade_counter, WIN_WIDTH, WIN_HEIGHT))
		if self.direction == 2:#vertical screen fade down
			pygame.draw.rect(screen, self.colour, (0, 0, WIN_WIDTH, 0 + self.fade_counter))
		if self.fade_counter >= WIN_HEIGHT:
			fade_complete = True

		return fade_complete

PINK = (235, 65, 54)
BLACK = (0, 0, 0)

intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 6)

game_over = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    draw_bg()

    if main_menu:
        if start_button.draw(screen):
            main_menu = False
            start_intro = True
        if exit_button.draw(screen):
             running = False
    else:
        if game_over == 0:
            if not player.check_alive():
                game_over = -1
                player.shoot_bullet = True
            world.draw(screen, screen_scroll)
            item_box_group.draw(screen)
            item_box_group.update(player, screen_scroll)
            player.draw(screen)
            screen_scroll = player.update(world.tile_list, bg_scroll)
            bg_scroll -= screen_scroll
            for enemy in enemy_group:
                enemy.draw(screen)
                enemy.update(screen_scroll)
                enemy.ai(world.tile_list)

            player_bullet_group.draw(screen)
            player_bullet_group.update(world.tile_list, screen_scroll)
            enemy_bullet_group.draw(screen)
            enemy_bullet_group.update(world.tile_list, screen_scroll)
            granade_group.draw(screen)
            granade_group.update(explosion_group, player, enemy_group, world.tile_list, screen_scroll)
            explosion_group.draw(screen)
            explosion_group.update(screen_scroll)

            if start_intro:
                if intro_fade.fade():
                    start_intro = False
                    intro_fade.fade_counter = 0

            player.show_info(screen)

            for tile in world.tile_list:
                if tile[2] == 23:
                    if player.rect.x > tile[1].x or tile[1].colliderect(player.rect):
                        game_over = 1
                        player.shoot_bullet = True

        elif game_over == -1:
            if death_fade.fade():
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    game_over = 0
                    restart()
                if exit_button.draw(screen):
                     running = False

    if game_over == 1:
        next_level()
        main_menu = True
        game_over = 0

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()