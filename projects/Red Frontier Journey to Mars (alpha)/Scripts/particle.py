import random
import UniPy as up

class particle:
    def __init__(self):
        self._dx = random.randint(-1, 1)
        self._timeToDeath = random.randint(10, 30)
        self._speed = random.randint(1, 5)
        self.obj = up.OBJ()
    
    def Start(self):
        size = random.randint(16, 48)
        self.this.width = size
        self.this.height = size
        self.this.y = self.obj.rect.bottom
        self.this.rect.centerx = self.obj.rect.centerx
        self.this.color = (225, random.randint(0, 255), 0)
        self.this.render = True
    
    def Update(self):
        if self._timeToDeath > 0:
            if self._dx == 0:self.this.rect.x += self._speed
            elif self._dx == 1:self.this.rect.x -= self._speed
            self.this.rect.y += self._speed
            self._timeToDeath -= 1
        else:
            up.DelObj(self.this)