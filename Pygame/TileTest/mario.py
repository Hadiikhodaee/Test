from configs import *

WIN_WIDTH, WIN_HEIGTH = 775, 395
tile_width, tile_heigth = 16, 16

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGTH))
pygame.display.set_caption("Tile Test")

main_tile_image = pygame.image.load(os.path.join(current_path, "assets", "main_tile_image.png"))
main_tile_image.set_colorkey((148, 148, 255))

tile_list = []
for col in range (4):
    for row in range(8):
        tile_img = main_tile_image.subsurface(pygame.Rect(row*tile_width+(row*1), col*tile_heigth+tile_heigth+(col*1), tile_width, tile_heigth))
        tile_img = pygame.transform.scale(tile_img, (16*5, 16*5))
        tile_list.append(tile_img)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        WIN.fill((0, 255, 90))
    
        for tile_col in range(4):
            tiles = tile_list[tile_col*8:(tile_col+1)*8]
            for i in range(len(tiles)):
                WIN.blit(tiles[i], (15+(15*i)+i*(16*5), 15+(15*tile_col)+tile_col*(16*5)))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

main()