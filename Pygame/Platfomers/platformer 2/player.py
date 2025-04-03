import pygame
from pygame.locals import *
from config import WIN_HEIGHT

class Player:
    def __init__(self, x, y):
        
        self.reset(x, y)

        self.coin_goten = 0
        self.livies = 5

    def reset(self, x, y):
        self.move_right_images = []
        self.move_left_images = []

        self.idle_right_images = []
        self.idle_left_images = []

        self.dead_image = pygame.image.load("assets/images/characters/ghost.png")
        self.dead_image.set_alpha(200)

        for i in range(1, 5):
            move_img = pygame.image.load(f"assets/images/characters/guy{i}.png")
            move_img_right = pygame.transform.scale(move_img, (40, 80))
            move_img_left = pygame.transform.flip(move_img_right, True, False)

            self.move_right_images.append(move_img_right)
            self.move_left_images.append(move_img_left)

        for i in range(1,2):
            idle_img = pygame.image.load(f"assets/images/characters/guy{i}.png")

            idle_img_right = pygame.transform.scale(idle_img, (40, 80))
            idle_img_left = pygame.transform.flip(idle_img_right, True, False)

            self.idle_right_images.append(idle_img_right)
            self.idle_left_images.append(idle_img_left)

        self.image = self.move_right_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vel_y = 0
        self.vel_x = 5
        self.jump_time = True
        self.jump_speed = 25

        self.current_image = 0

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.lava_dead_cd = 0

        self.get_coin_sound = pygame.mixer.Sound("assets/sounds/coin.wav")
        self.get_coin_sound.set_volume(0.3)
        self.game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.wav")
        self.jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav")
        self.jump_sound.set_volume(0.3)

    def animate(self, image_list, speed):
        if self.current_image < len(image_list) - 2:
            self.current_image += speed
        else:
            self.current_image = 0

        self.image = image_list[int(self.current_image)]

    def update(self, display_surface, tile_list, blob_group, coin_group, game_over, WIN_WIDTH):
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()

        if game_over == 0:

            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 0:
                dx -= self.vel_x
                self.animate(self.move_left_images, 0.1)
            elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < WIN_WIDTH:
                dx += self.vel_x
                self.animate(self.move_right_images, 0.1)
            else:
                if self.image in self.move_right_images:
                    self.animate(self.idle_right_images, 0.1)
                elif self.image in self.move_left_images:
                    self.animate(self.idle_left_images, 0.1)
                    
            self.vel_y += 1

            if self.vel_y > 10:
                self.vel_y = 10

            dy += self.vel_y

            for tile in tile_list:
                if tile[2] in [0, 1, 2]:
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                        elif self.vel_y >= 0:
                            dy = tile[1].top - self.rect.bottom
                            self.jump_time = True
                if tile[2] == 3:
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                        elif self.vel_y >= 0:
                            dy = tile[1].top - self.rect.bottom - 1
                            self.jump_time = True
                if tile[2] == 2:
                    if tile[1].colliderect(self.rect.x, self.rect.y + 5, self.width, self.height):
                        dx += tile[3].velocity * tile[3].delta
                if tile[2] in [1, 2, 3]:
                    if tile[1].colliderect(self.rect.x, self.rect.y + 5, self.width, self.height):
                        self.jump_speed = 25
                        self.vel_x = 5
                if tile[2] in [1, 2, 3]:
                    if tile[1].colliderect(self.rect.x, self.rect.y + 5, self.width, self.height):
                        if self.lava_dead_cd > 0:
                            self.lava_dead_cd -= 1
                if tile[2] in [4, 5]:
                    if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                        self.vel_y = 0.2
                        self.vel_x = 1
                        self.jump_time = True
                        self.lava_dead_cd += 1
                        if self.lava_dead_cd >= 60 * 3:
                            game_over = -1
                            self.game_over_sound.play(0)
                            self.lava_dead_cd = 0
                            self.livies -= 1
                if tile[2] in [7, 8]:
                    if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height) and keys[pygame.K_RETURN]:
                        game_over = 1
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                self.game_over_sound.play(0)
                self.livies -= 1
            if pygame.sprite.spritecollide(self, coin_group, True):
                self.get_coin_sound.play(0)
                self.coin_goten += 1

            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > WIN_HEIGHT:
                self.rect.bottom = WIN_HEIGHT
                dy = 0
                game_over = -1
                self.game_over_sound.play(0)
                self.livies -= 1

            if self.coin_goten == 20:
                self.livies += 1
                self.coin_goten = 0
            if self.livies == 0:
                game_over = -2

            font = pygame.font.SysFont("terminal", 32)

            self.coin_goten_text = font.render(f"X {self.coin_goten}", True, (255, 255, 255))
            self.coin_goten_text_rect = self.coin_goten_text.get_rect()
            self.coin_goten_text_rect.topright = (WIN_WIDTH - 5, 20)
            coin_goten_img = pygame.image.load("assets/images/platforms/coin.png")
            self.coin_goten_image = pygame.transform.scale(coin_goten_img, (20 ,20))
            self.coin_goten_image_rect = self.coin_goten_image.get_rect()
            self.coin_goten_image_rect.topright = (self.coin_goten_text_rect.midleft[0] - 10, self.coin_goten_text_rect.topleft[1])

            self.livies_text = font.render(f"X {self.livies}", True, (255, 255, 255))
            self.livies_text_rect = self.livies_text.get_rect()
            self.livies_text_rect.topleft = (30, 20)
            lives_img = pygame.image.load("assets/images/characters/guy1.png")
            self.lives_image = pygame.transform.scale(lives_img, (20 ,40))
            self.lives_image_rect = self.lives_image.get_rect()
            self.lives_image_rect.midright = (self.livies_text_rect.midleft[0] - 6, self.livies_text_rect.midleft[1] - 4)

        elif game_over == -1:
            self.image = self.dead_image
            self.vel_x = 5
            self.vel_y = 1.5
            self.fly_speed = 3

            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 0:
                self.rect.x -= self.vel_x
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT])and self.rect.right < WIN_WIDTH - 10:
                self.rect.x += self.vel_x
            if keys[pygame.K_SPACE] and self.rect.top > 3:
                self.rect.y -= self.fly_speed
            elif self.rect.bottom < WIN_HEIGHT + 30:
                self.rect.y += self.vel_y

        display_surface.blit(self.image, self.rect)

        display_surface.blit(self.coin_goten_image, self.coin_goten_image_rect)
        display_surface.blit(self.coin_goten_text, self.coin_goten_text_rect)
        display_surface.blit(self.lives_image, self.lives_image_rect)
        display_surface.blit(self.livies_text, self.livies_text_rect)

        return game_over

    def jump(self):
        if self.jump_time:
            self.vel_y -= self.jump_speed
            self.jump_time = False
            self.jump_sound.play(1)