import UniPy as up
import pygame
import random

width, height = up.st.winApp.get_size()
num_colors = 0
colors = []

def Start():
    global colors, num_colors
    
    num_colors = up.GetObj("controller").GetModule("controller").colors
    colors = [pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(num_colors)]

def onFingerDown(_id, pos):
    if _id == 1:
        up.reloadApp()

def Update():
    for y in range(height):
        color_index = int(y / height * (num_colors - 1))
        color_start = colors[color_index]
        color_end = colors[color_index + 1]

        progress = (y / height) * (num_colors - 1) - color_index
        r = int(color_start.r + progress * (color_end.r - color_start.r))
        g = int(color_start.g + progress * (color_end.g - color_start.g))
        b = int(color_start.b + progress * (color_end.b - color_start.b))
        current_color = pygame.Color(r, g, b)
        
        pygame.draw.line(up.st.winApp, current_color, (0, y), (width, y))