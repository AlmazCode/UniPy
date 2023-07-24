import pygame

class Console:
    def __init__(self, win, **args):
        self.win = win
        self.x = args.get("x", 0)
        self.y = args.get("y", 0)
        self.tY = 0
        self.tX = 0
        self.surface = pygame.Surface((args.get("width", win.get_width() // 1.5), args.get("height", win.get_height() // 1.5)))
        self.bg_color = args.get("bg_color", (60, 60, 60))
        self.stroke_color = tuple([max(25, min(225, item - 25)) for item in self.bg_color])
        self.logs_type = {
            "log": [args.get("logColor", (255, 255, 255)), args.get("logImg", None)],
            "warning": [args.get("warningColor", (255, 255, 0)), args.get("warningImg", None)],
            "error": [args.get("errorColor", (255, 0, 0)), args.get("errorImg", None)]
        }
        self.img_size = 64
        self.fontPath = args.get("font", None)
        self.render = True
        self.lastMousePos = None
        self.scrolling = args.get("scrolling", True)
        self.scrollSpeed = args.get("scrollSpeed", 1)
        self.ADP()
	
    def ADP(self):
        self.ww = self.surface.get_width() if self.surface.get_width() < self.surface.get_height() else self.surface.get_height()
        self.wh = self.surface.get_height()
        self.width, self.height = self.surface.get_size()
        for obj in self.logs_type:
            self.logs_type[obj][1] = pygame.transform.scale(self.logs_type[obj][1], (int(self.img_size * (self.ww / self.wh)), self.img_size))
        self.textes = []
        self.textes_type = []
        self.font_size = self.surface.get_height() // 20 if self.surface.get_width() <= 800 else self.surface.get_height() // 10
        self.font = pygame.font.Font(self.fontPath, self.font_size)
	
    def Log(self, text, _type, file=None, line=None):
        if _type not in self.logs_type:
            self.textes.append(f"Log: from script \"{file}\": line [{line}]\n{text}")
            self.textes_type.append("log")
        else:
            if _type == "log":
                self.textes.append(f"Log: from script \"{file}\": line [{line}]\n{text}")
            else:
                self.textes.append(str(text))
            self.textes_type.append(_type)
            
        if len(self.textes) > 100:
            self.textes.pop(0)
            self.textes_type.pop(0)

    def update(self, MP, MBP):
        if self.render:
            
            if MBP:
                if self.scrolling and self.lastMousePos:
                    scroll_amount = (MP[0] - self.lastMousePos[0], MP[1] - self.lastMousePos[1])
                    self.tX += scroll_amount[0] * self.scrollSpeed
                    self.tY += scroll_amount[1] * self.scrollSpeed
                    if self.tX > 0: self.tX = 0
                    if self.tY > 0: self.tY = 0
                self.lastMousePos = MP
            
            self.surface.fill(self.bg_color)
            y = 10
            for tx, tp in zip(self.textes, self.textes_type):
                color, img = self.logs_type[tp]
                self.surface.blit(img, (10 + self.tX, y + self.tY))
                for s in tx.split("\n"):
                    text = self.font.render(s, 0, color)
                    self.surface.blit(text, (img.get_width() + 30 + self.tX, y + self.tY + img.get_height() // 2 - text.get_height() // 2))
                    y += text.get_height()
                y += self.font_size
            pygame.draw.rect(self.surface, self.stroke_color, (0, 0, self.width, self.height), 5)
            self.win.blit(self.surface, (self.x, self.y))