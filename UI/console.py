import pygame

class Console:
	def __init__(self, win, **args):
		
		self.win = win
		
		self.x = args.get("x", 0)
		self.y = args.get("y", 0)
		self.tY = 0
		self.tX = 0
		
		self.surface = pygame.Surface((args.get("width", win.get_width() // 1.5), args.get("height", win.get_height() // 1.5)))
		self.width, self.height = self.surface.get_size()
		
		self.logColor = args.get("logColor", (255, 255, 255))
		self.warningColor = args.get("warningColor", (255, 255, 0))
		self.errorColor = args.get("errorColor", (255, 0, 0))
		
		self.bgColor = args.get("bgColor", (60, 60, 60))
		self.strokeColor = tuple([max(15, min(240, item - 15)) for item in self.bgColor])
		
		self.textes = []
		self.textesType = []
		self.fontSize = self.surface.get_height() // 20 if self.surface.get_width() <= 800 else self.surface.get_height() // 10
		self.font = pygame.font.Font(args.get("font", None), self.fontSize)
		
		self.render = True
	
	def Log(self, text, type, file = None, line = None):
		if type != "log":
			self.textes.append(str(text))
		else:
			self.textes.append(f"Log: from script \"{file}\": line [{line}]\n{text}")
		self.textesType.append(type)
	
	def update(self):
		if self.render:
			self.surface.fill(self.bgColor)
			
			idx = 0
			y = 10
			for i in self.textes:
				if self.textesType[idx] == "warning": color = self.warningColor
				elif self.textesType[idx] == "error": color = self.errorColor 
				else: color = self.logColor
				
				for j in i.split("\n"):
					text = self.font.render(j, 0, color)
					self.surface.blit(text, (10 + self.tX, y + self.tY))
					y += text.get_height()
					
				y += self.fontSize
				idx += 1
			
			pygame.draw.rect(self.surface, self.strokeColor, (0, 0, self.width, self.height), 5)
			
			self.win.blit(self.surface, (self.x, self.y))