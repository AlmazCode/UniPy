import pygame

class ToggleButton:
    def __init__(self, surface, key, func, **args):
        toggle_buttons.append(self)
        self.surface = surface
        self.OI = args.get("image", None)
        self.color = args.get("color", (150, 150, 150))
        self.active = args.get("active", False)
        self.border_radius = args.get("borderRadius", -1)
        self.fill_size = args.get("fillSize", 0)
        self.rect = pygame.Rect(args.get("x", 0), args.get("y", 0), args.get("width", 75), args.get("height", 75))

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
        self.cw = pygame.Surface((self.rect.width, self.rect.height))
        self.cw.fill((1, 1, 1))
        self.cw.set_colorkey((1, 1, 1))

        pygame.draw.rect(self.cw, self.color, (0, 0, self.rect.width, self.rect.height), self.fill_size, self.border_radius)

    def press(self):
        self.active = not self.active
        if self.func is not None:
            eval(f"self.func{self.content}")

    def update(self):
        self.surface.blit(self.cw, self.rect)
        if self.active:
            if isinstance(self.image, pygame.Surface):
                self.surface.blit(self.image, (self.rect.centerx - self.image.get_width() // 2, self.rect.centery - self.image.get_height() // 2))

toggle_buttons = []