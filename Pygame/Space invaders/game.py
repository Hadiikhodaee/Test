import pygame
from config import WIN_HEIGHT, WIN_WIDTH, current_path, os
from alien import Alien

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (40, 255, 20)
RED = (255, 0, 0)

class Game():
    def __init__(self, player, player_bullet_group):
        self.score = 0
        self.round = 0

        self.player = player
        self.player_bullet_group = player_bullet_group
        self.alien_group = pygame.sprite.Group()
        self.alien_bullet_group = pygame.sprite.Group()

        self.alien_hit_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "alien_hit.wav"))
        self.lose_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "breach.wav"))
        self.win_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "next_round.wav"))
        self.player_hit_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "player_hit.wav"))

        self.small_font = pygame.font.SysFont("terminal", 28)
        self.font = pygame.font.Font(os.path.join(current_path, "assets", "Facon.ttf"), 32)
        self.medfont = pygame.font.Font(os.path.join(current_path, "assets", "Facon.ttf"), 44) 
        self.big_font = pygame.font.Font(os.path.join(current_path, "assets", "Facon.ttf"), 128)

        self.win_text = self.big_font.render("You won", True, GREEN)
        self.win_text_rect = self.win_text.get_rect()
        self.win_text_rect.centerx = WIN_WIDTH // 2
        self.win_text_rect.centery = WIN_HEIGHT // 2

        self.lose_text = self.big_font.render("You lost", True, RED)
        self.lose_text_rect = self.lose_text.get_rect()
        self.lose_text_rect.centerx = WIN_WIDTH // 2
        self.lose_text_rect.centery = WIN_HEIGHT // 2 - 25

        self.new_game_text = self.medfont.render("Press Q to quit or ENTER to play again", True, (243, 157, 20))
        self.new_game_text_rect = self.new_game_text.get_rect()
        self.new_game_text_rect.center = (WIN_WIDTH // 2, self.lose_text_rect.bottom + 25)

        self.show_cheat_menu = False
        self.play_sound_once = True
        self.isVictory = False
        self.first_victory_time = 280
        self.victory_time = self.first_victory_time
        self.game_over = False

    def start_new_round(self):
        self.round += 1
        for row in range(11):
            for col in range(5):
                Alien(64 + row * 64, 64 + col * 64, self.round, self.alien_group, self.alien_bullet_group)

    def win(self, screen):
        if self.isVictory and not self.game_over:
            if self.play_sound_once:
                self.win_sound.play()
                self.alien_bullet_group.empty()
                self.score += 1000 * self.round
                self.play_sound_once = False
                self.show_cheat_menu = False
            screen.blit(self.win_text, self.win_text_rect)
            self.victory_time -= 1
            if self.victory_time <= 0:
                self.isVictory = False
                self.player.rect.centerx = WIN_WIDTH // 2
                self.play_sound_once = True
                self.player_bullet_group.empty()
                self.victory_time = self.first_victory_time
                self.start_new_round()

    def lose(self, screen):
        if self.game_over:
            if self.play_sound_once:
                self.lose_sound.play()
                self.player_bullet_group.empty()
                self.play_sound_once = False
                self.show_cheat_menu = False
                self.player.rect.centery = 0 - 32
            screen.blit(self.lose_text, self.lose_text_rect)
            screen.blit(self.new_game_text, self.new_game_text_rect)

    def shift_aliens(self):
        shift = False
        for alien in self.alien_group.sprites():
            if alien.rect.left < 0 or alien.rect.right > WIN_WIDTH:
                shift = True
        if shift:
            for alien in self.alien_group.sprites():
                if not self.game_over:
                    alien.rect.y += 10 * self.round
                alien.direction *= -1

                if alien.rect.bottom >= WIN_HEIGHT - 80:
                    self.player.lives = 0
                    self.game_over = True

    def check_collisions(self):
        if pygame.sprite.groupcollide(self.player_bullet_group, self.alien_group, True, True):
            self.alien_hit_sound.play()
            self.score += 100

        if pygame.sprite.spritecollide(self.player, self.alien_bullet_group, True):
            self.player_hit_sound.play()
            self.player.lives -= 1

    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        pygame.draw.line(screen, WHITE, (0, 50), (WIN_WIDTH, 50), 3)
        pygame.draw.line(screen, WHITE, (0, WIN_HEIGHT - 80), (WIN_WIDTH, WIN_HEIGHT - 80), 3)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (30, 9)

        round_text = self.font.render(f"Round: {self.round}", True, WHITE)
        round_text_rect = round_text.get_rect()
        round_text_rect.centerx = WIN_WIDTH // 2
        round_text_rect.centery = 25

        lives_text = self.font.render(f"Lives: {self.player.lives}", True, WHITE)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topright = (WIN_WIDTH - 30, 9)

        if not self.game_over:
            self.player.draw(screen)
            self.player_bullet_group.draw(screen)
        self.alien_bullet_group.draw(screen)
        self.alien_group.draw(screen)

        screen.blits([(score_text, score_text_rect),
                       (round_text, round_text_rect),
                       (lives_text, lives_text_rect)])

    def cheat(self, screen):
        keys = pygame.key.get_pressed()

        show_hide_text = self.small_font.render("Hide/Show => F1", True, WHITE)
        show_hide_text_rect = show_hide_text.get_rect()
        show_hide_text_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2 - 75)

        live_text = self.small_font.render("+1 Lives => F2", True, WHITE)
        live_text_rect = live_text.get_rect()
        live_text_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50)

        score_text = self.small_font.render("+100 Score => F3", True, WHITE)
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2 - 25)

        unlimited_laser_text = self.small_font.render("Unlimited laser => F4", True, WHITE)
        unlimited_laser_text_rect = unlimited_laser_text.get_rect()
        unlimited_laser_text_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2)

        clear_round = self.small_font.render("Clear round => F5", True, WHITE)
        clear_round_rect = clear_round.get_rect()
        clear_round_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 25)

        previous_round_text = self.small_font.render("Go previous round => F6", True, WHITE)
        previous_round_text_rect = previous_round_text.get_rect()
        previous_round_text_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50)

        next_round_text = self.small_font.render("Go next round => F7", True, WHITE)
        next_round_text_rect = next_round_text.get_rect()
        next_round_text_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 75)

        if self.show_cheat_menu:
            screen.blits([(show_hide_text, show_hide_text_rect),
                          (live_text, live_text_rect),
                          (score_text, score_text_rect),
                          (clear_round, clear_round_rect),
                          (unlimited_laser_text, unlimited_laser_text_rect),
                          (previous_round_text, previous_round_text_rect),
                          (next_round_text, next_round_text_rect)])
        
        if not self.game_over:
            if keys[pygame.K_F2] and keys[pygame.K_LSHIFT]:
                if self.player.lives > 1:
                    self.player.lives -= 1
            elif keys[pygame.K_F2]:
                self.player.lives += 1
            if keys[pygame.K_F3]:
                self.score += 100

    def update(self, screen):
        if not self.alien_group:
            self.isVictory = True
        if self.player.lives <= 0:
            self.game_over = True

        self.draw(screen)
        self.cheat(screen)
        self.shift_aliens()
        self.check_collisions()
        self.win(screen)
        self.lose(screen)

        if not self.game_over:
            self.player.update()
            self.player_bullet_group.update()
        self.alien_group.update()
        self.alien_bullet_group.update()