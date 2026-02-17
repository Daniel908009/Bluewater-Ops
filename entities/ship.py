from entities.entity import Entity
from entities.waypoint import Waypoint
import pygame
import math

class Ship(Entity):
    def __init__(self, game, position, type = "Carrier", image_path = "assets/carrier_symbol.png", headingAngle=0, maxRotationSpeed=3,
                 optimalTurnSpeed=0.5, maximumSpeedForward=30, maximumSpeedBackward=-15,
                 ACCELERATION_STEP=1, FRICTION=0.05):
        super().__init__(game, position)
        self.type = type
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (75, 75))
        self.rect = self.image.get_rect(center=position)
        self.headingAngle = headingAngle
        self.maxRotationSpeed = maxRotationSpeed

        self.optimalTurnSpeed = optimalTurnSpeed

        self.speed = 0
        self.maximumSpeedForward = maximumSpeedForward
        self.maximumSpeedBackward = maximumSpeedBackward
        self.ACCELERATION_STEP = ACCELERATION_STEP
        self.targetSpeed = 0
        self.FRICTION = FRICTION

        self.waypoints = []
    
    def addWaypoint(self, position):
        if len(self.waypoints) < 10:
            last_position = self.rect.center
            if len(self.waypoints) > 0:
                last_position = self.waypoints[-1].rect.center
                last_angle = self.waypoints[-1].endingAngle
            copy_self = self.physics_copy()
            waypoint = Waypoint(self.game, copy_self, position, start_position=last_position, angle_start=last_angle if self.waypoints else None)
            if waypoint.isValid:
                self.waypoints.append(waypoint)
            else:
                self.game.throw_message(f"Cannot add waypoint at {position}, no valid path found.")
        else:
            self.game.throw_message(f"Maximum waypoint limit for {self.type} reached.")
    def clearWaypoints(self):
        self.waypoints = []
        self.speed = 0 # has to be fixed later
    def clearLastWaypoint(self):
        if self.waypoints:
            self.waypoints.pop()
            self.speed = 0 # has to be fixed later

    def update(self, dt):
        if self.waypoints:
            should_reverse = self.waypoints[0].shouldReverse
            self.moveShip(not should_reverse, dt)
            for point in self.waypoints[0].path:
                pointPos = pygame.Vector2(point)
                if math.dist(self.rect.center, pointPos) < 15: # this needs to be more complicated so that it doesnt miss. maybe something like y < pos and x < pos or something. for now its good enough
                    self.waypoints[0].path.remove(point)
            if math.dist(self.rect.center, self.waypoints[0].rect.center) < 15:
                self.waypoints.pop(0)
                self.speed = 0 # this has to be fixed but for now ill just set it to 0
        else:
            self.moveShip(None, dt)

    def moveShip(self, forward, dt, waypoint = None):
        if forward is None:
            if self.speed > 0:
                self.speed -= self.FRICTION
                if self.speed < 0:
                    self.speed = 0
            elif self.speed < 0:
                self.speed += self.FRICTION
                if self.speed > 0:
                    self.speed = 0
            direction_vec = pygame.Vector2(
                math.cos(math.radians(self.headingAngle) - math.pi / 2),
                math.sin(math.radians(self.headingAngle) - math.pi / 2)
            )
            applied_speed = self.speed * dt
            self.position += direction_vec * applied_speed
            self.rect.center = self.position
            return
        waypoint_pos = waypoint.rect.center if waypoint else self.waypoints[0].rect.center

        ship_heading_rad = self.headingAngle * (math.pi / 180)
        # start
        to_waypoint_vec = (waypoint_pos - self.position).normalize()
        desired_heading = math.degrees(math.atan2(to_waypoint_vec.y, to_waypoint_vec.x)) + 90
        desired_heading = desired_heading % 360
        if forward:
            smallerHeading = min(desired_heading, math.degrees(ship_heading_rad))
            largerHeading = max(desired_heading, math.degrees(ship_heading_rad))
            heading_diff = abs((largerHeading - smallerHeading + 180) % 360 - 180)
        else:
            smallerHeading = min(desired_heading, (math.degrees(ship_heading_rad) + 180) % 360)
            largerHeading = max(desired_heading, (math.degrees(ship_heading_rad) + 180) % 360)
            heading_diff = abs((largerHeading - smallerHeading + 180) % 360 - 180)
        #print("Desired heading:", desired_heading)
        #print("Current heading:", math.degrees(ship_heading_rad))
        #print("Heading diff:", heading_diff)
        if heading_diff < 0.1:
            heading_diff = 0
        if heading_diff != 0:
            #print("Adjusting heading...")
            self.targetSpeed = self.maximumSpeedForward * self.optimalTurnSpeed
            if not forward:
                self.targetSpeed = self.maximumSpeedBackward * self.optimalTurnSpeed
            '''if self.speed > 0:
                self.speed -= self.FRICTION
                if self.speed < 0:
                    self.speed = 0
            elif self.speed < 0:
                self.speed += self.FRICTION
                if self.speed > 0:
                    self.speed = 0
            '''
            #print("Speed after friction:", self.speed)
            if self.speed < self.targetSpeed and self.speed < self.maximumSpeedForward and forward:
                step = self.ACCELERATION_STEP if self.ACCELERATION_STEP + self.speed <= self.targetSpeed else self.targetSpeed - self.speed
                self.changeSpeed(step)
                #self.speed += self.ACCELERATION_STEP
            elif self.speed > self.targetSpeed and forward:
                pass
            elif self.speed < self.targetSpeed and self.speed < abs(self.maximumSpeedBackward) and not forward:
                pass
            elif self.speed > self.targetSpeed and not forward:
                step = self.ACCELERATION_STEP if self.speed - self.ACCELERATION_STEP >= self.targetSpeed else self.speed - self.targetSpeed
                self.changeSpeed(-step)
            if forward:
                speedRatio = abs(self.speed) / self.maximumSpeedForward
            else:
                speedRatio = abs(self.speed) / abs(self.maximumSpeedBackward)
            speedRatio = max(0, min(1, speedRatio))
            #print("Speed ratio:", speedRatio)
            turnFactor = speedRatio * (1 - speedRatio) * 4
            #turnFactor *= speedRatio
            ship_turning = self.maxRotationSpeed * turnFactor * dt # this needs more work
            #print("Turn factor:", turnFactor)
            #print("Ship turning this frame:", ship_turning)
            #print("speed " + str(self.speed))
            if heading_diff < ship_turning:
                ship_turning = heading_diff
            if forward:
                if ((desired_heading - math.degrees(ship_heading_rad) + 360) % 360) < 180:
                    #print("ship heading before turn:", math.degrees(ship_heading_rad))
                    ship_heading_rad += math.radians(ship_turning)
                    #print("ship heading after turn:", math.degrees(ship_heading_rad))
                else:
                    #print("ship turning: ", ship_turning)
                    #print("ship heading before turn:", math.degrees(ship_heading_rad))
                    ship_heading_rad -= math.radians(ship_turning)
                    #print("ship heading after turn:", math.degrees(ship_heading_rad))
            else:
                if ((desired_heading - (math.degrees(ship_heading_rad) + 180) + 360) % 360) < 180:
                    ship_heading_rad += math.radians(ship_turning)
                else:
                    ship_heading_rad -= math.radians(ship_turning)
        else:
            #print("Maintaining heading...")
            #print("ship heading in dgs:", math.degrees(ship_heading_rad))
            self.targetSpeed = self.maximumSpeedForward
            if not forward:
                self.targetSpeed = self.maximumSpeedBackward
            '''if self.speed > 0:
                self.speed -= self.FRICTION
                if self.speed < 0:
                    self.speed = 0
            elif self.speed < 0:
                self.speed += self.FRICTION
                if self.speed > 0:
                    self.speed = 0'''
            if self.speed < self.targetSpeed and self.speed < self.maximumSpeedForward and forward:
                step = self.ACCELERATION_STEP if self.ACCELERATION_STEP + self.speed <= self.targetSpeed else self.targetSpeed - self.speed
                self.changeSpeed(step)
            elif self.speed > self.targetSpeed and forward:
                pass
            elif self.speed > self.targetSpeed and self.speed < abs(self.maximumSpeedBackward) and not forward:
                step = self.ACCELERATION_STEP if self.speed - self.ACCELERATION_STEP >= self.targetSpeed else self.speed - self.targetSpeed
                self.changeSpeed(-step)
                #print("here")
            elif self.speed > self.targetSpeed and not forward:
                pass
        direction_vec = pygame.Vector2(
            math.cos(ship_heading_rad - math.pi / 2),
            math.sin(ship_heading_rad - math.pi / 2)
        )
        applied_speed = self.speed * dt
        self.position += direction_vec * applied_speed

        #self.position += pygame.Vector2(
        #    self.speed * math.cos(direction_angle),
        #    self.speed * math.sin(direction_angle)
        #)
        self.headingAngle = ship_heading_rad * (180 / math.pi) % 360
        self.rect.center = self.position
        #print(";;;;;;;;;;;;;;;;")
        #print("target angle:", desired_heading)
        #print("heading angle after moveShip:", self.headingAngle)
        #print("position after moveShip:", self.position)

    def physics_copy(self):
        c = Ship.__new__(Ship)
        c.game = self.game
        c.position = pygame.Vector2(self.position)
        c.rect = self.rect.copy()
        c.headingAngle = self.headingAngle
        c.maxRotationSpeed = self.maxRotationSpeed
        c.optimalTurnSpeed = self.optimalTurnSpeed
        c.speed = self.speed
        c.maximumSpeedForward = self.maximumSpeedForward
        c.maximumSpeedBackward = self.maximumSpeedBackward
        c.ACCELERATION_STEP = self.ACCELERATION_STEP
        c.FRICTION = self.FRICTION
        return c
    
    def changeSpeed(self, delta):
        self.speed += delta
        if self.speed > self.maximumSpeedForward:
            self.speed = self.maximumSpeedForward
        elif self.speed < self.maximumSpeedBackward:
            self.speed = self.maximumSpeedBackward
            
    def draw(self, screen, camera):
        pygame.draw.line(screen, (255, 0, 0), camera.apply(pygame.Vector2(self.rect.center)), camera.apply(pygame.Vector2(
            self.rect.centerx + 50 * math.cos(math.radians(self.headingAngle - 90)),
            self.rect.centery + 50 * math.sin(math.radians(self.headingAngle - 90))
        )), 2)
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