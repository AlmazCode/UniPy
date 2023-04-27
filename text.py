import pygame
import UniPy as pe
import settings as st

class Text:
    def __init__(self, surface: pygame.Surface, x: int, y: int, text: str, fs: int, font: str, color: tuple, tsp: int, a: int, r: int, fx: bool, fy: bool, cx: str, cy: str, sx: int, sy: int, sfs: int, tc: str):
        self.win = surface
        
        self.factor = min(surface.get_width() / st.projectSize[1], surface.get_height() / st.projectSize[0]) if surface.get_width() != st.projectSize[0] and surface.get_height() != st.projectSize[1] else 1
        
        self.x = int(sx * self.factor)
        self.y = int(sy * self.factor)
        self.oldX, self.oldY = x, y
        
        self._text = text
        self._fontSize = int(sfs * self.factor)
        self._sfs = sfs
        self.fontPath = font
        try:
            self._font = pygame.font.Font(font, self._fontSize) if font != "None" else pygame.font.Font(None, self.fontSize)
        except:
            self._font = pygame.font.Font(None, self._fontSize)
        GC = color.split(" ")
        self.color = (int(GC[0]), int(GC[1]), int(GC[2]))
        self.transparent = tsp
        
        self.flipX = False if fx == 0 else True
        self.flipY = False if fy == 0 else True
        
        self._sx = sx
        self._sy = sy
        
        self.cx = cx
        self.cy = cy
        
        self.textCentering = tc if tc in ["left", "center", "right"] else "left"
        
        self.render = True if r == 1 else False
        self.angle = a
        
        tx = self.font.render(self.text, 0, self.color)
        self.width, self.height = tx.get_width(), tx.get_height()
        
        self.posSetted = False
    
    def setPosObject(self):
        
        if self.cx[:4] == "objX" and self.cx[4] == "(" and self.cx[-1] == ")":
            if self.cx[5:-1] in pe.objName:
            	self.x = int(self._sx * self.factor)
            	self.x = pe.GetObj(self.cx[5:-1]).x + self.x
        
        if self.cy[:4] == "objY" and self.cy[4] == "(" and self.cy[-1] == ")":
            if self.cy[5:-1] in pe.objName:
            	self.y = int(self._sy * self.factor)
            	self.y = pe.GetObj(self.cy[5:-1]).y + self.y
    
    def setPos(self):
        tx = self.font.render(str(self.text).split("\\n")[0], 0, self.color)
        self.width, self.height = tx.get_width(), tx.get_height()
        
        if self.cx == "right": self.x = self.win.get_width() - self.width + self._sx
            
        elif self.cx == "centerx": self.x = self.win.get_width() // 2 - self.width // 2 + self._sx
            
        if self.cy == "bottom": self.y = self.win.get_height() - self.height + self._sy
        
        elif self.cy == "centery": self.y = self.win.get_height() // 2 - self.height  // 2 + self._sy
        
    @property
    def fontSize(self):
        return self._fontSize
    
    @property
    def font(self):
        return self._font
    
    @property
    def text(self):
        return self._text
    
    @property
    def sx(self):
        return self._sx
    @property
    def sy(self):
        return self._sy
    
    @property
    def sfs(self):
        return self._sfs
    
    @sx.setter
    def sx(self, value):
        self._sx = value
        self.x = int(self._sx * self.factor)
    
    @sy.setter
    def sy(self, value):
        self._sy = value
        self.y = int(self._sy * self.factor)
    
    @fontSize.setter
    def fontSize(self, value):
        self._fontSize = value
        self._font = pygame.font.Font(self.fontPath, self._fontSize) if self.fontPath != "None" else pygame.font.Font(None, self._fontSize)
        self.setPos()
        self.setPosObject()
    
    @sfs.setter
    def sfs(self, value):
        self._sfs = value
        self._fontSize = int(self._sfs * self.factor)
        self._font = pygame.font.Font(self.fontPath, self._fontSize) if self.fontPath != "None" else pygame.font.Font(None, self._fontSize)
    
    @font.setter
    def font(self, value):
        self._font = pygame.font.Font(value, self._fontSize)
        self.fontPath = value
        self.setPos()
        self.setPosObject()
    
    @text.setter
    def text(self, value):
        self._text = value
        self.setPos()
        self.setPosObject()
    
    def update(self):
        if self.render:
            y = 0
            firstText = self.font.render(str(self._text).split("\\n")[0], 0, self.color)
            for i in str(self._text).split("\\n"):
                text = self.font.render(i, 0, self.color)
                endText = text
                if self.angle != 0: endText = pygame.transform.rotate(endText, self.angle)
                endText = pygame.transform.flip(endText, self.flipX, self.flipY)
                if self.transparent != 255: endText.set_alpha(self.transparent)
                if self.textCentering == "center" and y != 0: pos = endText.get_rect(center=(self.x + firstText.get_width() // 2, 0))
                elif self.textCentering == "left": pos = (self.x, self.y)
                elif self.textCentering == "right": pos = endText.get_rect(right=self.x + firstText.get_width())
                else: pos = (self.x, self.y)
                
                self.win.blit(endText, (pos[0], self.y + y))
                y += text.get_height()
                lastText = endText