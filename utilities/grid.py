import pygame

class Grid:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.game_camera = game.camera
        self.world_width = game.world_width
        self.world_height = game.world_height
    def draw(self):
        width, height = self.screen.get_size()
        offset = self.game_camera.offset
        cell_size = 50
        surface = pygame.Surface((min(width, self.world_width), min(height, self.world_height)), pygame.SRCALPHA)
        for x in range(0, self.world_width, cell_size):
            start_pos = (int(x - offset.x), int(0 - offset.y))
            end_pos = (int(x - offset.x), int(self.world_height - offset.y))
            pygame.draw.line(surface, (255, 255, 255, 25), start_pos, end_pos)
            if x - offset.x > width:
                break
        pygame.draw.line(surface, (255, 255, 255, 25), (int(0 - offset.x), int(self.world_height - offset.y)), (int(self.world_width - offset.x),  int(self.world_height - offset.y)))
        for y in range(0, self.world_height, cell_size):
            start_pos = (int(0 - offset.x), int(y - offset.y))
            end_pos = (int(self.world_width - offset.x), int(y - offset.y))
            pygame.draw.line(surface, (255, 255, 255, 25), start_pos, end_pos)
            if y - offset.y > height:
                break
        pygame.draw.line(surface, (255, 255, 255, 25), (int(self.world_width - offset.x), int(0 - offset.y)), (int(self.world_width - offset.x), int(self.world_height - offset.y)))
        self.screen.blit(surface, (0, 0))