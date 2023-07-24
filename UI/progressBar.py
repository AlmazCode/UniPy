import pygame

class ProgressBar:
    def __init__(self, win, **args):
        
        self.win = win
        
        self.x = args.get("x", 0)
        self.y = args.get("y", 0)
        
        self.title = args.get("title", "")
        self.items = 0
        self.itemsLoaded = 0
        self.progerss = 0.0
        
        self.titleImg = None
        self.itemNameImg = None
        self.progressImg = None
        
        self.surface = pygame.Surface((args.get("width", win.get_width() // 1.5), args.get("height", win.get_height() // 1.5)))
        self.width, self.height = self.surface.get_size()
        
        self.borderRadius = args.get("borderRadius", 15)
        
        self.bgColor = args.get("bgColor", (80, 80, 80))
        self.strokeColor = tuple([max(25, min(225, item - 25)) for item in self.bgColor])
        self.textColor = args.get("textColor", (255, 255, 255))
        
        self.PBC = args.get("progressBarColor", (0, 255, 0))
        self.PBBC = args.get("progressBarBgColor", (140, 140, 140))
        
        self.fontPath = args.get("font", None)
        self.render = True
        self.ADP()
        self.start(self.title, 0)
    
    def ADP(self):
        self.SPBW = self.surface.get_width() // 1.5
        self.PBW = self.SPBW
        self.PBH = self.surface.get_height() // 10
        self.PBP = (self.surface.get_width() // 2 - self.PBW // 2, self.surface.get_height() - self.PBH - 10)
        self.fontSize = self.surface.get_height() // 10
        self.titleFontSize = self.surface.get_height() // 8
        self.font = pygame.font.Font(self.fontPath, self.fontSize)
        self.titleFont = pygame.font.Font(self.fontPath, self.titleFontSize)
    
    def setItemName(self, name: str):
        self.itemNameImg = self.font.render(name, 0, self.textColor)
        
        f = False
        
        while 1:
            if self.PBP[0] + self.itemNameImg.get_width() > self.surface.get_width():
                name = name[:-1]
                self.itemNameImg = self.font.render(name, 0, self.textColor)
                f = True
            else:
                if f:
                    name = name[:-3]
                    self.itemNameImg = self.font.render(name + "...", 0, self.textColor)
                break
    
    def start(self, title: str, items: int):
        self.title = title
        self.items = items
        self.itemsLoaded = 0
        self.progerss = 0.0
        
        self.titleImg = self.titleFont.render(title, 0, self.textColor)
        
        f = False
        
        while 1:
            if self.surface.get_width() // 2 - self.titleImg.get_width() // 2 + self.titleImg.get_width() > self.surface.get_width():
                title = title[:-1]
                self.titleImg = self.titleFont.render(title, 0, self.textColor)
                f = True
            else:
                if f:
                    title = title[:-3]
                    self.titleImg = self.titleFont.render(title + "...", 0, self.textColor)
                break
                
        self.progressImg = self.font.render("0%", 0, self.textColor)
        self.PBW = 0
        self.setItemName("")
    
    def itemLoaded(self):
        self.itemsLoaded += 1
        self.progress = self.itemsLoaded / self.items * 100
        self.PBW = int(self.SPBW * (self.progress / 100))
        self.progressImg = self.font.render(f"{self.progress:.1f}%", 0, self.textColor)
    
    def update(self):
        if self.render:
            self.surface.fill((1, 1, 1))
            
            pygame.draw.rect(self.surface, self.bgColor, (0, 0, self.width, self.height), 0, self.borderRadius)
            
            pygame.draw.rect(self.surface, self.PBBC, (self.PBP[0], self.PBP[1], self.SPBW, self.PBH))
            pygame.draw.rect(self.surface, self.PBC, (self.PBP[0], self.PBP[1], self.PBW, self.PBH))

            self.surface.blit(self.titleImg, (self.surface.get_width() // 2 - self.titleImg.get_width() // 2, 10))
            self.surface.blit(self.progressImg, (self.PBP[0], self.PBP[1] - self.progressImg.get_height() - 10))
            
            self.surface.blit(self.itemNameImg, (self.PBP[0], self.PBP[1] - self.progressImg.get_height() - 10 - self.itemNameImg.get_height() - 10))
            
            pygame.draw.rect(self.surface, self.strokeColor, (0, 0, self.width, self.height), 5, self.borderRadius)
            
            self.surface.set_colorkey((1, 1, 1))
            self.win.blit(self.surface, (self.x, self.y))