import pygame
import os

class Conductor:
    def __init__(self, win, func, **args):
        
        self.startPath = args.get("startPath", "/storage/emulated/0")
        self.thisPath = self.startPath
        self.elements = []
        self.elemName = []
        
        self.images = args.get("images", [])
        self.drawImages = []
        self.textes = []
        self.textesPos = []
        self.viewTextImage = []
        self.viewTextImagePos = []
        
        self.MT = [".mp3", ".ogg", ".wav", ".flac"]
        self.FT = [".ttf", ".otf"]
        self.IT = [".png", ".jpg", ".jpeg"]
        
        self.oY = 0
        self.lastY = -1
        self.x, self.y = args.get("x", 0), args.get("y", 0)
        
        self.tX = 0
        self.tY = 0
        
        self.textColor = args.get("textColor", (255, 255, 255))
        self.color = args.get("color", (60, 60, 60))
        self.elemColor = args.get("elemColor", (100, 100, 100))
        self.elemSelectedColor = args.get("elemSelectedColor", (0, 160, 255))
        
        self.fontPath = args.get("fontPath", None)  # путь до шрфита, если == None, будет использоваться стандартый
        self.fontSize = args.get("height", 500) // 20 # размер шрифта
        self.font = pygame.font.Font(self.fontPath, self.fontSize)   # шрифт

        self.render = args.get("render", True)
        self.borderRadius = args.get("borderRadius", -1)
        self.fillSize = args.get("fillSize", 0)

        self.win = win
        self.surface = pygame.Surface((args.get("width", 500), args.get("height", 500)))
        
        self.elemWidth = self.surface.get_width() - 20
        self.elemHeight = self.surface.get_height() // 12 if self.surface.get_width() <= self.surface.get_height() else self.surface.get_height() // 10
        
        self.func = func
        self.elemIdx = -1
        self.content = args.get("content", "")
        self.onlyView = args.get("onlyView", False)
        self.viewText = False
        
        idx = 0
        for i in self.images:
            self.images[idx] = pygame.transform.scale(i, (int(self.surface.get_height() * (self.elemHeight / self.surface.get_height())), int(self.elemHeight)))
            idx += 1
        
        self.setPath()
        self.compileText()
    
    def ADPIMG(self):
        self.drawImages = []
        
        for i in self.elements:
            if os.path.splitext(i)[-1] in self.MT: self.drawImages.append(self.images[2])
            elif os.path.splitext(i)[-1] in self.FT: self.drawImages.append(self.images[3])
            elif os.path.isdir(f"{self.thisPath}/{i}"): self.drawImages.append(self.images[0])
            elif os.path.splitext(i)[-1] in self.IT:
                img = pygame.image.load(f"{self.thisPath}/{i}").convert()
                if img.get_height() - 60 > img.get_width():
                    img = pygame.transform.scale(img, (int(self.surface.get_width() * (self.elemHeight / self.surface.get_height()) * 1.2) if self.surface.get_height() > self.surface.get_width() else int(self.surface.get_height() * (self.elemHeight / self.surface.get_width()) * 1.4), int(self.elemHeight)))
                elif img.get_height() + 60 < img.get_width():
                    img = pygame.transform.scale(img, (int(self.surface.get_height() * (self.elemHeight / self.surface.get_width())) if self.surface.get_height() > self.surface.get_width() else int(self.surface.get_width() * (self.elemHeight / self.surface.get_height())) , int(self.elemHeight)))
                else:
                    img = pygame.transform.scale(img, (int(self.elemHeight), int(self.elemHeight)))
                self.drawImages.append(img)
            else: self.drawImages.append(self.images[1])
    
    def setPath(self):
        self.thisPath = self.startPath
        self.elements = []
        self.elemName = []
        self.drawImages = []
        
        for i in os.listdir(self.startPath):
            self.elements.append(i)
            self.elemName.append(i)
            
        self.oY = 0
        self.lastY = -1
        self.elemIdx = -1
        
        self.ADPIMG()
        self.nrm()
        self.compileText()
    
    def nrm(self):
        idx = 0
        for i in self.elemName:
            text = self.font.render(i, 0, self.textColor)
            if self.drawImages[idx].get_width() + 20 + text.get_width() > self.surface.get_width() - 20:
                while 1:
                    text = self.font.render(self.elemName[idx], 0, self.textColor)
                    if self.drawImages[idx].get_width() + 20 + text.get_width() > self.surface.get_width() - 20:
                        self.elemName[idx] = self.elemName[idx][:-1]
                    else:
                        self.elemName[idx] = self.elemName[idx][:-3] + "..."
                        break
            idx += 1
    
    def Back(self):
        if self.viewText: self.viewText = False
        if self.thisPath != self.startPath:
            get = self.thisPath.split("/")
            self.thisPath = "/".join(get[0:-1])
            self.elemIdx = -1
            self.oY = 0
            self.lastY = -1
            self.elements = []
            self.elemName = []
            for i in os.listdir(self.thisPath):
                self.elements.append(i)
                self.elemName.append(i)
                                    
            self.ADPIMG()
            self.nrm()
            self.compileText()
    
    def getIdxPos(self, idx):
        y = 10
        idxx = 0
        for i in self.elemName:
            if idxx == idx:
                return y + self.oY + self.y
            idxx += 1
            y += self.elemHeight + 10
    
    def openText(self):
    	size = self.fontSize if self.surface.get_width() > self.surface.get_height() else self.fontSize // 2
    	font = pygame.font.Font(self.fontPath, size)
    	try:
    		f = open(self.thisPath, "r").read()
    	except:
    		get = self.thisPath.split("/")
    		self.thisPath = "/".join(get[0:-1])
    		return 0
    		
    	y = 0
    	f = f.replace("\t", "    ")
    	
    	self.viewTextImage = []
    	self.viewTextImagePos = []
    	self.viewText = True
    	self.elemIdx = -1
    	self.tX, self.tY = (0, 0)
    	
    	y = 10
    	for i in f.split("\n"):
    		tx = font.render(i, 0, self.textColor)
	    	tx.set_colorkey((0, 0, 0))
	    	self.viewTextImage.append(tx)
	    	self.viewTextImagePos.append((10, y))
    		y += size + 2
    
    def compileText(self):
        y = 10
        idx = 0
        self.textes = []
        self.textesPos = []
        for i in self.elements:
        	text = self.font.render(self.elemName[idx], 0, self.textColor)
        	textWin = text.get_rect(center = (0, y + self.elemHeight // 2))
        	self.textes.append(text)
        	self.textesPos.append(textWin)
        	y += self.elemHeight + 10
        	idx += 1
    
    def reOpenPath(self):
        self.elemIdx = -1
        self.oY = 0
        self.lastY = -1
        self.elements = []
        self.elemName = []

        try:
            for i in os.listdir(self.thisPath):
                self.elements.append(i)
                self.elemName.append(i)
            self.ADPIMG()
            self.nrm()
        except:
            self.Back()
        
        self.compileText()
    
    def Press(self):
        mPos = list(pygame.mouse.get_pos())
        mBT = pygame.mouse.get_pressed()
        
        if mBT[0] and not self.viewText:
            y = 10
            idx = 0
            c = 0
            for i in self.elements:
                rect = pygame.Rect(10, y + self.oY, self.elemWidth, self.elemHeight)
                
                if rect.collidepoint((mPos[0], mPos[1] - self.y)) and self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(mPos):
                    c += 1
                    if idx >= 0 and idx == self.elemIdx:
                        
                        if os.path.isdir(self.thisPath + f"/{i}"):
                            self.thisPath += f"/{i}"
                            self.reOpenPath()
                        elif len(os.path.splitext(self.thisPath + f"/{i}")) > 1 and self.onlyView:
                        	self.thisPath += f"/{i}"
                        	self.openText()
                        else:
                            if not self.onlyView:
                                self.elemIdx = -1
                                f = f"({self.content}, '{self.thisPath}/{i}')" if self.content != "" else f"('{self.thisPath}/{i}')"
                                eval(f"self.func{f}")
                    else:
                        self.elemIdx = idx
                    break
                y += self.elemHeight + 10
                idx += 1
            
            if c == 0 and self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(mPos):
                self.elemIdx = -1
    
    def update(self):
        if self.render:
            self.surface.fill(self.color)
            
            y = 10
            idx = 0
            
            if len(self.elements) == 0:
                txEmpty = self.font.render("Empty :(", 0, self.textColor)
                txPos = txEmpty.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2))
                self.surface.blit(txEmpty, txPos)
            
            idx = 0
            if self.viewText:
            	for img in self.viewTextImage:
	            	self.surface.blit(img, (self.viewTextImagePos[idx][0] + self.tX, self.viewTextImagePos[idx][1] + self.tY))
	            	idx += 1
            
            # draw elements
            if not self.viewText:
	            for i in self.elements:
	                rect = pygame.Rect(10, y + self.oY, self.elemWidth, self.elemHeight)
	                if rect.y + rect.height < self.surface.get_height() and rect.y + rect.height > 0:
	                    pygame.draw.rect(self.surface, self.elemColor if idx != self.elemIdx else self.elemSelectedColor, (10, y + self.oY, self.elemWidth, self.elemHeight), self.fillSize, self.borderRadius)
	                    
	                    self.surface.blit(self.textes[idx], (self.drawImages[idx].get_width() + 20, self.textesPos[idx][1] + self.oY))
	                    self.surface.blit(self.drawImages[idx], (10, y + self.oY))
	                
	                y += self.elemHeight + 10
	                idx += 1
	            
	            if self.lastY == -1:
	                self.lastY = y - self.elemHeight - 20
            
            self.win.blit(self.surface, (self.x, self.y))