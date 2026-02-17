from entities.marineCommando import MarineCommando
from entities.ship import Ship
import pygame

class Carrier(Ship):
    def __init__(self, game, position):
        super().__init__(game, position)
        self.addWaypoint((500, 500))
        self.landUnits = []
        self.airUnits = []
        self.landUnitsUnloading = []
        self.landUnitsTimer = 3
        self.airUnitsUnloading = []
        self.airUnitsTimer = 5
        self.capacityLand = 50
        self.capacityAir = 20
        for _ in range(5):
            self.landUnits.append(MarineCommando(game, (0, 0)))
    def update(self, dt):
        super().update(dt)
        self.unloadUnits(dt)
    def unloadUnits(self, dt):
        if self.landUnitsUnloading:
            self.landUnitsTimer -= dt
            if self.landUnitsTimer <= 0:
                if self.landUnitsUnloading:
                    unit = self.landUnitsUnloading.pop(0)
                    self.landUnits.remove(unit)
                    unit.position = pygame.Vector2(self.position.x + 60, self.position.y + 60)
                    unit.rect.center = (unit.position.x, unit.position.y)

                    unit.rect.center = unit.position
                    self.game.all_sprites.add(unit)
                self.landUnitsTimer = 10
        if self.airUnitsUnloading:
            self.airUnitsTimer -= dt
            if self.airUnitsTimer <= 0:
                if self.airUnitsUnloading:
                    unit = self.airUnitsUnloading.pop(0)
                    self.airUnits.remove(unit)
                    unit.position = pygame.Vector2(self.position.x + 60, self.position.y + 60)
                    unit.rect.topleft = (unit.position.x, unit.position.y)
                    self.game.all_sprites.add(unit)
                self.airUnitsTimer = 8
    def drawMenu(self, screen, camera):
        menu_x = self.game.screen.get_width() - 50
        length = len(self.landUnits) + len(self.airUnits)
        menu_y = screen.get_height() / 2 - (length * 25) / 2
        pygame.draw.rect(screen, (50, 50, 50), (menu_x, menu_y, 50, length * 25))
        font = pygame.font.SysFont(None, 24)
        for i, unit in enumerate(self.landUnits + self.airUnits):
            unit_text = f"{unit.shortName}"
            color = (255, 255, 255)
            if unit in self.landUnitsUnloading or unit in self.airUnitsUnloading:
                color = (0, 255, 0)
            text_surface = font.render(unit_text, True, color)
            screen.blit(text_surface, (menu_x + 10, menu_y + i * 25 + 5))
    def clicked(self, mouse_pos):
        #print("clicked position:", mouse_pos)
        menu_x = self.game.screen.get_width() - 50
        #print("menu_x:", self.game.screen.get_width() - 50)
        length = len(self.landUnits) + len(self.airUnits)
        menu_y = self.game.screen.get_height() / 2 - (length * 25) / 2
        clicked = False
        if menu_x <= mouse_pos[0] and mouse_pos[0] <= menu_x + 50:
            #print("within x")
            for i in range(length):
                if menu_y + i * 25 <= mouse_pos[1] <= menu_y + i * 25 + 25:
                    #print("within y")
                    unit = (self.landUnits + self.airUnits)[i]
                    if unit in self.landUnits:
                        if unit in self.landUnitsUnloading:
                            self.landUnitsUnloading.remove(unit)
                            #print("here land remove")
                        else:
                            self.landUnitsUnloading.append(unit)
                            #print("here land add")
                    else:
                        if unit in self.airUnitsUnloading:
                            self.airUnitsUnloading.remove(unit)
                            #print("here air remove")
                        else:
                            self.airUnitsUnloading.append(unit)
                            #print("here air add")
                    clicked = True
        return clicked