import UniPy as up

class gifAnim:
    def __init__(self):
        self.frames = ""
        self.speed = 10
        self.play = True
        self._thisTick = 0
        self._thisFrame = 0
        self._IMGS = []
    
    def Start(self):
        get = self.frames.split(",")
        self._IMGS = [up.GetTexture(img.strip()) for img in get]
    
    def Update(self):
        if self.play:
            if self._thisTick == self.speed:
                self._thisFrame += 1
                if self._thisFrame == len(self._IMGS) - 1:
                    self._thisFrame = 0
                self._thisTick = 0
                self.this.image = self._IMGS[self._thisFrame]
            else: self._thisTick += 1