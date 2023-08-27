import UniPy as up

class block:
    def __init__(self):
        self.image = "grass"
        self.through = False
    
    def Setup(self):
        self.this.image = up.GetTexture(self.image)
        if self.through:
            self.this.bodyType = "None"