import random
import UniPy as up

class stoneController:
    def __init__(self):
        ...
    
    def Start(self):
        if up.GetModule("gameController").endStartScene:
            self.this.render = True
            self.this.rect.topleft = (random.randint(-200, up.wWidth + 200), random.randint(-200, up.wHeight + 200))