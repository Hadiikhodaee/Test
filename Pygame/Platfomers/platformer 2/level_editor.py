import pickle
import pygame
from button import Button
from config import WIN_WIDTH, WIN_HEIGHT, FPS, TILE_SIZE

pygame.init()
clock = pygame.time.Clock()

SIDE_MORGIN = 300
LOWER_MARGIN = 100
hell_mode = False

screen = pygame.display.set_mode((WIN_WIDTH + SIDE_MORGIN, WIN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")

bg_img = pygame.image.load("assets/images/sky.png")
bg_image = pygame.transform.scale(bg_img, (WIN_WIDTH, WIN_HEIGHT))
sun_image = pygame.image.load("assets/images/sun.png")

hell_bg_img = pygame.image.load("assets/images/hell.gif")
hell_bg_image = pygame.transform.scale(hell_bg_img, (1400, WIN_HEIGHT))

def draw_bg():
    screen.fill((10,240,30))
    screen.blit(bg_image, (0, 0))
    screen.blit(sun_image, (100, 100))

def draw_hell_bg():
    screen.fill((10,240,30))
    screen.blit(hell_bg_image, (0, 0))

tile_img_list = []
hell_tile_img_list = []

dirt_image = pygame.transform.scale(pygame.image.load("assets/images/platforms/dirt.png"), (TILE_SIZE, TILE_SIZE))
grass_image = pygame.transform.scale(pygame.image.load("assets/images/platforms/grass.png"), (TILE_SIZE, TILE_SIZE))
lava_image = pygame.transform.scale(pygame.image.load("assets/images/platforms/lava.png"), (TILE_SIZE, TILE_SIZE))
lava_pool_image = pygame.transform.scale(pygame.image.load("assets/images/platforms/lava pool.png"), (TILE_SIZE, TILE_SIZE))
platformx_image = pygame.transform.scale(pygame.image.load("assets/images/platforms/platform_x.png"), (TILE_SIZE, TILE_SIZE / 2))
platformy_image = pygame.transform.scale(pygame.image.load("assets/images/platforms/platform_y.png"), (TILE_SIZE, TILE_SIZE / 2))
exit_door_image = pygame.transform.scale(pygame.image.load("assets/images/platforms/exit.png"), (TILE_SIZE, TILE_SIZE * 2))
big_exit_door_image = pygame.transform.scale(pygame.image.load("assets/images/platforms/exit.png"), (TILE_SIZE * 3, TILE_SIZE * 4))
blob_image = pygame.image.load("assets/images/characters/blob.png")

hell_dirt_image = pygame.transform.scale(pygame.image.load("assets/images/hell images/dirt.png"), (TILE_SIZE, TILE_SIZE))
hell_grass_image = pygame.transform.scale(pygame.image.load("assets/images/hell images/grass.png"), (TILE_SIZE, TILE_SIZE))
hell_lava_image = pygame.transform.scale(pygame.image.load("assets/images/hell images/lava.png"), (TILE_SIZE, TILE_SIZE))
hell_lava_pool_image = pygame.transform.scale(pygame.image.load("assets/images/hell images/lava pool.png"), (TILE_SIZE, TILE_SIZE))
hell_platformx_image = pygame.transform.scale(pygame.image.load("assets/images/hell images/platform_x.png"), (TILE_SIZE, TILE_SIZE / 2))
hell_platformy_image = pygame.transform.scale(pygame.image.load("assets/images/hell images/platform_y.png"), (TILE_SIZE, TILE_SIZE / 2))
hell_exit_door_image = pygame.transform.scale(pygame.image.load("assets/images/hell images/exit.png"), (TILE_SIZE, TILE_SIZE * 2))
big_hell_exit_door_image = pygame.transform.scale(pygame.image.load("assets/images/hell images/exit.png"), (TILE_SIZE * 3, TILE_SIZE * 4))
hell_blob_image = pygame.image.load("assets/images/hell images/hell_blob.png")

change_direction_image = pygame.transform.scale(pygame.image.load("assets/images/platforms/change_direction.png"), (TILE_SIZE - 10, TILE_SIZE - 10))
coin_image = pygame.transform.scale(pygame.image.load("assets/images/platforms/coin.png"), (35, 35))
player_image = pygame.transform.scale(pygame.image.load("assets/images/characters/guy1.png"), (40, 80))

tile_img_list.append((dirt_image, 0))
tile_img_list.append((grass_image, 1))
tile_img_list.append((platformx_image, 2))
tile_img_list.append((platformy_image, 3))
tile_img_list.append((lava_image, 4))
tile_img_list.append((lava_pool_image, 5))
tile_img_list.append((coin_image, 6))
tile_img_list.append((exit_door_image, 7))
tile_img_list.append((big_exit_door_image, 8))
tile_img_list.append((blob_image, 9))
tile_img_list.append((player_image, 10))
tile_img_list.append((change_direction_image, 11))

hell_tile_img_list.append((hell_dirt_image, 0))
hell_tile_img_list.append((hell_grass_image, 1))
hell_tile_img_list.append((hell_platformx_image, 2))
hell_tile_img_list.append((hell_platformy_image, 3))
hell_tile_img_list.append((hell_lava_image, 4))
hell_tile_img_list.append((hell_lava_pool_image, 5))
hell_tile_img_list.append((coin_image, 6))
hell_tile_img_list.append((hell_exit_door_image, 7))
hell_tile_img_list.append((big_hell_exit_door_image, 8))
hell_tile_img_list.append((hell_blob_image, 9))
hell_tile_img_list.append((player_image, 10))
hell_tile_img_list.append((change_direction_image, 11))

button_list = list()
button_row = 0
button_col = 0
current_tile = 0

for i in range(len(tile_img_list)):
    button = Button(WIN_WIDTH + ( 75 * button_col) + 50, 75 * button_row + 50, tile_img_list[i][0], (40, 40))
    button_list.append(button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

hell_button_list = list()
hell_button_row = 0
hell_button_col = 0

for i in range(len(hell_tile_img_list)):
    hell_button = Button(1400 + ( 75 * hell_button_col) + 50, 75 * hell_button_row + 50, hell_tile_img_list[i][0], (40, 40))
    hell_button_list.append(hell_button)
    hell_button_col += 1
    if hell_button_col == 3:
        hell_button_row += 1
        hell_button_col = 0

MAX_COL = 20
ROWS = 14

world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COL
    world_data.append(r)
for tile in range(MAX_COL):
    world_data[-1][tile] = 1

def draw_world():
    if not hell_mode:
        tile_list = tile_img_list
    else:
        tile_list = hell_tile_img_list
    for i in range(len(world_data)):
        for j in range(len(world_data[i])):
            if world_data[i][j] >= 0:
                if world_data[i][j] == 6:
                    screen.blit(tile_list[world_data[i][j]][0], (j * TILE_SIZE + 7.5, i * TILE_SIZE + 7.5))
                elif world_data[i][j] == 7:
                    screen.blit(tile_list[world_data[i][j]][0], (j * TILE_SIZE, i * TILE_SIZE - 50))
                elif world_data[i][j] == 8:
                    screen.blit(tile_list[world_data[i][j]][0], (j * TILE_SIZE - 25, i * TILE_SIZE - 150))
                elif world_data[i][j] == 9:
                    if not hell_mode:
                        screen.blit(tile_list[world_data[i][j]][0], (j * TILE_SIZE + 2, i * TILE_SIZE + 15))
                    else:
                        screen.blit(tile_list[world_data[i][j]][0], (j * TILE_SIZE + 1, i * TILE_SIZE + 1))
                elif world_data[i][j] == 10:
                    screen.blit(tile_list[world_data[i][j]][0], (j * TILE_SIZE, i * TILE_SIZE + 20))
                elif world_data[i][j] == 11:
                    screen.blit(tile_list[world_data[i][j]][0], (j * TILE_SIZE + 5, i * TILE_SIZE + 5))
                else:
                    screen.blit(tile_list[world_data[i][j]][0], (j * TILE_SIZE, i * TILE_SIZE))

def reset_world():
    world_data.clear()
    if not hell_mode:
        for row in range(ROWS):
            r = [-1] * MAX_COL
            world_data.append(r)
        for tile in range(MAX_COL):
            world_data[-1][tile] = 1
    else:
        for row in range(ROWS):
            r = [-1] * MAX_COL
            world_data.append(r)
        for tile in range(MAX_COL):
            world_data[-1][tile] = 1

def change_world_data():
    global pre_level_was_hell
    if hell_mode:
        for row in world_data:
            for i in range(8):
                row.append(-1)
        for i in range(MAX_COL):
            world_data[-1][i] = 1
    elif pre_level_was_hell:
        for row in world_data:
            del row[-8:]
            pre_level_was_hell = False

save_button_img = pygame.image.load("assets/images/editors/save_btn.png")
load_button_img = pygame.image.load("assets/images/editors/load_btn.png")

save_button = Button(10, WIN_HEIGHT + LOWER_MARGIN / 2 - 19, save_button_img, (2 * TILE_SIZE, 1.2 * TILE_SIZE))
load_button = Button(WIN_WIDTH - 80 - 10 , WIN_HEIGHT + LOWER_MARGIN / 2 - 19, load_button_img, (2 * TILE_SIZE, 1.2 * TILE_SIZE))

font = pygame.font.SysFont("terminal", 42)
small_font = pygame.font.SysFont("terminal", 22)

def draw_text(text, font, color, x, y, bg=False):
    if bg:
        t = font.render(text, True, color, (0, 0, 0))
    else:
        t = font.render(text, True, color)
    r = t.get_rect()
    r.centerx = x
    r.centery = y
    screen.blit(t, r)

show_control = False
def show_controls():
    draw_text("Show/Hide controls -> F1", small_font, (255, 154, 0), WIN_WIDTH/2, WIN_HEIGHT/2 - 40, True)
    draw_text("Show/Hide grid -> V", small_font, (255, 154, 0), WIN_WIDTH/2, WIN_HEIGHT/2 - 20, True)
    draw_text("Reset world -> R", small_font, (255, 154, 0), WIN_WIDTH/2, WIN_HEIGHT/2 + 20, True)
    draw_text("Grid on/behind tiles -> Q", small_font, (255, 154, 0), WIN_WIDTH/2, WIN_HEIGHT/2 + 40, True)

def draw_grid():
    for i in range(MAX_COL):
        pygame.draw.line(screen, (255,255,255), (i * TILE_SIZE, 0), (i * TILE_SIZE, WIN_HEIGHT - 1))
    for i in range(ROWS):
        pygame.draw.line(screen, (255,255,255), (0, i * TILE_SIZE), (WIN_WIDTH, i * TILE_SIZE))

def hell_mode_or_not():
    global hell_mode, MAX_COL, change_screen, pre_level_was_hell
    if level % 5 == 0 and level > 0:
        hell_mode = True
        MAX_COL = 28
        pre_level_was_hell = True
    else:
        hell_mode = False
        MAX_COL = 20
    change_world_data()
    change_screen = True

show_grid = 1
grin_on_tiles = 1

level = 1
pre_level_was_hell = False
change_screen = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                level += 1
                hell_mode_or_not()
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if level > 0:
                    level -= 1
                    hell_mode_or_not()
            if event.key == pygame.K_v:
                if show_grid:
                    show_grid = 0
                else:
                    show_grid = 1
            if event.key == pygame.K_r:
                reset_world()
            if event.key == pygame.K_q:
                grin_on_tiles *= -1
            if event.key == pygame.K_F1:
                if not show_control:
                    show_control = True
                else:
                    show_control = False

    if change_screen:
        if hell_mode:
            WIN_WIDTH = 1400
            screen = pygame.display.set_mode((WIN_WIDTH + SIDE_MORGIN, WIN_HEIGHT + LOWER_MARGIN))
            change_screen = False
        else:
            WIN_WIDTH = 1000
            screen = pygame.display.set_mode((WIN_WIDTH + SIDE_MORGIN, WIN_HEIGHT + LOWER_MARGIN))
            change_screen = False

    pos = pygame.mouse.get_pos()
    x = pos[0] // TILE_SIZE
    y = pos[1] // TILE_SIZE

    if pos[0] < WIN_WIDTH and pos[1] < WIN_HEIGHT:
        for tile in tile_img_list:
            if pygame.mouse.get_pressed()[0]:
                if world_data[y][x] != current_tile:
                    world_data[y][x] = current_tile
    if pygame.mouse.get_pressed()[2]:
        try:
            world_data[y][x] = -1
        except:
            None

    if not hell_mode:
        draw_bg()
    else:
        draw_hell_bg()
    if grin_on_tiles == 1:
        draw_world()
        if show_grid:
            draw_grid()
    else:
        if show_grid:
            draw_grid()
        draw_world()
    if show_control:
        show_controls()

    draw_text(f"Level: {level}", font, (0, 0, 0), WIN_WIDTH / 2, WIN_HEIGHT + LOWER_MARGIN / 2)

    if not hell_mode:
        for i in range(len(button_list)):
            if button_list[i].draw(screen):
                current_tile = tile_img_list[i][1]
        load_button.rect.x = WIN_WIDTH - 80 - 10
        pygame.draw.rect(screen, (255, 0, 0), button_list[current_tile].rect, 3)
    else:
        for i in range(len(hell_button_list)):
            if hell_button_list[i].draw(screen):
                current_tile = tile_img_list[i][1]
        load_button.rect.x = WIN_WIDTH - 80 - 10
        pygame.draw.rect(screen, (255, 0, 0), hell_button_list[current_tile].rect, 3)

    if save_button.draw(screen):
        f = open(f"levels/level{level}_data.py", "wb")
        pickle.dump(world_data, f)
        f.close()

        print("saved!")

    if load_button.draw(screen):
        f = open(f"levels/level{level}_data.py", "rb")
        world_data = pickle.load(f)
        f.close()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()