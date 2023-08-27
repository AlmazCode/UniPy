import pygame

class ToggleButton:
    def __init__(self, surface, key, func, **args):
        toggle_buttons.append(self)
        self.surface = surface
        self.OI = args.get("image", None)
        self.active_color = args.get("active_color", [130, 130, 130])
        self.non_active_color = args.get("non_active_color", [100, 100, 100])
        self.active_stroke_color = args.get("active_stroke_color", [100, 100, 100])
        self.non_active_stroke_color = args.get("non_active_stroke_color", [70, 70, 70])
        self.render = args.get("render", True)
        self.active = args.get("active", False)
        self.border_radius = args.get("border_radius", -1)
        self.fill_size = args.get("fill_size", 0)
        self.stroke_size = args.get("stroke_size", 0)

        self.func = func
        self.key = key
        self.content = args.get("content", f"('{self.key}')")
        self.cx = args.get("cx", "!n")
        self.cy = args.get("cy", "!n")
        self.width = args.get("width", 200)
        self.height = args.get("height", 50)
        self.x = args.get("x", 0)
        self.y = args.get("y", 0)
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
        if self.OI is not None:
            factor = min(self.rect.width / self.OI.get_width(), self.rect.height / self.OI.get_height())
            self.image = pygame.transform.scale(self.OI, (int(self.OI.get_width() * factor), int(self.OI.get_height() * factor)))
            
        self.active_img = pygame.Surface((self.rect.width, self.rect.height))
        self.non_active_img = pygame.Surface((self.rect.width, self.rect.height))
        
        self.active_img.fill((1, 1, 1))
        self.active_img.set_colorkey((1, 1, 1))
        self.non_active_img.fill((1, 1, 1))
        self.non_active_img.set_colorkey((1, 1, 1))

        pygame.draw.rect(self.active_img, self.active_color, (0, 0, self.rect.width, self.rect.height), self.fill_size, self.border_radius)
        pygame.draw.rect(self.non_active_img, self.non_active_color, (0, 0, self.rect.width, self.rect.height), self.fill_size, self.border_radius)
        
        if self.stroke_size > 0:
            pygame.draw.rect(self.active_img, self.active_stroke_color, (0, 0, self.rect.width, self.rect.height), self.stroke_size, self.border_radius)
            pygame.draw.rect(self.non_active_img, self.non_active_stroke_color, (0, 0, self.rect.width, self.rect.height), self.stroke_size, self.border_radius)

    def press(self):
        self.active = not self.active
        if self.func is not None:
            eval(f"self.func{self.content}")

    def update(self):
        if self.render:
            self.surface.blit(self.active_img if self.active else self.non_active_img, self.rect)
            if self.active:
                if isinstance(self.image, pygame.Surface):
                    self.surface.blit(self.image, (self.rect.centerx - self.image.get_width() // 2, self.rect.centery - self.image.get_height() // 2))

toggle_buttons = []