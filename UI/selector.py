import pygame

class Selector:
    def __init__(self, win, func, **args):
        self.elements = args.get("elements", [])
        self.oY = 0
        self.lastY = -1
        self.x, self.y = args.get("x", 0), args.get("y", 0)
        self.text_color = args.get("text_color", [255, 255, 255])
        self.pressed_text_color = args.get("pressed_text_color", [255, 255, 255])
        self.stroke_color = args.get("stroke_color", [40, 40, 40])
        self.elem_stroke_color = args.get("elem_stroke_color", [70, 70, 70])
        self.pressed_elem_stroke_color = args.get("pressed_elem_stroke_color", [0, 114, 255])
        self.pressed_text_color = args.get("pressed_text_color", [255, 255, 255])
        self.color = args.get("color", [60, 60, 60])
        self.pressed_color = args.get("pressed_color", [60, 60, 60])
        self.elem_color = args.get("elem_color", [100, 100, 100])
        self.pressed_elem_color = args.get("pressed_elem_color", [30, 144, 255])
        self.font_path = args.get("fontPath", None)
        self.render = args.get("render", True)
        self.border_radius = args.get("border_radius", -1)
        self.elem_border_radius = args.get("elem_border_radius", -1)
        self.fill_size = args.get("fill_size", 0)
        self.elem_fill_size = args.get("elem_fill_size", 0)
        self.win = win
        self.func = func
        self.content = args.get("content", "()")
        self.elem_idx = -1
        self.last_elem = 0
        self.surface = pygame.Surface((args.get("width", win.get_width()), args.get("height", win.get_height())))
        self.lastMousePos = None
        self.scrolling = args.get("scrolling", True)
        self.scroll_speed = args.get("scroll_speed", 1)
        self.mouse_scroll_speed = args.get("mouse_scroll_speed", 5)
        self.centering = args.get("centering", "center")
        self.textCentering = args.get("text_centering", "left")
        self.elem_width_div = args.get("elem_width_div", 1)
        self.elem_height_div = args.get("elem_height_div", 10)
        self.stroke_size = args.get("stroke_size", 0)
        self.elem_stroke_size = args.get("elem_stroke_size", 0)
        self.text_offset = args.get("text_offset", 0)
        self.normalize()
    
    def normalize(self):
        self.elem_name = self.elements[:]
        self.elem_width = self.surface.get_width() // self.elem_width_div
        self.elem_height = self.surface.get_height() // self.elem_height_div
        self.surface.set_colorkey((1, 1, 1))
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
        
        self.ce = pygame.Surface((self.elem_width, self.elem_height))
        self.cpe = pygame.Surface((self.elem_width, self.elem_height))
        
        self.bg_surf = pygame.Surface(self.surface.get_size())
        self.bg_surf.fill((1, 1, 1))
        self.bg_surf.set_colorkey((1, 1, 1))
        pygame.draw.rect(self.bg_surf, self.color, (0, 0, *self.surface.get_size()), self.fill_size, self.border_radius)
        
        self.ce.fill((1, 1, 1))
        self.ce.set_colorkey((1, 1, 1))
        self.cpe.fill((1, 1, 1))
        self.cpe.set_colorkey((1, 1, 1))
            
        pygame.draw.rect(self.ce, self.elem_color, (0, 0, self.elem_width, self.elem_height), self.elem_fill_size, self.elem_border_radius)
        pygame.draw.rect(self.cpe, self.pressed_elem_color, (0, 0, self.elem_width, self.elem_height), self.elem_fill_size, self.elem_border_radius)
        
        if self.stroke_size > 0:
            pygame.draw.rect(self.bg_surf, self.stroke_color, (0, 0, *self.surface.get_size()), self.stroke_size, self.border_radius)
        
        if self.elem_stroke_size > 0:
            pygame.draw.rect(self.ce, self.elem_stroke_color, (0, 0, self.elem_width, self.elem_height), self.elem_stroke_size, self.elem_border_radius)
            pygame.draw.rect(self.cpe, self.pressed_elem_stroke_color, (0, 0, self.elem_width, self.elem_height), self.elem_stroke_size, self.elem_border_radius)
        
        if self.centering == "center":
            self.posX = self.ce.get_rect(centerx = self.surface.get_width() // 2)[0]
        elif self.centering == "right":
            self.posX = self.ce.get_rect(right = self.surface.get_width())[0] - 10
        else:
            self.posX = 10
    
    def get_idx_pos(self, idx):
        y = 10
        for idxx, i in enumerate(self.elem_name):
            if idxx == idx:
                return y + self.oY + self.y
            y += self.elem_height + 10
    
    def drag(self, bt, pos):
        if bt in [4, 5] and self.scrolling and self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(pos):
            if bt == 4:
                self.oY += self.mouse_scroll_speed
            else:
                self.oY -= self.mouse_scroll_speed
    
    def press(self, mPos):
        y = 10
        for idx, i in enumerate(self.elements):
            rect = pygame.Rect(self.x + self.posX, y + self.oY, self.elem_width, self.elem_height)
    
            if rect.collidepoint((mPos[0], mPos[1] - self.y)):
                if idx >= 0 and idx == self.elem_idx:
                    func = eval(f"self.func{self.content}")
                    self.elem_idx = -1
                else:
                    self.elem_idx = idx
                    self.ename = i
                return
            y += self.elem_height + 10
    
        if self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(mPos):
            self.elem_idx = -1
    
    def update(self, MP, MBP):
        if self.render:
            if self.scrolling and self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(MP) and MBP:
                if self.lastMousePos:
                    scroll_amount = MP[1] - self.lastMousePos[1]
                    self.oY += scroll_amount * self.scroll_speed
                self.lastMousePos = MP
            if self.oY > 0: self.oY = 0
            if abs(self.oY) > self.lastY:
                self.oY = -self.lastY
            
            self.surface.fill((1, 1, 1))
            self.surface.blit(self.bg_surf, (0, 0))
            y = 10
            for idx, i in enumerate(self.elem_name):
                self.surface.blit(self.ce if idx != self.elem_idx else self.cpe, (self.posX, y + self.oY))
                tx = self.font.render(i, 0, self.text_color if idx != self.elem_idx else self.pressed_text_color)
                yPos = tx.get_rect(centery= y + self.elem_height // 2)[1]
                if self.textCentering == "center":
                    xPos = tx.get_rect(centerx = self.posX + self.ce.get_width() // 2)[0]
                elif self.textCentering == "right":
                    xPos = tx.get_rect(right = self.surface.get_width())[0] - 20
                else:
                    xPos = self.posX + 10
                self.surface.blit(tx, (xPos + self.text_offset, yPos + self.oY))
                y += self.elem_height + 10
            if len(self.elements) > 0: self.lastY = y - self.elem_height - 20
            self.win.blit(self.surface, (self.x, self.y))