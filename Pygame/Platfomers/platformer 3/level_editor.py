import csv, pickle, pygame
from button import Button
from config import WIN_WIDTH, WIN_HEIGHT, FPS, TILE_SIZE

pygame.init()

clock = pygame.time.Clock()

SIDE_MORGIN = 300
LOWER_MARGIN = 100

screen = pygame.display.set_mode((WIN_WIDTH + SIDE_MORGIN, WIN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")

pine1_img = pygame.image.load("assets/img/background/pine1.png")
pine2_img = pygame.image.load("assets/img/background/pine2.png")
mountain_img = pygame.image.load("assets/img/background/mountain.png")
sky_img = pygame.image.load("assets/img/background/sky_cloud.png")

def draw_bg():
    screen.fill((10,240,30))
    width = sky_img.get_width()
    for i in range(6):
        screen.blit(sky_img, (i * width - scroll * 0.5, 0))
        screen.blit(mountain_img, (i * width - scroll * 0.6, WIN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, (i * width - scroll * 0.7, WIN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, (i * width - scroll * 0.8, WIN_HEIGHT - pine2_img.get_height()))

tile_img_list = []

for i in range(24):
    tile_img = pygame.image.load(f"assets/img/tile/{i}.png")
    tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))
    tile_img_list.append(tile_img)
change_direction_img = pygame.transform.scale(pygame.image.load("assets/img/tile/24.png"), (TILE_SIZE, TILE_SIZE))
tile_img_list.append(change_direction_img)

button_list = list()
button_row = 0
button_col = 0
current_tile = 0

for i in range(len(tile_img_list)):
    button = Button(WIN_WIDTH + ( 75 * button_col) + 50, 75 * button_row + 50, tile_img_list[i], (40, 40))
    button_list.append(button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

MAX_COL = 150
ROWS = 16

world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COL
    world_data.append(r)
for tile in range(MAX_COL):
    world_data[-1][tile] = 1

def draw_world():
    for i in range(len(world_data)):
        for j in range(len(world_data[i])):
            if world_data[i][j] >= 0:
                screen.blit(tile_img_list[world_data[i][j]], (j * TILE_SIZE - scroll, i * TILE_SIZE))

mini_sky_img = pygame.transform.scale(sky_img, (300, 100))
mini_mountain_img = pygame.transform.scale(mountain_img, (300, 100))
mini_pine1_img = pygame.transform.scale(pine1_img, (300, 100))
mini_pine2_img = pygame.transform.scale(pine2_img, (300, 100))

def draw_mini_map():
    screen.blit(mini_sky_img, (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(mini_mountain_img, (WIN_WIDTH, WIN_HEIGHT + 5))
    screen.blit(mini_pine1_img, (WIN_WIDTH, WIN_HEIGHT + 15))
    screen.blit(mini_pine2_img, (WIN_WIDTH, WIN_HEIGHT + 30))
    for i in range(len(world_data)):
        for j in range(len(world_data[i])):
            if world_data[i][j] >= 0:
                mini_tile_img = pygame.transform.scale(tile_img_list[world_data[i][j]], (TILE_SIZE // 6.4, TILE_SIZE // 6))
                screen.blit(mini_tile_img, (WIN_WIDTH + j * 2, WIN_HEIGHT + (i * TILE_SIZE // 6.4)))
    pygame.draw.rect(screen, (0, 0, 0), (WIN_WIDTH, WIN_HEIGHT, WIN_WIDTH + SIDE_MORGIN, WIN_HEIGHT + LOWER_MARGIN), 1)

def reset_world():
    world_data.clear()
    for row in range(ROWS):
        r = [-1] * MAX_COL
        world_data.append(r)
    for tile in range(MAX_COL):
        world_data[-1][tile] = 1

save_button_img = pygame.image.load("assets/img/save_btn.png")
load_button_img = pygame.image.load("assets/img/load_btn.png")

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
    draw_text("Show/Hide controls -> F1", small_font, (255, 154, 0), WIN_WIDTH/2, WIN_HEIGHT/2 - 60, True)
    draw_text("Scroll Left -> A or <", small_font, (255, 154, 0), WIN_WIDTH/2, WIN_HEIGHT/2 - 40, True)
    draw_text("Scroll Right -> D or >", small_font, (255, 154, 0), WIN_WIDTH/2, WIN_HEIGHT/2 - 20, True)
    draw_text("Fast scroll -> RSHIFT/LSHIFT", small_font, (255, 154, 0), WIN_WIDTH/2, WIN_HEIGHT/2, True)
    draw_text("Show/Hide grid -> V", small_font, (255, 154, 0), WIN_WIDTH/2, WIN_HEIGHT/2 + 20, True)
    draw_text("Reset world -> R", small_font, (255, 154, 0), WIN_WIDTH/2, WIN_HEIGHT/2 + 40, True)
    draw_text("Grid on/behind tiles -> Q", small_font, (255, 154, 0), WIN_WIDTH/2, WIN_HEIGHT/2 + 60, True)

def darw_grid():
    for i in range(MAX_COL  + 1):
        pygame.draw.line(screen, (255,255,255), (i * TILE_SIZE - scroll, 0), (i * TILE_SIZE - scroll, WIN_HEIGHT - 1))
    for i in range(ROWS + 1):
        pygame.draw.line(screen, (255,255,255), (0, i * TILE_SIZE), (WIN_WIDTH, i * TILE_SIZE))
show_grid = 1
grin_on_tiles = 1

scroll_left = False
scroll_right = False
fast_scroll = False
scroll = 0
scroll_speed = 20

level = 1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                current_tile = 24
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                scroll_left = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                scroll_right = True
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                fast_scroll = True
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if level > 1:
                    level -= 1
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
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                scroll_left = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                scroll_right = False
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                fast_scroll = False

    if scroll_left and scroll > 0:
        scroll -= 5
        if fast_scroll:
            scroll -= scroll_speed
    if scroll_right and scroll < MAX_COL * TILE_SIZE - WIN_WIDTH:
        scroll += 5
        if fast_scroll:
            scroll += scroll_speed
    if scroll < 0:
        scroll = 0

    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    if pos[0] < WIN_WIDTH and pos[1] < WIN_HEIGHT:
        if pygame.mouse.get_pressed()[0]:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2]:
            world_data[y][x] = -1

    draw_bg()
    if grin_on_tiles == 1:
        draw_world()
        if show_grid:
            darw_grid()
    else:
        if show_grid:
            darw_grid()
        draw_world()
    if show_control:
        show_controls()

    draw_text(f"Level: {level}", font, (0, 0, 0), WIN_WIDTH / 2, WIN_HEIGHT + LOWER_MARGIN / 2)
    
    pygame.draw.rect(screen, (10,240,30), (WIN_WIDTH, 0, SIDE_MORGIN, WIN_HEIGHT))
    for i in range(len(button_list)):
        if button_list[i].draw(screen):
            current_tile = i
    pygame.draw.rect(screen, (255, 0, 0), button_list[current_tile].rect, 3)

    if save_button.draw(screen):
        with open(f"levels\level{level}.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            for row in world_data:
                writer.writerow(row)
        
        #f = open(f"levels\level{level}", "wb")
        #pickle.dump(world_data, f)
        #f.close()
                
        print("saved!")

    if load_button.draw(screen):
        scroll = 0

        with open(f"levels\level{level}.csv", "r", newline="") as csv_file:
            reader = list(csv.reader(csv_file, delimiter=","))
            for i in range(len(reader)):
                for j in range(len(reader[i])):
                    world_data[i][j] = int(reader[i][j])

        #f = open(f"levels\level{level}", "rb")
        #world_data = pickle.load(f)
        #f.close()

    draw_mini_map()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()