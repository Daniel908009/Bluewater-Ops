import pygame

class MainMenu:
    def __init__(self,game):
        self.game = game
        self.screen = game.screen
    def draw(self):
        pass
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
    def update(self, dt):
        pass

class GameUI:
    def __init__(self,game):
        self.game = game
        self.screen = game.screen
    def draw(self):
        width, height = self.game.screen.get_size()
        camera_position_text = f"Camera Position: ({int(self.game.camera.offset.x)}, {int(self.game.camera.offset.y)})"
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(camera_position_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))
        fps_text = f"FPS: {int(self.game.clock.get_fps())}"
        fps_text_render = font.render(fps_text, True, (255, 255, 255))
        self.screen.blit(fps_text_render, (10, 30))
        if self.game.selected_entity:
            entity_text = f"Selected Entity: {self.game.selected_entity.type} at {self.game.selected_entity.rect.topleft}"
            entity_text_render = font.render(entity_text, True, (255, 255, 255))
            self.screen.blit(entity_text_render, (10,  height - entity_text_render.get_height()*2 - 10))
            waypoints_text = f"Waypoints: {len(self.game.selected_entity.waypoints)}"
            waypoints_text_render = font.render(waypoints_text, True, (255, 255, 255))
            self.screen.blit(waypoints_text_render, (10, height - waypoints_text_render.get_height() - 10))
            entity_speed_text = f"Speed: {int(self.game.selected_entity.speed)}"
            entity_speed_text_render = font.render(entity_speed_text, True, (255, 255, 255))
            self.screen.blit(entity_speed_text_render, (200, height - entity_speed_text_render.get_height() - 10))
class PlanControlUI:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
    def draw(self):
        pass
    def handle_events(self):
        pass
    def update(self, dt):
        pass

class GameMessage:
    def __init__(self, game, text, duration):
        self.game = game
        self.text = text
        self.duration = duration
        self.startFading_time = duration - duration / 4
        self.elapsed_time = 0
        self.font = pygame.font.SysFont(None, 36)
        self.text_surface = self.font.render(self.text, True, (255, 255, 0))
    def update(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time >= self.duration:
            self.game.message = None
        if self.elapsed_time >= self.startFading_time:
            fade_ratio = (self.elapsed_time - self.startFading_time) / (self.duration - self.startFading_time)
            alpha = max(0, 255 * (1 - fade_ratio))
            self.text_surface.set_alpha(alpha)
    def draw(self):
        width, height = self.game.screen.get_size()
        self.game.screen.blit(self.text_surface, ((width - self.text_surface.get_width()) // 2, height // 8))