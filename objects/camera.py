import pygame

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.target = None
        self.x = 0
        self.y = 0

    def apply(self, entity):
        if self.target is None:
            return entity.move(self.x, self.y)

        return entity.move(self.camera.x - self.target.rect.width // 2, self.camera.y - self.target.rect.height // 2)

    def update(self):
        if self.target is not None:
            x = -self.target.rect.x + self.width // 2 + self.x
            y = -self.target.rect.y + self.height // 2 + self.y

            self.camera.x += (x - self.camera.x) * 0.2
            self.camera.y += (y - self.camera.y) * 0.2

            self.camera.x = int(self.camera.x)
            self.camera.y = int(self.camera.y)