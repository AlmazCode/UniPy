import pygame, re
import UniPy as pe
import settings as st
import engineUI as eui

class Text:
    def __init__(self, surface: pygame.Surface, x: int, y: int, text: str, fs: int, font: str, color: tuple, tsp: int, a: int, render: int, fx: bool, fy: bool, cx: str, cy: str, sx: int, sy: int, sfs: int, tc: str, rt: bool, s: str, sc: str, scc: str, uc: bool, PARENT: str, l: int, t: str, sm: bool):
        self.win = surface
        
        self.PARENT = PARENT
        
        self.factor = min(surface.get_width() / st.projectSize[0], surface.get_height() / st.projectSize[1]) if surface.get_width() > st.projectSize[0] and surface.get_height() > st.projectSize[1] else min(surface.get_width() / st.projectSize[0], surface.get_height() / st.projectSize[1])
        
        self.x = int(sx * self.factor)
        self.y = int(sy * self.factor)
        
        self._text = str(text).replace("\n", "\\n").replace("\t", "    ")
        self._fontSize = int(max(0, min(2048, sfs)) * self.factor)
        self._sfs = max(0, min(2048, sfs))
        self.fontPath = font
        self.richText = rt
        
        try: self._font = pygame.font.Font(font, self._fontSize) if font != "None" else pygame.font.SysFont("Arial", self.fontSize)
        except: self._font = pygame.font.SysFont("Arial", self.fontSize)
        
        self._color = list(color)
        self.transparent = tsp
        
        self.flipX = fx
        self.flipY = fy
        
        self._sx = sx
        self._sy = sy
        
        self.cx = str(cx)
        self.cy = str(cy)
        
        self.textCentering = tc if tc in ["left", "center", "right"] else "left"
        
        self.render = render
        self.angle = a
        
        self.useCamera = uc
        self.layer = l
        self.tag = t
        self.smooth = sm
        
        # SCRIPT
        self.script = str(s)
        self.S_LINKS = []
        
        self.S_CONTENT = sc
        self.SC_CHANGED = scc
        
        # ANIMS
        self.anims = []
        
        self.width, self.height = (0, 0)
        self.compileText()
    
    def adapt(self):
        sfss = self.fontSize - int(self.sfs * self.factor)
        self.factor = min(self.win.get_width() / st.projectSize[0], self.win.get_height() / st.projectSize[1]) if self.win.get_width() > st.projectSize[0] and self.win.get_height() > st.projectSize[1] else min(self.win.get_width() / st.projectSize[0], self.win.get_height() / st.projectSize[1])
        
        self.fontSize = int(self.sfs * self.factor) + sfss
    
    def compileText(self):
        self.textes = []
        
        if self.richText:
            lastColor = self.color
            for TEXT in self.text.split("\\n"):
                
                color_pattern = re.compile(r'\(\$?(\d+),\$?(\d+),\$?(\d+)\)')
                TEXT = re.sub(color_pattern, r'(\1, \2, \3)', TEXT)
                color_tags = re.findall(r"\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)", TEXT)
                
                i = 0
                substrings = []
                stack = [lastColor]
                
                while i < len(TEXT):
                    char = TEXT[i]
                    if len(TEXT) > 1 and char == "$" and i != len(TEXT)-1 and TEXT[i+1] == "(":
                        if color_tags:
                            color = tuple(map(int, color_tags.pop(0)[1:-1].split(",")))
                            stack.append(color)
                            lastColor = color
                            
                            i += len(str(color)) + 1
                        else:
                            if substrings != []: substrings[-1][0] += "$"
                            else:
                                substrings.append(["$", self.color])
                            i += 1
                            stack.append(lastColor)
                    else:
                        j = i + 1
                        while j < len(TEXT) and TEXT[j] != "$": j += 1
                        substr = TEXT[i:j]
                        substrings.append([substr, stack[-1]])
                        i = j
                
                x = 0
                surf = pygame.Surface(self.font.size("".join(item[0] for item in substrings)))
                surf.fill((1, 1, 1))
                s = ""
                for subr, color in substrings:
                    tx = self.font.render(subr, self.smooth, color)
                    s += subr
                    surf.blit(tx, (x, 0))
                    x += tx.get_width()
                
                if self.angle != 0 and s != "":
                    surf = pygame.transform.rotate(surf, self.angle)
                surf = pygame.transform.flip(surf, self.flipX, self.flipY)
                surf.set_colorkey((1, 1, 1))
                self.textes.append(surf)
        
        else:
            for i in self.text.split("\\n"):
                tx = self.font.render(i, self.smooth, self.color)
                if self.angle != 0 and i != "":
                    tx = pygame.transform.rotate(tx, self.angle)
                tx = pygame.transform.flip(tx, self.flipX, self.flipY)
                self.textes.append(tx)
        
        self.width = max(sublist.get_width() for sublist in self.textes)
        self.height = sum(sublist.get_height() for sublist in self.textes)
    
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
    
    @property
    def color(self):
        return self._color
    
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
        self._fontSize = max(0, min(2048, value))
        self._font = pygame.font.Font(self.fontPath, self.fontSize) if self.fontPath != None else pygame.font.SysFont("Arial", self.fontSize)
        
        self.compileText()
        self.setPos()
        self.setPosObject()
    
    @color.setter
    def color(self, value):
        self._color = list(value)
        self.compileText()
    
    @sfs.setter
    def sfs(self, value):
        self._sfs = max(0, min(2048, value))
        self._fontSize = int(self.sfs * self.factor)
        self._font = pygame.font.Font(self.fontPath, self.fontSize) if self.fontPath != None else pygame.font.SysFont("Arial", self.fontSize)
    
    @font.setter
    def font(self, value):
        self.fontPath = value
        self._font = pygame.font.Font(value, self.fontSize)
        
        self.compileText()
        self.setPos()
        self.setPosObject()
    
    @text.setter
    def text(self, value):
        self._text = value.replace("\n", "\\n").replace("\t", "    ")
        self.compileText()
        self.setPos()
        self.setPosObject()
    
    def AddAnim(self, speed: list, anim: str, end_anim_func: list = [], runtime_functions: list = [], align: bool = False):
        if end_anim_func in [[], None]:
            end_anim_func = [None] * len(speed)
        if runtime_functions in [[], None]:
            runtime_functions = [None] * len(speed)
        value = [i.split("=")[1].strip() for i in anim.split(";")]
        idx = 0
        for i in value:
            try:
                value[idx] = eval(i)
            except:
                pass
            idx += 1
    
        anim = [i.split("=")[0].strip() for i in anim.split(";")]
        variables = [i[1:] if i[0] == "_" else i for i in dir(self)]
    
        for var in anim:
            if var not in variables:
                eui._consoleLog(f"UniPy Error: in adding anim: \"{var}\" is not defined", "error")
                eui.error = True
                return 0
    
        self.anims.append([])
        for index, _v in enumerate(anim):
            if (_v in ["x", "y", "angle", "transparent", "color", "fontSize"] and
                    (type(end_anim_func[index]).__name__ == "function" or end_anim_func[index] is None) and (type(runtime_functions[index]).__name__ == "function" or runtime_functions[index] is None) and
                    type(speed[index]) == int):
                self.anims[-1].append([_v, value[index], speed[index], end_anim_func[index], runtime_functions[index], align])
    
    def CheckAnim(self):
        if self.anims:
            anim = self.anims[0]
    
            for idx, _a in enumerate(anim):
                if _a[0] in ["x", "y", "angle", "transparent", "fontSize"]:
                    attr_name = _a[0]
                    target_value = _a[1]
                    step = _a[2]
    
                    current_value = getattr(self, attr_name)
                    if current_value > target_value:
                        setattr(self, attr_name, current_value - step)
                        if getattr(self, attr_name) < target_value:
                            setattr(self, attr_name, target_value)
                        if _a[4] != None:
                            _a[4]()
                        if _a[5]:
                            self.setPos()
                            self.setPosObject()
                    elif current_value < target_value:
                        setattr(self, attr_name, current_value + step)
                        if getattr(self, attr_name) > target_value:
                            setattr(self, attr_name, target_value)
                        if _a[4] != None:
                            _a[4]()
                        if _a[5]:
                            self.setPos()
                            self.setPosObject()
                    else:
                        if _a[3] is not None:
                            _a[3]()
                        self.anims[0].pop(idx)
    
                elif _a[0] == "color":
                    target_color = _a[1]
                    step = _a[2]
    
                    current_color = self.color
                    updated_color = []
    
                    for i in range(3):
                        if current_color[i] > target_color[i]:
                            updated_color.append(max(current_color[i] - step, target_color[i]))
                        elif current_color[i] < target_color[i]:
                            updated_color.append(min(current_color[i] + step, target_color[i]))
                        else:
                            updated_color.append(current_color[i])
                    if _a[4] != None:
                            _a[4]()
                    self.color = updated_color
    
                    if self.color == target_color:
                        if _a[3] is not None:
                            _a[3]()
                        self.anims[0].pop(idx)
    
            if not self.anims[0]:
                self.anims.pop(0)
    
    def GetModule(self, name: str):
        md = [type(i).__name__ for i in self.S_LINKS]
        
        if name in md:
            return self.S_LINKS[md.index(name)]
        else:
            eui._console.Log(f"UniPy Error: in getting module: \"{name}\" is not defined", "warning")
            eui.error = True
    
    def setPosObject(self):
        wfc = self.textes[0].get_width()
        
        if self.cx[:4] == "objX" and self.cx[4] == "(" and self.cx[-1] == ")":
            if self.cx[5:-1] in pe.objName:
            	self.x = pe.GetObj(self.cx[5:-1]).x + self.sx * self.factor
        elif self.cx[:5] == "objCX" and self.cx[5] == "(" and self.cx[-1] == ")":
            if self.cx[6:-1] in pe.objName:
            	self.x = pe.GetObj(self.cx[6:-1]).rect.centerx - wfc // 2
        
        if self.cy[:4] == "objY" and self.cy[4] == "(" and self.cy[-1] == ")":
            if self.cy[5:-1] in pe.objName:
            	self.y = pe.GetObj(self.cy[5:-1]).y + self.sy * self.factor
        elif self.cy[:5] == "objCY" and self.cy[5] == "(" and self.cy[-1] == ")":
            if self.cy[6:-1] in pe.objName:
            	self.y = pe.GetObj(self.cy[6:-1]).rect.centery - self.height // 2
    
    def setPos(self):
        wfc = self.textes[0].get_width()
        
        if self.cx == "right":
            self.x = self.win.get_width() - wfc + self.sx
        elif self.cx == "center":
            self.x = self.win.get_width() // 2 - wfc // 2 + self.sx
            
        if self.cy == "bottom":
            self.y = self.win.get_height() - self.height + self.sy
        elif self.cy == "center":
            self.y = self.win.get_height() // 2 - self.height  // 2 + self.sy
    
    def update(self):
        self.CheckAnim()
        
        if self.render and self.fontSize != 0:
            y = 0
            firstText = self.textes[0]

            for text in self.textes:

                endText = text
                
                if self.transparent != 255: endText.set_alpha(self.transparent)
                if self.textCentering == "center" and y != 0: pos = endText.get_rect(center = (self.x + firstText.get_width() // 2, 0))
                elif self.textCentering == "left": pos = (self.x, self.y)
                elif self.textCentering == "right": pos = endText.get_rect(right = self.x + firstText.get_width())
                else: pos = (self.x, self.y)
                
                r = endText.get_rect(topleft=(pos[0], self.y + y))
                
                self.win.blit(endText, pe.Camera.apply(r) if self.useCamera else r)
                y += text.get_height()
                lastText = endText