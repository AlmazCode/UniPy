import pygame

class Message:
    def __init__(self, surface, **args):
        self.surface = surface
        messages.append(self)
        
        self.color = args.get("color", [80, 80, 80])
        self.fill_size = args.get("fill_size", 0)
        self.transparent = 0
        self.border_radius = args.get("border_radius", -1)
        self.stroke_size = args.get("stroke_size", 0)
        self.text_color = args.get("text_color", [255, 255, 255])
        self.stroke_color = args.get("stroke_color", [60, 60, 60])
        self.width = args.get("width", self.surface.get_width() // 2)
        self.height = args.get("height", self.surface.get_height() // 24 if self.surface.get_width() < self.surface.get_height() else self.surface.get_height() // 12)
        self.OM = args.get("message", "{msg}")
        self.font_path = args.get("font", None)
        self.stop_time = args.get("stop_time", 90)
        self.start_time = (255 - 0) / args.get("start_time", 30)
        self.end_time = (0 - 255) / args.get("end_time", 30)
        self.state = 0
        self.ADP()
        self.x = args.get("x", self.surface.get_width() // 2 - self.width // 2)
        self.y = args.get("y", None)
        if self.y is None:
            self.y = self.surface.get_height() - self.height - 10
        self.ifDel = False
    
    def ADP(self):
        self.message = self.OM
        self.font = pygame.font.Font(self.font_path, int(self.height / 1.7))
        idx = 0
        x = 10
        while 1:
            if idx == len(self.message) - 1: break
            if x + self.font.size(self.message[idx])[0] > self.width - self.font.size(self.message[idx][-1])[0]:
                if self.message[idx] not in ["\n", " "]:
                    g = list(self.message)
                    g.insert(idx, "\n")
                    self.message = "".join(g)
                    x = 10
            elif self.message[idx] == "\n": x = 10
            else: x += self.font.size(self.message[idx])[0]
            idx += 1
        self.textes = []
        for i in self.message.split("\n"):
            self.textes.append(self.font.render(i, 0, self.text_color))
            self.height += self.textes[-1].get_height()
        self.height -= self.textes[-1].get_height()
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((1, 1, 1))
        self.image.set_colorkey((1, 1, 1))
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height), self.fill_size, self.border_radius)
        
        if self.stroke_size > 0:
            pygame.draw.rect(self.image, self.stroke_color, (0, 0, self.width, self.height), self.stroke_size, self.border_radius)
        
        y = 10
        for tx in self.textes:
            self.image.blit(tx, (10, y))
            y += tx.get_height()
    
    def update(self):
        if self.transparent >= 255 and self.state == 0: self.state = 1
        if self.state == 1:
            if self.stop_time == 0:
                self.state = 2
            else:
                self.stop_time -= 1
        if self.transparent <= 0 and self.state == 2:
            self.ifDel = True
        if self.state != 1:
            self.transparent += self.start_time if self.state == 0 else self.end_time
        self.image.set_alpha(self.transparent)
        self.surface.blit(self.image, (self.x, self.y))

messages = []