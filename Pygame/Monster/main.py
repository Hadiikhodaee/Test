import pygame
from config import WIN_HEIGHT, WIN_WIDTH, current_path, os
from player import Player
from game import Game

pygame.init()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Monster")
pygame.display.set_icon(pygame.image.load(os.path.join(current_path, "assets", "images", "Knight.png")))

FPS = 60
clock = pygame.time.Clock()

def main():
    player = Player()
    monster_group = pygame.sprite.Group()
    game = Game(player, monster_group)
    game.start_new_round()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.alive == True:
                    player.wrap()
                if event.key == pygame.K_F1:
                    if game.show_cheat_menu:
                        game.show_cheat_menu = False
                    else:
                        game.show_cheat_menu = True
                if event.key == pygame.K_F8:
                    game.start_new_round()
                if event.key == pygame.K_F7 and game.round_number > 1:
                    game.round_number -= 2
                    game.start_new_round()
                if event.key == pygame.K_q and game.game_over:
                    running = False
                elif event.key == pygame.K_RETURN and game.game_over:
                    main()
                    quit()

        win.fill((0, 0, 0))
        game.update(win)
        
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

main()