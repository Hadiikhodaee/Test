import random
from pygame.sprite import Sprite
from config import WIN_HEIGHT, WIN_WIDTH

class Monster(Sprite):
    def __init__(self, x, y, image, monster_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.monster_type = monster_type # 0=>blue,     1=> green,       2=> purple,     3 => yellow
        self.velocity = random.randint(1, 5)

        self.dx = random.choice([1, -1])
        self.dy = random.choice([1, -1])

    def movement(self):
        if self.rect.top <= 100 or self.rect.bottom >= WIN_HEIGHT - 100:
            self.dy *= -1
        if self.rect.left <= 0 or self.rect.right >= WIN_WIDTH:
            self.dx *= -1

        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def update(self):
        self.movement()