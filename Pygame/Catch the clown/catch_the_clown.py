import pygame, os
from random import choice, randint
current_path = os.path.dirname(__file__)

pygame.init()

WINDOW_WIDTH = 945
WINDOW_HEIGHT = 600

FPS = 60
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch the Clown")
pygame.display.set_icon(pygame.image.load(os.path.join(current_path, "assets", "images", "clown.png")))

small_font = pygame.font.SysFont('terminal', 34)
font = pygame.font.SysFont('terminal', 64)
text_alpha = 200

bg_img = pygame.image.load(os.path.join(current_path, "assets", "images", "background.png"))
bg_image = pygame.transform.scale(bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
bg_image_rect = bg_image.get_rect(topleft = (0, 0))

coin_image = pygame.image.load(os.path.join(current_path, "assets", "images", "coin.png"))
coin_rect = coin_image.get_rect(topleft = (30, 30))

heart_img = pygame.image.load(os.path.join(current_path, "assets", "images", "heart.png"))
heart_rect = heart_img.get_rect(topleft = (800, 30))
broken_heart_image = pygame.image.load(os.path.join(current_path, "assets", "images", "broken_heart.png"))

catch_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "catch.wav"))
miss_sound = pygame.mixer.Sound(os.path.join(current_path, "assets", "sounds", "miss.wav"))

game_over_text = small_font.render("Press Q to quit or ENTER to play again", True, RED)
game_over_text_rect = game_over_text.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

def cheats(show_cheats, clown_velocity, dx, dy):
    show_hide_text = small_font.render("Show/Hide => F1", True, RED)
    show_hide_text_rect = show_hide_text.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 25))

    lives_text = small_font.render("+1 live => F2",  True, RED)
    lives_text_rect = lives_text.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

    velocity_text = small_font.render("Less/More velocity => F3/F4", True, RED)
    velocity_text_rect = velocity_text.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 25))
    
    clown_velocity_text = small_font.render(f"Clown velocity: {clown_velocity:.1f}", True, RED)
    clown_velocity_text_rect = clown_velocity_text.get_rect(bottomleft = (5, WINDOW_HEIGHT - 5))

    dx_dy_text = small_font.render(f"DX: {dx} | DY: {dy}", True, RED)
    dx_dy_text_rect = dx_dy_text.get_rect(bottomright = (WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5))

    if show_cheats:
        win.blits([(show_hide_text, show_hide_text_rect),
                   (lives_text, lives_text_rect),
                   (velocity_text, velocity_text_rect),
                   (clown_velocity_text, clown_velocity_text_rect),
                   (dx_dy_text, dx_dy_text_rect)])

def main():
    pygame.mixer.music.load(os.path.join(current_path, "assets", "sounds", "BGmusic.mp3"))
    pygame.mixer.music.play(-1) 

    clown_img = pygame.image.load(os.path.join(current_path, "assets", "images", "clown.png"))
    clown_image = pygame.transform.scale(clown_img, (64, 64))
    clown_rect = clown_image.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

    heart_image = heart_img

    dx = choice([-1, 1])
    dy = choice([-1, 1])

    clown_velocity = 5
    lives = 5
    score = 0
    game_over = False
    show_cheats = False

    CLOWN_ACCELEATOIN = 0.1

    score_text = font.render(f": {score}", True, BLACK)
    score_text_rect = score_text.get_rect(topleft = (80, 30))

    lives_text = font.render(f": {lives}", True, BLACK)
    lives_text_rect = lives_text.get_rect(topleft = (850, 30))

    catch_miss_text = font.render("", True, BLACK)
    catch_miss_text_rect = catch_miss_text.get_rect()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_q:
                        quit()
                        running = False
                    elif event.key == pygame.K_RETURN:
                        main()
                        quit()
                else:
                    if event.key == pygame.K_F1:
                        if show_cheats:
                            show_cheats = False
                        else:
                            show_cheats = True
                    if pygame.key.get_pressed()[pygame.K_LSHIFT] and event.key == pygame.K_F2:
                        if lives > 1:
                            lives -= 1
                    elif event.key == pygame.K_F2 and lives < 5:
                        lives += 1
                    if event.key == pygame.K_F3 and clown_velocity > 5:
                        clown_velocity -= CLOWN_ACCELEATOIN
                    if event.key == pygame.K_F4:
                        clown_velocity += CLOWN_ACCELEATOIN
                if event.key == pygame.K_COMMA:
                    pygame.display.toggle_fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if pygame.mouse.get_pressed()[0]:
                    set_alpha = text_alpha
                    if clown_rect.collidepoint(event.pos):
                        score += 10
                        clown_rect.center = (randint(34, WINDOW_WIDTH-34), randint(34, WINDOW_HEIGHT-34))
                        dx = choice([-1, 1])
                        dy = choice([-1, 1])
                        clown_velocity += CLOWN_ACCELEATOIN
                        catch_miss_text = font.render("Caught", True, GREEN)
                        catch_sound.play()
                    else:
                        lives -= 1
                        catch_miss_text = font.render("Missed", True, RED)
                        miss_sound.play()

                    mouse_pos = pygame.mouse.get_pos()
                    catch_miss_text_rect.center = (mouse_pos[0]-catch_miss_text.get_width()/2, mouse_pos[1])

        win.fill(BLACK)
        score_text = font.render(f": {score}", True, BLACK)
        lives_text = font.render(f": {lives}", True, BLACK)

        if lives <= 0:
            game_over = True

        if not game_over:

            try:
                set_alpha -= 5
                catch_miss_text.set_alpha(set_alpha)
            except:
                None

            clown_rect.x += dx * clown_velocity
            clown_rect.y += dy * clown_velocity

            if clown_rect.left < 0 or clown_rect.right > WINDOW_WIDTH:
                dx *= -1
            if clown_rect.top < 0 or clown_rect.bottom > WINDOW_HEIGHT:
                dy *= -1

        win.blits([(bg_image, bg_image_rect),
                   (coin_image, coin_rect),
                   (score_text, score_text_rect),
                   (heart_image, heart_rect),
                   (lives_text, lives_text_rect),
                   (clown_image, clown_rect),
                   (catch_miss_text, catch_miss_text_rect)])
        
        cheats(show_cheats, clown_velocity, dx, dy)
        
        if game_over:
            show_cheats = False
            pygame.mixer.music.pause()
            heart_image = broken_heart_image
            catch_miss_text = font.render("", True, BLACK)
            win.blit(game_over_text, game_over_text_rect)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

main()