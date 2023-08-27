import pygame

class ProgressBar:
    def __init__(self, win, **args):
        self.win = win
        
        self.x = args.get("x", 0)
        self.y = args.get("y", 0)
        self.title = args.get("title", "")
        self.items = 0
        self.items_loaded = 0
        self.progerss = 0.0
        self.surface = pygame.Surface((args.get("width", self.win.get_width() // 1.5), args.get("height", self.win.get_height() // 1.5)), pygame.SRCALPHA)
        self.border_radius = args.get("border_radius", 15)
        self.fill_size = args.get("fill_size", 0)
        self.progress_border_radius = args.get("progress_border_radius", -1)
        self.color = args.get("color", [100, 100, 100])
        self.stroke_color = tuple([max(25, min(225, item - 25)) for item in self.color])
        self.text_color = args.get("text_color", [255, 255, 255])
        self.title_color = args.get("title_color", [255, 255, 255])
        self.progress_color = args.get("progress_color", [0, 255, 0])
        self.progress_bg_color = args.get("progress_bg_color", [140, 140, 140])
        self.font_path = args.get("font", None)
        self.render = True
        self.ADP()
        self.start(self.title, 0)
    
    def ADP(self):
        self.SPBW = self.surface.get_width() // 1.5
        self.PBW = self.SPBW
        self.PBH = self.surface.get_height() // 10
        self.PBP = (self.surface.get_width() // 2 - self.PBW // 2, self.surface.get_height() - self.PBH - 10)
        self.font_size = self.surface.get_height() // 10
        self.title_font_size = self.surface.get_height() // 8
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.title_font = pygame.font.Font(self.font_path, self.title_font_size)
    
    def setItemName(self, name: str):
        self.item_name_img = self.font.render(name, 0, self.text_color)
        
        f = False
        while 1:
            if self.PBP[0] + self.item_name_img.get_width() > self.surface.get_width():
                name = name[:-1]
                self.item_name_img = self.font.render(name, 0, self.text_color)
                f = True
            else:
                if f:
                    name = name[:-3]
                    self.item_name_img = self.font.render(name + "...", 0, self.text_color)
                break
    
    def start(self, title: str, items: int):
        self.title = title
        self.items = items
        self.items_loaded = 0
        self.progerss = 0.0
        
        self.title_img = self.title_font.render(title, 0, self.title_color)
        
        f = False
        
        while 1:
            if self.surface.get_width() // 2 - self.title_img.get_width() // 2 + self.title_img.get_width() > self.surface.get_width():
                title = title[:-1]
                self.title_img = self.title_font.render(title, 0, self.text_color)
                f = True
            else:
                if f:
                    title = title[:-3]
                    self.title_img = self.title_font.render(title + "...", 0, self.text_color)
                break
                
        self.progress_img = self.font.render("0%", 0, self.text_color)
        self.PBW = 0
        self.setItemName("")
    
    def itemLoaded(self):
        self.items_loaded += 1
        self.progress = self.items_loaded / self.items * 100
        self.PBW = int(self.SPBW * (self.progress / 100))
        self.progress_img = self.font.render(f"{self.progress:.1f}%", 0, self.text_color)
    
    def update(self):
        if self.render:
            self.surface.fill((0, 0, 0, 0))
            pygame.draw.rect(self.surface, self.color, (0, 0, self.surface.get_width(), self.surface.get_height()), self.fill_size, self.border_radius)
            pygame.draw.rect(self.surface, self.progress_bg_color, (self.PBP[0], self.PBP[1], self.SPBW, self.PBH), 0, self.progress_border_radius)
            pygame.draw.rect(self.surface, self.progress_color, (self.PBP[0], self.PBP[1], self.PBW, self.PBH), 0, self.progress_border_radius)
            self.surface.blit(self.title_img, (self.surface.get_width() // 2 - self.title_img.get_width() // 2, 10))
            self.surface.blit(self.progress_img, (self.PBP[0], self.PBP[1] - self.progress_img.get_height() - 10))
            self.surface.blit(self.item_name_img, (self.PBP[0], self.PBP[1] - self.progress_img.get_height() - 10 - self.item_name_img.get_height() - 10))
            pygame.draw.rect(self.surface, self.stroke_color, (0, 0, self.surface.get_width(), self.surface.get_height()), 5, self.border_radius)
            #self.surface.set_colorkey((1, 1, 1))
            self.win.blit(self.surface, (self.x, self.y))