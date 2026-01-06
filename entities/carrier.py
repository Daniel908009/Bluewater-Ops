import pygame
from entities.entity import Entity
from entities.waypoint import Waypoint
import math

class Carrier(Entity):
    def __init__(self, game, position):
        super().__init__(game, position)
        self.type = "carrier"
        self.image = pygame.transform.scale(pygame.image.load("assets/carrier_symbol.png").convert_alpha(), (75, 75))
        self.rect = self.image.get_rect(center=position)
        self.headingAngle = 0
        self.maxRotationSpeed = 3

        self.optimalTurnSpeed = 0.5

        self.speed = 0
        self.maximumSpeedForward = 20
        self.maximumSpeedBackward = -5
        self.ACCELERATION_STEP = 4
        self.targetSpeed = 0
        self.FRICTION = 2

        self.waypoints = []
        #self.waypoints.append(Waypoint(self, game, (1000, 500)))
        self.addWaypoint((100, 500))
    def addWaypoint(self, position):
        if len(self.waypoints) < 1:
            waypoint = Waypoint(self.game, self, position)
            if waypoint.isValid:
                self.waypoints.append(waypoint)
            else:
                return
    def clearWaypoints(self):
        self.waypoints = []
    def update(self, dt):
        if self.waypoints:
            target = self.waypoints[0]
            if abs(self.rect.centerx - target.rect.centerx) < 10 and abs(self.rect.centery - target.rect.centery) < 10:
                self.waypoints[0].kill()
                self.waypoints.pop(0)

    def draw(self, screen, camera):
        pygame.draw.line(screen, (255, 0, 0), camera.apply(pygame.Vector2(self.rect.center)), camera.apply(pygame.Vector2(
            self.rect.centerx + 50 * math.cos(math.radians(self.headingAngle - 90)),
            self.rect.centery + 50 * math.sin(math.radians(self.headingAngle - 90))
        )), 2)
        adjusted_position = camera.apply(pygame.Vector2(self.rect.topleft))
        screen.blit(self.image, adjusted_position)
        if self.game.selected_entity == self:
            pygame.draw.rect(screen, (0, 255, 0), (*adjusted_position, self.rect.width, self.rect.height), 2)
        lastWaypointPos = camera.apply(pygame.Vector2(self.rect.center))
        for waypoint in self.waypoints:
            adjusted_waypoint = camera.apply(pygame.Vector2(waypoint.rect.center))
            pygame.draw.line(screen, (0, 255, 0), lastWaypointPos, adjusted_waypoint, 2)
            lastWaypointPos = adjusted_waypoint
            pygame.draw.circle(screen, (0, 255, 0), adjusted_waypoint, 5)
        # Draw control points for debugging
        if self.waypoints:
            if self.waypoints[0].distance and self.game.selected_entity == self:
                for point in self.waypoints[0].distance:
                    pygame.draw.circle(screen, (255, 0, 0), camera.apply(pygame.Vector2(point)), 3)
                    #print("Control point:", point)
        pygame.draw.circle(screen, (0, 0, 255), camera.apply(pygame.Vector2(self.rect.center)), 10, 1)