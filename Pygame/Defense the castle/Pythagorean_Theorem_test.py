import math, pygame
from config import *

pygame.init()

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Hypotenuse Theorem")
font = pygame.font.SysFont("terminal", 34)

def get_distance(rect1, rect2, ray):
    x1, y1 = rect1.topleft
    x1b, y1b = rect1.bottomright
    x2, y2 = rect2.topleft
    x2b, y2b = rect2.bottomright
    left = x2b < x1
    right = x1b < x2
    top = y2b < y1
    bottom = y1b < y2
    if bottom and left:
        if ray[0]: pygame.draw.line(WIN, (0, 255, 0), (x1, y1b), (x2b, y2), ray[1])
        return math.hypot(x2b-x1, y2-y1b)
    elif left and top:
        if ray[0]: pygame.draw.line(WIN, (0, 255, 0), (x1, y1), (x2b, y2b), ray[1])
        return math.hypot(x2b-x1, y2b-y1)
    elif top and right:
        if ray[0]: pygame.draw.line(WIN, (0, 255, 0), (x1b, y1), (x2, y2b), ray[1])
        return math.hypot(x2-x1b, y2b-y1)
    elif right and bottom:
        if ray[0]: pygame.draw.line(WIN, (0, 255, 0), (x1b, y1b), (x2, y2), ray[1])
        return math.hypot(x2-x1b, y2-y1b)
    elif left:
        if ray[0]: pygame.draw.line(WIN, (0, 255, 0), (x1, rect1.midleft[1]), (x2b, rect2.midright[1]), ray[1])
        return x1 - x2b
    elif right:
        if ray[0]: pygame.draw.line(WIN, (0, 255, 0), (x1b, rect1.midright[1]), (x2, rect2.midleft[1]), ray[1])
        return x2 - x1b
    elif top:
        if ray[0]: pygame.draw.line(WIN, (0, 255, 0), (rect1.midtop[0], y1), (rect2.midbottom[0], y2b), ray[1])
        return y1 - y2b
    elif bottom:
        if ray[0]: pygame.draw.line(WIN, (0, 255, 0), (rect1.midbottom[0], y1b), (rect2.midtop[0], y2), ray[1])
        return y2 - y1b
    else:
        return 0
    
def grid(grid_size):
    for col in range(WIN_WIDTH//grid_size+1):
       pygame.draw.line(WIN, (255, 255, 255), (col*grid_size, 0), (col*grid_size, WIN_WIDTH))
    for row in range(WIN_HEIGHT//grid_size):
        pygame.draw.line(WIN, (255, 255, 255), (0, row*grid_size), (WIN_WIDTH, row*grid_size))

def main():
    clock = pygame.time.Clock()
    ray = False
    ray_size = 3
    show_grid = False
    grid_size_list = [10, 20, 30, 40, 50, 100]
    grid_size = 0

    #red one
    rect1_x, rect1_y = 50, WIN_HEIGHT/2 - 25
    #blue one
    rect2_x, rect2_y = WIN_WIDTH - 100, WIN_HEIGHT/2 - 25

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    main()
                    quit()
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_g:
                    show_grid = not show_grid
                if show_grid:
                    if event.key == pygame.K_v:
                        grid_size = (grid_size - 1) % len(grid_size_list)
                    elif event.key == pygame.K_b:
                        grid_size = (grid_size + 1) % len(grid_size_list)
                if event.key == pygame.K_r:
                    ray = not ray
                if ray:
                    if event.key == pygame.K_e:
                        if ray_size > 1: ray_size -= 1
                    elif event.key == pygame.K_t:
                        if ray_size < 10: ray_size += 1

        WIN.fill((0, 0, 0))
        keys = pygame.key.get_pressed()

        #red one
        rect1 = pygame.draw.rect(WIN, (255, 0, 0), (rect1_x, rect1_y, 50, 50), 5)
        #blue one
        rect2 = pygame.draw.rect(WIN, (0, 0, 255), (rect2_x, rect2_y, 50, 50), 5)

        #rect1 movement
        if keys[pygame.K_w] and rect1.top > 0:
            rect1_y -= 1
        elif keys[pygame.K_s] and rect1.bottom < WIN_HEIGHT:
            rect1_y += 1
        if keys[pygame.K_a] and rect1.left > 0:
            rect1_x -= 1
        elif keys[pygame.K_d] and rect1.right < WIN_WIDTH:
            rect1_x += 1
        #rect2 movement
        if keys[pygame.K_UP] and rect2.top > 0:
            rect2_y -= 1
        elif keys[pygame.K_DOWN] and rect2.bottom < WIN_HEIGHT:
            rect2_y += 1
        if keys[pygame.K_LEFT] and rect2.left > 0:
            rect2_x -= 1
        elif keys[pygame.K_RIGHT] and rect2.right < WIN_WIDTH:
            rect2_x += 1

        (distance:=get_distance(rect1, rect2, (ray, ray_size)))

        distance_txt = font.render(f"Distance: {distance:.2f}", True, (255, 255, 255))
        distance_rect = distance_txt.get_rect(centerx=WIN_WIDTH/2, top=10)

        if show_grid:
            grid(grid_size_list[grid_size])

        WIN.blit(distance_txt, distance_rect)

        clock.tick(60)
        pygame.display.update()

    pygame.quit()

main()