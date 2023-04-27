import pygame

pygame.init()

# enigine settings
version = "pre-alpha 0.2"

# create engine display
win = pygame.display.set_mode((0, 0), vsync = 0)
clock = pygame.time.Clock()
pygame.display.set_caption(f"UniPy {version}")

# start display settings
width = win.get_width()
height = win.get_height()
AppWidth = width
AppHeight = height - 80
fps = 60
dt = 0 # delta time

# app display
winApp = pygame.Surface((AppWidth, AppHeight))

# other settings
lastSelectionObject = None
lastPressedInput = None
IsRightMouseButton = False
scrollForceShowdown = 4
lastSelectionObjectClass = None
isRenameFile = False
isRenameProject = False
isCreateObject = False
isSelector = False
isConsole = False
lastSelectorContent = None

# returns the path to the project
def GPTP():
	return f"./projects/{projects[projectIdx]}/"

LPBFS = None #last pressed button for selector

layer = -1

"""
-1 choose project
0 - editor
1 - app
2 - conductor
3 - project assets conductor
"""

# for project system
modules = []
projects = []
files = []
projectIdx = 0
projectSize = (0,0)
MHFS = []
MHFU = []

# game settings
GBGSC = (255, 255, 255) # game bg start color
GBGC = GBGSC # game bg color

# UI settings
uiTColor = (255, 255, 255) # engine ui text color
uiBgColor = (60, 60, 60) # engine bg color
uiBC = (130, 130, 130) # ui buttons color
uiBPC = (100, 100, 100) # ui buttons pressed color
uiIC = (150, 150, 150) # ui inputs color
uiIPC = (100, 100, 100) # ui inputs pressed color
uiSOHBGC = (50, 50, 50) # ui selection object hierarchy bg color
uiCC = (50, 50, 50) # ui conductor color
uiSOHC = (100, 100, 100) # ui selection object hierarchy color
uiPEC = (100, 100, 100) # ui project elem color
uiCEC = (100, 100, 100) # ui conductor elem color
uiEIC = (255, 255, 255) # ui engine images color

uiPRW = width // 1.5 # ui project rect width
uiPRH = height // 10 # ui project rect height
uiBS = width // 8 if height > 720 else width // 18  # ui buttons size
uiBFS = 1 # ui button font size
uiIW = width // 2 # ui input width
uiIH = uiIW // 4 if height >= width else uiIW // 10 # ui input height
uiSOCP = 10 # start object components pos
uiWBBR = 15 # widgets buttons border radius
uiWIBR = 15 # widgets inputs border radius
uiWPEOEEBR = -1 # widgets project elements, object hierarchy elements border radius
uiISIOISV = 128 # image size in object inspector, small version
uiISIOIBV = 256 # image size in object inspector, big version