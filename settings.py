import pygame, re, os
import pather as pt

pygame.init()

# enigine settings
version = "alpha 0.1.1"
# engine development started on 02/19/2023

# create engine display
win = pygame.display.set_mode((0, 0), pygame.RESIZABLE, vsync = 1)
clock = pygame.time.Clock()
pygame.display.set_caption(f"UniPy {version}")

# start display settings
width, height = win.get_size()
AppWidth = width
AppHeight = height - 80
fps = 60
WR = pygame.Rect(0, 0, AppWidth, AppHeight)

# app display
winApp = pygame.Surface((AppWidth, AppHeight))

# other settings
lastSelectionObject = None
lastPressedInput = None
scrollSpeed = 1
lastSelectionObjectClass = None
isRenameFile = False
isRenameProject = False
isCreateObject = False
isSelector = False
isConsole = False
lastSelectorContent = None
exportProjectPath = pt._defaultPath
MP, MBP = None, None

LPBFS = None # last pressed button for selector

drawingLayer = -1

# for project system
modules = []
projects = []
files = []
projectIdx = 0
projectSize = (0, 0)
MHFU = []

# game settings
GBGSC = (255, 255, 255) # game bg start color
GBGC = GBGSC # game bg color

# UI settings for the engine's graphical user interface

# Colors for various UI elements
uiTColor = (255, 255, 255)  # Text color for the engine UI
uiBgColor = (60, 60, 60)  # Background color for the engine UI
uiBC = (130, 130, 130)  # UI buttons color
uiBPC = (100, 100, 100)  # UI buttons pressed color
uiIC = (150, 150, 150)  # UI inputs color
uiIPC = (100, 100, 100)  # UI inputs pressed color
uiSOHTC = (255, 255, 255)  # UI selection object hierarchy text color
uiPSEC = (30, 144, 255)  # UI project selected element color
uiSOHSEC = (30, 144, 255)  # UI selection object hierarchy selected element color
uiCC = (50, 50, 50)  # UI conductor color
uiCSEC = (30, 144, 255)  # UI conductor selected element color
uiSOHC = (50, 50, 50)  # UI selection object hierarchy color
uiPMC = (60, 60, 60)  # UI project manager color
uiSOHEC = (100, 100, 100)  # UI selection object hierarchy element color
uiPEC = (100, 100, 100)  # UI project manager element color
uiCEC = (100, 100, 100)  # UI conductor element color
uiEIC = (255, 255, 255)  # UI engine images color
uiCBC = (60, 60, 60)  # UI console background color
uiCTC = (255, 255, 255)  # UI conductor text color
uiPMTC = (255, 255, 255)  # UI project manager text color
uiITC = (255, 255, 255)  # UI inputs text color
uiPBBGC = (120, 120, 120)  # UI progress bar background color
uiPBTC = (255, 255, 255)  # UI progress bar text color
uiPBC = (0, 255, 0)  # UI progress bar color
uiPBBC = (140, 140, 140)  # UI progress bar background color
uiMBGC = (80, 80, 80)  # UI messages background color
uiMTC = (255, 255, 255)  # UI messages text color
uiCCBGC = (40, 44, 52)  # UI conductor code background color
uiCCKC = (177, 13, 201)  # UI conductor code keyword color
uiCCFC = (0, 116, 217)  # UI conductor code function color
uiCCCC = (170, 170, 170)  # UI conductor code comment color
uiCCSC = (46, 204, 64)  # UI conductor code string color
uiCCNC = (255, 165, 0)  # UI conductor code number color
uiCCVC = (231, 76, 60)  # UI conductor code variable color

# UI element dimensions
uiPRW = width // 1.5  # UI project rect width
uiPRH = height // 10  # UI project rect height
uiBS = width // 8 if height > 720 else width // 18  # UI buttons size, dynamically adjusted for screen size
if pt._platform != "Android":
    uiBS = uiBS // 3.5  # If not on Android, further reduce the button size
uiBFS = 1  # UI button font size
uiIW = width // 2 if height > width else width // 4  # UI input width
uiIH = uiIW // 4  # UI input height, dynamically adjusted for screen orientation
uiSOCP = 10  # Start object components position
uiWBBR = 15  # Widgets buttons border radius
uiWIBR = 15  # Widgets inputs, toggle buttons border radius
uiWPEOEEBR = 15  # Widgets project elements, object hierarchy elements border radius
uiPBBR = 15  # Progress bar border radius
uiMBR = 15  # Messages border radius
uiSOHBGBR = 15 # UI selection object hierarchy bg border radius
uiMFS = 0  # Messages fill size
uiPMFS = 0  # Project manager fill size
uiSOHFL = 0  # UI selection object hierarchy fill size
uiSOHBGFL = 0 # UI selection object hierarchy bg fill size
uiISIOI = 196  # Image size in the object inspector
uiFont = f"assets{pt.s}calibri.ttf" # Engine UI font path
uiTFont = pygame.font.Font(uiFont, height // 20  if height > 720 else height // 10) # Engine UI font size (big)
uiTSFont = pygame.font.Font(uiFont, height // 32 if height > 720 else height // 18) # Engine UI font size (small)

# images that won't change their color
uiII = ["error", "message", "warning"]

config_name = "names" # config names, you can have several (separated by commas)
load_config = False # if true it will load the config files from "configs" folder
not_found_cfgs = []

if load_config:
    possible_configs = os.listdir("configs/")
    for cfg in config_name.split(","):
        if cfg + ".txt" in possible_configs:
            with open(f"configs/{cfg.strip()}.txt", "r") as config:
                get = config.read().split("\n")
                for obj in get:
                    exec(obj)
        else: not_found_cfgs.append(cfg)