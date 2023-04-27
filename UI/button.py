import pygame

class Button:
    def __init__(self, surface, **args):
        
        self.surface = surface     # окно на котором будет рисоваться кнопка
        
        self.color = args.get("color", (150, 150, 150))   # цвет кнопки
        self.pressedColor = args.get("pressedColor", (120, 120, 120))   # цвет кнопки когда она нажата

        self.func = args.get("func", None)   # функция которая будет вызываться при нажатии кнопки

        self.text = args.get("text", "")   # текст кнопки

        self.textColor = args.get("textColor", (255, 255, 255))   # цвет текста
        
        self.fast = args.get("fast", False)    # говорит о том будет ли вызываться функция после отжатия кнопки или до тех пор пока кнопка нажата

        self.mode = 0   # режим отрисовки кнопки
        self.press = False
        self.render = args.get("render", True)  # переменная, отвечающая за отрисовку кнопки на экране, если == True, то кнопка будет рисоваться, иначе нет.
        self.borderRadius = args.get("borderRadius", -1)  # уровень сглаживания углов у кнопки, если == -1, то сглаживание не будет
        self.fillSize = args.get("fillSize", 0)   # уровень заливки кнопки, если == 0, то будет заливаться полностью
        
        self.key = args.get("key", "")
        self.content = args.get("content", "()")

        self.rect = pygame.Rect(args.get("x", 0), args.get("y", 0), args.get("width", 100), args.get("height", 100))
        
        self.fontSize = args.get("fontSize", 50)
        self.fontPath = args.get("fontPath", None)    # путь до шрифта, если == None, то будет использован стандартный
        self.font = pygame.font.Font(self.fontPath, self.fontSize)
        
        self.image = args.get("image", None)
        self.OI = self.image
        
        self.ADP()
    
    def ADP(self):
        
        if self.image != None:
            factor = min(self.rect.width / self.image.get_width(), self.rect.height / self.image.get_height())
            self.image = pygame.transform.scale(self.OI, (int(self.image.get_width() * factor), int(self.image.get_height() * factor)))
        else:
            FW, FH = self.font.size(self.text)
            self.fontSize = int(min(self.rect.width / FW, self.rect.height / FH))
            self.font = pygame.font.Font(self.fontPath, self.fontSize)
    
    # функция обнавляющая всю кнопку и взоимодействие с ней
    def update(self):
        
        if self.render:

            mousePos = pygame.mouse.get_pos()
            mBT = pygame.mouse.get_pressed()
            
            # если переменная fast == False
            if not self.fast:

                # как только ЛКМ была нажата, и позиция мыши касалась кнопки - [mode = 1]
                if mBT[0] and self.rect.collidepoint(mousePos) and not self.press:
                    self.mode = 1
                    self.press = True

                # как только ЛКМ была отжата, и позиция мыши не касалась кнопки, и при этом до этого ЛКМ была нажата - [mode = 0]
                if not mBT[0] and self.press and self.rect.collidepoint(mousePos):
                    eval(f"self.func{self.content}")
                        
                    self.mode = 0
                    self.press = False
                
                # как только позиция мыши не касается кнопки, и при этом ЛКМ была нажата - [mode = 0]
                if not self.rect.collidepoint(mousePos) and self.press and mBT[0]:
                    self.mode = 0
                    self.press = False
                
                # как только позиция мыши не касается кнопки, и ЛКМ не была нажата - [mode = 0]
                if not self.rect.collidepoint(mousePos) and not self.press and not mBT[0]:
                    self.mode = 0
            
            # иначе
            if self.fast:

                # как только ЛКМ была нажата, и позиция мыши касалась кнопки - [mode = 1]
                if mBT[0] and self.rect.collidepoint(mousePos):
                    self.mode = 1
                    eval(f"self.func{self.content}")
                    self.press = True
                
                # как только ЛКМ была отжата, и при этом позиция мыши касалась кнопки - [mode = 0]
                if not mBT[0] and self.press and self.rect.collidepoint(mousePos):
                    self.mode = 0
                    self.press = False
                
                # как только позиция мыши не касается кнопки, и при этом ЛКМ была нажата - [mode = 0]
                if not self.rect.collidepoint(mousePos) and self.press and mBT[0]:
                    self.mode = 0
                    self.press = False
                
                # как только позиция мыши не касается кнопки, и при этом ЛКМ не была нажата - [mode = 0]
                if not self.rect.collidepoint(mousePos) and not self.press and not mBT[0]:
                    self.mode = 0

            self.draw()
            
    def draw(self):

        # отрисовка кнопки от зависимости переменной [mode]
        if self.mode == 0:
            pygame.draw.rect(self.surface, self.color, self.rect, self.fillSize, self.borderRadius)
        elif self.mode == 1:
            pygame.draw.rect(self.surface, self.pressedColor, self.rect, self.fillSize, self.borderRadius)
        
        if self.image == None:
            # отрисовка текста кнопки
            if self.text != '':
                text = self.font.render(self.text, 0, self.textColor)
                textWin = text.get_rect(center=(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
                self.surface.blit(text, textWin)
        
        else:
            self.surface.blit(self.image, (self.rect.centerx - self.image.get_width() // 2, self.rect.centery - self.image.get_height() // 2))