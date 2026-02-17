from entities.landUnit import LandUnit
import pygame

class MarineCommando(LandUnit):
    def __init__(self, game, position):
        super().__init__(game, position, "Marine", shortname="MC", health= 100, maxSpeed=7)
        self.attack_power = 25
        self.attack_range = 60