import math
from entities.entity import Entity
import pygame

class Waypoint(Entity):
    def __init__(self, game, parent, position):
        super().__init__(game, position)
        self.type = "waypoint"
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 255, 0), (5, 5), 5)
        self.rect = self.image.get_rect(center=position)
        self.parent = parent
        self.isValid = True
        self.shouldReverse = False
        self.distance = self.calculate_route_distance(parent)
    def calculate_route_distance(self, parent):
        ship_pos = pygame.Vector2(parent.rect.center)
        waypoint_pos = pygame.Vector2(self.rect.center)
        
        ship_target_speed = pygame.Vector2(0, 0)

        ship_heading_rad = abs(math.radians(parent.headingAngle))
        ship_turning_rate = parent.maxRotationSpeed
        ship_optimal_turn_speed = parent.optimalTurnSpeed

        ship_max_speed = parent.maximumSpeedForward
        ship_max_speed_backward = parent.maximumSpeedBackward
        ship_speed = parent.speed
        ship_acceleration_step = parent.ACCELERATION_STEP
        ship_water_resistance = parent.FRICTION
        forwardLoopIterations = 0
        backwardLoopIterations = 0
        currentlyReversing = False
        maxLoopIterations = 10000
        control_points_forward = []
        control_points_backward = []
        looping = True
        loopingAllowed = {"forward": True, "backward": False}
        while looping:
            to_waypoint_vec = (waypoint_pos - ship_pos).normalize()
            desired_heading = math.degrees(math.atan2(to_waypoint_vec.y, to_waypoint_vec.x)) + 90
            #old_heading = math.degrees(ship_heading_rad)
            heading_diff = abs((desired_heading - math.degrees(ship_heading_rad) + 180) % 360 - 180)
            #print("heading diff:", heading_diff)
            #print("ship heading rad:", math.degrees(ship_heading_rad))
            #break
            if heading_diff != 0:
                ship_target_speed = ship_max_speed * ship_optimal_turn_speed
                if currentlyReversing:
                    ship_target_speed = ship_max_speed_backward * ship_optimal_turn_speed
                #print("ship target speed (turning):", ship_target_speed)
                ship_speed -= ship_water_resistance
                if ship_speed < ship_target_speed and ship_speed < ship_max_speed:
                    ship_speed += ship_acceleration_step
                elif ship_speed > ship_target_speed + ship_acceleration_step:
                    ship_speed -= ship_acceleration_step
                speedRatio = ship_speed / ship_max_speed
                speedRatio = max(0, min(1, speedRatio))
                turnFactor = speedRatio * (1 - speedRatio)
                ship_turning = ship_turning_rate * (1 + turnFactor)
                if heading_diff < ship_turning:
                    ship_turning = heading_diff
                #print("desired heading:", desired_heading)
                #print("current heading:", math.degrees(ship_heading_rad))
                #print("heading diff:", heading_diff)
                #print("ship turning rate:", ship_turning)
                #break
                if ((desired_heading - math.degrees(ship_heading_rad) + 360) % 360) < 180:
                    #print("turning right")
                    ship_heading_rad += math.radians(ship_turning)
                else:
                    #print("turning left")
                    ship_heading_rad -= math.radians(ship_turning)
                #else:
                    #ship_heading_rad -= math.radians(ship_turning)
                ship_pos += pygame.Vector2(
                    ship_speed * math.cos(ship_heading_rad - math.pi / 2),
                    ship_speed * math.sin(ship_heading_rad - math.pi / 2)
                )
                #print("/////////////////////////////////")
                #print("desired heading:", desired_heading)
                #print("current heading:", old_heading)
                #print("heading diff:", heading_diff)
                #print("turn factor:", turnFactor)
                #print("turning rate:", ship_turning)
                #print("ship speed:", ship_speed)
                #print("ship desired speed:", ship_target_speed)
                #print("total turning distance:", total_distance_traveled["turning_distance"])
                control_points_forward.append((ship_pos.x, ship_pos.y))
            else:
                ship_target_speed = ship_max_speed
                ship_speed -= ship_water_resistance
                if ship_speed < ship_target_speed and ship_speed < ship_max_speed:
                    ship_speed += ship_acceleration_step
                elif ship_speed > ship_target_speed:
                    pass
                ship_pos += pygame.Vector2(
                    ship_speed * math.cos(ship_heading_rad - math.pi / 2),
                    ship_speed * math.sin(ship_heading_rad - math.pi / 2)
                )
                control_points_forward.append((ship_pos.x, ship_pos.y))
            ship_heading_rad = ship_heading_rad % (2 * math.pi)
            if maxLoopIterations <= 0:
                #print("Max loop iterations reached in waypoint distance calculation.")
                if currentlyReversing:
                    loopingAllowed["backward"] = False
                else:
                    loopingAllowed["forward"] = False
            maxLoopIterations -= 1
            if currentlyReversing:
                backwardLoopIterations += 1
            else:
                forwardLoopIterations += 1
            currentlyLooping = loopingAllowed["backward"] if currentlyReversing else loopingAllowed["forward"]
            if ship_pos.distance_to(waypoint_pos) < 10 or not currentlyLooping:
                if currentlyReversing:
                    looping = False
                else:
                    currentlyReversing = True
                    ship_speed = 0
                    ship_heading_rad = math.radians(parent.headingAngle)
                    ship_pos = pygame.Vector2(parent.rect.center)
                    maxLoopIterations = 10000
        if backwardLoopIterations >= forwardLoopIterations:
            self.shouldReverse = False
        elif backwardLoopIterations < forwardLoopIterations:
            self.shouldReverse = True
        if loopingAllowed["backward"] == False and loopingAllowed["forward"] == False:
            self.isValid = False
            self.game.throw_message("Unable to calculate valid route to waypoint.")
        return control_points_forward if not self.shouldReverse else control_points_backward