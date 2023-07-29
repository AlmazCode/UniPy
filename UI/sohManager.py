import pygame

class SOHManager:
    def __init__(self, win, func, **args):
        self.elements = args.get("elements", [])
        self.ce = []
        self.cpe = []
        self.oY = 0
        self.lastY = -1
        self.key = args.get("key", "")
        self.x, self.y = args.get("x", 0), args.get("y", 0)
        self.text_color = args.get("textColor", (255, 255, 255))
        self.color = args.get("color", (60, 60, 60))
        self.elem_color = args.get("elemColor", (100, 100, 100))
        self.elem_selected_color = args.get("elemSelectedColor", (0, 160, 255))
        self.font_path = args.get("fontPath", None)
        self.render = args.get("render", True)
        self.border_radius = args.get("borderRadius", -1)
        self.fill_size = args.get("fillSize", 0)
        self.win = win
        self.func = func
        self.content = args.get("content", "()")
        self.elem_idx = -1
        self.last_elem = 0
        self.maxD = args.get("maxD", 15)
        self.minD = args.get("minD", 10)
        self.surface = pygame.Surface((args.get("width", win.get_width()), args.get("height", win.get_height())))
        self.lastMousePos = None
        self.scrolling = args.get("scrolling", True)
        self.scrollSpeed = args.get("scrollSpeed", 1)
        self.normalize()
    
    def normalize(self):
        self.elem_name = self.elements[:]
        self.elem_width = self.surface.get_width() // 1.5
        self.elem_height = int(self.surface.get_height() // self.maxD if self.win.get_width() <= self.win.get_height() else self.surface.get_height() // self.minD)
        self.font_size = self.elem_height // 3
        self.font = pygame.font.Font(self.font_path, self.font_size)
        for idx, i in enumerate(self.elem_name):
            text = self.font.render(i, 0, self.text_color)
            if text.get_width() > self.elem_width:
                while True:
                    text = self.font.render(self.elem_name[idx], 0, self.text_color)
                    if text.get_width() > self.elem_width:
                        self.elem_name[idx] = self.elem_name[idx][:-1]
                    else:
                        self.elem_name[idx] = self.elem_name[idx][:-4] + "..."
                        break
        
        self.ce = [pygame.Surface((self.elem_width, self.elem_height))] * len(self.elements)
        self.cpe = [pygame.Surface((self.elem_width, self.elem_height))] * len(self.elements)
        
        for elem in self.ce:
            elem.fill((1, 1, 1))
            elem.set_colorkey((1, 1, 1))
            
            pygame.draw.rect(elem, self.elem_color, (0, 0, self.elem_width, self.elem_height), self.fill_size, self.border_radius)
        
        for elem in self.cpe:
            elem.fill((1, 1, 1))
            elem.set_colorkey((1, 1, 1))
            
            pygame.draw.rect(elem, self.elem_selected_color, (0, 0, self.elem_width, self.elem_height), self.fill_size, self.border_radius)
    
    def press(self, mPos):
        y = 10
        c = 0
        for idx, i in enumerate(self.elements):
            rect = pygame.Rect(self.x + 10, y + self.oY, self.elem_width, self.elem_height)
    
            if rect.collidepoint((mPos[0], mPos[1] - self.y)):
                c += 1
                if idx >= 0 and idx == self.elem_idx:
                    func = eval(f"self.func{self.content}")
                    self.elem_idx = -1
                else:
                    self.elem_idx = idx
                    self.last_elem = idx
                break
            y += self.elem_height + 10
    
        if c == 0 and self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(mPos):
            self.elem_idx = -1
    
    def update(self, MP, MBP):
        if self.render:
            
            if self.scrolling and self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(MP) and MBP:
                if self.lastMousePos:
                    scroll_amount = MP[1] - self.lastMousePos[1]
                    self.oY += scroll_amount * self.scrollSpeed
                    if self.oY > 0: self.oY = 0
                    if abs(self.oY) > self.lastY:
                        self.oY = -self.lastY
                self.lastMousePos = MP
            
            self.surface.fill(self.color)
            y = 10
            for idx, i in enumerate(self.elements):
               rect = pygame.Rect(10, y + self.oY, self.elem_width, self.elem_height)
               if rect.y // 2 + rect.height // 2 < self.surface.get_height() and rect.y + rect.height > 0:
                   self.surface.blit(self.ce[idx] if idx != self.elem_idx else self.cpe[idx], (10, y + self.oY))
                   tx = self.font.render(i, 0, self.text_color)
                   txPos = tx.get_rect(center=(0, y + self.elem_height // 2))
                   self.surface.blit(tx, (20, txPos[1] + self.oY))
               y += self.elem_height + 10
            if len(self.elements) > 0: self.lastY = y - self.elem_height - 20
            self.win.blit(self.surface, (self.x, self.y))