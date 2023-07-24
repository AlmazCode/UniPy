import pygame

pygame.init()

EngineVersion = "{EV}"

# create display
winApp = pygame.display.set_mode((0, 0), pygame.RESIZABLE, vsync = 1)
clock = pygame.time.Clock()
pygame.display.set_caption("{AppName}")

AppWidth, AppHeight = winApp.get_size()
fps = 60
WR = pygame.Rect(0, 0, AppWidth, AppHeight)
AppStarted = True
MBP = None

projectSize = (0, 0)
EIK = "00000.png"
version = "{VR}"
files = []
dirs = []
MHFU = []

GBGSC = (255, 255, 255)
GBGC = GBGSC