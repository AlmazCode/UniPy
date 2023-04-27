import pygame

class ToggleButton:
    def __init__(self, surface, key, func, **args):
        toggleButtons.append(self)
        
        self.surface = surface     # окно на котором будет рисоваться кнопка
        
        self.image = args.get("image", None)
        
        self.color = args.get("color", (150, 150, 150))   # цвет кнопки
        
        self.active = False
        
        self.borderRadius = args.get("borderRadius", -1)  # уровень сглаживания углов у кнопки, если == -1, то сглаживание не будет
        self.fillSize = args.get("fillSize", 0)   # уровень заливки кнопки, если == 0, то будет заливаться полностью

        self.rect = pygame.Rect(args.get("x", 0), args.get("y", 0), args.get("width", 75), args.get("height", 75))
        
        if self.image != None:
            factor = min(self.rect.width / self.image.get_width(), self.rect.height / self.image.get_height())
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * factor), int(self.image.get_height() * factor)))
        
        self.startX = self.rect.x
        self.startY = self.rect.y
        
        self.func = func
        self.key = key
            
    def update(self):

        # отрисовка кнопки от зависимости переменной [mode]
        if not self.active:
            pygame.draw.rect(self.surface, self.color, self.rect, self.fillSize, self.borderRadius)
        else:
            pygame.draw.rect(self.surface, self.color, self.rect, self.fillSize, self.borderRadius)
            if type(self.image) == pygame.Surface:
                self.surface.blit(self.image, (self.rect.centerx - self.image.get_width() // 2, self.rect.centery - self.image.get_height() // 2))

toggleButtons = []          