

class Entity:
    """Base class for all entities"""
    def __init__(self, pos):
        self.x, self.y = pos
        self.velocity = [0, 0]