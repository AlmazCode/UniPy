import pygame

class SOH_Manager():
    def __init__(self, win, func, **args):
        self.elements = args.get("elements", [])
        self.elemName = self.elements
            
        self.oY = 0
        self.lastY = -1
        self.key = args.get("key", "")
        
        self.x, self.y = args.get("x", 0), args.get("y", 0)
        
        self.textColor = args.get("textColor", (255, 255, 255))  # цвет текста
        self.color = args.get("color", (60, 60, 60))
        self.elemColor = args.get("elemColor", (100, 100, 100))
        self.elemSelectedColor = args.get("elemSelectedColor", (0, 160, 255))
        
        self.fontPath = args.get("fontPath", None)  # путь до шрфита, если == None, будет использоваться стандартый
        self.render = args.get("render", True)   # переменная, отвечающая за отрисовку input на экране, если == True, то input будет рисоваться, иначе нет.
        self.borderRadius = args.get("borderRadius", -1)   # уровень сглаживания углов у кнопки, если == -1, то сглаживание не будет
        self.fillSize = args.get("fillSize", 0)   # уровень заливки кнопки, если == 0, то будет заливаться полностью

        self.win = win # окно на котором будет рисоваться окно
        
        self.func = func
        self.content = args.get("content", "()")
        self.elemIdx = -1
        self.lastElem = 0
        self.surface = pygame.Surface((args.get("width", win.get_width()), args.get("height", win.get_height())))
        
        self.elemWidth = self.surface.get_width() // 1.5
        self.elemHeight = int(self.surface.get_height() // args.get("maxD", 15) if win.get_width() <= win.get_height() else self.surface.get_height() // args.get("minD", 10))
        
        self.fontSize = self.elemHeight // 3 # размер шрифта
        self.font = pygame.font.Font(self.fontPath, self.fontSize) # шрифт
        
        self.nrm()
    
    def nrm(self):
        idx = 0
        self.lastY = -1
        for i in self.elemName:
            text = self.font.render(i, 0, self.textColor)
            if text.get_width() > self.elemWidth:
                while 1:
                    text = self.font.render(self.elemName[idx], 0, self.textColor)
                    if text.get_width() > self.elemWidth:
                        self.elemName[idx] = self.elemName[idx][:-1]
                    else:
                        self.elemName[idx] = self.elemName[idx][:-4] + "..."
                        break
            idx += 1
    
    def Press(self, mPos):
    
        if 1:
            y = 10
            idx = 0
            c = 0
            for i in self.elements:
                rect = pygame.Rect(self.x + 10, y + self.oY, self.elemWidth, self.elemHeight)
    
                if rect.collidepoint((mPos[0], mPos[1] - self.y)):
                    c += 1
                    if idx >= 0 and idx == self.elemIdx:
                        func = eval(f"self.func{self.content}")
                        self.elemIdx = -1
                    else:
                        self.elemIdx = idx
                        self.lastElem = idx
                    break
                y += self.elemHeight + 10
                idx += 1
    
            if c == 0 and self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(mPos):
                self.elemIdx = -1
    
    def update(self):
        if self.render:
            
            self.surface.fill(self.color)

            idx = 0
            y = 10
            for i in self.elemName:
               rect = pygame.Rect(10, y + self.oY, self.elemWidth, self.elemHeight)
               if rect.y // 2 + rect.height // 2 < self.surface.get_height() and rect.y + rect.height > 0:
                   pygame.draw.rect(self.surface, self.elemColor if idx != self.elemIdx else self.elemSelectedColor, (10, y + self.oY, self.elemWidth, self.elemHeight), 0, self.borderRadius)
                   tx = self.font.render(i, 0, self.textColor)
                   txPos = tx.get_rect(center=(0, y + self.elemHeight // 2))
                   self.surface.blit(tx, (20, txPos[1] + self.oY))

               y += self.elemHeight + 10
               idx += 1
    
            if self.lastY == -1: self.lastY = y - self.elemHeight - 20
            
            self.win.blit(self.surface, (self.x, self.y))