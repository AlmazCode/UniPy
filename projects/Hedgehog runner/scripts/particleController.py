import UniPy as up
import random as rd

class particleController:
    def __init__(self):
        self._speed = up.GetModule("gameController").moveSpeed
    
    def Start(self):
        size = rd.randint(6, 18)
        self.this.width = size
        self.this.height = size
        self.this.y = rd.randint(-self.this.height - 250, -self.this.height)
        self.this.x = rd.randint(0, up.wWidth-self.this.width)
        self.gc = up.GetModule("gameController")
    
    def Update(self):
        if not self.gc.end:
            self.this.y += self._speed
            if self.this.rect.top > up.wHeight:
                up.DelObj(self.this)