import pygame
from monster import Monster
import random
from config import WIN_HEIGHT, WIN_WIDTH, current_path, os

BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (226, 73, 243)
YELLOW = (243, 157, 20)

class Game():
    def __init__(self, player, monster_group):
        self.score = 0
        self.round_number = 0
        self.round_time = 0

        self.player = player
        self.monster_group = monster_group
        self.victory_time = 170
        self.victory_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "next_level.wav"))
        self.death_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "death.wav"))
        self.small_font = pygame.font.SysFont("terminal", 24)
        self.font = pygame.font.Font(os.path.join(current_path, "assets", "Abrushow.ttf"), 32)
        self.medfont = pygame.font.SysFont("terminal", 54)
        self.bigfont = pygame.font.Font(os.path.join(current_path, "assets", "Abrushow.ttf"), 126)
        self.play_sound_once = True
        self.game_over = False
        self.show_cheat_menu = False

        self.victory_text = self.bigfont.render("You Won", True, (0, 255, 0))
        self.victory_text_rect = self.victory_text.get_rect()
        self.victory_text_rect.center = (WIN_WIDTH//2, WIN_HEIGHT//2)

        self.time_out_text = self.bigfont.render("Time Out", True, (255, 0, 0))
        self.time_out_text_rect = self.victory_text.get_rect()
        self.time_out_text_rect.center = (WIN_WIDTH//2, WIN_HEIGHT//2)

        self.death_text = self.bigfont.render("You Lost", True, (255, 0, 0))
        self.death_text_rect = self.victory_text.get_rect()
        self.death_text_rect.center = (WIN_WIDTH//2, WIN_HEIGHT//2)

        self.new_game_text = self.medfont.render("Press Q to quit or ENTER to play again", True, (243, 157, 20))
        self.new_game_text_rect = self.new_game_text.get_rect()
        self.new_game_text_rect.center = (WIN_WIDTH//2, self.death_text_rect.bottom + 25)

        blue_monster = pygame.image.load(os.path.join(current_path, "assets", "images", "blue_monster.png"))
        green_monster = pygame.image.load(os.path.join(current_path, "assets", "images", "green_monster.png"))
        purple_monster = pygame.image.load(os.path.join(current_path, "assets", "images", "purple_monster.png"))
        yellow_monster = pygame.image.load(os.path.join(current_path, "assets", "images", "yellow_monster.png"))

        self.target_monster_images = [blue_monster, green_monster, purple_monster, yellow_monster]
        self.target_monster_type = random.randint(0, 3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]
        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = WIN_WIDTH/2
        self.target_monster_rect.top = 37

        self.isVictory = False

    def draw(self, screen):
        colors = [BLUE, GREEN, PURPLE, YELLOW]

        self.monster_group.draw(screen)
        screen.blit(self.target_monster_image, self.target_monster_rect)
        pygame.draw.rect(screen, colors[self.target_monster_type], (WIN_WIDTH/2 - 32, 36, 64, 64), 3)
        pygame.draw.rect(screen, colors[self.target_monster_type], (0, 100, WIN_WIDTH, WIN_HEIGHT-200), 3)

        time_text = self.font.render(f"Time: {self.round_time:.1f}s", True, YELLOW)
        time_text_rect = time_text.get_rect()
        time_text_rect.topleft = (5, 10)

        score_text = self.font.render(f"Score: {self.score}", True, YELLOW)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (5, time_text_rect.bottom + 8)

        round_text = self.font.render(f"Round {self.round_number}", True, YELLOW)
        round_text_rect = round_text.get_rect()
        round_text_rect.centerx = (WIN_WIDTH // 2)
        round_text_rect.y = 5

        wraps_text = self.font.render(f"Wraps: {self.player.wraps}", True, YELLOW)
        wraps_text_rect = wraps_text.get_rect()
        wraps_text_rect.topright = (WIN_WIDTH - 5, 10)

        hp_text = self.font.render(f"HP: {self.player.health}", True, YELLOW)
        hp_text_rect = hp_text.get_rect()
        hp_text_rect.topright = (WIN_WIDTH - 5, wraps_text_rect.bottom + 8)

        screen.blit(time_text, time_text_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(round_text, round_text_rect)
        screen.blit(wraps_text, wraps_text_rect)
        screen.blit(hp_text, hp_text_rect)

        if self.player.alive:
            self.player.draw(screen)

    def start_new_round(self):
        self.player.reset()
        self.round_number += 1
        self.round_time = 60 * self.round_number
        self.player.wraps = 2 * self.round_number

        self.monster_group.empty()
        for i in range(self.round_number*4):
            monster_type = random.randint(0, 3)
            monster = Monster(random.randint(64, WIN_WIDTH - 64), random.randint(164, WIN_HEIGHT-164), self.target_monster_images[monster_type], monster_type)
            self.monster_group.add(monster)

    def new_target(self):
            while True:
                random_target = random.randint(0, 3)
                monster_exists = any(monster.monster_type == random_target for monster in self.monster_group)
                if monster_exists:
                    self.target_monster_type = random_target
                    self.target_monster_image = self.target_monster_images[self.target_monster_type]
                    break

    def check_collisions(self):
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monster_group)
        if collided_monster:
            if collided_monster.monster_type == self.target_monster_type:
                self.score += 10
                self.player.catch_sound.play()
                collided_monster.kill()
                if self.monster_group:
                    self.new_target()
            else:
                self.player.reset()
                self.player.health -= 1
                self.player.die_sound.play()

    def update(self, screen):
        if self.player.alive == True:
            self.player.update()
        self.monster_group.update()
        if self.round_time > 0 and not self.isVictory and self.player.alive:
            self.round_time -= 0.01

        monster_exists = any(monster.monster_type == self.target_monster_type for monster in self.monster_group)
        if not monster_exists and self.monster_group:
            self.new_target()

        self.check_collisions()

        self.draw(screen)
        self.cheat(screen)

        if not self.monster_group:
            self.isVictory = True
        if self.isVictory:
            if self.play_sound_once == True:
                self.victory_sound.play()
                self.score += 100
                self.play_sound_once = False
                self.show_cheat_menu = False
            screen.blit(self.victory_text, self.victory_text_rect)
            self.victory_time -= 1
            if self.victory_time <= 0:
                self.start_new_round()
                self.isVictory = False
                self.victory_time = 170
                self.play_sound_once = True

        if self.round_time <= 0 and not self.isVictory:
            if self.play_sound_once:
                self.death_sound.play()
                self.play_sound_once = False
                self.game_over = True
                self.player.alive = False
                self.show_cheat_menu = False
            screen.blit(self.time_out_text, self.time_out_text_rect)

        if self.player.health <= 0:
            if self.play_sound_once:
                self.death_sound.play()
                self.play_sound_once = False
                self.game_over = True
                self.player.alive = False
                self.show_cheat_menu = False
            screen.blit(self.death_text, self.death_text_rect)

        if self.game_over:
            screen.blit(self.new_game_text, self.new_game_text_rect)

    def cheat(self, screen):
        keys = pygame.key.get_pressed()
        YELLOW = (243, 157, 20)
        
        hide_show_text = self.small_font.render("Hide/Show => F1", True, YELLOW)
        hide_show_text_rect = hide_show_text.get_rect()
        hide_show_text_rect.center = (WIN_WIDTH//2, (WIN_HEIGHT//2)-70)

        hp_text = self.small_font.render("HP +1 => F2", True, YELLOW)
        hp_text_rect = hp_text.get_rect()
        hp_text_rect.center = (WIN_WIDTH//2, (WIN_HEIGHT//2)-50)
        
        wrap_text = self.small_font.render("Wrap +1 => F3", True, YELLOW)
        wrap_text_rect = wrap_text.get_rect()
        wrap_text_rect.center = (WIN_WIDTH//2, (WIN_HEIGHT//2)-30)

        time_text = self.small_font.render("Time +10s => F4", True, YELLOW)
        time_text_rect = time_text.get_rect()
        time_text_rect.center = (WIN_WIDTH//2, (WIN_HEIGHT//2)-10)

        score_text = self.small_font.render("Score +10 => F5", True, YELLOW)
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (WIN_WIDTH//2, (WIN_HEIGHT//2)+10)

        clear_round_text = self.small_font.render("Clear round => F6", True, YELLOW)
        clear_round_text_rect = clear_round_text.get_rect()
        clear_round_text_rect.center = (WIN_WIDTH//2, (WIN_HEIGHT//2)+30)

        previous_round_text = self.small_font.render("Go previous round => F8", True, YELLOW)
        previous_round_text_rect = previous_round_text.get_rect()
        previous_round_text_rect.center = (WIN_WIDTH//2, (WIN_HEIGHT//2)+50)

        next_round_text = self.small_font.render("Go next round => F7", True, YELLOW)
        next_round_text_rect = next_round_text.get_rect()
        next_round_text_rect.center = (WIN_WIDTH//2, (WIN_HEIGHT//2)+70)

        list = [
            (hide_show_text, hide_show_text_rect),
            (hp_text, hp_text_rect),
            (wrap_text, wrap_text_rect),
            (time_text, time_text_rect),
            (score_text, score_text_rect),
            (clear_round_text, clear_round_text_rect),
            (previous_round_text, previous_round_text_rect),
            (next_round_text, next_round_text_rect)
        ]

        if keys[pygame.K_F2]:
            self.player.health += 1
        if keys[pygame.K_F3]:
            self.player.wraps += 1
        if keys[pygame.K_F4]:
            self.round_time += 10
        if keys[pygame.K_F5]:
            self.score += 10
        if keys[pygame.K_F6]:
            self.monster_group.empty()

        if self.show_cheat_menu:
            screen.blits(list)