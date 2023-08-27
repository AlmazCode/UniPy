import pygame
import settings as st


class Button:
    def __init__(self, surface, **args):
        BUTTONS.append(self)
        self.surface = surface
        self.color = args.get("color", [130, 130, 130])
        self.pressed_color = args.get("pressed_color", [100, 100, 100])
        self.stroke_color = args.get("stroke_color", [100, 100, 100])
        self.pressed_stroke_color = args.get("pressed_stroke_color", [70, 70, 70])
        self.func = args.get("func", None)
        self.fast = args.get("fast", False)
        self.mode = 0
        self.press = False
        self.render = args.get("render", True)
        self.border_radius = args.get("border_radius", -1)
        self.fill_size = args.get("fill_size", 0)
        self.stroke_size = args.get("stroke_size", 0)
        self.key = args.get("key", "")
        self.content = args.get("content", "()")
        self.cx = args.get("cx", "!n")
        self.cy = args.get("cy", "!n")
        self.width = args.get("width", 100)
        self.height = args.get("height", 100)
        self.x = args.get("x", 0)
        self.y = args.get("y", 0)
        self.image = args.get("image", None)
        self.original_image = self.image
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
        self.static_img = pygame.Surface((self.rect.width, self.rect.height))
        self.pressed_img = pygame.Surface((self.rect.width, self.rect.height))
        self.static_img.fill((1, 1, 1))
        self.pressed_img.fill((1, 1, 1))
        self.static_img.set_colorkey((1, 1, 1))
        self.pressed_img.set_colorkey((1, 1, 1))
        
        pygame.draw.rect(self.static_img, self.color, (0, 0, self.rect.width, self.rect.height), self.fill_size, self.border_radius)
        pygame.draw.rect(self.pressed_img, self.pressed_color, (0, 0, self.rect.width, self.rect.height), self.fill_size, self.border_radius)
        
        if self.stroke_size > 0:
            pygame.draw.rect(self.static_img, self.stroke_color, (0, 0, self.rect.width, self.rect.height), self.stroke_size, self.border_radius)
            pygame.draw.rect(self.pressed_img, self.pressed_stroke_color, (0, 0, self.rect.width, self.rect.height), self.stroke_size, self.border_radius)
        
        if self.image is not None:
            factor = min(self.rect.width / self.image.get_width(), self.rect.height / self.image.get_height())
            self.image = pygame.transform.scale(self.original_image, (int(self.image.get_width() * factor), int(self.image.get_height() * factor)))

    def update(self):
        if self.render:

            if not self.fast:
                if st.MBP and self.rect.collidepoint(st.MP) and not self.press:
                    self.mode = 1
                    self.press = True

                if not st.MBP and self.press and self.rect.collidepoint(st.MP):
                    if self.func is not None:
                        eval(f"self.func{self.content}")
                    self.mode = 0
                    self.press = False

                if not self.rect.collidepoint(st.MP) and self.press and st.MBP:
                    self.mode = 0
                    self.press = False

                if not self.rect.collidepoint(st.MP) and not self.press and not st.MBP:
                    self.mode = 0
            else:
                if st.MBP and self.rect.collidepoint(st.MP):
                    self.mode = 1
                    if self.func is not None:
                        eval(f"self.func{self.content}")
                    self.press = True

                if not st.MBP and self.press and self.rect.collidepoint(st.MP):
                    self.mode = 0
                    self.press = False

                if not self.rect.collidepoint(st.MP) and self.press and st.MBP:
                    self.mode = 0
                    self.press = False

                if not self.rect.collidepoint(st.MP) and not self.press and not st.MBP:
                    self.mode = 0

            self.draw()

    def draw(self):
        self.surface.blit(self.static_img if self.mode == 0 else self.pressed_img, self.rect)

        if self.image is not None:
            self.surface.blit(self.image, (self.rect.centerx - self.image.get_width() // 2, self.rect.centery - self.image.get_height() // 2))

BUTTONS = []