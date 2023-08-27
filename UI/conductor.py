import pygame
import pather as pt
import os

class Conductor:
    def __init__(self, win, func, **args):
        
        self.startPath = args.get("startPath", pt._defaultPath)
        self.thisPath = self.startPath
        self.elements = []
        self.elem_name = []
        
        self.OI = args.get("images", [])
        self.MT = [".mp3", ".ogg", ".wav", ".flac"]
        self.FT = [".ttf", ".otf"]
        self.IT = [".png", ".jpg", ".jpeg"]
        
        self.oY = 0
        self.lastY = -1
        self.x, self.y = args.get("x", 0), args.get("y", 0)
        self.tX = 0
        self.tY = 0
        
        self.text_color = args.get("text_color", [255, 255, 255])
        self.pressed_text_color = args.get("pressed_text_color", [255, 255, 255])
        self.color = args.get("color", [60, 60, 60])
        self.elem_color = args.get("elem_color", [100, 100, 100])
        self.pressed_elem_color = args.get("pressed_elem_color", [30, 144, 255])
        self.elem_stroke_color = args.get("elem_stroke_color", [70, 70, 70])
        self.pressed_elem_stroke_color = args.get("pressed_elem_stroke_color", [0, 114, 255])
        self.font_path = args.get("font_path", None)
        self.code_font_path = args.get("code_font_path", None)
        self.render = args.get("render", True)
        self.border_radius = args.get("border_radius", -1)
        self.fill_size = args.get("fill_size", 0)
        self.elem_border_radius = args.get("elem_border_radius", 15)
        self.elem_fill_size = args.get("elem_fill_size", 0)
        self.elem_stroke_size = args.get("elem_stroke_size", 0)

        self.win = win
        self.surface = pygame.Surface((args.get("width", 500), args.get("height", 500)))
        self.func = func
        self.elem_idx = -1
        self.content = args.get("content", "")
        self.onlyView = args.get("onlyView", False)
        self.viewText = False
        
        self.code_bg_color = args.get("code_bg_color", [40, 44, 52])
        self.code_text_color = tuple([max(200, min(200, item - 55)) for item in self.text_color])
        self.line_bg_color = tuple([max(15, min(240, item - 15)) for item in self.code_bg_color])
        self.line_color = tuple([max(35, min(220, item + 35)) for item in self.line_bg_color])
        self.elem_offset_y = args.get("elem_offset_y", 10)
        self.lastMousePos = None
        self.scrolling = args.get("scrolling", True)
        self.scroll_speed = args.get("scroll_speed", 1)
        self.mouse_scroll_speed = args.get("mouse_scroll_speed", 5)
        
        self.ADP()
        self.setPath()
        self.compileText()
    
    def ADP(self):
        self.elem_width = self.surface.get_width() - 20
        self.elem_height = self.surface.get_height() // 12 if self.surface.get_width() <= self.surface.get_height() else self.surface.get_height() // 10
        self.font_size = self.surface.get_height() // 25
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.code_font_size = int(self.font_size // 1.1 if self.surface.get_width() > self.surface.get_height() else self.font_size // 2.2)
        self.code_font = pygame.font.Font(self.code_font_path, self.code_font_size)
        self.images = []
        for i in self.OI:
            self.images.append(pygame.transform.smoothscale(i, (int(self.surface.get_height() * (self.elem_height / self.surface.get_height())), int(self.elem_height))))
        
        self.ce = pygame.Surface((self.elem_width, self.elem_height))
        self.cpe = pygame.Surface((self.elem_width, self.elem_height))
        
        self.ce.fill((1, 1, 1))
        self.ce.set_colorkey((1, 1, 1))
        self.cpe.fill((1, 1, 1))
        self.cpe.set_colorkey((1, 1, 1))
            
        pygame.draw.rect(self.ce, self.elem_color, (0, 0, self.elem_width, self.elem_height), self.elem_fill_size, self.elem_border_radius)
        pygame.draw.rect(self.cpe, self.pressed_elem_color, (0, 0, self.elem_width, self.elem_height), self.elem_fill_size, self.elem_border_radius)
        
        if self.elem_stroke_size > 0:
            pygame.draw.rect(self.ce, self.elem_stroke_color, (0, 0, self.elem_width, self.elem_height), self.elem_stroke_size, self.elem_border_radius)
            pygame.draw.rect(self.cpe, self.pressed_elem_stroke_color, (0, 0, self.elem_width, self.elem_height), self.elem_stroke_size, self.elem_border_radius)
    
    def ADPIMG(self):
        self.drawImages = []

        for i in self.elements:
            if os.path.splitext(i)[-1] in self.MT:
                self.drawImages.append(self.images[2])
            elif os.path.splitext(i)[-1] in self.FT:
                self.drawImages.append(self.images[3])
            elif os.path.isdir(f"{self.thisPath}{pt.s}{i}"):
                self.drawImages.append(self.images[0])
            elif os.path.splitext(i)[-1] in self.IT:
                img = pygame.image.load(f"{self.thisPath}{pt.s}{i}").convert()
                if ((img.get_height() - img.get_width()) / img.get_width()) * 100 > 24:
                    img = pygame.transform.smoothscale(img, (int(self.surface.get_width() * (self.elem_height / self.surface.get_height())) if self.surface.get_height() > self.surface.get_width() else int(self.surface.get_height() * (self.elem_height / self.surface.get_width())), int(self.elem_height)))
                elif ((img.get_width() - img.get_height()) / img.get_height()) * 100 > 24:
                    img = pygame.transform.smoothscale(img, (int(self.surface.get_height() * (self.elem_height / self.surface.get_width())) if self.surface.get_height() > self.surface.get_width() else int(self.surface.get_width() * (self.elem_height / self.surface.get_height())) , int(self.elem_height)))
                else:
                    img = pygame.transform.smoothscale(img, (int(self.elem_height), int(self.elem_height)))
                self.drawImages.append(img)
            else:
                self.drawImages.append(self.images[1])
    
    def setPath(self, path: str = ""):
        self.thisPath = self.startPath if path == "" else path
        self.elements = []
        self.elem_name = []
        self.drawImages = []
        self.viewText = False
        
        for i in sorted(os.listdir(self.thisPath)):
            self.elements.append(i)
            self.elem_name.append(i)
            
        self.oY = 0
        self.elem_idx = -1
        
        self.ADPIMG()
        self.nrm()
        self.compileText()
    
    def nrm(self):
        for idx, i in enumerate(self.elem_name):
            text = self.font.render(i, 0, self.text_color)
            if self.drawImages[idx].get_width() + 20 + text.get_width() > self.surface.get_width() - 20:
                while 1:
                    text = self.font.render(self.elem_name[idx], 0, self.text_color)
                    if self.drawImages[idx].get_width() + 20 + text.get_width() > self.surface.get_width() - 20:
                        self.elem_name[idx] = self.elem_name[idx][:-1]
                    else:
                        self.elem_name[idx] = self.elem_name[idx][:-3] + "..."
                        break
    
    def Back(self):
        self.viewText = False
        if self.thisPath != self.startPath:
            get = self.thisPath.split(pt.s)
            self.thisPath = f"{pt.s}".join(get[0:-1])
            self.elem_idx = -1
            self.oY = 0
            self.lastY = -1
            self.elements = []
            self.elem_name = []
            
            for i in sorted(os.listdir(self.thisPath)):
                self.elements.append(i)
                self.elem_name.append(i)
                                    
            self.ADPIMG()
            self.nrm()
            self.compileText()
    
    def get_idx_pos(self, idx):
        y = self.pinf.get_height() + 20
        for idxx, i in enumerate(self.elem_name):
            if idxx == idx:
                return y + self.oY + self.y
            y += self.elem_height + self.elem_offset_y
    
    def openText(self):
        try:
            f = open(self.thisPath, "r").read()
        except:
            get = self.thisPath.split(pt.s)
            self.thisPath = pt.s.join(get[0:-1])
            return 0
        self.viewTextImage = []
        self.viewTextLineImage = []
        self.viewTextImagePos = []
        self.viewText = True
        self.elem_idx = -1
        self.tX, self.tY = (0, 0)
        
        code = f.replace("\t", "    ").split("\n")
        self.viewTextImage = [self.code_font.render(i, 0, self.code_text_color) for i in code]
        self.MLS = self.code_font.render(str(len(code)), 0, self.text_color).get_width()
                
        y = 10
        for idx in range(len(code)):
            line = self.code_font.render(str(idx+1), 0, self.line_color)
            self.viewTextLineImage.append(line)
            self.viewTextImagePos.append((self.MLS + 25, y))
            y += self.code_font_size + 2
    
    def compileText(self):
        inf = self.thisPath
        self.pinf = self.font.render(inf, 0, self.text_color)
        if 10 + self.pinf.get_width() > self.surface.get_width():
            while 1:
                self.pinf = self.font.render(inf, 0, self.text_color)
                if 10 + self.pinf.get_width() > self.surface.get_width():
                    inf = inf[1:]
                else:
                    inf = "..." + inf[3:]
                    self.pinf = self.font.render(inf, 0, self.text_color)
                    break
        
        y = self.pinf.get_height() + 20
        self.textes = []
        self.pressedTextes = []
        self.textesPos = []
        for idx, i in enumerate(self.elements):
            text = self.font.render(self.elem_name[idx], 0, self.text_color)
            text2 = self.font.render(self.elem_name[idx], 0, self.pressed_text_color)
            textWin = text.get_rect(center = (0, y + self.elem_height // 2))
            self.textes.append(text)
            self.pressedTextes.append(text2)
            self.textesPos.append(textWin)
            y += self.elem_height + self.elem_offset_y
    
    def reOpenPath(self):
        self.elem_idx = -1
        self.oY = 0
        self.elements = []
        self.elem_name = []

        try:
            for i in sorted(os.listdir(self.thisPath)):
                self.elements.append(i)
                self.elem_name.append(i)
            self.ADPIMG()
            self.nrm()
        except:
            self.Back()
        
        self.compileText()
    
    def drag(self, bt, pos):
        if bt in [4, 5] and self.scrolling and self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(pos):
            if not self.viewText:
                if bt == 4:
                    self.oY += self.mouse_scroll_speed
                else:
                    self.oY -= self.mouse_scroll_speed
            else:
                if bt == 4:
                    self.tY += self.mouse_scroll_speed
                else:
                    self.tY -= self.mouse_scroll_speed
    
    def Press(self, pos):
        if not self.viewText:
            y = self.pinf.get_height() + 20
            for idx, i in enumerate(self.elements):
                rect = pygame.Rect(10, y + self.oY, self.elem_width, self.elem_height)
                
                if rect.collidepoint((pos[0], pos[1] - self.y)) and self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(pos):
                    if idx >= 0 and idx == self.elem_idx:
                        if os.path.isdir(self.thisPath + f"{pt.s}{i}"):
                            self.thisPath += f"{pt.s}{i}"
                            self.reOpenPath()
                        elif os.path.isfile(self.thisPath + f"{pt.s}{i}") and self.onlyView:
                            self.thisPath += f"{pt.s}{i}"
                            self.openText()
                        else:
                            if not self.onlyView and self.func != None:
                                self.elem_idx = -1
                                c = f"({self.content}, '{self.thisPath}{pt.s}{i}')" if self.content != "" else f"('{self.thisPath}{pt.s}{i}')"
                                c = c.replace("\\", "\\\\")
                                eval(f"self.func{c}")
                    else:
                        self.elem_idx = idx
                    return
                y += self.elem_height + self.elem_offset_y
            
            if self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(pos):
                self.elem_idx = -1
    
    def update(self, MP, MBP):
        if self.render:
            self.surface.fill(self.color if not self.viewText else self.code_bg_color)
            if not self.viewText and self.scrolling and self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(MP) and MBP:
                if self.lastMousePos:
                    scroll_amount = MP[1] - self.lastMousePos[1]
                    self.oY += scroll_amount * self.scroll_speed
                self.lastMousePos = MP
            
            if self.oY > 0: self.oY = 0
            if abs(self.oY) > self.lastY:
                self.oY = -self.lastY
        
            if self.viewText and MBP:
                if self.lastMousePos:
                    scroll_amount = (MP[0] - self.lastMousePos[0], MP[1] - self.lastMousePos[1])
                    self.tX += scroll_amount[0] * self.scroll_speed
                    self.tY += scroll_amount[1] * self.scroll_speed
                self.lastMousePos = MP
                
            if self.tX > 0: self.tX = 0
            if self.tY > 0: self.tY = 0
            
            if len(self.elements) == 0:
                txEmpty = self.font.render("Empty", 0, self.textColor)
                txPos = txEmpty.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2))
                self.surface.blit(txEmpty, txPos)
            
            y = self.pinf.get_height() + 20
            if self.viewText:
                pygame.draw.rect(self.surface, self.line_bg_color, (0 + self.tX, 0, self.MLS + 10, self.surface.get_height()), 0, self.border_radius, border_top_right_radius=0)
                for idx, img in enumerate(self.viewTextImage):
                    self.surface.blit(img, (self.viewTextImagePos[idx][0] + self.tX, self.viewTextImagePos[idx][1] + self.tY))
                    pos = self.viewTextLineImage[idx].get_rect(centerx = self.MLS//2+5)
                    self.surface.blit(self.viewTextLineImage[idx], (pos[0] + self.tX, self.viewTextImagePos[idx][1] + self.tY))
            
            else:
                for idx in range(len(self.elements)):
                    rect = pygame.Rect(10, y + self.oY, self.elem_width, self.elem_height)
                    if rect.y + rect.height < self.surface.get_height() and rect.y + rect.height > 0:
                        self.surface.blit(self.ce if idx != self.elem_idx else self.cpe, (10, y + self.oY))
                        self.surface.blit(self.textes[idx] if idx != self.elem_idx else self.pressedTextes[idx], (self.drawImages[idx].get_width() + 20, self.textesPos[idx][1] + self.oY))
                        self.surface.blit(self.drawImages[idx], (10, y + self.oY))
                
                    y += self.elem_height + self.elem_offset_y
                    
                pygame.draw.rect(self.surface, (self.color), (0, 0, self.surface.get_width(), self.pinf.get_height() + 20))
                self.surface.blit(self.pinf, (10, 10))
	            
            if len(self.elements) > 0:
                self.lastY = y - self.elem_height - self.elem_offset_y - 20 - self.pinf.get_height()
            self.win.blit(self.surface, (self.x, self.y))