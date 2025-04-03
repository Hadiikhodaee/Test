import pygame
from config import WIN_HEIGHT, WIN_WIDTH, FPS, current_path, os
from game import Game
from player import Player

pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Space invaders")
pygame.display.set_icon(pygame.image.load(os.path.join(current_path, "assets", "Gameicon.png")))

def main():
    player_bullet_group = pygame.sprite.Group()
    player = Player(player_bullet_group)

    game = Game(player, player_bullet_group)
    game.start_new_round()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game.game_over:
                    game.player.fire()
                if not game.game_over:
                    if event.key == pygame.K_F1:
                        if game.show_cheat_menu:
                            game.show_cheat_menu = False
                        else:
                            game.show_cheat_menu = True
                    if event.key == pygame.K_F4:
                        if player.laser_limit == 2:
                            player.laser_limit = 1000
                        else:
                            player.laser_limit = 2
                    if event.key == pygame.K_F5:
                        game.alien_group.empty()
                    if event.key == pygame.K_F6 and game.round > 1:
                        game.round -= 2
                        game.alien_group.empty()
                        game.start_new_round()
                    if event.key == pygame.K_F7:
                        game.alien_group.empty()
                        game.start_new_round()
                if game.game_over:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        main()
                        quit()

        game.update(win)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

main()