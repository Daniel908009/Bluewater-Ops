import pygame
from utilities.widgets import MainMenu, GameUI, GameMessage
from utilities.camera import Camera
from utilities.grid import Grid
from entities.carrier import Carrier

class Game:
    def __init__(self):
        self.running = True
        self.world_width = 5000
        self.world_height = 5000
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption("Bluewater Ops")
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.game_state = "playing"
        self.camera = Camera(self)
        self.grid = Grid(self)
        self.mainMenu = MainMenu(self)
        self.gameUI = GameUI(self)
        self.message = None
        self.selected_entity = None
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(Carrier(self, (500, 500)))
    def run(self):
        dt = self.clock.tick(60) / 1000
        while self.running:
            if self.game_state == "playing":
                self.draw()
                self.handle_events()
                self.update(dt)
                self.all_sprites.update(dt)
            elif self.game_state == "main_menu":
                self.mainMenu.draw()
                self.mainMenu.handle_events()
                self.mainMenu.update(dt)
            pygame.display.flip()
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.grid.draw()
        self.drawGroup(self.all_sprites)
        self.gameUI.draw()
        if self.message:
            self.message.draw()
        self.drawMouseCursor()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            self.camera.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #print("Left click at world position:", self.screen_to_world(pygame.mouse.get_pos()))
                    for sprite in self.all_sprites:
                        if sprite.rect.collidepoint(self.screen_to_world(pygame.mouse.get_pos())):
                            #print("Clicked on sprite:", sprite.type)
                            self.selected_entity = sprite
                        else:
                            self.selected_entity = None
                elif event.button == 3:
                    if self.selected_entity:
                        self.selected_entity.addWaypoint(self.screen_to_world(pygame.mouse.get_pos()))
            if event.type == pygame.KEYDOWN and self.game_state == "playing":
                if event.key == pygame.K_c:
                    if self.selected_entity:
                        self.selected_entity.clearWaypoints()
    def update(self, dt):
        if self.message:
            self.message.update(dt)
    def drawMouseCursor(self):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(self.screen, (255, 0, 0), mouse_pos, 5)
    def drawGroup(self, group):
        for sprite in group:
            sprite.draw(self.screen, self.camera)        
    def screen_to_world(self, screen_pos):
        return pygame.Vector2(screen_pos) + self.camera.offset
    def throw_message(self, text, duration=4):
        if self.message is None:
            self.message = GameMessage(self, text, duration)