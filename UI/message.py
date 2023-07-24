import pygame

class Message:
    def __init__(self, surface, **args):
        self.surface = surface
        messages.append(self)
        
        self.bg_color = args.get("bgColor", (80, 80, 80))
        self.fill_size = args.get("fillSize", 0)
        self.transparent = 0
        self.border_radius = args.get("borderRadius", -1)
        self.text_color = args.get("textColor", (255, 255, 255))
        self.width = args.get("width", self.surface.get_width() // 2)
        self.height = args.get("height", self.surface.get_height() // 24 if self.surface.get_width() < self.surface.get_height() else self.surface.get_height() // 12)
        self.OM = args.get("message", "{msg}")
        self.fontPath = args.get("font", None)
        
        self.stopTime = args.get("stopTime", 90)
        self.startTime = (255 - 0) / args.get("startTime", 30)
        self.endTime = (0 - 255) / args.get("endTime", 30)
        self.state = 0
        self.ADP()
        self.oX = args.get("oX", 0)
        self.oY = args.get("oY", 0)
        self.x = args.get("x", self.surface.get_width() // 2 - self.width // 2) + args.get("oX", 0)
        self.y = args.get("y", self.surface.get_height() - self.height - 10) + args.get("oY", 0)
    
    def ADP(self):
        self.message = self.OM
        self.font = pygame.font.Font(self.fontPath, int(self.height / 1.7))
        idx = 0
        x = 10
        while 1:
            if idx == len(self.message) - 1: break
            if x + self.font.size(self.message[idx])[0] > self.width:
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
        pygame.draw.rect(self.image, self.bg_color, (0, 0, self.width, self.height), self.fill_size, self.border_radius)
        y = 10
        for tx in self.textes:
            self.image.blit(tx, (10, y))
            y += tx.get_height()
    
    def update(self):
        if self.transparent >= 255 and self.state == 0: self.state = 1
        if self.state == 1:
            if self.stopTime == 0:
                self.state = 2
            else: self.stopTime -= 1
        if self.transparent <= 0 and self.state == 2: messages.remove(self)
        if self.state != 1: self.transparent += self.startTime if self.state == 0 else self.endTime
        self.image.set_alpha(self.transparent)
        self.surface.blit(self.image, (self.x, self.y))

messages = []