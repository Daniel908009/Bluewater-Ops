from entities.entity import Entity
import pygame

class Ship(Entity):
    def __init__(self, game, position, type = "Carrier", image_path = "assets/carrier_symbol.png", headingAngle=0, maxRotationSpeed=3,
                 optimalTurnSpeed=0.5, maximumSpeedForward=20, maximumSpeedBackward=-15,
                 ACCELERATION_STEP=4, FRICTION=2):
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