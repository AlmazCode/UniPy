import pygame, re, os
import pather as pt
import json

pygame.init()

# enigine settings
version = "alpha 0.1.6"
# engine development started on 02/19/2023

# create engine display
win = pygame.display.set_mode((0, 0) if pt._platform == "Android" else (1280, 720), pygame.RESIZABLE, vsync = 1)
clock = pygame.time.Clock()
pygame.display.set_caption(f"UniPy {version}")

# start display settings
width, height = win.get_size()
AppWidth = width
AppHeight = height - (80 if pt._platform == "Android" else 40)
fps = 60
WR = pygame.Rect(0, 0, AppWidth, AppHeight)

# app display
winApp = pygame.Surface((AppWidth, AppHeight))

# other settings
lastSelectionObject = None
lastPressedInput = None
scrollSpeed = 1
mouseScrollSpeed = 15
lastSelectionObjectClass = None
isRenameFile = False
isRenameProject = False
isCreateObject = False
isSelector = False
isConsole = False
lastSelectorContent = None
exportProjectPath = pt._defaultPath
MP, MBP = None, None
LPBFS = None
drawingLayer = -1
scollPos = None

# for project system
modules = []
projects = []
files = []
projectIdx = -1
projectSize = (0, 0)
MHFU = []

UI_Settings = {}
settingsPath = f".{pt.s}Settings{pt.s}"
if os.path.exists(settingsPath):
    for setting in os.listdir(settingsPath):
        if setting.split(".")[-1] == "json":
            with open(f"{settingsPath}{setting}", "r") as f:
                inf = json.load(f)
                UI_Settings.update(inf)

# game settings
GBGSC = (255, 255, 255) # game bg start color
GBGC = GBGSC # game bg color

# Colors for various UI elements
mainSettings = UI_Settings.get("Main")
if mainSettings is not None:
    uiTColor = mainSettings.get("text_color", [255, 255, 255])
    uiBgColor = mainSettings.get("bg_color", [60, 60, 60])
    uiSCIOI = mainSettings.get("stroke_color_in_object_inspector", [130, 130, 130])
    uiEIC = mainSettings.get("engine_images_color", [255, 255, 255])
    uiISIOI = mainSettings.get("image_size_in_object_inspector", 196)
    uiFont = mainSettings.get("font", "calibri.ttf")
else:
    uiTColor = [255, 255, 255]
    uiBgColor = [60, 60, 60]
    uiSCIOI = [130, 130, 130]
    uiEIC = [255, 255, 255]
    uiISIOI = 196
    uiFont = f"calibri.ttf"

uiFont = f"assets{pt.s}{uiFont}"

if pt._platform == "Android":
    uiTFontSize = height // 20  if height > width else height // 10
    uiTSFontSize = height // 32 if height > width else height // 18
    uiIW = width // 2 if height > width else width // 4
    uiIH = uiIW // 4
    uiBS = width // 8 if height > width else width // 18
else:
    uiTFontSize = height // 32  if height > width else height // 18
    uiTSFontSize = height // 50 if height > width else height // 25
    uiIW = width // 2 if height > width else width // 4
    uiIH = uiIW // 6
    uiISIOI /= 2
    uiBS = width // 10 if height > width else width // 20

uiTFont = pygame.font.Font(uiFont, uiTFontSize)
uiTSFont = pygame.font.Font(uiFont, uiTSFontSize)

# engine images that won't change their color
uiII = ["error", "message", "warning", "ENGINE_ICON", "engineIcon"]