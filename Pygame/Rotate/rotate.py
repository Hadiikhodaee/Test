import pygame
import random
import os
current_path = os.path.dirname(__file__)

pygame.init()

win_width, win_height = 400, 400

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Rotator")
pygame.display.set_icon(pygame.image.load(os.path.join(current_path, "knight.png")))

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("arial", 30)

class knight():
    def __init__(self, image_path, scale:tuple=(64,64)):
        self.image = pygame.transform.scale(pygame.image.load(image_path), scale)
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (win_width//2,win_height//2)
        self.angle = 0

    def draw(self):
        win.blit(self.image, self.rect)

        angle_text = font.render(f"Angle:{self.angle}", True, WHITE)
        angle_text_rect = angle_text.get_rect(topleft=(10, 10))

        win.blit(angle_text, angle_text_rect)

    def rotate(self, delay):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.angle -= 1
            if self.angle < -360:
                self.angle = 0
            pygame.time.delay(delay)
        if keys[pygame.K_a]:
            self.angle += 1
            if self.angle > 360:
                self.angle = 0
            pygame.time.delay(delay)

        if keys[pygame.K_r]:
            self.angle = 0

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_q]:
                    self.angle = random.randint(-360, 360)
                if pygame.key.get_pressed()[pygame.K_f]:
                    self.original_image = pygame.transform.flip(self.original_image, True, False)
                if pygame.key.get_pressed()[pygame.K_v]:
                    self.original_image = pygame.transform.flip(self.original_image, False, True)
                if pygame.key.get_pressed()[pygame.K_g]:
                    self.original_image = pygame.transform.flip(self.original_image, True, True)

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

def main():

    player = knight(os.path.join(current_path, "knight.png"))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill(BLACK)
        player.draw()
        player.rotate(2)
        pygame.display.update()

    pygame.quit()

main()