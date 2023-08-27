import pygame

class Input:
    def __init__(self, surface, func, **args):
        INPUTS.append(self)
        if args.get("ATL", True):
            inputs.append(self)

        self.no_text = args.get("noText", "Text")
        self.text = args.get("text", "")
        self.old_text = self.text
        self.text_color = args.get("text_color", [255, 255, 255])
        self.pressed_text_color = args.get("pressed_text_color", [225, 225, 225])
        self.color = args.get("color", [150, 150, 150])
        self.pressed_color = args.get("pressed_color", [100, 100, 100])
        self.stroke_color = args.get("stroke_color", [100, 100, 100])
        self.pressed_stroke_color = args.get("pressed_stroke_color", [70, 70, 70])
        self.cursor_color = args.get("cursor_color", [0, 150, 255])
        self.start_time = args.get("cursor_tick_time", 30)
        self.time = self.start_time
        self.direction = -1
        self.max_chars = args.get("max_chars", 256)
        self.text_end = 0
        self.mode = 0
        self.render = args.get("render", True)
        self.border_radius = args.get("border_radius", -1)
        self.fill_size = args.get("fill_size", 0)
        self.surface = surface
        self.key = args.get("key", "")
        self.func = func
        self.content = args.get("content", "()")
        self.cx = args.get("cx", "!n")
        self.cy = args.get("cy", "!n")
        self.width = args.get("width", 200)
        self.height = args.get("height", 50)
        self.x = args.get("x", 0)
        self.y = args.get("y", 0)
        self.stroke_size = args.get("stroke_size", 0)
        self.text_offset = args.get("text_offset", 0)
        self.font_path = args.get("fontPath", None)
        self.adjust_dimensions_and_positions()
    
    def adjust_dimensions_and_positions(self):
        x = eval(self.x) if type(self.x) == str else self.x
        y = eval(self.y) if type(self.y) == str else self.y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        if self.cx == "right":
            self.rect.x = self.surface.get_width() - self.width + x
        elif self.cx == "center":
            self.rect.x = self.surface.get_width() // 2 - self.width // 2 + x
        if self.cy == "bottom":
            self.rect.y = self.surface.get_height() - self.height + y
        elif self.cy == "center":
            self.rect.y = self.surface.get_height() // 2 + self.height // 2 + y
        self.font_size = self.rect.height // 2
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.cdw = pygame.Surface((self.rect.width, self.rect.height))
        self.cpw = pygame.Surface((self.rect.width, self.rect.height))

        self.cdw.fill((1, 1, 1))
        self.cpw.fill((1, 1, 1))
        self.cdw.set_colorkey((1, 1, 1))
        self.cpw.set_colorkey((1, 1, 1))

        pygame.draw.rect(self.cdw, self.color, (0, 0, self.rect.width, self.rect.height), self.fill_size, self.border_radius)
        pygame.draw.rect(self.cpw, self.pressed_color, (0, 0, self.rect.width, self.rect.height), self.fill_size, self.border_radius)
        
        if self.stroke_size > 0:
            pygame.draw.rect(self.cdw, self.stroke_color, (0, 0, self.rect.width, self.rect.height), self.stroke_size, self.border_radius)
            pygame.draw.rect(self.cpw, self.pressed_stroke_color, (0, 0, self.rect.width, self.rect.height), self.stroke_size, self.border_radius)

    def set_old_text(self):
        self.text = self.old_text
        self.end_text = 0
        self.check_text()

    def has_press(self, pos):
        if self.rect.collidepoint(pos) and self.mode == 0:
            self.old_text = self.text
            self.mode = 1
            pygame.key.start_text_input()
            return True
        elif pos == (-1, -1):
            self.mode = 1
            pygame.key.start_text_input()
            return True
        return False

    def has_unpress(self, pos, close_keyboard=True):
        if not self.rect.collidepoint(pos) and self.mode == 1:
            self.mode = 0
            if close_keyboard:
                pygame.key.stop_text_input()
            if self.func is not None:
                eval(f"self.func{self.content}")
                return True
        return False

    def check_text(self):
        self.text_end = 0
        try:
            while True:
                tx = self.font.render(self.text[self.text_end:-1] + self.text[-1], 1, (255, 255, 255))
                rect = pygame.Rect(tx.get_width(), 0, 0, 0)

                if rect.right + 20 > self.rect.width:
                    self.text_end += 1
                    continue
                else:
                    break
        except:
            pass

    def press(self, key):

        if self.render and self.mode == 1:

            if key == "ETR":
                pygame.key.stop_text_input()
                self.mode = 0
                if self.func is not None:
                    eval(f"self.func{self.content}")

            if key != "BS" and key != "ETR" and self.mode == 1 and len(self.text) < self.max_chars:
                self.text += key

                try:
                    while True:
                        tx = self.font.render(self.text[self.text_end:-1] + self.text[-1], 1, (255, 255, 255))
                        rect = pygame.Rect(tx.get_width(), 0, 0, 0)

                        if rect.right + 20 > self.rect.width:
                            self.text_end += 1
                            continue
                        else:
                            break
                except:
                    pass

            elif key == "BS" and self.mode == 1 and self.text != '':
                self.text = self.text[:-1]
                if self.text_end > 0:
                    self.text_end -= 1

                try:
                    while True:
                        tx = self.font.render(self.text[self.text_end:-1] + self.text[-1], 1, (255, 255, 255))
                        rect = pygame.Rect(tx.get_width(), 0, 0, 0)

                        if rect.right + 20 > self.rect.width:
                            self.text_end += 1
                            continue
                        else:
                            break
                except:
                    pass

    def update(self):
        if self.render:
            if self.mode == 1:

                if self.direction == -1:
                    self.time -= 1
                    if self.time <= 0:
                        self.direction = 1
                else:
                    self.time += 1
                    if self.time >= self.start_time:
                        self.direction = -1

            mBT = pygame.mouse.get_pressed()
            mx, my = pygame.mouse.get_pos()

            self.draw()

    def draw(self):
        self.surface.blit(self.cdw if self.mode == 0 else self.cpw, self.rect)

        if self.text == '':
            no_text = self.font.render(self.no_text, 0, self.text_color if self.mode == 0 else self.pressed_text_color)
            no_text.set_alpha(128)

            self.surface.blit(no_text, (self.rect.x + 10 + self.text_offset, self.rect.y + no_text.get_height() // 2))

        else:
            text = self.font.render(str(self.text)[self.text_end:], 0, self.text_color if self.mode == 0 else self.pressed_text_color)

            self.surface.blit(text, (self.rect.x + 10 + self.text_offset, self.rect.centery - text.get_height() // 2))

            if self.mode == 1 and self.direction == -1 and text.get_width() + 20 < self.rect.width:
                pygame.draw.rect(self.surface, self.cursor_color, (self.rect.x + text.get_width() + 15 + self.text_offset, self.rect.centery - self.font_size // 2, self.font_size // 12, self.font_size))

inputs = []
INPUTS = []