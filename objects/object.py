import pygame, math
import UniPy as pe
import settings as st
import engineUI as eui

class Object:
    def __init__(self, surface: pygame.Surface, x: int, y: int, w: int, h: int, render: bool, image: str, bd: str, a: int, sw: int, sh: int, fx: bool, fy: bool, sx: int, sy: int, cx: str, cy: str, tsp: int, ufa: int, s: str, sc: str, scc: str, c: tuple, uc: bool, PARENT: str, l: int, t: str):
        self.win = surface
        self.oldWinSize = self.win.get_size()
        
        self.PARENT = PARENT
        
        self.factor = min(surface.get_width() / st.projectSize[0], surface.get_height() / st.projectSize[1]) if surface.get_width() > st.projectSize[0] and surface.get_height() > st.projectSize[1] else min(surface.get_width() / st.projectSize[0], surface.get_height() / st.projectSize[1])
        
        self._x = int(sx * self.factor)
        self._y = int(sy * self.factor)
        
        self.flipX = fx
        self.flipY = fy
        
        self._width = int(sw * self.factor)
        self._height = int(sh * self.factor)
        
        self.wa = self._width
        self.ha = self._height
        
        self._SW = sw
        self._SH = sh
        self._sx = sx
        self._sy = sy
        
        self.cx = cx
        self.cy = cy
        
        self._color = list(c)

        self._pressed = False
        
        self.onPressed = None
        self.onPressedContent = "()"
        self.onUnPressed = None
        self.onUnPressedContent = "()"
        self.finger_id = -1
        
        self.frame = 1
        self.collidedObj = None
        self.leftCollided = False
        self.rightCollided = False
        self.topCollided = False
        self.bottomCollided = False
        self.onCollided = None
        self.onCollidedContent = "()"
        self.onUnCollided = None
        self.onUnCollidedContent = "()"
        
        self.render = render
        self.useCamera = uc
        
        self.bodyType = bd if bd in ["None", "dynamic", "static"] else "None"
        self._angle = a
        self.useFullAlpha = ufa
        
        self.rect = pygame.Rect(int(self._x), int(self._y), self.width, self.height)
        
        self.imagePath = image
        try: self._image = pe.textures[image] if not self.useFullAlpha else pe.texturesTSP[image]
        except: self._image = None
        
        self.CI = self.image
        
        self._transparent = tsp
        
        if self._image != None:
            self.CI = pygame.transform.scale(self.image, (self._width, self._height))
            self.CI = pygame.transform.rotate(self.CI, self._angle)
            self.wa, self.ha = self.CI.get_size()
            if self.color != [255, 255, 255]: self.CI.fill(self.color, special_flags=pygame.BLEND_RGB_MULT)
            if self._transparent != 255: self.CI.set_alpha(self._transparent)
        
        self.layer = l
        self.tag = t
	        
        # PHYSICS
        self.gravity = 10
        self.thisGravity = self.gravity
        self.force = 0
        self.lastTop = self.rect.top
        self.lastPos = self.rect.topleft
        
        # SCRIPT
        self.script = s
        self.S_LINKS = []
        
        self.S_CONTENT = sc
        self.SC_CHANGED = scc
        
        # ANIMS
        self.anims = []
    
    def adapt(self):
        ww, hh = self.width - int(self.SW * self.factor), self.height - int(self.SH * self.factor)
        xx, yy = self.rect.x - int(self.sx * self.factor), self.rect.y - int(self.sy * self.factor)
        self.factor = min(self.win.get_width() / st.projectSize[0], self.win.get_height() / st.projectSize[1]) if self.win.get_width() > st.projectSize[0] and self.win.get_height() > st.projectSize[1] else min(self.win.get_width() / st.projectSize[0], self.win.get_height() / st.projectSize[1])
        self.x = int(self.sx * self.factor) + xx
        self.y = int(self.sy * self.factor) + yy
        self.width = int(self.SW * self.factor) + abs(ww)
        self.height = int(self.SH * self.factor) + abs(hh)
    
    def SSC(self):
        for s in self.S_LINKS:
            new = type(s).__name__ not in self.S_CONTENT
            if new:
                self.S_CONTENT[type(s).__name__] = {}
                self.SC_CHANGED[type(s).__name__] = {}
    
            variables = [var for var in dir(s) if not callable(getattr(s, var)) and not var.startswith("__")]
            if "this" in variables:
                del variables[variables.index("this")]
    
            for j in variables[::-1]:
                if new or j not in self.SC_CHANGED[type(s).__name__]:
                    self.SC_CHANGED[type(s).__name__][j] = False
                if not self.SC_CHANGED[type(s).__name__][j]:
                    value = getattr(s, j)
                    value_type = type(value).__name__
                    if value_type in ["PATH", "OBJ"]:
                        if value_type != "OBJ":
                            if value.value in [i.split(".")[0] for i in pe.audios]:
                                evaluated_value = f"pe.GetSound('{value.value}')"
                            else:
                                evaluated_value = f"pe.GetTexture('{value.value}')"
                        else:
                            evaluated_value = f"pe.GetObj('{value.value}')"
                    elif value_type == "NoneType":
                        evaluated_value = eval("{value}")
                    else:
                        evaluated_value = eval(f"{value_type}({value})")
                    self.S_CONTENT[type(s).__name__][j] = [evaluated_value, value_type]
    
    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y
    
    @property
    def width(self):
    	return self._width
    @property
    def height(self):
    	return self._height
    
    @property
    def SW(self):
        return self._SW
    @property
    def SH(self):
        return self._SH
    
    @property
    def sx(self):
        return self._sx
    @property
    def sy(self):
        return self._sy
    
    @property
    def image(self):
    	return self._image
    
    @property
    def color(self):
        return self._color
    
    @property
    def transparent(self):
    	return self._transparent
    
    @property
    def angle(self):
        return self._angle
    
    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = value
    
    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = value
    
    @width.setter
    def width(self, value):
    	self._width = value
    	self.wa = value
    	self.rect.width = value
    	if self.CI != None:
        	self.CI = pygame.transform.scale(self.image, (self._width, self._height))
        	self.CI = pygame.transform.rotate(self.CI, self._angle)
        	if self.color != [255, 255, 255]: self.CI.fill(self.color, special_flags=pygame.BLEND_RGB_MULT)
        	if self._transparent != 255: self.CI.set_alpha(self._transparent)
    
    @height.setter
    def height(self, value):
    	self._height = value
    	self.ha = value
    	self.rect.height = value
    	if self.CI != None:
        	self.CI = pygame.transform.scale(self.image, (self._width, self._height))
        	self.CI = pygame.transform.rotate(self.CI, self._angle)
        	if self.color != [255, 255, 255]: self.CI.fill(self.color, special_flags=pygame.BLEND_RGB_MULT)
        	if self._transparent != 255: self.CI.set_alpha(self._transparent)
    
    @sx.setter
    def sx(self, value):
        self._sx = value
        self._x = int(self._sx * self.factor)
        self.rect.x = self._x
    
    @sy.setter
    def sy(self, value):
        self._sy = value
        self._y = int(self._sy * self.factor)
        self.rect.y = self._y
    
    @SW.setter
    def SW(self, value):
        self._SW = value
        self.width = int(self._SW * self.factor)
        self.wa = self.width
    
    @SH.setter
    def SH(self, value):
        self._SH = value
        self.height = int(self._SH * self.factor)
        self.ha = self.height
    
    @image.setter
    def image(self, value):
    	
    	if value != None:
    	    
    	    if self.image == None and self.SW == 0 and self.SH == 0:
    	        self._image = value
    	        self.CI = self._image
    	        self.SW, self.SH = self.CI.get_size()
    	    else:
    	        self._image = value
    	        self.CI = pygame.transform.scale(self._image, (self._width, self._height))
    	        self.SW, self.SH = self.CI.get_size()
    	    
    	    self.CI = pygame.transform.scale(self.image, (self._width, self._height))
    	    self.CI = pygame.transform.rotate(self.CI, self._angle)
    	    self.wa, self.ha = self.CI.get_size()
    	    if self.color != [255, 255, 255]: self.CI.fill(self.color, special_flags=pygame.BLEND_RGB_MULT)
    	    if self._transparent != 255: self.CI.set_alpha(self._transparent)
    	else:
    	    self._image = value
    
    @color.setter
    def color(self, value):
        self._color = list(value)
        if self.CI != None:
            self.CI = pygame.transform.scale(self.image, (self._width, self._height))
            self.CI = pygame.transform.rotate(self.CI, self._angle)
            if self.color != [255, 255, 255]: self.CI.fill(self.color, special_flags=pygame.BLEND_RGB_MULT)
            if self._transparent != 255: self.CI.set_alpha(self._transparent)
    
    @transparent.setter
    def transparent(self, value):
    	self._transparent = value
    	if self._transparent != 255 and self.CI != None: self.CI.set_alpha(self._transparent)
    
    @angle.setter
    def angle(self, value):
        self._angle = value
        if self.CI != None:
            self.CI = pygame.transform.scale(self.image, (self._width, self._height))
            self.CI = pygame.transform.rotate(self.CI, self._angle)
            self.wa, self.ha = self.CI.get_size()
            if self.color != [255, 255, 255]: self.CI.fill(self.color, special_flags=pygame.BLEND_RGB_MULT)
            if self._transparent != 255: self.CI.set_alpha(self._transparent)
    
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
                eui._console.Log(f"UniPy Error: in adding anim: \"{var}\" is not defined", "error")
                eui.error = True
                return 0
    
        self.anims.append([])
        for index, _v in enumerate(anim):
            if (_v in ["x", "y", "width", "height", "angle", "transparent", "color"] and
                    (type(end_anim_func[index]).__name__ == "function" or end_anim_func[index] is None) and (type(runtime_functions[index]).__name__ == "function" or runtime_functions[index] is None) and
                    type(speed[index]) == int):
                self.anims[-1].append([_v, value[index], speed[index], end_anim_func[index], runtime_functions[index], align])
    
    def GetModule(self, name: str):
        md = [type(i).__name__ for i in self.S_LINKS]
        
        if name in md:
            return self.S_LINKS[md.index(name)]
        else:
            eui._console.Log(f"UniPy Error: in getting module: \"{name}\" is not defined", "warning")
    
    def HasPressed(self, pos, id):
        r = pe.Camera.apply(self.rect) if self.useCamera else self.rect
        if self.onPressed != None and r.collidepoint(pos) and self.render:
            self._pressed = True
            self.finger_id = id
            
            eval(f"self.onPressed{self.onPressedContent}")
            
            if self.onUnPressed == None:
            	self._pressed = False
            	self.finger_id = -1
    
    def HasUnPressed(self, id):
        if self._pressed and self.render and id == self.finger_id:
            self._pressed = False
            self.finger_id = -1
            
            if self.onUnPressed != None:
                eval(f"self.onUnPressed{self.onUnPressedContent}")
    
    def pressed(self):
        if self.pressed:
        	r = pe.Camera.apply(self.rect) if self.useCamera else self.rect
        	for i in pe.fingersPos:
        		if r.collidepoint(i):
        			return True
        	return False
    
    def setPosObject(self):
        if self.cx[:4] == "objX" and self.cx[4] == "(" and self.cx[-1] == ")":
            if self.cx[5:-1] in pe.objName:
                self.rect.x = pe.GetObj(self.cx[5:-1]).x + self.sx * self.factor
                self._x = self.rect.x
        
        elif self.cx[:5] == "objCX" and self.cx[5] == "(" and self.cx[-1] == ")":
            if self.cx[6:-1] in pe.objName:
            	self.rect.x = pe.GetObj(self.cx[6:-1]).x + pe.GetObj(self.cx[6:-1]).width // 2 - self._width // 2
            	self._x = self.rect.x
        
        if self.cy[:4] == "objY" and self.cy[4] == "(" and self.cy[-1] == ")":
            if self.cy[5:-1] in pe.objName:
            	self.rect.y = pe.GetObj(self.cy[5:-1]).y + self.sy * self.factor
            	self._y = self.rect.y
        
        elif self.cy[:5] == "objCY" and self.cy[5] == "(" and self.cy[-1] == ")":
           if self.cy[6:-1] in pe.objName:
            	self.rect.y = pe.GetObj(self.cy[6:-1]).y + pe.GetObj(self.cy[6:-1]).height // 2 - self._height // 2
            	self._y = self.rect.y
    
    def setPos(self):
        
        if self.cx == "right":
            self.rect.x = self.win.get_width() - self.wa + self.sx
            self._x = self.rect.x
            
        elif self.cx == "center":
            self.rect.x = self.win.get_width() // 2 - self.wa // 2 + self.sx
            self._x = self.rect.x
            
        if self.cy == "bottom":
            self.rect.y = self.win.get_height() - self.ha + self.sy
            self._y = self.rect.y
        
        elif self.cy == "center":
            self.rect.y = self.win.get_height() // 2 - self.ha // 2 + self.sy
            self._y = self.rect.y
    
    def addForce(self, force: float):
    	self.force += force
    
    def CheckAnim(self):
        if self.anims:
            anim = self.anims[0]
            idx = 0
    
            for _a in anim:
                if _a[0] in ["x", "y", "angle", "transparent", "width", "height"]:
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
    
                idx += 1
    
            if not self.anims[0]:
                self.anims.pop(0)
    
    def update(self):
    
        if self.bodyType == "dynamic":
    	     c = 0
    	     rc = False
    	     lc = False
    	     tc = False
    	     bc = False
    	     ico = False
    	     
    	     if self.thisGravity > 64:
    	         self.thisGravity = 64
    	         
    	     if self.gravity == 0 and self.thisGravity != 0:
    	         self.thisGravity = 0
    	     
    	     if self.force <= 0.5:
    	         self.rect.y += self.thisGravity
    	         self.thisGravity += self.thisGravity * 0.049
    	     else:
    	         self.rect.y -= self.force
    	         self.force /= 1.5
    	         
    	         if self.force <= 0.5:
    	             self.force = 0
    	             self.thisGravity = self.force
    	     
    	     for obj in pe.objects:
    	     	if obj != self and hasattr(obj, "bodyType") and self.rect.colliderect(obj.rect) and obj.bodyType != "None":
    	     		if obj == self.collidedObj: ico = True
    	     		self.collidedObj = obj
    	     		if self.onCollided != None and self.collidedObj != obj:
    	     		    eval(f"self.onCollided{self.onCollidedContent}")
    	     		c += 1
    	     		dx = min(abs(self.rect.right - obj.rect.left), abs(self.rect.left - obj.rect.right))
    	     		dy = min(abs(self.rect.bottom - obj.rect.top - 8), abs(self.rect.top - obj.rect.bottom - 8))
    	     		
    	     		if dx < dy:
    	     			c = 0
    	     			if self.rect.right > obj.rect.left and self.rect.left < obj.rect.left:
    	     			    self.rightCollided = True
    	     			    rc = True
    	     			    self.rect.right = obj.rect.left
    	     			elif self.rect.left < obj.rect.right and self.rect.right > obj.rect.right:
    	     			    lc = True
    	     			    self.leftCollided = True
    	     			    self.rect.left = obj.rect.right
    	     		else:
    	     			if self.rect.top < obj.rect.bottom and self.rect.top > obj.rect.top or self.lastTop > obj.rect.top:
    	     				self.rect.top = obj.rect.bottom
    	     				tc = True
    	     				self.topCollided = True
    	     				self.force = 0
    	     				self.thisGravity = 0
    	     			else:
    	     				bc = True
    	     				self.bottomCollided = True
    	     				self.rect.bottom = obj.rect.top
    	     				self.thisGravity = 0
    	     
    	     if self.frame % 2 == 0:
    	         if not bc: self.bottomCollided = False
    	         if not tc: self.topCollided = False
    	         if not lc: self.leftCollided = False
    	         if not rc: self.rightCollided = False
    	     
    	     if c == 0 and self.thisGravity == 0 and self.frame % 2 == 1:
    	     	self.thisGravity = self.gravity
    	     if self.collidedObj != None and not ico and self.frame % 2 == 1:
    	         
    	         if not self.rect.colliderect(pygame.Rect(self.collidedObj.rect.x - 2, self.collidedObj.rect.y - 2, self.collidedObj.rect.width + 4, self.collidedObj.rect.height + 4)):
    	             self.collidedObj = None
    	             if self.onUnCollided != None:
    	                 eval(f"self.onUnCollided{self.onUnCollidedContent}")
        
        self.lastTop = self.rect.top
        self.lastPos = self.rect.topleft
        self.CheckAnim()
        self.frame += 1
        
        r = pe.Camera.apply(self.rect) if self.useCamera else self.rect
        
        if self.render and self.image != None and st.WR.colliderect(r):
            img = self.CI
                
            if self.flipX: img = pygame.transform.flip(img, True, False)
            if self.flipY: img = pygame.transform.flip(img, False, True)
                
            self.win.blit(img, r)