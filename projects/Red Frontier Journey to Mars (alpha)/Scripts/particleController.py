import random
import UniPy as up

class particleController:
    def __init__(self):
        ...
    
    def Start(self):
        self.this.rect.topleft = (random.randint(-200, up.wWidth + 200), random.randint(-200, up.wHeight + 200))