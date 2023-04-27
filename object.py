import pygame
import UniPy as pe
import settings as st

class Object:
    def __init__(self, surface: pygame.Surface, x: int, y: int, w: int, h: int, render: bool, image: str, bd: str, a: int, sw: int, sh: int, fx: bool, fy: bool, sx: int, sy: int, cx: str, cy: str, tsp: int):
        self.win = surface
        
        self.factor = min(surface.get_width() / st.projectSize[1], surface.get_height() / st.projectSize[0]) if surface.get_width() != st.projectSize[0] and surface.get_height() != st.projectSize[1] else 1
        
        self._x = int(sx * self.factor)
        self._y = int(sy * self.factor)
        
        self.flipX = False if fx == 0 else True
        self.flipY = False if fy == 0 else True
        
        self._width = int(sw * self.factor)
        self._height = int(sh * self.factor)
        
        self._SW = sw
        self._SH = sh
        self._sx = sx
        self._sy = sy
        
        self.cx = cx
        self.cy = cy
        
        self._pressed = False
        
        self.onPressed = None
        self.onPressedContent = "()"
        self.onUnPressed = None
        self.onUnPressedContent = "()"
        self.finger_id = -1
        
        self.render = True if render == 1 else False
        
        self.bodyType = bd if bd in ["None", "dynamic", "static"] else "None"
        self.angle = a
        self.rect = pygame.Rect(self._x, self._y, self.width, self.height)
        
        self.imagePath = image
        self._image = pe.textures[image.split("/")[-1]] if image != "None" else None
        
        self.CI = self.image
        
        self._transparent = tsp
        
        if self._image != None:
	        self.CI = pygame.transform.scale(self.image, (self._width, self._height))
	        if self._transparent != 255: self.CI.set_alpha(self._transparent)
	        
        # PHYSICS
        self.gravity = 10
        self.thisGravity = self.gravity
        self.force = 0
    
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
    def transparent(self):
    	return self._transparent
    
    @x.setter
    def x(self, value):
        self.rect.x = value
        self._x = value
    
    @y.setter
    def y(self, value):
        self.rect.y = value
        self._y = value
    
    @width.setter
    def width(self, value):
    	self._width = value
    	self.rect.width = value
    	self.CI = pygame.transform.scale(self._image, (self._width, self._height))
    	if self._transparent != 255: self.CI.set_alpha(self._transparent)
    
    @height.setter
    def height(self, value):
    	self._height = value
    	self.rect.height = value
    	self.CI = pygame.transform.scale(self._image, (self._width, self._height))
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
    
    @SH.setter
    def SH(self, value):
        self._SH = value
        self.height = int(self._SH * self.factor)
    
    @image.setter
    def image(self, value):
    	self._image = value
    	
    	if self._image != None:
    		self.CI = pygame.transform.scale(self._image, (self._width, self._height))
    		if self._transparent != 255: self.CI.set_alpha(self._transparen)
    	
    	else:
    		self.CI = self._image
    
    @transparent.setter
    def transparent(self, value):
    	self._transparent = value
    	if self._transparent != 255: self.CI.set_alpha(self._transparent)
    
    def HasPressed(self, pos, id):
        if self.rect.collidepoint(pos) and self.render:
            eval(f"self.onPressed{self.onPressedContent}")
            self._pressed = True
            self.finger_id = id
            
            if self.onUnPressed == None:
            	self._pressed = False
            	self.finger_id = -1
    
    def HasUnPressed(self, id):
        if self._pressed and self.render and id == self.finger_id:
            eval(f"self.onUnPressed{self.onUnPressedContent}")
            self._pressed = False
            self.finger_id = -1
    
    def pressed(self):
        if self.pressed:
        	for i in pe.fingersPos:
        		if self.rect.collidepoint(i):
        			return True
        	return False
    
    def setPosObject(self):
    	if self.cx[:4] == "objX" and self.cx[4] == "(" and self.cx[-1] == ")":
    		if self.cx[5:-1] in pe.objName:
    		      self.rect.x = pe.GetObj(self.cx[5:-1]).x + self.sx
    		      self._x = self.rect.x
    	
    	if self.cy[:4] == "objY" and self.cy[4] == "(" and self.cy[-1] == ")":
            if self.cy[5:-1] in pe.objName:
            	self.rect.y = pe.GetObj(self.cy[5:-1]).y + self.y
            	self._y = self.rect.y
    
    def setPos(self):
        
        if self.cx == "right":
            self.rect.x = self.win.get_width() - self.width + self.sx
            self._x = self.rect.x
            
        elif self.cx == "centerx":
            self.rect.x = self.win.get_width() // 2 - self.width // 2 + self.sx
            self._x = self.rect.x
            
        if self.cy == "bottom":
            self.rect.y = self.win.get_height() - self.height + self.sy
            self._y = self.rect.y
        
        elif self.cy == "centery":
            self.rect.y = self.win.get_height() // 2 - self.height // 2 + self.sy
            self._y = self.rect.y
    
    def addForce(self, force):
    	self.force += force
    
    def update(self):
    	if self.bodyType == "dynamic":
    	     c = 0
    	     
    	     if self.thisGravity > 100: self.thisGravity = 100
    	     
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
    	     		c += 1
    	     		dx = min(abs(self.rect.right - obj.rect.left), abs(self.rect.left - obj.rect.right))
    	     		dy = min(abs(self.rect.bottom - obj.rect.top), abs(self.rect.top - obj.rect.bottom))
    	     		
    	     		if dx < dy:
    	     			c = 0
    	     			if self.rect.right > obj.rect.left and self.rect.left < obj.rect.left: self.rect.right = obj.rect.left
    	     			elif self.rect.left < obj.rect.right and self.rect.right > obj.rect.right: self.rect.left = obj.rect.right
    	     		else:
    	     			if self.rect.bottom > obj.rect.top and self.rect.top < obj.rect.top:
    	     				self.rect.bottom = obj.rect.top
    	     				if self.thisGravity > 0:
    	     					self.thisGravity = 0
    	     			elif self.rect.top < obj.rect.bottom and self.rect.bottom > obj.rect.bottom:
    	     				self.rect.top = obj.rect.bottom
    	     				self.force = 0
    	     				self.thisGravity = 0
    	     				if self.thisGravity < 0:
    	     					self.thisGravity = 0
    	     if c == 0 and self.thisGravity == 0:
    	     	self.thisGravity = self.gravity
		        	
    	img = self.CI
    	
    	if self.angle != 0:
    		img = pygame.transform.rotate(img, self.angle)
    	if self.flipX: img = pygame.transform.flip(img, True, False)
    	if self.flipY: img = pygame.transform.flip(img, False, True)
    	
    	if self.image != None:
    		self.win.blit(img, self.rect)