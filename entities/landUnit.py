from entities.entity import Entity
from entities.waypoint import LandWaypoint
import pygame
import math

class LandUnit(Entity):
    def __init__(self, game, position, type, shortname, health, maxSpeed, image_path="assets/inf_image.png"):
        super().__init__(game, position)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (50, 40))
        self.rect = self.image.get_rect(center=position)
        self.type = type
        self.shortName = shortname
        self.health = health
        self.maxSpeed = maxSpeed
        self.speed = 0
        self.waypoints = []
    def moveLandUnit(self, dt, waypoint = None):
        targetWaypoint = waypoint if waypoint else (self.waypoints[0] if self.waypoints else None)
        if targetWaypoint:
            print(self.waypoints.index(targetWaypoint))
            print(self.waypoints)
            direction = (targetWaypoint.position - self.position).normalize()
            self.speed = self.maxSpeed # I need to add acceleration and deceleration later
            movement = direction * self.speed * dt
            self.position += movement
            self.rect.center = self.position
    def update(self, dt):
        if self.waypoints:
            self.moveLandUnit(dt)
            for point in self.waypoints[0].path:
                pointPos = pygame.Vector2(point)
                if math.dist(self.rect.center, pointPos) < 15:
                    self.waypoints[0].path.remove(point)
            if math.dist(self.rect.center, self.waypoints[0].rect.center) < 15:
                self.waypoints.pop(0)
                self.speed = 0
        else:
            pass
    def addWaypoint(self, position):
        if len(self.waypoints) < 10:
            clone = self.clone(self)
            #print("initial pos", self.position)
            if len(self.waypoints) > 0:
                clone.position = self.waypoints[-1].position
                #print("there is a waypoint")
            #print("end pos", self.position)
            waypoint = LandWaypoint(self.game, position, clone)
            self.waypoints.append(waypoint)
    def clearWaypoints(self):
        self.waypoints = []
        self.speed = 0 # has to be fixed later
    def clearLastWaypoint(self):
        if self.waypoints:
            self.waypoints.pop()
            self.speed = 0 # has to be fixed later
    def draw(self, screen, camera):
        adjusted_position = camera.apply(pygame.Vector2(self.rect.topleft))
        screen.blit(self.image, adjusted_position)
        if self.game.selected_entity == self:
            pygame.draw.rect(screen, (0, 255, 0), (*adjusted_position, self.rect.width, self.rect.height), 2)
            if hasattr(self, 'drawMenu') and callable(getattr(self, 'drawMenu')):
                self.drawMenu(screen, camera)
        lastWaypointPos = camera.apply(pygame.Vector2(self.rect.center))
        for waypoint in self.waypoints:
            adjusted_waypoint = camera.apply(pygame.Vector2(waypoint.rect.center))
            pygame.draw.line(screen, (0, 255, 0), lastWaypointPos, adjusted_waypoint, 2)
            lastWaypointPos = adjusted_waypoint
            pygame.draw.circle(screen, (0, 255, 0), adjusted_waypoint, 5)
        if self.waypoints:
            for i, waypoint in enumerate(self.waypoints):
                if self.waypoints[i].path and self.game.selected_entity == self:
                    for point in self.waypoints[i].path:
                        self.game.screen.blit(self.waypoints[i].image, camera.apply(pygame.Vector2(point)))
        pygame.draw.circle(screen, (255,255,255), (camera.apply(self.position)), 10)
    def clone(self, parent):
        c = LandUnit.__new__(LandUnit)
        c.game = parent.game
        c.position = pygame.Vector2(parent.position)
        c.type = parent.type
        c.shortName = parent.shortName
        c.health = parent.health
        c.maxSpeed = parent.maxSpeed
        c.speed = parent.speed
        c.rect = self.rect.copy()
        c.waypoints = []
        return c