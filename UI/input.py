import pygame

pygame.init()

class Input:
    def __init__(self, surface, func, **args):
        if args.get("ATL", True):
            inputs.append(self)

        self.noText = args.get("noText", "Text")   # текст который будет отоброжаться когда текст input будет пустой
        self.text = args.get("text", "")  # текст input
        
        self.textColor = args.get("textColor", (255, 255, 255))  # цвет текста
        self.color = args.get("color", (150, 150, 150))  # цвет input
        self.pressedColor = args.get("pressedColor", (100, 100, 100))   # цвет input когда она будет нажата

        self.cursorColor = args.get("cursorColor", (0, 150, 255))   # цвет курсора
        
        self.StartTime = 30
        self.time = 30
        self.direct = -1

        self.maxChars = args.get("maxChars", 16)   # максимальное количество символов в input
        
        self.textEnd = 0

        self.mode = 0   # режим отрисовки текста
        self.render = args.get("render", True)   # переменная, отвечающая за отрисовку input на экране, если == True, то input будет рисоваться, иначе нет.
        self.borderRadius = args.get("borderRadius", -1)   # уровень сглаживания углов у кнопки, если == -1, то сглаживание не будет
        self.fillSize = args.get("fillSize", 0)   # уровень заливки кнопки, если == 0, то будет заливаться полностью

        self.surface = surface   # окно на котором будет рисоваться кнопка
        
        self.key = args.get("key", "")
        self.func = func
        self.content = args.get("content", "()")

        self.rect = pygame.Rect(args.get("x", 10), args.get("y", 10), args.get("width", 200), args.get("height", 50))
        
        self.startX = self.rect.x
        self.startY = self.rect.y
        
        self.fontSize = self.rect.height // 2 # размер шрифта
        self.fontPath = args.get("fontPath", None)  # путь до шрфита, если == None, будет использоваться стандартый
        self.font = pygame.font.Font(self.fontPath, self.fontSize)   # шрифт
    
    def hasPress(self, pos):
         if self.rect.collidepoint(pos):
         	self.mode = 1
         	pygame.key.start_text_input()
         	return True
         elif pos == (-1, -1):
         	self.mode = 1
         	pygame.key.start_text_input()
         	return True
         return False
    
    def hasUnPress(self, pos, closeKeyboard = True):
        if not self.rect.collidepoint(pos):
	        self.mode = 0
	        if closeKeyboard: pygame.key.stop_text_input()
	        if self.func != None:
	            eval(f"self.func{self.content}")
	            return True
	        return False
    
    def checkText(self):
        self.textEnd = 0
        try:
            while 1:
                tx = self.font.render(self.text[self.textEnd:-1] + self.text[-1], 1, (255, 255, 255))
                rect = pygame.Rect(tx.get_width(), 0, 0, 0)

                if rect.right + 20 > self.rect.width:
                    self.textEnd += 1
                    continue
                else: break
        except: pass
    
    # функция которая добавляет символ в текст
    def Press(self, key):

        if self.render and self.mode == 1:
            
            if key == "ETR":
                pygame.key.stop_text_input()
                self.mode = 0
                if self.func != None:
                    eval(f"self.func{self.content}")

            # добавление символа в текст
            if key != "BS" and key != "ETR" and self.mode == 1 and len(self.text) < self.maxChars:
                self.text += key

                # проверка не выходит ли текст за границы input, если да, то текст будет сдвинут влево на один символ
                try:
                    while 1:
                        tx = self.font.render(self.text[self.textEnd:-1] + self.text[-1], 1, (255, 255, 255))
                        rect = pygame.Rect(tx.get_width(), 0, 0, 0)

                        if rect.right + 20 > self.rect.width:
                            self.textEnd += 1
                            continue
                        else:
                            break
                except:
                    pass
            
            # удаление последнего символа в тексте
            elif key == "BS" and self.mode == 1 and self.text != '':
                self.text = self.text[:-1]
                if self.textEnd > 0: self.textEnd -= 1

                # проверка не выходит ли текст за границы input, если да, то текст будет сдвинут влево на один символ
                try:
                    while 1:
                        tx = self.font.render(self.text[self.textEnd:-1] + self.text[-1], 1, (255, 255, 255))
                        rect = pygame.Rect(tx.get_width(), 0, 0, 0)

                        if rect.right + 20 > self.rect.width:
                            self.textEnd += 1
                            continue
                        else:
                            break
                except:
                    pass
    
    # функция обвноляющая весь input и взоимодействие с ней
    def update(self):
        if self.render:
            if self.mode == 1:

                if self.direct == -1:
                    self.time -= 1
                    if self.time <= 0: self.direct = 1
                else:
                    self.time += 1
                    if self.time >= self.StartTime: self.direct = -1

            mBT = pygame.mouse.get_pressed()
            mx, my = pygame.mouse.get_pos()
            
            self.draw()

    def draw(self):

        # отрисовка input от зависимости переменной [mode]
        if self.mode == 0:
            pygame.draw.rect(self.surface, self.color, self.rect, self.fillSize, self.borderRadius)
        elif self.mode == 1:
            pygame.draw.rect(self.surface, self.pressedColor, self.rect, self.fillSize, self.borderRadius)
        
        # если текст в input пустой
        if self.text == '':
            noText = self.font.render(self.noText, 1, self.textColor)
            noText.set_alpha(128)
            textWin = noText.get_rect(center=((self.rect.x + noText.get_width() // 2) + 5, self.rect.centery))

            self.surface.blit(noText, textWin)
        
        # иначе
        else:
            Text = self.font.render(self.text[self.textEnd:], 0, self.textColor)
            textWin = Text.get_rect(center=((self.rect.x + Text.get_width() // 2) + 5, self.rect.centery))

            self.surface.blit(Text, textWin)
            rect = pygame.Rect(Text.get_width(), 0, 0, 0)

            # отрисовка курсора
            if self.mode == 1 and self.direct == -1 and rect.x + 20 < self.rect.width:
                pygame.draw.rect(self.surface, self.cursorColor, (self.rect.x + Text.get_width() + 10, self.rect.centery - self.fontSize // 2, self.fontSize // 12, self.fontSize))

inputs = []