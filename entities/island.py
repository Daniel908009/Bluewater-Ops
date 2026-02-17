from entities.entity import Entity

class Island(Entity):
    def __init__(self, game, position, islandType):
        super().__init__(game, position)
        self.type = islandType
        self.image = self.create_island_image(islandType)
        self.rect = self.image.get_rect(center=position)

    def create_island_image(self, islandType):
        pass