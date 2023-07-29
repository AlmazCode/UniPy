import UniPy as up
import random as rd

class logController:
    def __init__(self):
        self._speed = up.GetModule("gameController").moveSpeed
        self._delFunc = up.GetModule("gameController").onLogDeleted
    
    def Start(self):
        self.this.y = -self.this.height
        self.this.x = rd.randint(0, up.wWidth-self.this.width)
        self.gc = up.GetModule("gameController")
        self.this.AddAnim([5, 5], f"width = {self.this.width+25}; height = {self.this.height+25}")
        self.this.AddAnim([5, 5], f"width = {self.this.width}; height = {self.this.height}")
    
    def Update(self):
        if not self.gc.end:
            self.this.y += self._speed
            if self.this.rect.top > up.wHeight:
                self._delFunc()
                up.DelObj(self.this)