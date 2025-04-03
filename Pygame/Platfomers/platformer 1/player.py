from config import WIN_HEIGHT, WIN_WIDTH, current_path, os
import pygame
vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, grass_tile_group, water_tile_group):
        super().__init__()
        self.move_right_sprites = []
        self.move_left_sprites = []

        self.idle_right_sprites = []
        self.idle_left_sprites = []

        for i in range(1, 9):
            self.move_right_sprites.append(pygame.transform.scale(pygame.image.load(os.path.join(current_path, "assets", "Boy", f"Run ({i}).png")), (72, 72)))
        for sprite in self.move_right_sprites:
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

        for i in range(1, 10):
            self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load(os.path.join(current_path, "assets", "Boy", f"Idle ({i}).png")), (72, 72)))
        for sprite in self.idle_right_sprites:
            self.idle_left_sprites.append(pygame.transform.flip(sprite, True, False))

        self.current_sprite = 0

        self.image = self.move_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        self.mask = pygame.mask.from_surface(self.image)

        self.grass_tile_group = grass_tile_group
        self.water_tile_group = water_tile_group

        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        self.HORIZONTAL_ACCLERATION = 2
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCLERATION = 0.5
        self.VERTICAL_JUMP_SPEED = 13

        self.jump_time = True

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]

    def update(self):
        self.acceleration = vector(0, self.VERTICAL_ACCLERATION)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.acceleration.x = -1 * self.HORIZONTAL_ACCLERATION
            self.animate(self.move_left_sprites, 0.2)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.acceleration.x = 1 * self.HORIZONTAL_ACCLERATION
            self.animate(self.move_right_sprites, 0.2)
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, 0.2)
            if self.velocity.x < 0:
                self.animate(self.idle_left_sprites, 0.2)

        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity
        self.rect.bottomleft = self.position

        self.check_collisions()

        if self.position.x < 0:
            self.position.x = WIN_WIDTH
        if self.position.x > WIN_WIDTH:
            self.position.x = 0

    def jump(self):
        if self.jump_time:
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED
            self.jump_time = False

        self.velocity += self.acceleration
        self.position += self.velocity

    def check_collisions(self):
        colided_platform_grasses = pygame.sprite.spritecollide(self, self.grass_tile_group, False, pygame.sprite.collide_mask)
        if colided_platform_grasses:
            self.position.y = colided_platform_grasses[0].rect.top + 8
            self.velocity.y = 0
            self.VERTICAL_JUMP_SPEED = 13
            self.jump_time = True

        colided_platform_waters = pygame.sprite.spritecollide(self, self.water_tile_group, False, pygame.sprite.collide_mask)
        if colided_platform_waters:
            self.position.y = colided_platform_waters[0].rect.top + 8
            self.VERTICAL_JUMP_SPEED = 4
            self.jump_time = True