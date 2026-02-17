import math
from entities.entity import Entity
import pygame

class Waypoint(Entity): #ship waypoint
    def __init__(self, game, parent_copy, position, start_position=None, angle_start=None):
        super().__init__(game, position)
        self.type = "waypoint"
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (5, 5), 3)
        self.rect = self.image.get_rect(center=position)
        self.parent = parent_copy
        self.isValid = True
        self.shouldReverse = False
        self.endingPathAngles = {"reverse": None, "forward": None}
        self.endingAngle = None
        self.originalPosition = start_position if start_position else self.parent.position
        self.parent.position = pygame.Vector2(self.originalPosition)
        self.originalAngle = angle_start if angle_start is not None else self.parent.headingAngle
        self.parent.headingAngle = self.originalAngle
        self.maxLoopIterations = 10000
        self.path = self.getQuickerPath()
        #print(self.path)
    def getQuickerPath(self):
        backwardLoopIterations = 0
        forwardLoopIterations = 0
        loopingAllowed = {"forward": True, "backward": True}
        possible_paths = {"forward": [], "backward": []}
        dt = 0.1
        #print("Calculating forward path...")
        self.resetCalc()
        while True:
            #print(self.parent.position)
            #print(self.parent.rect.center)
            #print("angle:", self.parent.headingAngle)
            self.parent.moveShip(True, dt, waypoint = self)
            #print(self.parent.position)
            #print("angle:", self.parent.headingAngle)
            #print(self.parent.rect.center)
            #return []
            possible_paths["forward"].append((self.parent.position.x, self.parent.position.y))
            if math.dist(self.parent.position, self.rect.center) < 12:
                self.endingPathAngles["forward"] = self.parent.headingAngle
                break
            if self.maxLoopIterations <= 0:
                loopingAllowed["forward"] = False
                #print("breaking forward loop")
                break
            self.maxLoopIterations -= 1
            forwardLoopIterations += 1
        self.resetCalc()
        #return possible_paths["forward"]
        while True:
            self.parent.moveShip(False, dt, waypoint = self)
            possible_paths["backward"].append((self.parent.position.x, self.parent.position.y))
            if math.dist(self.parent.position, self.rect.center) < 12:
                self.endingPathAngles["reverse"] = self.parent.headingAngle
                break
            if self.maxLoopIterations <= 0:
                loopingAllowed["backward"] = False
                break
            self.maxLoopIterations -= 1
            backwardLoopIterations += 1
        #self.shouldReverse = True
        #return possible_paths["backward"]
        #return possible_paths["forward"]
        #print("Forward iterations:", forwardLoopIterations, "Backward iterations:", backwardLoopIterations)
        if backwardLoopIterations >= forwardLoopIterations:
            self.shouldReverse = False
            self.endingAngle = self.endingPathAngles["forward"]
        elif backwardLoopIterations < forwardLoopIterations:
            self.shouldReverse = True
            self.endingAngle = self.endingPathAngles["reverse"]
        if loopingAllowed["backward"] == False and loopingAllowed["forward"] == False:
            self.isValid = False
        #print("Chosen path:", "backward" if self.shouldReverse else "forward")
        chosen_path = possible_paths["backward"] if self.shouldReverse else possible_paths["forward"]
        for point in chosen_path:
            chosen_path[chosen_path.index(point)] = (point[0], point[1], True)
        for i in range(len(chosen_path)):
            if not chosen_path[i][2]:
                continue
            current_point = chosen_path[i]
            for j in range(len(chosen_path)):
                if i != j:
                    other_point = chosen_path[j]
                    if math.dist((current_point[0], current_point[1]), (other_point[0], other_point[1])) < 20:
                        chosen_path[j] = (other_point[0], other_point[1], False)
        final_chosen_path = []
        for point in chosen_path:
            if point[2]:
                final_chosen_path.append((point[0], point[1]))
        return final_chosen_path
    def resetCalc(self):
        self.maxLoopIterations = 10000
        self.parent.position = pygame.Vector2(self.originalPosition)
        self.parent.headingAngle = self.originalAngle
        self.parent.speed = 0

class LandWaypoint(Entity):
    def __init__(self, game, position, parentClone):
        super().__init__(game, position)
        self.type = "waypoint"
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (5, 5), 3)
        self.rect = self.image.get_rect(center=position)
        self.parent = parentClone
        self.path = self.getPath()
    def getPath(self):
        points = []
        dt = 0.1
        while True:
            self.parent.moveLandUnit(dt, waypoint = self)
            if math.dist(self.parent.position, self.rect.center) < 12:
                break
            points.append((self.parent.position.x, self.parent.position.y))
        #print(points)
        return points