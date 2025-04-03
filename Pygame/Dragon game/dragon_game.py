import pygame, os
from random import randint, choice
current_path = os.path.dirname(__file__)

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
FPS = 60

win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dragon game")
icon_image = pygame.transform.scale(pygame.image.load(os.path.join(current_path, "assets", "images", "main_dragon.png")), (64, 64))
icon_image = pygame.transform.flip(icon_image, True, False)
pygame.display.set_icon(icon_image)
clock = pygame.time.Clock()

small_font = pygame.font.SysFont("terminal", 24)
med_font = pygame.font.Font(os.path.join(current_path, "assets", "DragonHunter.otf"), 38)
font = pygame.font.Font(os.path.join(current_path, "assets", "DragonHunter.otf"), 48)

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (243, 157, 20)

right_dragon_image = pygame.image.load(os.path.join(current_path, "assets", "images", "dragon.png"))
right_dragon_image_rect = right_dragon_image.get_rect()
right_dragon_image_rect.topright = (WINDOW_WIDTH, 0)

left_dragon_image = pygame.transform.flip(right_dragon_image, True, False)
left_dragon_image_rect = left_dragon_image.get_rect()
left_dragon_image_rect.topleft = (0, 0)

coin_image = pygame.image.load(os.path.join(current_path, "assets", "images", "coin.png"))
coin_image_rect = coin_image.get_rect()
coin_image_rect.topleft = (WINDOW_WIDTH/7, 70)

title_text = font.render("Dragon game", True, GREEN)
title_text_rect = title_text.get_rect(top=0, centerx=WINDOW_WIDTH/2)

broken_heart_image = pygame.image.load(os.path.join(current_path, "assets", "images", "broken_heart.png"))

food_list = [pygame.image.load(os.path.join(current_path, "assets", "images", "foods", f"food_{i}.png")) 
         for i in range(len(os.listdir(os.path.join(current_path, "assets", "images", "foods"))))]

eat_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "eat_food.wav"))
miss_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "miss.wav"))

lose_text = med_font.render("Press Q to quit or ENTER to play again", True, ORANGE)
lose_text_rect = lose_text.get_rect(centerx=WINDOW_WIDTH/2, centery=(WINDOW_HEIGHT+128)/2)

def choice_food():
    food = choice(food_list)
    food_rect = food.get_rect(centerx=WINDOW_WIDTH+48, centery=randint(128+24, WINDOW_HEIGHT-24))

    return food, food_rect

def cheats(show_cheat_menu, player_velocity, food_velocity):
    show_hide_text = small_font.render("Show/Hide => F1", True, WHITE)
    show_hide_text_rect = show_hide_text.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT+128)/2-25))

    health_text = small_font.render("+1 lives => F2", True, WHITE)
    health_text_rect = health_text.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT+128)/2))

    more_velocity_text = small_font.render("Less velocity/More velocity => F3/F4", True, WHITE)
    more_velocity_text_rect = more_velocity_text.get_rect(center=(WINDOW_WIDTH/2, (WINDOW_HEIGHT+128)/2+25))

    player_velocity_text = small_font.render(f"Player velocity: {player_velocity:.1f}", True, WHITE)
    player_velocity_text_rect = player_velocity_text.get_rect(bottomleft=(5, WINDOW_HEIGHT-5))

    food_velocity_text = small_font.render(f"Food velocity: {food_velocity:.1f}", True, WHITE)
    food_velocity_text_rect = food_velocity_text.get_rect(bottomright=(WINDOW_WIDTH-5, WINDOW_HEIGHT-5))

    if show_cheat_menu:
        win.blits([(show_hide_text, show_hide_text_rect),
                    (health_text, health_text_rect),
                    (more_velocity_text, more_velocity_text_rect)])
        win.blits([(player_velocity_text, player_velocity_text_rect),
                   (food_velocity_text, food_velocity_text_rect)])

def main():
    pygame.mixer.music.load(os.path.join(current_path, "assets", "sounds", "Back_ground_sound.mp3"))
    pygame.mixer.music.play(-1)
    game_over = False
    show_cheat_menu = False

    PLAYER_STARTING_LIVES = 3
    PLAYER_VELOCITY = 10
    PLAYER_ACCELEATOIN = 0.2
    FOOD_STARTING_VLOCITY = 10
    FOOD_ACCELEATOIN = 0.5

    score = 0
    player_lives = PLAYER_STARTING_LIVES
    FOOD_VLOCITY = FOOD_STARTING_VLOCITY

    heart_image = pygame.image.load(os.path.join(current_path, "assets", "images", "heart.png"))
    heart_images = list()

    dragon_head = pygame.image.load(os.path.join(current_path, "assets", "images", "main_dragon.png"))
    dragon = pygame.transform.scale(pygame.transform.flip(dragon_head, True, False), (96, 96))
    dragon_rect = dragon.get_rect(centerx=50, centery=(WINDOW_HEIGHT + 128) // 2)

    for i in range(3):
        heart_images.append((heart_image, heart_image.get_rect(topleft=(700 + i * 50, 70))))
    
    score_text = font.render(f": {score}", True, GREEN)
    score_text_rect = score_text.get_rect(topleft= (190, 70))

    food, food_rect = choice_food()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                        if not show_cheat_menu:
                            show_cheat_menu = True
                        else:
                            show_cheat_menu = False
                if game_over:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        main()
                        quit()
                else:
                    if event.key == pygame.K_F2 and keys[pygame.K_LSHIFT]:
                        if player_lives > 1:
                            heart_images[3 - player_lives] = (broken_heart_image, broken_heart_image.get_rect(topleft=(700 + (3 - player_lives) * 50, 70)))
                            player_lives -= 1
                    elif event.key == pygame.K_F2 and player_lives < PLAYER_STARTING_LIVES:
                        heart_images[2 - player_lives] = (heart_image, heart_image.get_rect(topleft=(700 + (2 - player_lives) * 50, 70)))
                        player_lives += 1
                    if event.key == pygame.K_F3 and FOOD_VLOCITY > 10:
                        FOOD_VLOCITY -= FOOD_ACCELEATOIN
                        PLAYER_VELOCITY -= PLAYER_ACCELEATOIN
                    if event.key == pygame.K_F4:
                        PLAYER_VELOCITY += PLAYER_ACCELEATOIN
                        FOOD_VLOCITY += FOOD_ACCELEATOIN

        win.fill(BLACK)

        if not game_over:

            keys = pygame.key.get_pressed()

            if (keys[pygame.K_w] or keys[pygame.K_UP]) and dragon_rect.top > 128:
                dragon_rect.y -= PLAYER_VELOCITY
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and dragon_rect.bottom < WINDOW_HEIGHT:
                dragon_rect.y += PLAYER_VELOCITY

            food_rect.x -= FOOD_VLOCITY

            if dragon_rect.colliderect(food_rect):
                score += 10
                eat_sound.play()
                score_text = font.render(f": {score}", True, GREEN)
                food, food_rect = choice_food()
                FOOD_VLOCITY += FOOD_ACCELEATOIN
                PLAYER_VELOCITY += PLAYER_ACCELEATOIN

            elif food_rect.x < 0:
                heart_images[3 - player_lives] = (broken_heart_image, broken_heart_image.get_rect(topleft=(700 + (3 - player_lives) * 50, 70)))
                player_lives -= 1
                miss_sound.play()
                food, food_rect = choice_food()

            if player_lives <= 0:
                show_cheat_menu = False
                pygame.mixer.music.pause()
                game_over = True

        win.blits([(right_dragon_image, right_dragon_image_rect),
                  (left_dragon_image, left_dragon_image_rect),
                  (coin_image, coin_image_rect),
                  (score_text, score_text_rect),
                  (title_text, title_text_rect),
                  (dragon, dragon_rect),
                  (food, food_rect)] + heart_images)
        pygame.draw.line(win, WHITE, (0, 128), (WINDOW_WIDTH, 128), 4)

        cheats(show_cheat_menu, PLAYER_VELOCITY, FOOD_VLOCITY)

        if game_over:
            win.blit(lose_text, lose_text_rect)
            
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

main()