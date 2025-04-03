import pygame, os
from pygame.locals import *
from random import randint, choice
current_path = os.path.dirname(__file__)

pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 154, 0)

clock = pygame.time.Clock()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Dog Burger")
icon = pygame.transform.flip(pygame.image.load(os.path.join(current_path, "assets", "images", "dog.png")), True, False)
pygame.display.set_icon(icon)

tiny_font = pygame.font.SysFont('terminal', 14)
small_font = pygame.font.SysFont('terminal', 24)
med_font = pygame.font.SysFont('terminal', 32)
font = pygame.font.SysFont('terminal', 40)
big_font = pygame.font.SysFont('terminal', 128)

lose_txt = big_font.render("You lost", True, RED)
lose_txt_rect = lose_txt.get_rect(center = (WIN_WIDTH/2, WIN_HEIGHT/2))

game_over_txt = font.render("Press Q to quit or ENTER to play again", True, ORANGE)
game_over_txt_rect = game_over_txt.get_rect(center = (WIN_WIDTH/2, WIN_HEIGHT/2+75))

left_dog_img = pygame.image.load(os.path.join(current_path, "assets", "images", "dog.png"))
right_dog_img = pygame.transform.flip(left_dog_img, True, False)

coin_img = pygame.transform.scale(pygame.image.load(os.path.join(current_path, "assets", "images", "coin.png")), (32, 32))
coin_img.set_alpha(128)
coin_img_rect = coin_img.get_rect(topleft = (5, 60))

full_heart = pygame.transform.scale(pygame.image.load(os.path.join(current_path, "assets", "images", "heart.png")), (32, 32))
broken_heart = pygame.transform.scale(pygame.image.load(os.path.join(current_path, "assets", "images", "broken_heart.png")), (32, 32))

eat_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "eat_food.wav"))
miss_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "miss.wav"))

def cheats(show_cheats, dog_vel, dog_bost_vel, burger_vel, missed_burgers):
    show_hide_txt = small_font.render("Show/Hide => F1", True, WHITE)
    show_hide_txt_rect = show_hide_txt.get_rect(center = (WIN_WIDTH/2, WIN_HEIGHT/2-60))

    lives_txt = small_font.render("+1 Lives => F2", True, WHITE)
    lives_txt_rect = lives_txt.get_rect(center = (WIN_WIDTH/2, WIN_HEIGHT/2-40))

    full_bost_txt = small_font.render("Full bost => F3", True, WHITE)
    full_bost_txt_rect = full_bost_txt.get_rect(center = (WIN_WIDTH/2, WIN_HEIGHT/2-20))

    unlimited_bost_txt = small_font.render("Infinite bost => F4", True, WHITE)
    unlimited_bost_txt_rect = unlimited_bost_txt.get_rect(center = (WIN_WIDTH/2, WIN_HEIGHT/2))

    vel_change_txt = small_font.render("Less/More velocity => F5/F6", True, WHITE)
    vel_change_txt_rect = vel_change_txt.get_rect(center = (WIN_WIDTH/2, WIN_HEIGHT/2+20))

    dog_vel_change_txt = small_font.render("Less/More dog velocity => F7/F8", True, WHITE)
    dog_vel_change_txt_rect = dog_vel_change_txt.get_rect(center = (WIN_WIDTH/2, WIN_HEIGHT/2+40))

    burger_vel_change_txt = small_font.render("Less/More burger velocity => F9/F10", True, WHITE)
    burger_vel_change_txt_rect = burger_vel_change_txt.get_rect(center = (WIN_WIDTH/2, WIN_HEIGHT/2+60))
    
    dog_vel_txt = tiny_font.render(f"Dog vel: {dog_vel:.1f}", True, WHITE)
    dog_vel_txt_rect = dog_vel_txt.get_rect(bottomleft = (5, WIN_HEIGHT-15))

    dog_bost_vel_txt = tiny_font.render(f"Dog bost vel: {dog_bost_vel:.1f}", True, WHITE)
    dog_bost_vel_txt_rect = dog_bost_vel_txt.get_rect(bottomleft = (5, WIN_HEIGHT-5))

    burger_vel_txt = tiny_font.render(f"Burger vel: {burger_vel:.1f}", True, WHITE)
    burger_vel_txt_rect = burger_vel_txt.get_rect(bottomright = (WIN_WIDTH-5, WIN_HEIGHT-15))

    missed_burgers_txt = tiny_font.render(f"Missed burgers: {missed_burgers}", True, WHITE)
    missed_burgers_txt_rect = missed_burgers_txt.get_rect(bottomright = (WIN_WIDTH-5, WIN_HEIGHT-5))

    if show_cheats:
        win.blits([(show_hide_txt, show_hide_txt_rect),
                   (lives_txt, lives_txt_rect),
                   (full_bost_txt, full_bost_txt_rect),
                   (unlimited_bost_txt, unlimited_bost_txt_rect),
                   (vel_change_txt, vel_change_txt_rect),
                   (dog_vel_change_txt, dog_vel_change_txt_rect),
                   (burger_vel_change_txt, burger_vel_change_txt_rect),
                   (dog_vel_txt, dog_vel_txt_rect),
                   (dog_bost_vel_txt, dog_bost_vel_txt_rect),
                   (burger_vel_txt, burger_vel_txt_rect),
                   (missed_burgers_txt, missed_burgers_txt_rect)])

def main():
    HUMBURGER_VELOCITY = 5
    HUMBURGER_ACCELEATOIN = 0.25
    DOG_NORMAL_VELOCITY = 5
    DOG_NORMAL_ACCELEATOIN = 0.1
    DOG_BOST_VELOCITY = 10
    DOG_BOST_ACCELEATOIN = 0.1

    player_lives = 5
    dog_velocity = DOG_NORMAL_VELOCITY
    score = 0
    humburger_eaten = 0
    missed_burgers = 0
    speed_boost_level = 100
    game_over = False
    show_cheats = False
    unlimited_bost = False

    dog_img = choice([left_dog_img, right_dog_img])
    dog_img_rect = dog_img.get_rect(bottom = WIN_HEIGHT, centerx = WIN_WIDTH / 2)

    burger_img = pygame.image.load(os.path.join(current_path, "assets", "images", "hamburger.png"))
    burger_img_rect = burger_img.get_rect(center = (randint(24, WIN_WIDTH-24), -60))

    heart_img = full_heart
    heart_img.set_alpha(128)
    heart_img_rect = heart_img.get_rect(topright = (640, 60))

    pygame.mixer.music.load(os.path.join(current_path, "assets", "sounds", "bg_music.mp3"))
    pygame.mixer.music.play(-1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    if not show_cheats:
                        show_cheats = True
                    else:
                        show_cheats = False
                if not game_over:
                    if event.key == pygame.K_F2:
                        if pygame.key.get_pressed()[K_LSHIFT]:
                            if player_lives > 1:
                                player_lives -= 1
                        else:
                            player_lives += 1
                    if event.key == pygame.K_F3:
                        speed_boost_level = 100
                    if event.key == pygame.K_F4:
                        if unlimited_bost:
                            unlimited_bost = False
                        else:
                            unlimited_bost = True
                    if event.key == pygame.K_F5:
                        if DOG_NORMAL_VELOCITY > 5:
                            DOG_NORMAL_VELOCITY -= DOG_NORMAL_ACCELEATOIN
                            DOG_BOST_VELOCITY -= DOG_BOST_ACCELEATOIN
                        if HUMBURGER_VELOCITY > 5:
                            HUMBURGER_VELOCITY -= HUMBURGER_ACCELEATOIN
                    if event.key == pygame.K_F6:
                        DOG_NORMAL_VELOCITY += DOG_NORMAL_ACCELEATOIN
                        DOG_BOST_VELOCITY += DOG_BOST_ACCELEATOIN
                        HUMBURGER_VELOCITY += HUMBURGER_ACCELEATOIN
                    if event.key == pygame.K_F7 and DOG_NORMAL_VELOCITY > 5:
                        DOG_NORMAL_VELOCITY -= DOG_NORMAL_ACCELEATOIN
                        DOG_BOST_VELOCITY -= DOG_BOST_ACCELEATOIN
                    if event.key == pygame.K_F8:
                        DOG_NORMAL_VELOCITY += DOG_NORMAL_ACCELEATOIN
                        DOG_BOST_VELOCITY += DOG_BOST_ACCELEATOIN
                    if event.key == pygame.K_F9 and HUMBURGER_VELOCITY > 5:
                        HUMBURGER_VELOCITY -= HUMBURGER_ACCELEATOIN
                    if event.key == pygame.K_F10:
                        HUMBURGER_VELOCITY += HUMBURGER_ACCELEATOIN
                else:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        main()
                        quit()

        win.fill(BLACK)

        if not game_over:
            score_text = font.render(f'X {score}', True, ORANGE)
            score_text_rect = score_text.get_rect(topleft = (coin_img_rect.right , 64))
            score_text.set_alpha(128)
    
            title = font.render('Burger Dog', True, ORANGE)
            title_rect = title.get_rect(topleft = (WIN_HEIGHT / 2, 20))
            title.set_alpha(128)
    
            eaten_text = font.render(f'Burger eaten : {humburger_eaten}', True, ORANGE)
            eaten_rect = eaten_text.get_rect(topleft = (WIN_HEIGHT / 2, 60))
            eaten_text.set_alpha(128)
    
            lives_text = font.render(f' X {player_lives}', True, ORANGE)
            lives_rect = lives_text.get_rect(topleft = (heart_img_rect.right, 62))
            lives_text.set_alpha(128)
    
            if unlimited_bost:
                speed_boost_level = 100
                bost_text = font.render('Infinite bost', True, ORANGE)
                bost_rect = bost_text.get_rect(topleft = (heart_img_rect.left, 20))
                bost_text.set_alpha(128)
            else:
                bost_text = font.render(f'Boost lv: {speed_boost_level}', True, ORANGE)
                bost_rect = bost_text.get_rect(topleft = (heart_img_rect.left, 20))
                bost_text.set_alpha(128)
    
            burger_point = (WIN_HEIGHT - burger_img_rect.y) // 10
            point_text = font.render(f'Burger point : {burger_point}', True, ORANGE)
            point_rect = point_text.get_rect(topleft = (coin_img_rect.left + 5, 20))
            point_text.set_alpha(128)
            
            keys = pygame.key.get_pressed()
            if keys[K_SPACE] and speed_boost_level > 0:
                dog_velocity = DOG_BOST_VELOCITY
                speed_boost_level -= 1
            else:
                dog_velocity = DOG_NORMAL_VELOCITY
            if (keys[K_d] or keys[K_RIGHT]) and dog_img_rect.right < WIN_WIDTH:
                dog_img = right_dog_img
                dog_img_rect.x += dog_velocity
            if (keys[K_a] or keys[K_LEFT]) and dog_img_rect.left > 0:
                dog_img = left_dog_img
                dog_img_rect.x -= dog_velocity
            if (keys[K_w] or keys[K_UP]) and dog_img_rect.top > 0:
                dog_img_rect.y -= dog_velocity
            if (keys[K_s] or keys[K_DOWN]) and dog_img_rect.bottom < WIN_HEIGHT:
                dog_img_rect.y += dog_velocity
    
        burger_img_rect.y += HUMBURGER_VELOCITY
    
        if dog_img_rect.colliderect(burger_img_rect):
            eat_sound.play()
            if speed_boost_level <= 90:
                speed_boost_level += 10
            elif speed_boost_level > 90:
                speed_boost_level = 100
            score += burger_point
            humburger_eaten += 1
            HUMBURGER_VELOCITY += HUMBURGER_ACCELEATOIN
            DOG_NORMAL_VELOCITY += DOG_NORMAL_ACCELEATOIN
            DOG_BOST_VELOCITY += DOG_BOST_ACCELEATOIN
            burger_img_rect.center = (randint(24, WIN_WIDTH-24), -60)
        elif burger_img_rect.bottom > WIN_HEIGHT:
            if not game_over:
                player_lives -= 1
                missed_burgers += 1
            miss_sound.play()
            burger_img_rect.center = (randint(24, WIN_WIDTH-24), -60)
        if player_lives <= 0 and not game_over:
            game_over = True
            pygame.mixer.music.pause()
            show_cheats = False
            lives_text = font.render(f' X {player_lives}', True, ORANGE)
            lives_text.set_alpha(128)
            dog_img_rect.topleft = (-75, -75)
            heart_img = broken_heart
            heart_img.set_alpha(128)

        win.blits([(burger_img, burger_img_rect),
                   (point_text, point_rect),
                   (title, title_rect),
                   (bost_text, bost_rect),
                   (coin_img, coin_img_rect),
                   (score_text, score_text_rect),
                   (eaten_text, eaten_rect),
                   (heart_img, heart_img_rect),
                   (lives_text, lives_rect)])

        if not game_over:
            win.blit(dog_img, dog_img_rect)

        cheats(show_cheats, dog_velocity, DOG_BOST_VELOCITY, HUMBURGER_VELOCITY, missed_burgers)

        if game_over:
            win.blits([(lose_txt, lose_txt_rect),(game_over_txt, game_over_txt_rect)])
        
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

main()