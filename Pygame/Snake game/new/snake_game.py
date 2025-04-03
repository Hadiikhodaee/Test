import pygame
import random

pygame.init()

screen_width = 600
screen_height = 400

white = (255, 255, 255)
neon_green = (57, 255, 20)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 51, 0)

window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Neon Snake Game")
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 35)
score_font = pygame.font.SysFont(None, 35)

try:
    with open("snake_high_score.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

def show_score(score, high_score):
    score -= 3
    if score < 0:
        score = 0
    value = score_font.render("Score: " + str(score), True, white)
    high_score_value = score_font.render("High Score: " + str(high_score), True, white)
    window.blit(value, [0, 0])
    window.blit(high_score_value, [screen_width - 185, 0])

def snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1:
            pygame.draw.rect(window, orange, [x[0], x[1], snake_block, snake_block])
        else:
            pygame.draw.rect(window, neon_green, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    window.blit(mesg, [screen_width / 6, screen_height / 3])

def game_loop():
    global high_score
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(10, screen_width - snake_block - 10) / 10.0) * 10.0
    foody = round(random.randrange(10, screen_height - snake_block- 10) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            window.fill(red)
            message("You Lost! Press Q-Quit or C-Play Again", white)
            show_score(length_of_snake - 1, high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y1_change = snake_block
                    x1_change = 0
                if len(snake_list) < 4:
                    length_of_snake = 4

        if x1 >= screen_width:
            x1 = 0 - snake_block
        elif x1 < 0:
            x1 = screen_width
        if y1 >= screen_height:
            y1 = 0 - snake_block
        elif y1 < 0:
            y1 = screen_height

        x1 += x1_change
        y1 += y1_change
        window.fill(black)
        pygame.draw.circle(window, red, [foodx, foody], snake_block // 2.5)

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        snake(snake_block, snake_list)
        show_score(length_of_snake - 1, high_score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            if length_of_snake - 4 > high_score:
                high_score = length_of_snake - 4
                with open("snake_high_score.txt", "w") as f:
                    f.write(str(high_score))

        clock.tick(snake_speed)

    pygame.quit()

game_loop()