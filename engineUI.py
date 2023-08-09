from UI import (
	button,
	input,
	toggleButton,
	conductor,
	projectManager,
	sohManager,
	console,
	progressBar,
	message
)

from objects.object import Object
from objects.text import Text
from exporter import build

import engineOUAR as ouar
import UniPy as pe
import settings as st
import os, traceback, shutil, copy, re, sys, collections, zipfile, pygame, importlib, ast
import pather as pt

pygame.mixer.init()

# settings
error = False
objComponents = []
compiledTextes_FOC = []
CTFOCXOF = []
CSTN = []
CSTN_POS = []
SISL = None
OPII = 0

# import engine assets
uiEngineImages = {}
imgs = os.listdir("assets")
for img in [file for file in imgs if file.split(".")[-1] not in ["otf", "ttf"]]:
    uiEngineImages[img.split(".", 1)[0]] = pygame.image.load(f"assets{pt.s}{img}").convert()

uiEngineImages["down"] = pygame.transform.rotate(uiEngineImages["up"], 180)
uiEngineImages["back"] = pygame.transform.rotate(uiEngineImages["up"], 90)
uiEngineImages["plus"] = pygame.transform.rotate(uiEngineImages["cancel"], 45)
uiEngineImages["ENGINE_ICON"] = pygame.transform.smoothscale(uiEngineImages["engineIcon"], (int(st.width / 7.5) if st.width <= 720 else st.width // 15, int(st.width / 7.5) if st.width <= 720 else st.width // 15))

# image color redraw
for i in uiEngineImages:
    uiEngineImages[i].set_colorkey((0, 0, 0))
    if i not in st.uiII: uiEngineImages[i].fill(st.uiEIC, special_flags=pygame.BLEND_RGB_MULT)

# object image in inspector
OIII = None
OIIIW, OIIIH = 0, 0

# object font name in inspector
OFNII = None
OFNIIW, OFNIIH = 0, 0

# load projects
PATH = f'.{pt.s}projects'
st.projects = os.listdir(PATH)

# for export project menu
uiEPMST = ["Export path", "Version"]
uiEPMT = None
uiEPME = None

# to choose project
def toCP():
    st.drawingLayer = -1
    pe.objects = []
    pe.objName = []
    pe.objClass = []

def loadProjectInfoData(path):
    if not os.path.exists(f"{path}{pt.s}project_info.txt"):
        with open(f"{path}{pt.s}project_info.txt", "w") as f:
            f.write(f"{st.AppWidth} {st.AppHeight}, 0.1")
    
    inf = open(f"{path}{pt.s}project_info.txt", "r").read().split(",")
    size = inf[0].split(" ")
    vr = inf[1].strip() if len(inf) > 1 else "0.1"
    return (int(size[0]), int(size[1])), vr

# open project
def openProject(idx):
    
    st.projectIdx = idx
    
    st.projects = os.listdir(PATH)
    st.files, st.dirs = loadAllFilesFromDir(f"{PATH}{pt.s}{st.projects[st.projectIdx]}")
    PB.start(PB.title, len(st.files))
    
    # set project size
    st.projectSize = loadProjectInfoData(f"{PATH}{pt.s}{st.projects[idx]}")[0]
    pe.pWidth, pe.pHeight = st.projectSize
    
    # load all files from project
    for i in st.files:
    	
    	PB.setItemName(i)
    	drawProjects()
    	PB.update()
    	for msg in message.messages: msg.update()
    	pygame.display.flip()
    	
    	if os.path.splitext(i)[-1] in [".png", ".jpg", ".jpeg"]:
    		txs = pygame.image.load(f"{st.dirs[st.files.index(i)]}{pt.s}{i}").convert_alpha()
    		f = False
    		pe.texturesTSP[i] = pygame.image.load(f"{st.dirs[st.files.index(i)]}{pt.s}{i}").convert_alpha()
    		
    		pe.textures[i] = pygame.image.load(f"{st.dirs[st.files.index(i)]}{pt.s}{i}").convert()
    		
    		replacement_color = (1, 1, 1)
    		
    		# Replace transparent pixels with the replacement color
    		for x in range(txs.get_width()):
    		    for y in range(txs.get_height()):
    		        if list(txs.get_at((x, y)))[-1] == 0:
    		            txs.set_at((x, y), replacement_color)
    		            f = True
    		
    		pe.textures[i] = pygame.Surface(txs.get_size()).convert()
    		pe.textures[i].blit(txs, (0, 0))
    		pe.textures[i].set_colorkey(replacement_color)
    	
    	elif i.split(".")[-1] in pe._audioTypes: pe.audios[i] = pygame.mixer.Sound(f"{st.dirs[st.files.index(i)]}{pt.s}{i}")
    	
    	PB.itemLoaded()
    	drawProjects()
    	PB.update()
    	for msg in message.messages: msg.update()
    	pygame.display.flip()
        	
    # load game objects
    ouar.loadObjs(pe, f"{PATH}{pt.s}{st.projects[idx]}{pt.s}ObjectInfo.txt")
    
    st.drawingLayer = 0
    PAC.startPath = f".{pt.s}projects{pt.s}{st.projects[idx]}"
    PAC.setPath()
    
    SOHM.oY = 0
    SOHM.elements = pe.objName[:]
    SOHM.normalize()

# functions

def createMessage(surface, text: str, stopTime: int = 90, startTime: int = 30, endTime: int = 30, *args):
    oY = None
    if message.messages:
        oY = message.messages[-1].y - message.messages[-1].image.get_height() - 10
    message.Message(surface, message = text, bgColor = st.uiMBGC, font = st.uiFont, textColor = st.uiMTC, borderRadius = st.uiMBR, fillSize = st.uiMFS, startTime = startTime, endTime = endTime, stopTime = stopTime, y = oY)

# create new project
def createProject():
    c = 1
    if not os.path.exists(f"{PATH}{pt.s}new project"):
        os.makedirs(f"{PATH}{pt.s}new project")
        shutil.copytree(f".{pt.s}Built-in_Scripts", f"{PATH}{pt.s}new project{pt.s}Built-in_Scripts")
    else:
        while 1:
            if not os.path.exists(f"{PATH}{pt.s}new project ({c})"):
                os.makedirs(f"{PATH}{pt.s}new project ({c})")
                shutil.copytree(f".{pt.s}Built-in_Scripts", f"{PATH}{pt.s}new project ({c}){pt.s}Built-in_Scripts")
                break
            else: c += 1
    
    st.projects = os.listdir(PATH)
    PM.elements = st.projects
    PM.normalize()

# create new folder in project assets conductor
def createDirectory():
    c = 1
    if not os.path.exists(f"{PAC.thisPath}{pt.s}new folder"):
        os.makedirs(f"{PAC.thisPath}{pt.s}new folder")
    else:
        while 1:
            if not os.path.exists(f"{PAC.thisPath}{pt.s}new folder ({c})"):
                os.makedirs(f"{PAC.thisPath}{pt.s}new folder ({c})")
                break
            else: c += 1
    
    PAC.reOpenPath()

# download new file to project assets conductor from default conductor
def AddFileToPAC(path):
    
    try:
        if os.path.isdir(path):
            shutil.copytree(path, f"{PAC.thisPath}{pt.s}{file}")
        else:
            shutil.copy(path, PAC.thisPath)
    except: ...
    
    if path.split(".")[-1] in pe._imgTypes:
    	txs = pygame.image.load(path).convert_alpha()
    	f = False
    	pe.textures[path.split(pt.s)[-1]] = pygame.image.load(path).convert()
    	pe.texturesTSP[path.split(pt.s)[-1]] = pygame.image.load(path).convert_alpha()
    	
    	replacement_color = (1, 1, 1)
    	
    	# Replace transparent pixels with the replacement color
    	for x in range(txs.get_width()):
    		for y in range(txs.get_height()):
    			if list(txs.get_at((x, y)))[-1] == 0:
    				txs.set_at((x, y), replacement_color)
    				f = True
    	
    	pe.textures[path.split(pt.s)[-1]] = pygame.Surface(txs.get_size()).convert()
    	pe.textures[path.split(pt.s)[-1]].blit(txs, (0, 0))
    	pe.textures[path.split(pt.s)[-1]].set_colorkey(replacement_color)
    
    elif path.split(".")[-1] in pe._audioTypes:
        pe.audios[path.split(pt.s)[-1]] = pygame.mixer.Sound(path)
    
    PAC.setPath(PAC.thisPath)
    startPACR()
    btCancelCR.func = closeCR

def loadAllFilesFromDir(directory):
    _all = []
    DIRS = []
    for root, dirs, files in os.walk(directory):
        for i in files:
            DIRS.append(root)
            _all.append(i)
    return _all, DIRS

def loadModules(fpm = False):
    global error
    
    for script in st.modules:	
        try: sys.modules.pop(script.__name__)
        except: pass
    st.modules = []
    st.files, st.dirs = loadAllFilesFromDir(f"{PATH}{pt.s}{st.projects[st.projectIdx]}")
    
    for file in st.files:
        if file[-3:] == ".py":
            if fpm:
                PB.setItemName(file)
                drawProjects()
                PB.update()
                for msg in message.messages: msg.update()
                pygame.display.flip()
            try:
                st.modules.append(__import__(f"{st.dirs[st.files.index(file)].replace(pt.s, '.')}.{file[:-3]}"[2:], fromlist=["*"]))
            except Exception as e:
                error = True
                tb = e.__traceback__
                filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                _console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
            
            if fpm:
                PB.itemLoaded()
                drawProjects()
                PB.update()
                for msg in message.messages: msg.update()
                pygame.display.flip()

# copy project
def copyProject():
    shutil.copytree(f"{PATH}{pt.s}{PM.elements[PM.elem_idx]}", f"{PATH}{pt.s}{PM.elements[PM.elem_idx]} (1)")
    
    st.projects = os.listdir(PATH)
    PM.elements = st.projects
    PM.normalize()

def OpenMenuToExportProject():
    vr = loadProjectInfoData(f"{PATH}{pt.s}{PM.elements[PM.elem_idx]}")[1]
    InputSetExportProjectVersion.text = vr
    InputSetExportProjectVersion.check_text()
    AEPME()
    st.drawingLayer = 4

def CloseMenuToExportProject():
    st.drawingLayer = -1

def ExportProject():
    size, vr = loadProjectInfoData(f"{PATH}{pt.s}{PM.elements[PM.elem_idx]}")
    build.createProject(st.exportProjectPath, f"{PATH}{pt.s}{PM.elements[PM.elem_idx]}", PM.elements[PM.elem_idx], PM.elements[PM.elem_idx], size, vr)
    createMessage(st.win, f'The project was successfully exported to path:\n"{st.exportProjectPath}"', stopTime = 120)

# delete project
def deleteFolderInPM():
    shutil.rmtree(f"{PATH}{pt.s}{PM.elements[PM.elem_idx]}")
    
    st.projects = os.listdir(PATH)
    PM.elements = st.projects
    PM.normalize()

# delete file from project assets conductor
def deleteFileInPAC():
    path = f"{PAC.thisPath}{pt.s}{PAC.elements[PAC.elem_idx]}"
    try:
        os.remove(path)
        if path in pe.textures:
        	del pe.textures[path]
        	del pe.texturesTSP[path]
    except:
        shutil.rmtree(path)
    PAC.reOpenPath()

# EDITOR FUNCS
def centerx():
    idx = pe.objName.index(st.lastSelectionObject)
    return st.AppWidth // 2 - pe.objects[idx].width // 2

def centery():
    idx = pe.objName.index(st.lastSelectionObject)
    return st.AppHeight // 2 - pe.objects[idx].height // 2

def top(): return 0
def left(): return 0

def bottom():
    idx = pe.objName.index(st.lastSelectionObject)
    return st.AppHeight - pe.objects[idx].height

def right():
    idx = pe.objName.index(st.lastSelectionObject)
    return st.AppWidth - pe.objects[idx].width

def ww(): return st.AppWidth
def wh(): return st.AppHeight
####

# close object info
def closeObjectInfo():
    
    st.lastSelectionObject = None
    st.isSelector = False

# delete game object
def deleteObj():
    global OPIE
    
    idx = pe.objName.index(SOHM.ename)
    pe.objName.pop(idx)
    pe.objClass.pop(idx)
    pe.objects.pop(idx)
    st.lastSelectionObject = None
    ouar.saveObjs(pe, f"{PATH}{pt.s}{st.projects[st.projectIdx]}{pt.s}ObjectInfo.txt")
    
    SOHM.elements = pe.objName[:]
    SOHM.elem_idx = -1
    SOHM.normalize()

# back path in conductor
def backCR():
    if st.drawingLayer == 2: fileConductor.Back()
    else: PAC.Back()

# start conductor from project assets conductor
def startCRfromPAC():
    st.drawingLayer = 2
    btCancelCR.func = closeCRfromPAC
    
    fileConductor.content = ""
    fileConductor.func = AddFileToPAC
    fileConductor.startPath = pt._defaultPath
    fileConductor.setPath(fileConductor.thisPath)
    
def startCRfromMoveFile():
    st.drawingLayer = 2
    btDeleteCR.render = False
    btDoneCR.render = True
    btDoneCR.func = moveFileInPAC
    
    btCancelCR.func = closeCRfromPAC
    fileConductor.content = ""
    fileConductor.func = None
    fileConductor.startPath = f".{pt.s}projects{pt.s}{st.projects[st.projectIdx]}"
    fileConductor.setPath()

def setExportProjectPath():
    st.exportProjectPath = fileConductor.thisPath
    st.drawingLayer = 4

def startCRfromExportProject():
    st.drawingLayer = 2
    btDeleteCR.render = False
    btDoneCR.render = True
    btDoneCR.func = setExportProjectPath
    
    btCancelCR.func = closeCRfromExportProject
    fileConductor.content = ""
    fileConductor.func = None
    fileConductor.startPath = st.exportProjectPath
    fileConductor.setPath()

def moveFileInPAC():
    try: shutil.move(f"{PAC.thisPath}{pt.s}{PAC.elements[PAC.elem_idx]}", f"{fileConductor.thisPath}")
    except: pass
    
    PAC.setPath(fileConductor.thisPath)
    startPACR()
    btCancelCR.func = closeCR

def startCRfromImportProject():
    st.drawingLayer = 2
    btDeleteCR.render = False
    btDoneCR.render = True
    btDoneCR.func = importProjects
    
    btCancelCR.func = closeCRfromImportProject
    fileConductor.content = ""
    fileConductor.func = None
    fileConductor.startPath = pt._defaultPath
    fileConductor.setPath()

def importProjects():
    if fileConductor.elem_idx != -1:
        if os.path.isdir(f"{fileConductor.thisPath}{pt.s}{fileConductor.elements[fileConductor.elem_idx]}"):
            try: shutil.copytree(f"{fileConductor.thisPath}{pt.s}{fileConductor.elements[fileConductor.elem_idx]}", f"{PATH}{pt.s}{fileConductor.elements[fileConductor.elem_idx]}")
            except: ...
    else:
        fls = os.listdir(fileConductor.thisPath)
        for f in fls:
            if os.path.isdir(f"{fileConductor.thisPath}{pt.s}{f}"):
                try:
                    shutil.copytree(f"{fileConductor.thisPath}{pt.s}{f}", f"{PATH}{pt.s}{f}")
                except: ...
    st.drawingLayer = -1
    st.projects = os.listdir(PATH)
    PM.elements = st.projects
    PM.normalize()

# close conductor from project assets conductor
def closeCRfromPAC():
    st.drawingLayer = 3
    btCancelCR.func = closeCR

def closeCRfromExportProject():
    st.drawingLayer = 4

def closeCRfromImportProject():
    st.drawingLayer = -1

# start conductor
def startCR():
    st.drawingLayer = 2
    btDeleteCR.render = True
    btDoneCR.render = False
    
    fileConductor.func = changeObjProperty
    fileConductor.startPath = f".{pt.s}projects{pt.s}{st.projects[st.projectIdx]}"
    fileConductor.setPath()

def startPACR():
    st.drawingLayer = 3
    PAC.reOpenPath()
    btDeleteCR.render = False
    btDoneCR.render = False
    
# close conductor
def closeCR():
    st.drawingLayer = 0

# rename file in project assets conductor
def startRenameFilePAC():
    st.isRenameFile = True
    st.lastPressedInput = IFFIPAC
    IFFIPAC.text = PAC.elements[PAC.elem_idx]
    IFFIPAC.has_press((-1, -1))
    IFFIPAC.check_text()
    IFFIPAC.rect.y = PAC.getIdxPos(PAC.elem_idx)

# rename project
def startRenameProject():
    st.isRenameProject = True
    st.lastPressedInput = IFRPIPM
    IFRPIPM.text = PM.elements[PM.elem_idx]
    IFRPIPM.has_press((-1, -1))
    IFRPIPM.check_text()
    IFRPIPM.rect.y = PM.get_idx_pos(PM.elem_idx)

# end rename project
def endRenameProject():
    if IFRPIPM.text != "" and PM.elements[PM.elem_idx] != IFRPIPM.text:
	    os.rename(f"{PATH}{pt.s}{PM.elements[PM.elem_idx]}", f"{PATH}{pt.s}{IFRPIPM.text}")
	    st.projects = os.listdir(PATH)
	    PM.elements = st.projects
	    PM.normalize()
	    
    st.isRenameProject = False
    st.lastPressedInput = None

# end rename file in project assets conductor
def endRenameFilePAC():
    
    if IFFIPAC.text != "" and PAC.elements[PAC.elem_idx] != IFFIPAC.text:
        os.rename(f"{PAC.thisPath}{pt.s}{PAC.elements[PAC.elem_idx]}", f"{PAC.thisPath}{pt.s}{IFFIPAC.text}")
        if PAC.elements[PAC.elem_idx] in pe.textures:
            data = pe.textures[PAC.elements[PAC.elem_idx]]
            data2 = pe.texturesTSP[PAC.elements[PAC.elem_idx]]
            del pe.textures[PAC.elements[PAC.elem_idx]]
            del pe.texturesTSP[PAC.elements[PAC.elem_idx]]
            pe.textures[IFFIPAC.text] = data
            pe.texturesTSP[IFFIPAC.text] = data2
        elif PAC.elements[PAC.elem_idx] in pe.audios:
            data = pe.audios[PAC.elements[PAC.elem_idx]]
            del pe.audios[PAC.elements[PAC.elem_idx]]
            pe.audios[IFFIPAC.text] = data

        PAC.setPath(PAC.thisPath)
    
    st.isRenameFile = False
    st.lastPressedInput = None

def renameExportProjectVersion():
    size = loadProjectInfoData(f"{PATH}{pt.s}{PM.elements[PM.elem_idx]}")[0]
    with open(f"{PATH}{pt.s}{PM.elements[PM.elem_idx]}{pt.s}project_info.txt", "w") as f:
            f.write(f"{size[0]} {size[1]}, {InputSetExportProjectVersion.text.strip()}")

# includes a widget for selecting items in object inspector
def startSelectorForObjectInspector(elems, button, key):
	ObjSW.key = key
	button.func = closeSelectorForObjectInspector
	st.lastSelectorContent = button.content
	st.LPBFS = button
	button.content = "(self)"
	st.isSelector = True
	ObjSW.elements = elems
	ObjSW.elem_name = elems
	ObjSW.normalize()
	ObjSW.x = button.rect.x
	ObjSW.y = button.rect.y - ObjSW.surface.get_height() - 10
	ObjSW.elem_idx = eval(f"ObjSW.elements.index(pe.objects[pe.objName.index(st.lastSelectionObject)].{key})")

# turns off the widget for selecting items in object inspector
def closeSelectorForObjectInspector(button):
	st.isSelector = False
	
	button.func = startSelectorForObjectInspector
	button.content = st.lastSelectorContent

# includes a object font name in object inspector
def ADP_OFNII(idx):
    global OFNII, OFNIIW, OFNIIH
    
    text = str(pe.objects[idx].fontPath).split(pt.s)[-1]
    
    try: f = pygame.font.Font(pe.objects[idx].fontPath, 1)
    except: text = "None"

    OFNII = st.uiTSFont.render(text, 0, st.uiTColor)
    OFNIIW, OFNIIH = OFNII.get_size()
    
    if ObjLoadFont.rect.right + OFNII.get_width() + 50 > st.width:

        while 1:
            OFNII = st.uiTSFont.render(text, 0, st.uiTColor)
            if ObjLoadFont.rect.right + OFNII.get_width() + 50 > st.width:
                text = text[:-1]
            else:
                text = text[:-3] + "..."
                OFNII = st.uiTSFont.render(text, 0, st.uiTColor)
                OFNIIW, OFNIIH = OFNII.get_size()
                break

def ADP_OIII(idx):
    global OIII, OIIIW, OIIIH

    try: img = pe.textures[pe.objects[idx].imagePath]
    except: return 0
    
    if ((img.get_height() - img.get_width()) / img.get_width()) * 100 > 24:
        OIII = pygame.transform.scale(img, (int(st.win.get_width() * (st.uiISIOI / st.win.get_height())) if st.win.get_height() > st.win.get_width() else int(st.win.get_height() * (st.uiISIOI / st.win.get_width())), int(st.uiISIOI)))
    elif ((img.get_width() - img.get_height()) / img.get_height()) * 100 > 24:
        OIII = pygame.transform.scale(img, (int(st.win.get_height() * (st.uiISIOI / st.win.get_width())) if st.win.get_height() > st.win.get_width() else int(st.win.get_width() * (st.uiISIOI / st.win.get_height())) , int(st.uiISIOI)))
    else:
        OIII = pygame.transform.scale(img, (int(st.uiISIOI), int(st.uiISIOI)))

    OIII = pygame.transform.flip(OIII, pe.objects[idx].flipX, pe.objects[idx].flipY)
    OIII = pygame.transform.rotate(OIII, pe.objects[idx].angle)
    OIIIW = OIII.get_width()
    OIIIH = OIII.get_height()

# move up an object in the hierarchy
def objectUp():
    idx = pe.objName.index(SOHM.elements[SOHM.elem_idx])
    
    if idx > 0:
        pe.objName[idx], pe.objName[idx-1] = pe.objName[idx-1], pe.objName[idx]
        pe.objects[idx], pe.objects[idx-1] = pe.objects[idx-1], pe.objects[idx]
        pe.objClass[idx], pe.objClass[idx-1] = pe.objClass[idx-1], pe.objClass[idx]
        SOHM.elem_idx -= 1
        SOHM.elements = pe.objName[:]
        SOHM.normalize()
        ouar.saveObjs(pe, f"{PATH}{pt.s}{st.projects[st.projectIdx]}{pt.s}ObjectInfo.txt")

# move down an object in the hierarchy
def objectDown():
    idx = pe.objName.index(SOHM.elements[SOHM.elem_idx])
    
    if idx != len(SOHM.elements)-1:
        pe.objName[idx], pe.objName[idx+1] = pe.objName[idx+1], pe.objName[idx]
        pe.objects[idx], pe.objects[idx+1] = pe.objects[idx+1], pe.objects[idx]
        pe.objClass[idx], pe.objClass[idx+1] = pe.objClass[idx+1], pe.objClass[idx]
        SOHM.elem_idx += 1
        SOHM.elements = pe.objName[:]
        SOHM.normalize()
        ouar.saveObjs(pe, f"{PATH}{pt.s}{st.projects[st.projectIdx]}{pt.s}ObjectInfo.txt")

# copy object
def copyObject():
    idx = pe.objName.index(SOHM.ename)
    
    pe.objects.append(copy.copy(pe.objects[idx]))
    pe.objName.append(f"{pe.objName[idx]} (1)")
    pe.objClass.append(pe.objClass[idx])
    SOHM.elements = pe.objName[:]
    SOHM.elem_idx = len(SOHM.elements)-1
    SOHM.normalize()
    
    ouar.saveObjs(pe, f"{PATH}{pt.s}{st.projects[st.projectIdx]}{pt.s}ObjectInfo.txt")

# show console
def showConsole():
	st.isConsole = True
	btSCC.func = closeConsole

# close console
def closeConsole():
	st.isConsole = False
	btSCC.func = showConsole

def loadObjectScriptLinks(one = False):
    global error
    
    n = 0 if not one else len(pe.objects)-1
    mn = [i.__name__.split(".")[-1] for i in st.modules]
    
    for obj in pe.objects[n:]:
        if obj.script != "None":
            err = False
            scripts = [i.strip().split(".")[-1] for i in obj.script.split(",")]
            
            ss = [i for i in obj.S_CONTENT]
            for s in ss:
                if s not in mn:
                    del obj.S_CONTENT[s]
                    del obj.SC_CHANGED[s]
            
            for ojj in scripts:
                try:
                    if ojj in mn:
                        pe.OWS.append(eval(f"st.modules[mn.index(\"{ojj}\")].{ojj}()"))
                        pe.OWS[-1].this = obj
                        obj.S_LINKS.append(pe.OWS[-1])
                    else:
                        _console.Log(f"UniPy Error: in object \"{pe.objName[pe.objects.index(obj)]}\": script \"{ojj}\" is not defined", "error")
                        error = True
                except Exception as e:
                    error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    _console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
                    err = True
                    continue
            
            for idx, ojj in enumerate(scripts):
                if ojj in mn and ojj in obj.S_CONTENT:
                    try: _v = [var for var in dir(obj.S_LINKS[idx]) if not callable(getattr(obj.S_LINKS[idx], var)) and not var.startswith("_")]
                    except: continue
                    if "this" in _v: _v.remove("this")
                    for jjj in _v:
                        if jjj in obj.S_CONTENT[ojj] and obj.SC_CHANGED[ojj][jjj]:
                            vv = obj.S_CONTENT[ojj][jjj][0]
                            vvt = obj.S_CONTENT[ojj][jjj][1]
                            exec(f"obj.S_LINKS[{idx}].{jjj} = vv")

def loadOBJScriptLinks(idx):
    obj = pe.objects[idx]
    scripts = [script.strip() for script in obj.script.split(",")] if obj.script != "None" else {}
    
    result = {}
    
    if scripts:
        for script in scripts:
            parsed_ast = None
            result[script] = {}
            try:
                with open(f"{PATH}{pt.s}{st.projects[st.projectIdx]}{pt.s}{script.replace('.', pt.s)}.py") as code:
                    parsed_ast = ast.parse(code.read())
            except:
                return {}
            
            idx = next((i for i, bd in enumerate(parsed_ast.body) if isinstance(bd, ast.ClassDef)), None)
            
            if idx is not None:
                init_body = parsed_ast.body[idx].body[0].body
                
                for statement in init_body:
                    if isinstance(statement, ast.Assign):
                        for target in statement.targets:
                            if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == 'self':
                                variable_name = target.attr
                                try: variable_value = ast.literal_eval(statement.value)
                                except: variable_value = "func & unknown"
                                if not variable_name.startswith("_") and variable_value != None:
                                    result[script][variable_name] = variable_value
            
        return result
    else:
        return {}
    
# start app
def startApp():
    global error
    
    pe.objects = []
    pe.objClass = []
    pe.objName = []
    ouar.loadObjs(pe, f"{PATH}{pt.s}{st.projects[st.projectIdx]}{pt.s}ObjectInfo.txt")
    pe.OON = pe.objName.copy()
    pe.OWS = []
    pe.Camera.target = None
    pe.Camera.x, pe.Camera.y = 0, 0
    
    MHFS = []
    st.MHFU = []
    st.GBGC = st.GBGSC
    _console.textes = []
    _console.textes_type = []
    _console.tX, _console.tY = (0, 0)
    error = False
    
    loadModules()
    loadObjectScriptLinks()
    
    for i in st.modules:
        if hasattr(i, "Start"): MHFS.append(i)
        if hasattr(i, "Update"): st.MHFU.append(i)
    
    for i in pe.OWS:
        if hasattr(i, "Start"): MHFS.append(i)
        if hasattr(i, "Update"): st.MHFU.append(i)
    
    st.drawingLayer = 1
    btStartApp.func = returnToEditor
    btStartApp.original_image = uiEngineImages["cancel"]
    btStartApp.height = st.height - st.AppHeight - 20
    btStartApp.width = btStartApp.height * 2
    btStartApp.adjust_dimensions_and_positions()
    
    for obj in pe.objects: obj.setPos()
    for obj in pe.objects: obj.setPosObject()
    
    for script in MHFS:
        try:
            script.Start()
        except Exception as e:
                error = True
                tb = e.__traceback__
                filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                _console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")

# close app
def returnToEditor():
    
    pygame.mixer.stop()
    
    pe.objects = []
    pe.objClass = []
    pe.objName = []
    st.drawingLayer = 0
    st.isConsole = False
    btSCC.func = showConsole
    btStartApp.func = startApp
    btStartApp.original_image = uiEngineImages["play"]
    btStartApp.height = st.uiBS
    btStartApp.width = st.uiBS
    btStartApp.adjust_dimensions_and_positions()
    
    ouar.loadObjs(pe, f"{PATH}{pt.s}{st.projects[st.projectIdx]}{pt.s}ObjectInfo.txt")

# show objects that can be created
def SOTCBC():
    SOHM.scrolling = False
    st.isCreateObject = True
    btShowPanel.fontSize = st.uiBFS
    btShowPanel.original_image = uiEngineImages["cancel"]
    btShowPanel.func = COTCBC
    btShowPanel.adjust_dimensions_and_positions()

# close objects that can be created
def COTCBC():
    SOHM.scrolling = True
    st.isCreateObject = False
    btShowPanel.fontSize = st.uiBFS
    btShowPanel.original_image = uiEngineImages["plus"]
    btShowPanel.func = SOTCBC
    btShowPanel.adjust_dimensions_and_positions()

def createObject(Class):
    
    st.isCreateObject = False
    SOHM.scrolling = True
    btShowPanel.original_image = uiEngineImages["plus"]
    btShowPanel.func = SOTCBC
    btShowPanel.adjust_dimensions_and_positions()
    ouar.addObj(pe, f"{PATH}{pt.s}{st.projects[st.projectIdx]}{pt.s}ObjectInfo.txt", Class)
    
    SOHM.elements = pe.objName[:]
    SOHM.elem_idx = -1
    SOHM.normalize()

# change object property
def changeObjProperty(key, content = None):
    global OIII, OIIIW, OIIIH
    
    idx = pe.objName.index(st.lastSelectionObject)
    obj = None
    
    for i in objComponents:
        if i.key == key:
            obj = i
            break
    
    if key == "name":
        if ObjName.text.strip() not in pe.objName:
            pe.objName[idx] = ObjName.text
            SOHM.elements = pe.objName[:]
            SOHM.normalize()
            st.lastSelectionObject = ObjName.text
        else:
            ObjName.text = pe.objName[idx]
            createMessage(st.win, f"Oops, an object with that name already exists.", stopTime = 120)
        
    elif key == "x":
        try:
            pe.objects[idx].sx = int(eval(ObjX.text))
            ObjX.text = str(pe.objects[idx].sx)
        except:
            ObjX.text = str(pe.objects[idx].sx)
            
    elif key == "y":
       try:
            pe.objects[idx].sy = int(eval(ObjY.text))
            ObjY.text = str(pe.objects[idx].sy)
       except:
            ObjY.text = str(pe.objects[idx].sy)
    
    elif key == "cx":
        if ObjCX.text != "":
            pe.objects[idx].cx = ObjCX.text
        else: ObjCX.text = pe.objects[idx].cx
            
    elif key == "cy":
        if ObjCY.text != "":
            pe.objects[idx].cy = ObjCY.text
        else: ObjCY.text = pe.objects[idx].cy
    
    elif key == "width":
        try:
            pe.objects[idx].SW = int(eval(ObjWidth.text))
            ObjWidth.text = str(pe.objects[idx].SW)
        except:
            ObjWidth.text = str(pe.objects[idx].SW)
            
    elif key == "height":
        try:
            pe.objects[idx].SH = int(eval(ObjHeight.text))
            ObjHeight.text = str(pe.objects[idx].SH)
        except:
            ObjHeight.text = str(pe.objects[idx].SH)
    
    elif key == "angle":
        try:
            pe.objects[idx].angle = int(eval(ObjAngle.text))
            ObjAngle.text = str(pe.objects[idx].angle)
            ADP_OIII(idx)
        except:
            ObjAngle.text = str(pe.objects[idx].angle)
        setObjProperty(st.lastSelectionObject, False)
    
    elif key == "render":
        pe.objects[idx].render = ObjRender.active
    
    elif key == "bodyType":
        pe.objects[idx].bodyType = content
        st.isSelector = False
    
    elif key == "textCentering":
        pe.objects[idx].textCentering = content
        st.isSelector = False
    
    elif key == "flipX":
        pe.objects[idx].flipX = ObjFlipX.active
        try: ADP_OIII(idx)
        except: pass
    
    elif key == "flipY":
        pe.objects[idx].flipY = ObjFlipY.active
        try: ADP_OIII(idx)
        except: pass
    
    elif key == "text":
        pe.objects[idx].text = ObjText.text
        
    elif key == "fontSize":
        try:
            pe.objects[idx].sfs = int(eval(ObjFontSize.text))
            ObjFontSize.text = str(pe.objects[idx].sfs)
        except:
            ObjFontSize.text = str(pe.objects[idx].sfs)
    
    elif key == "layer":
        try:
            pe.objects[idx].layer = int(ObjLayer.text)
        except:
            ObjLayer.text = str(pe.objects[idx].layer)
    
    elif key == "tag":
        pe.objects[idx].tag = ObjTag.text
    
    elif key == "color":
        try:
            pe.objects[idx].color = eval(ObjColor.text)
            ObjColor.text = str(pe.objects[idx].color)
        except:
            ObjColor.text = str(pe.objects[idx].color)
    
    elif key == "transparent":
        try:
	        pe.objects[idx].transparent = max(0, min(255, eval(ObjTSP.text)))
	        ObjTSP.text = str(pe.objects[idx].transparent)
        except:
            ObjTSP.text = str(pe.objects[idx].transparent)
    
    elif key == "richText":
        pe.objects[idx].richText = ObjRichText.active
     
    elif key == "useFullAlpha":
        pe.objects[idx].useFullAlpha = ObjUseFullAlpha.active
    
    elif key == "smooth":
        pe.objects[idx].smooth = ObjSmooth.active
    
    elif key == "useCamera":
        pe.objects[idx].useCamera = ObjUseCamera.active
    
    elif key == "script":
        l = [i.strip() for i in ObjScript.text.split(",")]
        c = 0
        for i in l:
            if l.count(i) > 1:
                ObjScript.text = pe.objects[idx].script
                c += 1
                break
        
        if c == 0:
            pe.objects[idx].script = ObjScript.text
                    	
            setObjProperty(st.lastSelectionObject, False)
    
    elif key == "font":
        st.drawingLayer = 0
        try:
            font = pygame.font.Font(content, 1)
            pe.objects[idx].font = content
            ADP_OFNII(idx)
        except: pass
    
    elif key == "image":
        st.drawingLayer = 0
        fileConductor.thisPath = pt._defaultPath
        
        if content != None and content.split('.')[-1] in pe._imgTypes:
            pe.objects[idx].image = pe.textures[content.split(pt.s)[-1]] if not pe.objects[idx].useFullAlpha else pe.texturesTSP[content.split(pt.s)[-1]]
            pe.objects[idx].imagePath = content.split(pt.s)[-1]
            ObjWidth.text = str(pe.objects[idx].width)
            ObjHeight.text = str(pe.objects[idx].height)
            ADP_OIII(idx)
        elif content == None:
            pe.objects[idx].image = content
            pe.objects[idx].imagePath = content
            OIII = None
        setObjProperty(st.lastSelectionObject, False)
    
    try:
        obj.endText = 0
        obj.check_text()
    except: pass
    
    ouar.saveObjs(pe, f"{PATH}{pt.s}{st.projects[st.projectIdx]}{pt.s}ObjectInfo.txt")

def setScriptVarValue(script, type, var, value, OBJ = None):
    idx = pe.objName.index(st.lastSelectionObject)
    obj = pe.objects[idx]
    
   # try:
    value = eval(f"{type}('{value}')")
    _val = str(value)
            
    g = loadOBJScriptLinks(idx)
    if script.split(".")[-1] in obj.SC_CHANGED:
        if g[script][var] == value:
            obj.SC_CHANGED[script.split(".")[-1]][var] = False
        else:
            obj.SC_CHANGED[script.split(".")[-1]][var] = True
    else:
        obj.S_CONTENT[script.split(".")[-1]] = {}
        obj.SC_CHANGED[script.split(".")[-1]] = {}
        obj.S_CONTENT[script.split(".")[-1]][var] = [g[script][var], type]
        obj.SC_CHANGED[script.split(".")[-1]][var] = True
                            
    if var not in obj.S_CONTENT[script.split(".")[-1]]:
        obj.S_CONTENT[script.split(".")[-1]][var] = [value, type]
        obj.SC_CHANGED[script.split(".")[-1]][var] = True
    else:
        obj.S_CONTENT[script.split(".")[-1]][var][0] = value
    ouar.saveObjs(pe, f"{PATH}{pt.s}{st.projects[st.projectIdx]}{pt.s}ObjectInfo.txt")
    #except:
#        OBJ.set_old_text()

# load object property
def setObjProperty(text, resetOPII = True):
    global OPII, objComponents, OIII, OIIIW, OIIIH, compiledTextes_FOC, CSTN, CSTN_POS, CTFOCXOF, SISL
    
    st.lastSelectionObject = text
    compiledTextes_FOC = []
    CSTN = []
    CSTN_POS = []
    CTFOCXOF = []
    
    idx = pe.objName.index(st.lastSelectionObject)
    
    if pe.objClass[idx] == "Object":
        objComponents = [ObjName, ObjX, ObjY, ObjWidth, ObjHeight, ObjAngle, ObjTSP, ObjCX, ObjCY, ObjColor, ObjLayer, ObjTag, ObjBD, ObjRender, ObjFlipX, ObjFlipY, ObjUseFullAlpha, ObjUseCamera, ObjLoadImage, ObjScript]
        fileConductor.content = "'image'"
        btDeleteCR.content = "('image', None)"
        
        if pe.objects[idx].image != None: ADP_OIII(idx)
     
        else: OIII = None
    
    elif pe.objClass[idx] == "Text":
       objComponents = [ObjName, ObjX, ObjY, ObjText, ObjFontSize, ObjLoadFont, ObjColor, ObjTSP, ObjAngle, ObjCX, ObjCY, ObjTC, ObjLayer, ObjTag, ObjRender, ObjFlipX, ObjFlipY, ObjRichText, ObjUseCamera, ObjSmooth, ObjScript]
       fileConductor.content = "'font'"
       btDeleteCR.content = "('font', None)"
   
    elif pe.objClass[idx] == "Group":
        objComponents = [ObjName, ObjX, ObjY, ObjRender, ObjTag, ObjScript]
       
    idxx = 1
    objComponents[0].rect.y = st.uiSOCP
    objComponents[0].start_y = st.uiSOCP
    for i in objComponents[1:]:
        objCm = st.uiTSFont.render(re.sub(r'(?<!^)([A-Z])', r' \1', i.key).title(), 0, st.uiTColor)
        compiledTextes_FOC.append(objCm)
        CTFOCXOF.append(0)
        i.rect.x = objCm.get_width() + 20
                
        i.rect.y = objComponents[idxx - 1].rect.y + objComponents[idxx - 1].rect.height + 20
        i.start_y = i.rect.y
        idxx += 1
    
    if pe.objClass[idx] == "Text": ADP_OFNII(idx)
    
    st.lastSelectionObjectClass = pe.objClass[idx]
    ObjName.text = st.lastSelectionObject
    for i in objComponents[1:]:
        if type(i) == input.Input:
            i.text = str(eval(f"pe.objects[idx].{i.key}"))
        elif type(i) == toggleButton.ToggleButton:
            i.active = eval(f"pe.objects[idx].{i.key}")
            
    ObjX.text = str(pe.objects[idx].sx)
    ObjY.text = str(pe.objects[idx].sy)
    
    if pe.objClass[idx] == "Object":
        ObjWidth.text = str(pe.objects[idx].SW)
        ObjHeight.text = str(pe.objects[idx].SH)
        
        if OIII != None:
            ObjScript.rect.y = ObjLoadImage.rect.top + OIIIH + 20
            ObjScript.start_y = ObjLoadImage.rect.top + OIIIH + 20
    
    if pe.objClass[idx] == "Text":
        ObjFontSize.text = str(pe.objects[idx].sfs)
    
    if pe.objects[idx].S_LINKS != {}:
        inf = loadOBJScriptLinks(idx)
    ile = False
    for s in inf:
        _vars = list(inf[s])
        _values = list(inf[s].values())
            
        if "this" in _vars: _vars.remove("this")
        CSTN.append(st.uiTFont.render(s.split(".")[-1], 0, st.uiTColor))
        CSTN_POS.append([50, objComponents[idxx - 1].rect.y + objComponents[idxx - 1].rect.height + 20])
        if _vars == [] and not ile:
            ile = True
        elif ile:
            CSTN_POS[-1][1] += CSTN[-2].get_height() + 20
        FINS = False
        for var, value in zip(_vars, _values):
            tp = type(value).__name__
            
            if pe.objects[idx].S_CONTENT != {} and var in pe.objects[idx].S_CONTENT[s.split(".")[-1]]:
                if pe.objects[idx].SC_CHANGED[s.split(".")[-1]][var]:
                    value = pe.objects[idx].S_CONTENT[s.split(".")[-1]][var][0]
            
            if tp == "bool":
                objComponents.append(toggleButton.ToggleButton(st.win, var, setScriptVarValue, borderRadius = st.uiWIBR, fillSize = 5, image = uiEngineImages["checkmark"], width = st.uiBS, height = st.uiBS, color = st.uiBC, content = f"('{s}', '{tp}', self.key, str(self.active))", active = value))
            else:
                objComponents.append(input.Input(st.win, setScriptVarValue, noText = f"value ({tp})...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = var, content = f"('{s}', '{tp}', self.key, self.text, self)", textColor = st.uiITC, text = str(value)))
            objComponents[-1].rect.y = objComponents[idxx - 1].rect.y + objComponents[idxx - 1].rect.height + 20
            if not FINS:
                objComponents[-1].rect.y += CSTN[-1].get_height() + 20
                FINS = True
            if ile:
                objComponents[-1].rect.y += CSTN[-2].get_height() + 20
                ile = False
            objComponents[-1].start_y = objComponents[-1].rect.y
            objCm = st.uiTSFont.render(re.sub(r'(?<!^)([A-Z])', r' \1', str(var)).title(), 0, st.uiTColor)
            compiledTextes_FOC.append(objCm)
            CTFOCXOF.append(40)
            objComponents[-1].rect.x = objCm.get_width() + 60
            idxx += 1
        
    OPII = 0 if resetOPII else OPII      
    for i in objComponents:
        i.rect.y = i.start_y + OPII
        if type(i) == input.Input:
            i.endText = 0
            i.check_text()

# button for start app
btStartApp = button.Button(st.win, width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, func = startApp, x = -10, y = -10, image = uiEngineImages["play"], color = st.uiBC, pressedColor = st.uiBPC, cx = "right", cy = "bottom")

# button for console
btSCC = button.Button(st.win, height = st.height - st.AppHeight - 20, width = (st.height - st.AppHeight - 20) * 2, text = "console", borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = st.uiFont, func = showConsole, x = f"-self.width * 1 - 20", y = -10, image = uiEngineImages["console"], color = st.uiBC, pressedColor = st.uiBPC, cx = "right", cy = "bottom")

# button for close object info
btCloseInfo = button.Button(st.win, y = 10, x = -10,  width = st.uiBS, height = st.uiBS, text = "X", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = closeObjectInfo, fontPath = st.uiFont, image = uiEngineImages["cancel"], color = st.uiBC, pressedColor = st.uiBPC, cx = "right")

# button for show panel for adding objects
btShowPanel = button.Button(st.win, width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = SOTCBC, fontPath = st.uiFont, x = -10, y = f"-self.height * 1 - 20", color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["plus"], cx = "right", cy = "bottom")

# button for return to choose project
btToCP = button.Button(st.win, width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = toCP, fontPath = st.uiFont, y = f"-self.height * 2 - 30", x = -10, color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["back"], cx = "right", cy = "bottom")

# button open project assets
btOPA = button.Button(st.win, width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startPACR, fontPath = st.uiFont, y = f"-self.height * 3 - 40", x = -10, image = uiEngineImages["files"], color = st.uiBC, pressedColor = st.uiBPC, cx = "right", cy = "bottom")

# button for down project
btPD = button.Button(st.win, width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = objectDown, fontPath = st.uiFont, y = f"-self.height * 4 - 50", x = -10, image = uiEngineImages["down"], color = st.uiBC, pressedColor = st.uiBPC, cx = "right", cy = "bottom")

# button for up project
btPU = button.Button(st.win, width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = objectUp, fontPath = st.uiFont, y = f"-self.height * 5 - 60", x = -10, image = uiEngineImages["up"], color = st.uiBC, pressedColor = st.uiBPC, cx = "right", cy = "bottom")

# button for copy object
btCopy = button.Button(st.win, width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = copyObject, fontPath = st.uiFont, y = f"-self.height * 6 - 70", x = -10, image = uiEngineImages["copy"], color = st.uiBC, pressedColor = st.uiBPC, cx = "right", cy = "bottom")

# button for delete object
btDeleteObj = button.Button(st.win, width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = deleteObj, fontPath = st.uiFont, y = f"-self.height * 7 - 80", x = -10, image = uiEngineImages["trash"], color = st.uiBC, pressedColor = st.uiBPC, cx = "right", cy = "bottom")

# button for cancel load file in conductor
btCancelCR = button.Button(st.win, y = 10, x = -10, width = st.uiBS, height = st.uiBS, text = "cancel", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = closeCR, fontPath = st.uiFont, image = uiEngineImages["cancel"], color = st.uiBC, pressedColor = st.uiBPC, cx = "right")

# button for back in conductor
btBackCR = button.Button(st.win, x = f"-self.width * 1 - 20", y = 10, width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = backCR, fontPath = st.uiFont, color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["back"], cx = "right")

# button for delete obj image or font in conductor
btDeleteCR = button.Button(st.win, y = 10, x = f"-self.width * 2 - 30", width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = changeObjProperty, fontPath = st.uiFont, content = "('image', None)", image = uiEngineImages["trash"], color = st.uiBC, pressedColor = st.uiBPC, cx = "right")

# button for file to project assets conductor
btAddFile = button.Button(st.win, y = 10, x = f"-self.width * 2 - 30", width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startCRfromPAC, fontPath = st.uiFont, color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["plus"], cx = "right")

# button for create new folder in project assets conductor
btAddFolder = button.Button(st.win, y = 10, x = f"-self.width * 3 - 40", width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = createDirectory, fontPath = st.uiFont, color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["create_dir"], cx = "right")

# button for file to project assets conductor
btDeleteFile = button.Button(st.win, y = 10, x = f"-self.width * 2 - 30", width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = deleteFileInPAC, fontPath = st.uiFont, color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["trash"], cx = "right")

# button for rename file in project assets conductor
btRenameFile = button.Button(st.win, y = 10, x = f"-self.width * 3 - 40", width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startRenameFilePAC, fontPath = st.uiFont, color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["rename"], cx = "right")

# button for move file/folder to other directory in project assets conductor
btMoveFile = button.Button(st.win, y = 10, x = f"-self.width * 4 - 50", width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startCRfromMoveFile, fontPath = st.uiFont, color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["moveFile"], cx = "right")

btDoneCR = button.Button(st.win, y = 10, x = f"-self.width * 2 - 30", width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = moveFileInPAC, fontPath = st.uiFont, image = uiEngineImages["checkmark"], color = st.uiBC, pressedColor = st.uiBPC, cx = "right")

# button for create new project
btCreateProject = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "+", borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = st.uiFont, func = createProject, x = -10, y = -10, color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["plus"], cx = "right", cy = "bottom")

btLoadProjects = button.Button(st.win, width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = st.uiFont, func = startCRfromImportProject, x = -10, y = f"-self.height * 1 - 20", color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["load_projects"], cx = "right", cy = "bottom")

# button for delete project
btDeleteProject = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "del", borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = st.uiFont, func = deleteFolderInPM, x = -10, y = f"-self.height * 2 - 30", color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["trash"], cx = "right", cy = "bottom")

# button for copy project
btCopyProject = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "del", borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = st.uiFont, func = copyProject, x = -10, y = f"-self.height * 3 - 40", color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["copy"], cx = "right", cy = "bottom")

# button for rename project
btRenameProject = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "rename", borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = st.uiFont, func = startRenameProject, x = -10, y = f"-self.height * 4 - 50", color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["rename"], cx = "right", cy = "bottom")

btOpenExportProject = button.Button(st.win, width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = st.uiFont, func = OpenMenuToExportProject, x = -10, y = f"-self.height * 5 - 60", color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["export"], cx = "right", cy = "bottom")

btCloseExportProject = button.Button(st.win, y = 10, x = -10, width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = CloseMenuToExportProject, fontPath = st.uiFont, image = uiEngineImages["cancel"], color = st.uiBC, pressedColor = st.uiBPC, cx = "right")

btSetExportPath = button.Button(st.win, width = st.uiBS, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = st.uiFont, func = startCRfromExportProject, color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["load"], x = 10)

btExportProject = button.Button(st.win, width = st.uiBS * 2, height = st.uiBS, borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = st.uiFont, func = ExportProject, x = 0, y = -10, color = st.uiBC, pressedColor = st.uiBPC, image = uiEngineImages["checkmark"], cx = "center", cy = "bottom")

# inputs for object inspector
ObjName = input.Input(st.win, changeObjProperty, noText = "Name...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "name", content = "(self.key)", textColor = st.uiITC, x = 10)

ObjX = input.Input(st.win, changeObjProperty, noText = "PosX...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "x", content = "(self.key)", textColor = st.uiITC)

ObjY = input.Input(st.win, changeObjProperty, noText = "PosY...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "y", content = "(self.key)", textColor = st.uiITC)

ObjWidth = input.Input(st.win, changeObjProperty, noText = "Width...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "width", content = "(self.key)", textColor = st.uiITC)

ObjHeight = input.Input(st.win, changeObjProperty, noText = "Height...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "height", content = "(self.key)", textColor = st.uiITC)

ObjAngle = input.Input(st.win, changeObjProperty, noText = "Angle...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "angle", content = "(self.key)", textColor = st.uiITC)

ObjCX = input.Input(st.win, changeObjProperty, noText = "pos...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "cx", content = "(self.key)", textColor = st.uiITC)

ObjCY = input.Input(st.win, changeObjProperty, noText = "pos...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "cy", content = "(self.key)", textColor = st.uiITC)

ObjText = input.Input(st.win, changeObjProperty, noText = "text...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "text", content = "(self.key)", textColor = st.uiITC)

ObjFontSize = input.Input(st.win, changeObjProperty, noText = "fontSize...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "fontSize", content = "(self.key)", textColor = st.uiITC)

ObjColor = input.Input(st.win, changeObjProperty, noText = "color...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "color", content = "(self.key)", textColor = st.uiITC)

ObjTSP = input.Input(st.win, changeObjProperty, noText = "transparent...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "transparent", content = "(self.key)", textColor = st.uiITC)

ObjScript = input.Input(st.win, changeObjProperty, noText = "script...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "script", content = "(self.key)", textColor = st.uiITC)

ObjLayer = input.Input(st.win, changeObjProperty, noText = "layer...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "layer", content = "(self.key)", textColor = st.uiITC)

ObjTag = input.Input(st.win, changeObjProperty, noText = "tag...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "tag", content = "(self.key)", textColor = st.uiITC)

# toggles button for object inspector
ObjRender = toggleButton.ToggleButton(st.win, "render", changeObjProperty, borderRadius = st.uiWIBR, fillSize = 5, image = uiEngineImages["checkmark"], width = st.uiBS, height = st.uiBS, color = st.uiBC)

ObjFlipX = toggleButton.ToggleButton(st.win, "flipX", changeObjProperty, borderRadius = st.uiWIBR, fillSize = 5, image = uiEngineImages["checkmark"], width = st.uiBS, height = st.uiBS, color = st.uiBC)

ObjFlipY = toggleButton.ToggleButton(st.win, "flipY", changeObjProperty, borderRadius = st.uiWIBR, fillSize = 5, image = uiEngineImages["checkmark"], width = st.uiBS, height = st.uiBS, color = st.uiBC)

ObjRichText = toggleButton.ToggleButton(st.win, "richText", changeObjProperty, borderRadius = st.uiWIBR, fillSize = 5, image = uiEngineImages["checkmark"], width = st.uiBS, height = st.uiBS, color = st.uiBC)

ObjUseFullAlpha = toggleButton.ToggleButton(st.win, "useFullAlpha", changeObjProperty, borderRadius = st.uiWIBR, fillSize = 5, image = uiEngineImages["checkmark"], width = st.uiBS, height = st.uiBS, color = st.uiBC)

ObjUseCamera = toggleButton.ToggleButton(st.win, "useCamera", changeObjProperty, borderRadius = st.uiWIBR, fillSize = 5, image = uiEngineImages["checkmark"], width = st.uiBS, height = st.uiBS, color = st.uiBC)

ObjSmooth = toggleButton.ToggleButton(st.win, "smooth", changeObjProperty, borderRadius = st.uiWIBR, fillSize = 5, image = uiEngineImages["checkmark"], width = st.uiBS, height = st.uiBS, color = st.uiBC)

# buttons for object inspector
ObjLoadImage = button.Button(st.win, x = st.width - 110, y = 10, width = st.uiBS, height = st.uiBS, text = "set", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startCR, fontPath = st.uiFont, key = "image", image = uiEngineImages["load"], color = st.uiBC, pressedColor = st.uiBPC)

ObjBD = button.Button(st.win, x = st.width - 110, y = 10, width = st.uiBS, height = st.uiBS, text = "select", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startSelectorForObjectInspector, fontPath = st.uiFont, image = uiEngineImages["body"], color = st.uiBC, pressedColor = st.uiBPC, key = "bodyType", content = f"(['None', 'dynamic', 'static'], self, 'bodyType')")

ObjTC = button.Button(st.win, x = st.width - 110, y = 10, width = st.uiBS, height = st.uiBS, text = "select", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startSelectorForObjectInspector, fontPath = st.uiFont, image = uiEngineImages["point"], color = st.uiBC, pressedColor = st.uiBPC, key = "textCentering", content = f"(['left', 'center', 'right'], self, 'textCentering')")

ObjLoadFont = button.Button(st.win, x = st.width - 110, y = 10, width = st.uiBS, height = st.uiBS, text = "set", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startCR, fontPath = st.uiFont, key = "font", image = uiEngineImages["load"], color = st.uiBC, pressedColor = st.uiBPC)

# selectors for object inspector
ObjSW = sohManager.SOHManager(st.win, changeObjProperty, fontPath = st.uiFont, borderRadius = btShowPanel.border_radius, color = btShowPanel.color, elemColor = btShowPanel.pressed_color, width = st.width // 2, height = st.height // 4 if st.width < st.height else st.height // 2, content = "(self.key, self.elements[self.elem_idx])", maxD = 5, minD = 3.5, key = "bodyType", elemSelectedColor = st.uiSOHSEC, fillSize = st.uiSOHFL, scrolling = False)

# file conductor
fileConductor = conductor.Conductor(st.win, changeObjProperty, width = st.width, height = st.height, fontSize = 60, y = 20 + st.uiBS, color = st.uiCC, fontPath = st.uiFont, elemColor = st.uiCEC, images = [uiEngineImages["directory"], uiEngineImages["file"], uiEngineImages["music"], uiEngineImages["font"]], content = "'image'", textColor = st.uiCTC, elemSelectedColor = st.uiCSEC, scrollSpeed = st.scrollSpeed)

# projects assets conductor
PAC = conductor.Conductor(st.win, None, width = st.width, height = st.height, fontSize = 60, y = 20 + st.uiBS, color = st.uiCC, fontPath = st.uiFont, elemColor = st.uiCEC, images = [uiEngineImages["directory"], uiEngineImages["file"], uiEngineImages["music"], uiEngineImages["font"]], onlyView = True, textColor = st.uiCTC, elemSelectedColor = st.uiCSEC, codeFontPath = f"assets{pt.s}Menlo-Regular.ttf", kColor = st.uiCCKC, fColor = st.uiCCFC, cColor = st.uiCCCC, sColor = st.uiCCSC, nColor = st.uiCCNC, CbgColor = st.uiCCBGC, vColor = st.uiCCVC, scrollSpeed = st.scrollSpeed)

# input for rename file in project assets conductor
IFFIPAC = input.Input(st.win, endRenameFilePAC, noText = "Name...", maxChars = 256, width = PAC.elemWidth, height = PAC.elemHeight, fontSize = 40, fontPath = st.uiFont, color = PAC.elemColor, pressedColor = st.uiIPC, x = 10, ATL = False, textColor = st.uiITC)

InputSetExportProjectVersion = input.Input(st.win, renameExportProjectVersion, noText = "version...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = st.uiFont, color = st.uiIC, pressedColor = st.uiIPC, textColor = st.uiITC, x = 10)

# project manager
PM = projectManager.ProjectManager(st.win, "eui.openProject", elements = st.projects[:], fontPath = st.uiFont, y = 10 + uiEngineImages["ENGINE_ICON"].get_height() + 50, borderRadius = st.uiWPEOEEBR, color = st.uiPMC, elemColor = st.uiPEC, width = st.width // 1.5, x = st.width // 2 - (st.width // 1.5) // 2, elemSelectedColor = st.uiPSEC, textColor = st.uiPMTC, fillSize = st.uiPMFS, scrollSpeed = st.scrollSpeed)

# input for rename project in project manager
IFRPIPM = input.Input(st.win, endRenameProject, noText = "Name...", maxChars = 256, width = PM.elem_width, height = PM.elem_height, fontSize = 40, fontPath = st.uiFont, color = PM.elem_color, pressedColor = st.uiIPC, x = PM.x, ATL = False, borderRadius = st.uiWPEOEEBR, textColor = st.uiITC)

# selection object hierarchy
SOHM = sohManager.SOHManager(st.win, setObjProperty, fontPath = st.uiFont, y = 10, x = 10, borderRadius = st.uiWPEOEEBR, color = st.uiSOHC, elemColor = st.uiSOHEC, width = st.width // 1.3, height = st.height - 20, content = "(self.elements[self.elem_idx])", elemSelectedColor = st.uiSOHSEC, fillSize = st.uiSOHFL, scrollSpeed = st.scrollSpeed, bgBorderRadius = st.uiSOHBGBR, bgFillSize = st.uiSOHBGFL)

# selection new object panel
SNOP = sohManager.SOHManager(st.win, createObject, fontPath = st.uiFont, y = btShowPanel.rect.y - st.height // 2 - 10, x = btShowPanel.rect.right - st.width // 1.5, borderRadius = btShowPanel.border_radius, color = btShowPanel.color, elemColor = btShowPanel.pressed_color, width = st.width // 1.5 if st.width < st.height else st.width // 3, height = st.height // 2, content = "(self.elements[self.elem_idx])", elements = ["Object", "Text"], maxD = 5, minD = 3.5, elemSelectedColor = st.uiSOHSEC, fillSize = st.uiSOHFL, scrollSpeed = st.scrollSpeed, bgBorderRadius = st.uiSOHBGBR, bgFillSize = st.uiSOHBGFL)

# engine console
_console = console.Console(st.win, height = st.AppHeight // 2, width = st.AppWidth, font = st.uiFont, y = st.AppHeight - st.AppHeight // 2, bgColor = st.uiCBC, logImg = uiEngineImages["message"], errorImg = uiEngineImages["error"], warningImg = uiEngineImages["warning"], scrollSpeed = st.scrollSpeed)

# progress bar for load project
h = st.height // 4 if st.height > st.width else st.height // 2
w = st.width // 1.2 if st.height > st.width else st.width // 2.4
PB = progressBar.ProgressBar(st.win, height = h, width = w, font = st.uiFont, y = st.height // 2 - h // 2, x = st.width // 2 - w // 2, bgColor = st.uiPBBGC, title = "Loading assets...", textColor = st.uiPBTC, progressBarColor = st.uiPBC, progressBarBgColor = st.uiPBBC, borderRadius = st.uiPBBR)

uiEPME = [btSetExportPath, InputSetExportProjectVersion]

def AEPME():
    global uiEPMT
    st.EPT = st.uiTFont.render("Project Export", 0, st.uiTColor)
    uiEPMT = [st.uiTSFont.render(tx, 0, st.uiTColor) for tx in uiEPMST]
    y = st.EPT.get_height() + 50
    for idx, tx in enumerate(uiEPMT):
        uiEPME[idx].rect.y = y + tx.get_height() + 30
        y += tx.get_height() + 60 + uiEPME[idx].rect.height

# function for draw engine UI
def drawUI():
    
    if st.lastSelectionObject == None:
        btStartApp.update()
        btShowPanel.update()
        
        if not st.isCreateObject:
            btToCP.update()
            btOPA.update()
            
            if SOHM.elem_idx != -1:
                btPD.update()
                btPU.update()
                btCopy.update()
                btDeleteObj.update()
        SOHM.update(st.MP, st.MBP)
        
        if st.isCreateObject: SNOP.update(st.MP, st.MBP)
    
    else:
        # update the object components
        for i in objComponents:
            i.update()
        
        if st.lastSelectionObjectClass == "Object":
            if OIII != None:
                st.win.blit(OIII, (ObjLoadImage.rect.right + 50, ObjLoadImage.rect.top))
                pygame.draw.rect(st.win, st.uiBC, (ObjLoadImage.rect.right + 50, ObjLoadImage.rect.top, OIIIW, OIIIH), 3)
        elif st.lastSelectionObjectClass == "Text":
            st.win.blit(OFNII, (ObjLoadFont.rect.right + 50, ObjLoadFont.rect.centery - OFNIIH // 2))
            pygame.draw.rect(st.win, st.uiBC, (ObjLoadFont.rect.right + 50 - 5, ObjLoadFont.rect.centery - OFNIIH // 2 - 5, OFNIIW + 10, OFNIIH + 10), 3)
        
        btCloseInfo.update()
        
        # draw the object component name
        for idx, i in enumerate(objComponents[1:]):
            pos = compiledTextes_FOC[idx].get_rect(center=(10, i.start_y + i.rect.height // 2))
            st.win.blit(compiledTextes_FOC[idx], (10 + CTFOCXOF[idx], pos[1] + OPII))
            
        for idx, i in enumerate(CSTN):
            st.win.blit(i, (CSTN_POS[idx][0], CSTN_POS[idx][1] + OPII))
        
        if st.isSelector:
        	ObjSW.update(st.MP, st.MBP)

def drawApp():
    global error
    
    st.winApp.fill(st.GBGC)
    btStartApp.update()
    btSCC.update()
        
    for script in st.MHFU:
    	try:
    		script.Update()
    	except Exception as e:
    	    error = True
    	    tb = e.__traceback__
    	    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
    	    _console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")

    pe.Camera.update()
    
    objLayers = {}
    for obj in pe.objects[::-1]:
        if obj.layer not in objLayers: objLayers[obj.layer] = []
        objLayers[obj.layer].append(obj)
    objLayers = collections.OrderedDict(sorted(objLayers.items()))
    
    for layer in objLayers:
        for obj in objLayers[layer]: obj.update()
    
    st.win.blit(st.winApp, (0, 0))
    
    if st.isConsole: _console.update(st.MP, st.MBP)
    
    appFps = st.uiTSFont.render(f"Fps: {str(int(st.clock.get_fps()))}", 0, st.uiTColor)
    st.win.blit(appFps, (10, st.height - appFps.get_height() // 2 - (st.height - st.AppHeight) // 2))
    
    if error:
        appError = st.uiTSFont.render(f"[Error]", 0, (255, 0, 0))
        st.win.blit(appError, (appFps.get_width() + 30, st.height - appFps.get_height() // 2 - (st.height - st.AppHeight) // 2))

# draw conductor
def drawCR():
    fileConductor.update(st.MP, st.MBP)
    btBackCR.update()
    btCancelCR.update()
    btDeleteCR.update()
    btDoneCR.update()

# draw project assets conductor
def drawPAC():
    PAC.update(st.MP, st.MBP)
    btBackCR.update()
    btCancelCR.update()
    
    if not PAC.viewText and PAC.elem_idx == -1:
	    btAddFile.update()
	    btAddFolder.update()
	    
    if PAC.elem_idx != -1:
        btDeleteFile.update()
        btRenameFile.update()
        btMoveFile.update()
    
    if st.isRenameFile:
        IFFIPAC.update()

# draw menu with projects
def drawProjects():
    PM.update(st.MP, st.MBP)
    btCreateProject.update()
    btLoadProjects.update()
    
    if PM.elem_idx != -1:
        btDeleteProject.update()
        btCopyProject.update()
        btRenameProject.update()
        btOpenExportProject.update()
    
    if st.isRenameProject:
        IFRPIPM.update()
    
    st.win.blit(uiEngineImages["ENGINE_ICON"], (10, 10))
    txENAV = st.uiTSFont.render(f"UniPy {st.version}", 0, st.uiTColor)
    txPos = txENAV.get_rect(center=(0, 10 + uiEngineImages["ENGINE_ICON"].get_height() // 2))
    st.win.blit(txENAV, (uiEngineImages["ENGINE_ICON"].get_width() + 20, txPos[1]))

def drawExportProject():
    btCloseExportProject.update()
    btExportProject.update()
    
    st.win.blit(st.EPT, (10, 10))
    
    y = st.EPT.get_height() + 50
    for tx, elem in zip(uiEPMT, uiEPME):
        st.win.blit(tx, (10, y))
        elem.update()
        y += tx.get_height() + 60 + elem.rect.height