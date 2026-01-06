import pygame

class Camera():
    def __init__(self, game):
        self.game = game
        self.offset = pygame.Vector2(100, 100)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            self.dragging = True
            self.last_mouse_pos = pygame.Vector2(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if getattr(self, 'dragging', False):
                mouse_pos = pygame.Vector2(event.pos)
                delta = mouse_pos - self.last_mouse_pos
                self.offset -= delta
                width, height = self.game.screen.get_size()
                if self.offset.x < 0:
                    self.offset.x = 0
                if self.offset.y < 0:
                    self.offset.y = 0
                if self.offset.x > self.game.world_width - width:
                    self.offset.x = self.game.world_width - width
                if self.offset.y > self.game.world_height - height:
                    self.offset.y = self.game.world_height - height
                self.last_mouse_pos = mouse_pos
    def apply(self, world_position):
        adjusted_position = world_position - self.offset
        return adjusted_position