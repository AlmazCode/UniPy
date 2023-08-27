import pygame, math, traceback
import UniPy as pe
import settings as st
import engineUI as eui

class Object:
    def __init__(self, surface: pygame.Surface, x: int, y: int, w: int, h: int, render: bool, image: str, bd: str, a: int, sw: int, sh: int, fx: bool, fy: bool, sx: int, sy: int, cx: str, cy: str, tsp: int, ufa: int, s: str, sc: dict, scc: dict, c: tuple, uc: bool, PARENT: str, l: int, t: str, m: int):
        self.win = surface
        self.PARENT = PARENT
        
        self.factor = min(surface.get_width() / st.projectSize[0], surface.get_height() / st.projectSize[1]) if surface.get_width() > st.projectSize[0] and surface.get_height() > st.projectSize[1] else min(surface.get_width() / st.projectSize[0], surface.get_height() / st.projectSize[1])
        
        self._x = int(sx * self.factor)
        self._y = int(sy * self.factor)
        self.flipX = fx
        self.flipY = fy
        self._width = int(max(0, min(2048, sw)) * self.factor)
        self._height = int(max(0, min(2048, sh)) * self.factor)
        self.wa = self._width
        self.ha = self._height
        self._SW = max(0, min(2048, sw))
        self._SH = max(0, min(2048, sh))
        self._sx = sx
        self._sy = sy
        self.cx = str(cx)
        self.cy = str(cy)
        
        self._color = list(c)

        self._pressed = False
        self.onPressed = None
        self.onUnPressed = None
        self.finger_id = -1
        
        self.frame = 1
        self.collidedObj = None
        self.leftCollided = False
        self.rightCollided = False
        self.topCollided = False
        self.bottomCollided = False
        self.onCollided = None
        self.onUnCollided = None
        
        self.render = render
        self.useCamera = uc
        
        self.bodyType = bd if bd in pe._bodyTypes else "None"
        self._angle = a
        self.useFullAlpha = ufa
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.imagePath = image
        try:
            self._image = pe.textures[image] if not self.useFullAlpha else pe.texturesTSP[image]
        except:
            self._image = None
        
        self.CI = self.image.copy() if self.image != None else None
        self._transparent = tsp
        self.readjust()
        
        self.layer = l
        self.tag = t
	        
        # PHYSICS
        self.velocity = pygame.math.Vector2()
        self.mass = m
        self.terminal_velocity = self.mass * pe.TERMINALVELOCITY
        self.lastX = self.rect.x
        self.lastY = self.rect.y
        
        # SCRIPT
        self.script = str(s)
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
    
    def readjust(self):
        if self.CI != None:
            self.CI = pygame.transform.scale(self.image, (self.width, self.height))
            self.CI = pygame.transform.rotate(self.CI, self.angle)
            if self.color != [255, 255, 255]: self.CI.fill(self.color, special_flags=pygame.BLEND_RGB_MULT)
            if self._transparent != 255: self.CI.set_alpha(self.transparent)
    
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
    	self._width = max(0, min(2048, value))
    	self.wa = self.width
    	self.rect.width = self.width
    	self.readjust()
    
    @height.setter
    def height(self, value):
    	self._height = max(0, min(2048, value))
    	self.ha = self.height
    	self.rect.height = self.height
    	self.readjust()
    
    @sx.setter
    def sx(self, value):
        self._sx = value
        self._x = int(self.sx * self.factor)
        self.rect.x = self._x
    
    @sy.setter
    def sy(self, value):
        self._sy = value
        self._y = int(self.sy * self.factor)
        self.rect.y = self._y
    
    @SW.setter
    def SW(self, value):
        self._SW = max(0, min(2048, value))
        self.width = int(self.SW * self.factor)
        self.wa = self.width
    
    @SH.setter
    def SH(self, value):
        self._SH = max(0, min(2048, value))
        self.height = int(self.SH * self.factor)
        self.ha = self.height
    
    @image.setter
    def image(self, value):
    	oldImg = self.image
    	self._image = value
    	self.CI = self.image.copy() if self.image != None else None
    	self.readjust()
    
    @color.setter
    def color(self, value):
        self._color = list(value)
        self.readjust()
    
    @transparent.setter
    def transparent(self, value):
    	self._transparent = value
    	if self._transparent != 255 and self.CI != None: self.CI.set_alpha(self._transparent)
    
    @angle.setter
    def angle(self, value):
        self._angle = value
        self.readjust()
    
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
            eui.error = True
            eui._console.Log(f"UniPy Error: in getting module: \"{name}\" is not defined", "warning")
    
    def HasPressed(self, pos, id):
        r = pe.Camera.apply(self.rect) if self.useCamera else self.rect
        if r.collidepoint(pos) and self.render:
            self._pressed = True
            self.finger_id = id
            if self.onUnPressed is None:
            	self._pressed = False
            	self.finger_id = -1
            
            if type(self.onPressed).__name__ in ["method", "function"]:
                self.onPressed()
    
    def HasUnPressed(self, id):
        if self._pressed and self.render and id == self.finger_id:
            self._pressed = False
            self.finger_id = -1
            
            if type(self.onUnPressed).__name__ in ["method", "function"]:
                self.onUnPressed()
    
    def pressed(self):
        if self.pressed:
        	r = pe.Camera.apply(self.rect) if self.useCamera else self.rect
        	for i in pe.fingersPos:
        		if i != None and r.collidepoint(i):
        			return True
        	return False
    
    def setPosObject(self):
        if self.cx[:4] == "objX" and self.cx[4] == "(" and self.cx[-1] == ")":
            if self.cx[5:-1] in pe.objName:
                self.x = pe.GetObj(self.cx[5:-1]).x + self.sx * self.factor
        elif self.cx[:5] == "objCX" and self.cx[5] == "(" and self.cx[-1] == ")":
            if self.cx[6:-1] in pe.objName:
            	self.x = pe.GetObj(self.cx[6:-1]).x + pe.GetObj(self.cx[6:-1]).width // 2 - self.width // 2
        
        if self.cy[:4] == "objY" and self.cy[4] == "(" and self.cy[-1] == ")":
            if self.cy[5:-1] in pe.objName:
            	self.y = pe.GetObj(self.cy[5:-1]).y + self.sy * self.factor
        elif self.cy[:5] == "objCY" and self.cy[5] == "(" and self.cy[-1] == ")":
           if self.cy[6:-1] in pe.objName:
            	self.y = pe.GetObj(self.cy[6:-1]).y + pe.GetObj(self.cy[6:-1]).height // 2 - self.height // 2
    
    def setPos(self):
        if self.cx == "right":
            self.x = self.win.get_width() - self.wa + self.sx
        elif self.cx == "center":
            self.x = self.win.get_width() // 2 - self.wa // 2 + self.sx
            
        if self.cy == "bottom":
            self.y = self.win.get_height() - self.ha + self.sy
        elif self.cy == "center":
            self.y = self.win.get_height() // 2 - self.ha // 2 + self.sy
    
    def addForce(self, force: float):
    	self.velocity.y = -force
    
    def CheckAnim(self):
        if self.anims:
            anim = self.anims[0]
    
            for idx, _a in enumerate(anim):
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
    
            if not self.anims[0]:
                self.anims.pop(0)
    
    def _collided(self, obj):
        self.collidedObj = obj
        if type(self.onCollided).__name__ in ["method", "function"]:
            try:
                self.onCollided()
            except:
                eui.error = True
                tb = e.__traceback__
                filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
    
    def check_collision(self, direction):
        if direction == "horizontal":
            if self.lastX != self.rect.x and self.frame % 2 == 0:
                self.rightCollided = False
                self.leftCollided = False
            for obj in pe.objects:
                if obj != self and hasattr(obj, "bodyType") and obj.bodyType != "None" and obj.rect.colliderect(self.rect):
                    self._collided(obj)
                    if obj.bodyType not in ["kinematic", "dynamic"]:
                        if self.velocity.x > 0:
                            self.rect.right = obj.rect.left
                            self.rightCollided = True
                        if self.velocity.x < 0:
                            self.rect.left = obj.rect.right
                            self.leftCollided = True
        elif direction == "vertical":
            if self.lastY != self.rect.y and self.frame % 2 == 0:
                self.bottomCollided = False
                self.topCollided = False
            for obj in pe.objects:
                if obj != self and hasattr(obj, "bodyType") and obj.bodyType != "None" and obj.rect.colliderect(self.rect):
                    self._collided(obj)
                    if obj.bodyType not in ["kinematic", "dynamic"]:
                        if self.velocity.y > 0:
                            self.rect.bottom = obj.rect.top
                            self.bottomCollided = True
                        if self.velocity.y < 0:
                            self.rect.top = obj.rect.bottom
                            self.topCollided = True
                        self.velocity.y = 0
                
    def update(self):
        if self.bodyType == "dynamic":
            self.velocity.y += pe.GRAVITY * self.mass
            if self.velocity.y > self.terminal_velocity:
                self.velocity.y = self.terminal_velocity
            self.velocity.x = 0 if self.rect.x == self.lastX else 1 if self.rect.x > self.lastX else -1
            self.check_collision("horizontal")
            self.rect.y += self.velocity.y
            self.check_collision("vertical")
    	    
            if self.collidedObj != None and self.frame % 2 == 1:
                if not self.rect.colliderect(pygame.Rect(self.collidedObj.rect.x - 2, self.collidedObj.rect.y - 2, self.collidedObj.rect.width + 4, self.collidedObj.rect.height + 4)):
                    self.collidedObj = None
                    if type(self.onUnCollided).__name__ in ["method", "function"]:
                        try:
                            self.onUnCollided()
                        except:
                            eui.error = True
                            tb = e.__traceback__
                            filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                            eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
        
        self.lastX = self.rect.x
        self.lastY = self.rect.y
        self.CheckAnim()
        self.frame += 1
        
        if self.render and self.image != None:
            if self.angle != 0:
                pos = self.CI.get_rect(center = (self.rect.x + self.width // 2, self.rect.y + self.height // 2))
            else: pos = self.rect
            r = pe.Camera.apply(pos) if self.useCamera else self.rect
            if st.WR.colliderect(r):
                img = self.CI
                if self.flipX:
                    img = pygame.transform.flip(img, True, False)
                if self.flipY:
                    img = pygame.transform.flip(img, False, True)
                        
                self.win.blit(img, r)