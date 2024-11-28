import pygame
# Laser class for shooting mechanics
class Laser():
    def __init__(self, x, y):
        self.image = pygame.image.load("assets\\images\\bullet\\a1.png")
        self.rect = self.image.get_rect()
        self.rect_x = x
        self.rect_y = y
        self.speed = -0.1
        self.is_fired = False
        self.is_engaged = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect_y += self.speed
        if self.rect_y > 0 or self.is_engaged:
            self.die()


    def fire(self):
        self.is_fired = True

    def die(self):
        self.is_fired = False

    def engage(self):
        self.is_engaged = True
        self.die()




