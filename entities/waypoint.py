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
        loopingAllowed = {"forward": True, "backward": True}
        while looping:
            to_waypoint_vec = (waypoint_pos - ship_pos).normalize()
            desired_heading = math.degrees(math.atan2(to_waypoint_vec.y, to_waypoint_vec.x)) + 90
            desired_heading = desired_heading % 360
            #print("Desired heading:", desired_heading)
            #break
            #old_heading = math.degrees(ship_heading_rad)
            if not currentlyReversing:
                smallerHeading = min(desired_heading, math.degrees(ship_heading_rad))
                largerHeading = max(desired_heading, math.degrees(ship_heading_rad))
                heading_diff = abs((largerHeading - smallerHeading + 180) % 360 - 180)
                #print("--------------------------------")
                #print("Currently moving forward, desired heading:", desired_heading)
                #print("Currently moving forward, ship heading:", math.degrees(ship_heading_rad))
                #print("Heading diff (forward):", heading_diff)
            else:
                #break
                #print("--------------------------------")
                #print("Currently reversing, desired heading:", desired_heading)
                #print("Currently reversing, ship heading:", ship_heading_rad)
                #print("Currently reversing, current heading:", ship_heading_rad + math.pi)
                smallerHeading = min(desired_heading, (math.degrees(ship_heading_rad) + 180) % 360)
                largerHeading = max(desired_heading, (math.degrees(ship_heading_rad) + 180) % 360)
                heading_diff = abs((largerHeading - smallerHeading + 180) % 360 - 180)
                #print("Currently reversing, desired heading:", desired_heading)
                #print("Currently reversing, ship heading tail:", (math.degrees(ship_heading_rad) + 180) % 360)
                #print("Heading diff (reversing):", heading_diff)
                #break
            #if currentlyReversing:
                #print("Reversing turning waypoint...")
                #print("Desired heading:", desired_heading)
                #print("Current heading:", math.degrees(ship_heading_rad) + 180 % 360)
                #print("Heading diff:", heading_diff)
                #break
            #print("heading diff:", heading_diff)
            #print("ship heading rad:", math.degrees(ship_heading_rad))
            #break
            if heading_diff < 0.1:
                heading_diff = 0
                #if currentlyReversing:
                    #print("Heading aligned.")
            if heading_diff != 0:
                ship_target_speed = ship_max_speed * ship_optimal_turn_speed
                if currentlyReversing:
                    ship_target_speed = ship_max_speed_backward * ship_optimal_turn_speed
                #print("ship target speed (turning):", ship_target_speed)
                ship_speed -= ship_water_resistance
                if ship_speed < ship_target_speed and ship_speed < ship_max_speed and not currentlyReversing:
                    ship_speed += ship_acceleration_step
                elif ship_speed > ship_target_speed + ship_acceleration_step and not currentlyReversing:
                    ship_speed -= ship_acceleration_step
                
                elif ship_speed < ship_target_speed and ship_speed < abs(ship_max_speed_backward) and currentlyReversing:
                    ship_speed += ship_acceleration_step
                elif ship_speed > ship_target_speed + ship_acceleration_step and currentlyReversing:
                    ship_speed -= ship_acceleration_step
                
                if not currentlyReversing:
                    speedRatio = ship_speed / ship_max_speed
                else:
                    speedRatio = ship_speed / abs(ship_max_speed_backward)
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
                if not currentlyReversing:
                    if ((desired_heading - math.degrees(ship_heading_rad) + 360) % 360) < 180:
                        #print("turning right")
                        ship_heading_rad += math.radians(ship_turning)
                    else:
                        #print("turning left")
                        ship_heading_rad -= math.radians(ship_turning)
                else:
                    if ((desired_heading - (math.degrees(ship_heading_rad) + 180) + 360) % 360) < 180:
                        ship_heading_rad += math.radians(ship_turning)
                    else:
                        ship_heading_rad -= math.radians(ship_turning)
                #else:
                    #ship_heading_rad -= math.radians(ship_turning)
                if not currentlyReversing:
                    ship_pos += pygame.Vector2(
                        ship_speed * math.cos(ship_heading_rad - math.pi / 2),
                        ship_speed * math.sin(ship_heading_rad - math.pi / 2)
                    )
                else:
                    #modified_heading = ship_heading_rad + math.pi
                    #print("modified heading (reversing):", math.degrees(modified_heading))
                    #break
                    ship_pos += pygame.Vector2(
                        ship_speed * math.cos(ship_heading_rad  - math.pi / 2),
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
                if currentlyReversing:
                    control_points_backward.append((ship_pos.x, ship_pos.y))
                else:
                    control_points_forward.append((ship_pos.x, ship_pos.y))
            else:
                if currentlyReversing:
                    pass
                    #print("reversing towards waypoint...")
                #    print("target speed", ship_target_speed)
                ship_target_speed = ship_max_speed
                if currentlyReversing:
                    ship_target_speed = ship_max_speed_backward
                    #print("ship speed:", ship_speed)
                    #break
                ship_speed -= ship_water_resistance
                if ship_speed < ship_target_speed and ship_speed < ship_max_speed and not currentlyReversing:
                    ship_speed += ship_acceleration_step
                elif ship_speed > ship_target_speed and not currentlyReversing:
                    pass

                elif ship_speed < ship_target_speed and ship_speed < abs(ship_max_speed_backward) and currentlyReversing:
                    ship_speed += ship_acceleration_step
                elif ship_speed > ship_target_speed and currentlyReversing:
                    pass
                
                if not currentlyReversing:
                    ship_pos += pygame.Vector2(
                        ship_speed * math.cos(ship_heading_rad - math.pi / 2),
                        ship_speed * math.sin(ship_heading_rad - math.pi / 2)
                    )
                else:
                    #print("Reversing towards waypoint...")
                    #print("Ship speed:", ship_speed)
                    #print("Ship heading (deg):", math.degrees(ship_heading_rad))
                    #print("target speed:", ship_target_speed)
                    #modified_heading = ship_heading_rad + math.pi
                    ship_pos += pygame.Vector2(
                        ship_speed * math.cos(ship_heading_rad  - math.pi / 2),
                        ship_speed * math.sin(ship_heading_rad - math.pi / 2)
                    )
                if currentlyReversing:
                    control_points_backward.append((ship_pos.x, ship_pos.y))
                    #pass
                else:
                    control_points_forward.append((ship_pos.x, ship_pos.y))
                    #pass
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
            if ship_pos.distance_to(waypoint_pos) < 12 or not currentlyLooping:
                if currentlyReversing:
                    looping = False
                else:
                    currentlyReversing = True
                    ship_speed = 0
                    ship_heading_rad = math.radians(parent.headingAngle)
                    ship_pos = pygame.Vector2(parent.rect.center)
                    maxLoopIterations = 10000
        
        # disabled for testing
        #if backwardLoopIterations >= forwardLoopIterations:
        #    self.shouldReverse = False
        #elif backwardLoopIterations < forwardLoopIterations:
        #    self.shouldReverse = True
        
        if loopingAllowed["backward"] == False and loopingAllowed["forward"] == False:
            self.isValid = False
            self.game.throw_message("Unable to calculate valid route to waypoint.")
        control_points = [] # for testing
        if loopingAllowed["backward"] == True:
            for point in control_points_backward:
                control_points.append(point)
        if loopingAllowed["forward"] == True:
            for point in control_points_forward:
                control_points.append(point)
        #print("length backwards:", len(control_points_backward))
        #print("length forwards:", len(control_points_forward))
        return control_points