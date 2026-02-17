import pygame
from utilities.widgets import MainMenu, GameUI, GameMessage, PlanControlUI
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
        self.mouseImage = pygame.transform.scale(pygame.image.load("assets/cursor.png"), (32, 32))
        self.clock = pygame.time.Clock()
        self.game_state = "playing"
        self.camera = Camera(self)
        self.grid = Grid(self)
        self.mainMenu = MainMenu(self)
        self.gameUI = GameUI(self)
        self.planControlUI = None
        self.message = None
        self.selected_entity = None
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(Carrier(self, (1000, 1000)))
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            if self.game_state == "playing":
                self.draw()
                #for sprite in self.all_sprites:
                #    print(sprite)
                self.handle_events()
                #print(self.selected_entity)
                self.update(dt)
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
        if self.planControlUI:
            self.planControlUI.draw()
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
                    manuClicked = False
                    if self.selected_entity and hasattr(self.selected_entity, 'clicked'):
                        manuClicked = self.selected_entity.clicked(pygame.mouse.get_pos())
                        #print("manuClicked:", manuClicked)
                    if not manuClicked:
                        #print("checking selection")
                        for sprite in self.all_sprites:
                            if sprite.rect.collidepoint(self.screen_to_world(pygame.mouse.get_pos())):
                                self.selected_entity = sprite
                                return
                            else:
                                self.selected_entity = None
                elif event.button == 3:
                    if self.selected_entity:
                        self.selected_entity.addWaypoint(self.screen_to_world(pygame.mouse.get_pos()))
            if event.type == pygame.KEYDOWN and self.game_state == "playing":
                if self.selected_entity:
                    if event.key == pygame.K_c:
                        self.selected_entity.clearWaypoints()
                    if event.key == pygame.K_v:
                        self.selected_entity.clearLastWaypoint()
                else:
                    if event.key == pygame.K_TAB:
                        self.planControlUI = PlanControlUI(self)
    def update(self, dt):
        if self.message:
            self.message.update(dt)
        self.updateGroup(self.all_sprites, dt)
    def drawMouseCursor(self):
        mouse_pos = pygame.mouse.get_pos()
        self.screen.blit(self.mouseImage, (mouse_pos[0] - 16, mouse_pos[1] - 16))
    def drawGroup(self, group):
        for sprite in group:
            sprite.draw(self.screen, self.camera)
    def updateGroup(self, group, dt):
        for sprite in group:
            sprite.update(dt)        
    def screen_to_world(self, screen_pos):
        return pygame.Vector2(screen_pos) + self.camera.offset
    def throw_message(self, text, duration=4):
        if self.message is None:
            self.message = GameMessage(self, text, duration)