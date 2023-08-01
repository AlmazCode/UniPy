import pygame
import pather as pt
import os, re, tokenize

class Conductor:
    def __init__(self, win, func, **args):
        
        self.startPath = args.get("startPath", pt._defaultPath)
        self.thisPath = self.startPath
        self.elements = []
        self.elemName = []
        
        self.OI = args.get("images", [])
        self.drawImages = []
        self.textes = []
        self.textesPos = []
        self.viewTextImage = []
        self.viewTextLineImage = []
        self.viewTextImagePos = []
        self.MLS = 0
        
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
        
        self.fontPath = args.get("fontPath", None)
        self.codeFontPath = args.get("codeFontPath", None)

        self.render = args.get("render", True)
        self.borderRadius = args.get("borderRadius", -1)
        self.fillSize = args.get("fillSize", 0)

        self.win = win
        self.surface = pygame.Surface((args.get("width", 500), args.get("height", 500)))
        
        self.func = func
        self.elem_idx = -1
        self.content = args.get("content", "")
        self.onlyView = args.get("onlyView", False)
        self.viewText = False
    
        self.kColor = args.get("kColor", (177, 13, 201)) # keyword
        self.fColor = args.get("fColor", (0, 116, 217)) # funcs
        self.cColor = args.get("cColor", (170, 170, 170)) # comment
        self.sColor = args.get("sColor", (46, 204, 64)) # string
        self.nColor = args.get("nColor", (255, 165, 0)) # number
        self.CbgColor = args.get("CbgColor", (40, 44, 52)) # bg
        self.vColor = args.get("vColor", (231, 76, 60)) # var
        
        self.dColor = tuple([max(200, min(200, item - 55)) for item in self.textColor]) # default color
        
        self.lineBgColor = tuple([max(15, min(240, item - 15)) for item in self.CbgColor])
        
        self.LN = ""
        self.LS = ""
        self.LT = ""
        
        self.PYTHON_KEYWORDS = [
            'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
            'case', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally',
            'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
            'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
        ]
        
        self.SPECsyb = ["def", "class"]
        
        self.lastMousePos = None
        self.scrolling = args.get("scrolling", True)
        self.scrollSpeed = args.get("scrollSpeed", 1)
        
        self.ADP()
        self.setPath()
        self.compileText()
    
    def ADP(self):
        self.elemWidth = self.surface.get_width() - 20
        self.elemHeight = self.surface.get_height() // 12 if self.surface.get_width() <= self.surface.get_height() else self.surface.get_height() // 10
        self.fontSize = self.surface.get_height() // 25
        self.font = pygame.font.Font(self.fontPath, self.fontSize)
        self.images = []
        for i in self.OI:
            self.images.append(pygame.transform.scale(i, (int(self.surface.get_height() * (self.elemHeight / self.surface.get_height())), int(self.elemHeight))))
    
    def get_token_color(self, token_type, token_value):
    
        if token_type == tokenize.NAME and token_value in self.PYTHON_KEYWORDS: return self.kColor
        
        elif token_type == tokenize.COMMENT: return self.cColor
        
        elif token_type == tokenize.STRING: return self.sColor
        
        elif token_type == tokenize.NUMBER: return self.nColor
        
        elif self.LN in self.SPECsyb and token_type == tokenize.NAME:
            self.LN = ""
            return self.fColor
        
        elif self.LS == "." and token_type == tokenize.NAME:
            self.LS = ""
            return self.fColor
        
        elif token_type == tokenize.NAME: return self.vColor
    
        else: return self.dColor
    
    def tokenize_python_code(self, code, pyf):
        tokens = []
        prev_end_row = 0
        prev_end_col = 0
    
        for tok in tokenize.generate_tokens(code.splitlines(True).__iter__().__next__):
            token_type = tok.type
            token_value = tok.string.strip()
            start_row, start_col = tok.start
            end_row, end_col = tok.end
    
            if start_row != prev_end_row:
                # Handle newline token separately
                tokens.append(['\n', (255, 255, 255)])
                
            if token_value == "(" and self.LT == tokenize.NAME:
                tokens[-1][1] = self.fColor if pyf else self.dColor
            
            tokens.append([token_value, self.get_token_color(token_type, token_value) if pyf else self.dColor, token_type])
            if token_value in self.PYTHON_KEYWORDS: self.LN = token_value
            self.LS = token_value
            self.LT = token_type
    
            prev_end_row = end_row
            prev_end_col = end_col

        return tokens
    
    def ADPIMG(self):
        self.drawImages = []
        
        for i in self.elements:
            if os.path.splitext(i)[-1] in self.MT: self.drawImages.append(self.images[2])
            elif os.path.splitext(i)[-1] in self.FT: self.drawImages.append(self.images[3])
            elif os.path.isdir(f"{self.thisPath}{pt.s}{i}"): self.drawImages.append(self.images[0])
            elif os.path.splitext(i)[-1] in self.IT:
                img = pygame.image.load(f"{self.thisPath}{pt.s}{i}").convert()
                if ((img.get_height() - img.get_width()) / img.get_width()) * 100 > 24:
                    img = pygame.transform.scale(img, (int(self.surface.get_width() * (self.elemHeight / self.surface.get_height())) if self.surface.get_height() > self.surface.get_width() else int(self.surface.get_height() * (self.elemHeight / self.surface.get_width())), int(self.elemHeight)))
                elif ((img.get_width() - img.get_height()) / img.get_height()) * 100 > 24:
                    img = pygame.transform.scale(img, (int(self.surface.get_height() * (self.elemHeight / self.surface.get_width())) if self.surface.get_height() > self.surface.get_width() else int(self.surface.get_width() * (self.elemHeight / self.surface.get_height())) , int(self.elemHeight)))
                else:
                    img = pygame.transform.scale(img, (int(self.elemHeight), int(self.elemHeight)))
                self.drawImages.append(img)
            else: self.drawImages.append(self.images[1])
    
    def setPath(self, path: str = ""):
        self.thisPath = self.startPath if path == "" else path
        self.elements = []
        self.elemName = []
        self.drawImages = []
        self.viewText = False
        
        for i in sorted(os.listdir(self.thisPath)):
            self.elements.append(i)
            self.elemName.append(i)
            
        self.oY = 0
        self.elem_idx = -1
        
        self.ADPIMG()
        self.nrm()
        self.compileText()
    
    def nrm(self):
        for idx, i in enumerate(self.elemName):
            text = self.font.render(i, 0, self.textColor)
            if self.drawImages[idx].get_width() + 20 + text.get_width() > self.surface.get_width() - 20:
                while 1:
                    text = self.font.render(self.elemName[idx], 0, self.textColor)
                    if self.drawImages[idx].get_width() + 20 + text.get_width() > self.surface.get_width() - 20:
                        self.elemName[idx] = self.elemName[idx][:-1]
                    else:
                        self.elemName[idx] = self.elemName[idx][:-3] + "..."
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
            self.elemName = []
            
            for i in sorted(os.listdir(self.thisPath)):
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
    
    def is_inside_code(self, line, pos):
        syb = ""
        for s in line[:pos]:
            if s == "\"" or s == '\'':
                syb = s
                break
        
        else: return False

        for s in line[pos+1:]:
            if s == syb: return True
        
        return False
    
    def openText(self):
        size = self.fontSize // 1.1 if self.surface.get_width() > self.surface.get_height() else self.fontSize // 2.2
        font = pygame.font.Font(self.codeFontPath, int(size))
        try: f = open(self.thisPath, "r").read()
        except:
            get = self.thisPath.split(pt.s)
            self.thisPath = f"{pt.s}".join(get[0:-1])
            return 0
        
        y = 0
        
        self.viewTextImage = []
        self.viewTextLineImage = []
        self.viewTextImagePos = []
        self.viewText = True
        self.elem_idx = -1
        self.tX, self.tY = (0, 0)
        
        lineColor = tuple([max(35, min(220, item + 35)) for item in self.lineBgColor])
        self.MLS = font.render(str(len(f.split("\n"))), 0, self.textColor).get_width()
        
        code = f.replace("\t", "    ")
        code = code.replace(" ", "♡")
        
        text = []
        tokens = self.tokenize_python_code(code, True if self.thisPath.split(".")[-1] == "py" else False)
        for i in tokens[1:-1]: text.append([i[0], i[1]])
                
        for i in text: i[0] = i[0].replace("♡", " ")
        x = 0
        SIZE = list(font.size("".join([i[0] for i in text]).split("\n")[0]))
        _surf = pygame.Surface((SIZE[0] + 10, SIZE[1]))
        _surf.fill((1, 1, 1))
            
        idx = 0
        for i in text:
            for j in i[0]:
                if j == "\n":
                    idx += 1
                    _surf.set_colorkey((1, 1, 1))
                    self.viewTextImage.append(_surf)
                    x = 0
                    SIZE = list(font.size("".join([i[0] for i in text]).split("\n")[idx]))
                    _surf = pygame.Surface((SIZE[0] + 10, SIZE[1]))
                    _surf.fill((1, 1, 1))
                    continue
                
                tx = font.render(j, 0, i[1])
                _surf.blit(tx, (x, 0))
                x += tx.get_width()
                
        y = 10
        for idx, i in enumerate(f.split("\n")):
            line = font.render(str(idx+1), 0, lineColor)
            self.viewTextLineImage.append(line)
            self.viewTextImagePos.append((self.MLS + 25, y))
            y += size + 2
    
    def compileText(self):
        y = 10
        self.textes = []
        self.textesPos = []
        for idx, i in enumerate(self.elements):
        	text = self.font.render(self.elemName[idx], 0, self.textColor)
        	textWin = text.get_rect(center = (0, y + self.elemHeight // 2))
        	self.textes.append(text)
        	self.textesPos.append(textWin)
        	y += self.elemHeight + 10
    
    def reOpenPath(self):
        self.elem_idx = -1
        self.oY = 0
        self.elements = []
        self.elemName = []

        try:
            for i in sorted(os.listdir(self.thisPath)):
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
            c = 0
            for idx, i in enumerate(self.elements):
                rect = pygame.Rect(10, y + self.oY, self.elemWidth, self.elemHeight)
                
                if rect.collidepoint((mPos[0], mPos[1] - self.y)) and self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(mPos):
                    c += 1
                    if idx >= 0 and idx == self.elem_idx:
                        
                        if os.path.isdir(self.thisPath + f"{pt.s}{i}"):
                            self.thisPath += f"{pt.s}{i}"
                            self.reOpenPath()
                        elif len(os.path.splitext(self.thisPath + f"{pt.s}{i}")) > 1 and self.onlyView:
                        	self.thisPath += f"{pt.s}{i}"
                        	self.openText()
                        else:
                            if not self.onlyView and self.func != None:
                                self.elem_idx = -1
                                f = f"({self.content}, '{self.thisPath}{pt.s}{i}')" if self.content != "" else f"('{self.thisPath}{pt.s}{i}')"
                                eval(f"self.func{f}")
                    else:
                        self.elem_idx = idx
                    break
                y += self.elemHeight + 10
            
            if c == 0 and self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(mPos):
                self.elem_idx = -1
    
    def update(self, MP, MBP):
        if self.render:
            
            if not self.viewText and self.scrolling and self.surface.get_rect(bottomleft=(self.x, self.y + self.surface.get_height())).collidepoint(MP) and MBP:
                if self.lastMousePos:
                    scroll_amount = MP[1] - self.lastMousePos[1]
                    self.oY += scroll_amount * self.scrollSpeed
                    if self.oY > 0: self.oY = 0
                    if abs(self.oY) > self.lastY:
                        self.oY = -self.lastY
                self.lastMousePos = MP
        
            if self.viewText and MBP:
                if self.lastMousePos:
                    scroll_amount = (MP[0] - self.lastMousePos[0], MP[1] - self.lastMousePos[1])
                    self.tX += scroll_amount[0] * self.scrollSpeed
                    self.tY += scroll_amount[1] * self.scrollSpeed
                    if self.tX > 0: self.tX = 0
                    if self.tY > 0: self.tY = 0
                self.lastMousePos = MP
            
            self.surface.fill(self.color if not self.viewText else self.CbgColor)
            
            if len(self.elements) == 0:
                txEmpty = self.font.render("Empty :(", 0, self.textColor)
                txPos = txEmpty.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2))
                self.surface.blit(txEmpty, txPos)
            
            y = 10
            if self.viewText:
            	pygame.draw.rect(self.surface, self.lineBgColor, (0 + self.tX, 0, self.MLS + 10, self.surface.get_height()))
            	for idx, img in enumerate(self.viewTextImage):
	            	self.surface.blit(img, (self.viewTextImagePos[idx][0] + self.tX, self.viewTextImagePos[idx][1] + self.tY))
	            	pos = self.viewTextLineImage[idx].get_rect(centerx = self.MLS//2+5)
	            	self.surface.blit(self.viewTextLineImage[idx], (pos[0] + self.tX, self.viewTextImagePos[idx][1] + self.tY))
            
            # draw elements
            if not self.viewText:
	            for idx, i in enumerate(self.elements):
	                rect = pygame.Rect(10, y + self.oY, self.elemWidth, self.elemHeight)
	                if rect.y + rect.height < self.surface.get_height() and rect.y + rect.height > 0:
	                    pygame.draw.rect(self.surface, self.elemColor if idx != self.elem_idx else self.elemSelectedColor, (10, y + self.oY, self.elemWidth, self.elemHeight), self.fillSize, self.borderRadius)
	                    
	                    self.surface.blit(self.textes[idx], (self.drawImages[idx].get_width() + 20, self.textesPos[idx][1] + self.oY))
	                    self.surface.blit(self.drawImages[idx], (10, y + self.oY))
	                
	                y += self.elemHeight + 10

            if len(self.elements) > 0: self.lastY = y - self.elemHeight - 20
            self.win.blit(self.surface, (self.x, self.y))