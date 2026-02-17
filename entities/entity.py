import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self,game, position):
        super().__init__()
        self.game = game
        self.position = pygame.Vector2(position)
    def update(self, dt):
        pass
    def draw(self, screen, camera):
        pass