from UI import (
	button,
	input,
	toggleButton,
	conductor,
	projectManager,
	sohManager,
	console
)

from object import Object
from text import Text
from engineTools import *

import pygame
import importlib
import engineOUAR as ouar
import UniPy as pe
import settings as st
import os, traceback, shutil, copy, re

# settings
uiFont = "fonts/calibri.ttf"
uiTFont = pygame.font.Font(uiFont, st.height // 15)
uiTSFont = pygame.font.Font(uiFont, st.height // 30 if st.height > 720 else st.height // 15)
uiTPFont = pygame.font.Font(uiFont, st.height // 25)

error = False
objComponents = []
compiledTextes_FOC = []

# objects pos in inspector
OPII = 0

# import engine assets
# check mark for toggle button
CK = pygame.image.load("assets/checkmark.png").convert()
CK.set_colorkey((0, 0, 0))

# engine icon
EI = pygame.image.load("assets/engineIcon.png").convert()
EI = pygame.transform.scale(EI, (int(st.width / 7.5) if st.width <= 720 else st.width // 15, int(st.width / 7.5) if st.width <= 720 else st.width // 15))

uiEI = {
    "IP": pygame.image.load("assets/play.png").convert(),
    "IC": pygame.image.load("assets/cancel.png").convert(),
    "IT": pygame.image.load("assets/trash.png").convert(),
    "IL": pygame.image.load("assets/load.png").convert(),
    "IU": pygame.image.load("assets/up.png").convert(),
    "ID": pygame.image.load("assets/up.png").convert(),
    "IB": pygame.image.load("assets/up.png").convert(),
    "IPlus": pygame.image.load("assets/cancel.png").convert(),
    "IF": pygame.image.load("assets/files.png").convert(),
    "IR": pygame.image.load("assets/rename.png").convert(),
    "Icopy": pygame.image.load("assets/copy.png").convert(),
    "dir": pygame.image.load("assets/directory.png").convert(),
    "file": pygame.image.load("assets/file.png").convert(),
    "music": pygame.image.load("assets/music.png").convert(),
    "font": pygame.image.load("assets/font.png").convert(),
    "ILD": pygame.image.load("assets/create_dir.png").convert(),
    "ISB": pygame.image.load("assets/body.png").convert(),
    "Ipoint": pygame.image.load("assets/point.png").convert()
}

uiEI["ID"] = pygame.transform.rotate(uiEI["ID"], 180)
uiEI["IB"] = pygame.transform.rotate(uiEI["IB"], 90)
uiEI["IPlus"] = pygame.transform.rotate(uiEI["IPlus"], 45)
for i in uiEI:
    uiEI[i].set_colorkey((0, 0, 0))
    uiEI[i].fill(st.uiEIC, special_flags=pygame.BLEND_RGB_MULT)

# object image in inspector
OIII = None
OIIIW = 0
OIIIH = 0

# load projects
path = './projects'
st.projects = os.listdir(path)

# to choose project
def toCP():
    st.layer = -1
    pe.objects = []
    pe.objName = []
    pe.objClass = []

# open project
def openProject(idx):
    global selectionObjects
    
    st.files = os.listdir(f"{path}/{st.projects[idx]}")
    st.projectIdx = idx
    st.modules = []
    st.MHFS = []
    st.MHFU = []
    try:
        getInf = open(f"{path}/{st.projects[idx]}/project_info.txt", "r").read()
    except:
        with open(f"{path}/{st.projects[idx]}/project_info.txt", "w") as f:
            f.write(f"{st.AppWidth} {st.AppHeight}")
    
    getInf = open(f"{path}/{st.projects[idx]}/project_info.txt", "r").read()
    inf = getInf.split(",")
    size = inf[0].split(" ")
    st.projectSize = (int(size[0]), int(size[1]))
    
    for i in st.files:
    	if os.path.splitext(i)[-1] in [".png", ".jpg", ".jpeg"]:
    		pe.textures[i] = pygame.image.load(f"{path}/{st.projects[idx]}/{i}")
    		
    		img = pe.textures[i]
    		replacement_color = (1, 1, 1)
    		# Replace transparent pixels with the replacement color
    		for x in range(img.get_width()):
    			for y in range(img.get_height()):
    				if img.get_at((x, y)) == (0, 0, 0, 0):
    					img.set_at((x, y), replacement_color)
    		
    		pe.textures[i] = pygame.Surface(img.get_size()).convert()
    		pe.textures[i].blit(img, (0, 0))
    		pe.textures[i].set_colorkey(replacement_color)
    
    ouar.loadObjs(pe, f"{path}/{st.projects[idx]}/ObjectInfo.txt")
    
    st.layer = 0
    PAC.startPath = f"./projects/{st.projects[idx]}"
    PAC.setPath()
    
    SOHM.elements = []
    SOHM.elemName = []
    for i in pe.objName:
        SOHM.elements.append(i)
        SOHM.elemName.append(i)
    SOHM.nrm()

# functions

def createProject():
    c = 1
    if not os.path.exists(f"{path}/new project"):
        os.makedirs(f"{path}/new project")
        with open(f"{path}/new project/ObjectInfo.txt", "w") as f:
            f.write("")
    else:
        while 1:
            if not os.path.exists(f"{path}/new project ({c})"):
                os.makedirs(f"{path}/new project ({c})")
                with open(f"{path}/new project ({c})/ObjectInfo.txt", "w") as f:
                    f.write("")
                break
            else: c += 1
    
    st.projects = os.listdir(path)
    PM.elements = st.projects
    PM.elemName = st.projects
    PM.nrm()

def createDirectory():
    c = 1
    if not os.path.exists(f"{PAC.thisPath}/new folder"):
        os.makedirs(f"{PAC.thisPath}/new folder")
    else:
        while 1:
            if not os.path.exists(f"{PAC.thisPath}/new folder ({c})"):
                os.makedirs(f"{PAC.thisPath}/new folder ({c})")
                break
            else: c += 1
    
    PAC.reOpenPath()

def AddFileToPAC(path):
    shutil.copy(path, PAC.thisPath)
    
    if os.path.splitext(path)[-1] in [".png", ".jpg", ".jpeg"]:
    	pe.textures[path] = pygame.image.load(path)
    	
    	img = pe.textures[path]
    	replacement_color = (1, 1, 1)
    	# Replace transparent pixels with the replacement color
    	for x in range(img.get_width()):
    		for y in range(img.get_height()):
    			if img.get_at((x, y)) == (0, 0, 0, 0):
    				img.set_at((x, y), replacement_color)
    	
    	pe.textures[i] = pygame.Surface(img.get_size()).convert()
    	pe.textures[i].blit(img, (0, 0))
    	pe.textures[i].set_colorkey(replacement_color)
    
    PAC.setPath()
    startPACR()
    btCancelCR.func = closeCR

def copyProject():
    shutil.copytree(f"{path}/{PM.elements[PM.elemIdx]}", f"{path}/{PM.elements[PM.elemIdx]} (1)")
    
    st.projects = os.listdir(path)
    PM.elements = st.projects
    PM.elemName = st.projects
    PM.nrm()

def deleteFolderInPM():
    shutil.rmtree(f"{path}/{PM.elements[PM.elemIdx]}")
    
    st.projects = os.listdir(path)
    PM.elements = st.projects
    PM.elemName = st.projects
    PM.nrm()

def deleteFileInPAC():
    path = f"{PAC.thisPath}/{PAC.elements[PAC.elemIdx]}"
    try:
        os.remove(path)
        if path in pe.textures:
        	del pe.textures[path]
    except:
        shutil.rmtree(path)
    PAC.reOpenPath()

# close object info
def closeObjectInfo():
    global OPIE
    
    st.lastSelectionObject = None
    st.isSelectBodyType = False

# delete game object
def deleteObj():
    global OPIE, selectionObjects
    
    idx = pe.objName.index(SOHM.elements[SOHM.elemIdx])
    pe.objName.pop(idx)
    pe.objClass.pop(idx)
    pe.objects.pop(idx)
    st.lastSelectionObject = None
    ouar.saveObjs(pe,  f"{path}/{st.projects[st.projectIdx]}/ObjectInfo.txt")
    
    SOHM.elements = []
    SOHM.elemName = []
    SOHM.elemIdx = -1
    for i in pe.objName:
        SOHM.elements.append(i)
        SOHM.elemName.append(i)
    SOHM.nrm()

# back path in conductor
def backCR():
    if st.layer == 2: fileConductor.Back()
    else: PAC.Back()

# start conductor from project assets conductor
def startCRfromPAC():
    st.layer = 2
    btCancelCR.func = closeCRfromPAC

# close conductor from project assets conductor
def closeCRfromPAC():
    st.layer = 3
    btCancelCR.func = closeCR

# start conductor
def startCR():
    st.layer = 2
    btDeleteCR.render = True
    fileConductor.func = changeObjProperty
    fileConductor.startPath = f"./projects/{st.projects[st.projectIdx]}"
    fileConductor.setPath()
    
# start project assets conductor
def startPACR():
    st.layer = 3
    PAC.reOpenPath()
    btDeleteCR.render = False
    fileConductor.content = ""
    fileConductor.func = AddFileToPAC
    fileConductor.startPath = "/storage/emulated/0"
    fileConductor.setPath()
    
# close conductor
def closeCR(): st.layer = 0

def startRenameFilePAC():
    st.isRenameFile = True
    st.lastPressedInput = IFFIPAC
    IFFIPAC.text = PAC.elements[PAC.elemIdx]
    IFFIPAC.hasPress((-1, -1))
    IFFIPAC.checkText()
    IFFIPAC.rect.y = PAC.getIdxPos(PAC.elemIdx)
    
def startRenameProject():
    st.isRenameProject = True
    st.lastPressedInput = IFRPIPM
    IFRPIPM.text = PM.elements[PM.elemIdx]
    IFRPIPM.hasPress((-1, -1))
    IFRPIPM.checkText()
    IFRPIPM.rect.y = PM.getIdxPos(PM.elemIdx)

def endRenameProject():
    if IFRPIPM.text != "":
	    st.isRenameProject = False
	    os.rename(f"{path}/{PM.elements[PM.elemIdx]}",f"{path}/{IFRPIPM.text}")
	    st.projects = os.listdir(path)
	    PM.elements = st.projects
	    PM.elemName = st.projects
	    PM.nrm()

def endRenameFilePAC():
    st.isRenameFile = False
    os.rename(f"{PAC.thisPath}/{PAC.elements[PAC.elemIdx]}",f"{PAC.thisPath}/{IFFIPAC.text}")
    PAC.reOpenPath()

def startSelectorForObjectInspector(elems, button, key):
	ObjSW.key = key
	button.func = closeSelectorForObjectInspector
	st.lastSelectorContent = button.content
	st.LPBFS = button
	button.content = "(self)"
	st.isSelector = True
	ObjSW.elements = elems
	ObjSW.elemName = elems
	ObjSW.nrm()
	ObjSW.x = button.rect.x
	ObjSW.y = button.rect.y - ObjSW.surface.get_height() - 10
	ObjSW.elemIdx = eval(f"ObjSW.elements.index(pe.objects[pe.objName.index(st.lastSelectionObject)].{key})")

def closeSelectorForObjectInspector(button):
	st.isSelector = False
	
	button.func = startSelectorForObjectInspector
	button.content = st.lastSelectorContent

def ADP_OIII(idx):
    global OIII, OIIIW, OIIIH
    
    img = pe.textures[pe.objects[idx].imagePath.split("/")[-1]]
    
    if img.get_width() > img.get_height() + 60:
        OIII = pygame.transform.scale(img, (st.uiISIOIBV, int(st.width * (st.uiISIOIBV / st.height)) if st.height > st.width else int(st.height * (st.uiISIOIBV / st.width))))
    elif img.get_width() < img.get_height() - 60:
        OIII = pygame.transform.scale(img, (st.uiISIOISV, int(st.height * (st.uiISIOISV / st.width)) if st.height > st.width else int(st.width * (st.uiISIOISV / st.height))))
    else:
        OIII = pygame.transform.scale(img, (st.uiISIOIBV, st.uiISIOIBV))
        
    OIII = pygame.transform.flip(OIII, pe.objects[idx].flipX, pe.objects[idx].flipY)
    OIII = pygame.transform.rotate(OIII, pe.objects[idx].angle)
    OIIIW = OIII.get_width()
    OIIIH = OIII.get_height()

def objectUp():
    idx = pe.objName.index(SOHM.elements[SOHM.elemIdx])
    
    if idx > 0:
        SOHM.elemName[idx], SOHM.elemName[idx-1] = SOHM.elemName[idx-1], SOHM.elemName[idx]
        SOHM.elements[idx], SOHM.elements[idx-1] = SOHM.elements[idx-1], SOHM.elements[idx]
        pe.objName[idx], pe.objName[idx-1] = pe.objName[idx-1], pe.objName[idx]
        pe.objects[idx], pe.objects[idx-1] = pe.objects[idx-1], pe.objects[idx]
        pe.objClass[idx], pe.objClass[idx-1] = pe.objClass[idx-1], pe.objClass[idx]
        SOHM.elemIdx -= 1
        ouar.saveObjs(pe,  f"{path}/{st.projects[st.projectIdx]}/ObjectInfo.txt")

def objectDown():
    idx = pe.objName.index(SOHM.elements[SOHM.elemIdx])
    
    if idx != len(SOHM.elements)-1:
        SOHM.elemName[idx], SOHM.elemName[idx+1] = SOHM.elemName[idx+1], SOHM.elemName[idx]
        SOHM.elements[idx], SOHM.elements[idx+1] = SOHM.elements[idx+1], SOHM.elements[idx]
        pe.objName[idx], pe.objName[idx+1] = pe.objName[idx+1], pe.objName[idx]
        pe.objects[idx], pe.objects[idx+1] = pe.objects[idx+1], pe.objects[idx]
        pe.objClass[idx], pe.objClass[idx+1] = pe.objClass[idx+1], pe.objClass[idx]
        SOHM.elemIdx += 1
        ouar.saveObjs(pe,  f"{path}/{st.projects[st.projectIdx]}/ObjectInfo.txt")

def copyObject():
    idx = pe.objName.index(SOHM.elements[SOHM.elemIdx])
    
    pe.objects.append(copy.copy(pe.objects[idx]))
    pe.objName.append(f"{pe.objName[idx]} (1)")
    pe.objClass.append(pe.objClass[idx])
    SOHM.elements.append(f"{pe.objName[idx]} (1)")
    SOHM.elemName.append(f"{pe.objName[idx]} (1)")
    SOHM.elemIdx = len(pe.objects)-1
    SOHM.nrm()

def showConsole():
	st.isConsole = True
	btSCC.func = closeConsole

def closeConsole():
	st.isConsole = False
	btSCC.func = showConsole

# start app
def startApp():
    global error
    
    ouar.loadObjs(pe, f"{path}/{st.projects[st.projectIdx]}/ObjectInfo.txt", "r")
    pe.oldObjects = pe.objects.copy()
    
    st.files = os.listdir(f"{path}/{st.projects[st.projectIdx]}")
    st.modules = []
    st.MHFS = []
    st.MHFU = []
    _console.textes = []
    _console.textesType = []
    _console.tX, _console.tY = (0, 0)
    error = False
    
    for file in st.files:
        if file[-3:] == ".py":
        	try:
        		st.modules.append(__import__(f"projects.{st.projects[st.projectIdx]}.{file[:-3]}", fromlist=["*"]))
        	except Exception as e:
        	       error = True
        	       tb = e.__traceback__
        	       filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
        	       _console.Log(f"UniPy Error: in script \"{filename.split('/')[-1]}\": in line [{line_num}]\n{e}", "error")
    
    for i in st.modules:
        if hasattr(i, "Start"): st.MHFS.append(i)
        if hasattr(i, "Update"): st.MHFU.append(i)
    
    for script in st.modules:
        importlib.reload(script)
    
    st.layer = 1
    st.GBGC = st.GBGSC
    btStartApp.func = returnToEditor
    btStartApp.OI = uiEI["IC"]
    btStartApp.rect.height = st.height - st.AppHeight - 20
    btStartApp.rect.width = btStartApp.rect.height * 2
    btStartApp.rect.y = st.height - btStartApp.rect.height - 10
    btStartApp.rect.x = st.width - btStartApp.rect.width - 10
    btStartApp.ADP()
    
    for obj in pe.objects: obj.setPos()
    for obj in pe.objects: obj.setPosObject()
    
    for script in st.MHFS:
        try: script.Start()
        except Exception as e:
                error = True
                tb = e.__traceback__
                filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                _console.Log(f"UniPy Error: in script \"{filename.split('/')[-1]}\": in line [{line_num}]\n{e}", "error")

# close app
def returnToEditor():
    
    pe.objects = pe.oldObjects.copy()
    st.layer = 0
    st.isConsole = False
    btSCC.func = showConsole
    btStartApp.func = startApp
    btStartApp.OI = uiEI["IP"]
    btStartApp.rect.height = st.uiBS
    btStartApp.rect.width = st.uiBS
    btStartApp.rect.y = st.height - st.uiBS - 10
    btStartApp.rect.x = st.width - st.uiBS - 10
    btStartApp.ADP()
    
    ouar.loadObjs(pe, f"{path}/{st.projects[st.projectIdx]}/ObjectInfo.txt", "r")

# show objects that can be created
def SOTCBC():
    st.isCreateObject = True
    btShowPanel.fontSize = st.uiBFS
    btShowPanel.OI = uiEI["IC"]
    btShowPanel.func = COTCBC
    btShowPanel.ADP()

# close objects that can be created
def COTCBC():
    st.isCreateObject = False
    btShowPanel.fontSize = st.uiBFS
    btShowPanel.OI = uiEI["IPlus"]
    btShowPanel.func = SOTCBC
    btShowPanel.ADP()

def createObject(Class):
    
    st.isCreateObject = False
    btShowPanel.OI = uiEI["IPlus"]
    btShowPanel.func = SOTCBC
    btShowPanel.ADP()
    ouar.addObj(pe, f"{path}/{st.projects[st.projectIdx]}/ObjectInfo.txt", Class)
    
    SOHM.elements = []
    SOHM.elemName = []
    for i in pe.objName:
        SOHM.elements.append(i)
        SOHM.elemName.append(i)
    SOHM.nrm()
    
    SOHM.elements = []
    SOHM.elemName = []
    for i in pe.objName:
        SOHM.elements.append(i)
        SOHM.elemName.append(i)
    SOHM.nrm()

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
        SOHM.elements[SOHM.lastElem] = ObjName.text
        SOHM.elemName[SOHM.lastElem] = ObjName.text
        SOHM.nrm()
        pe.objName[idx] = ObjName.text
        st.lastSelectionObject = ObjName.text
        
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
    
    elif key == "brightness":
        try:
       	 pe.objects[idx].brightness = max(0, eval(ObjBGT.text))
       	 ObjBGT.text = str(pe.objects[idx].brightness)
        except:
            ObjBGT.text = str(pe.objects[idx].brightness)
    
    elif key == "font":
        st.layer = 0
        try:
            if content != None:
                font = pygame.font.Font(content, 1)
                pe.objects[idx].font = content
            else: pe.objects[idx].font = content
        except: pass
    
    elif key == "image":
        st.layer = 0
        try:
	        if content != None:
	            pe.objects[idx].image = pe.textures[content.split("/")[-1]]
	            pe.objects[idx].imagePath = content
	            ADP_OIII(idx)
	        else:
	            pe.objects[idx].image = content
	            pe.objects[idx].imagePath = content
	            OIII = None
        except: pass
    
    try:
        obj.endText = 0
        obj.checkText()
    except: pass
    ouar.saveObjs(pe, f"{path}/{st.projects[st.projectIdx]}/ObjectInfo.txt")

# load object property
def setObjProperty(text):
    global OPII, objComponents, OIII, OIIIW, OIIIH, compiledTextes_FOC
    
    st.lastSelectionObject = text
    compiledTextes_FOC = []
    
    idx = pe.objName.index(st.lastSelectionObject)
    
    if pe.objClass[idx] == "Object":
        objComponents = [ObjName, ObjX, ObjY, ObjWidth, ObjHeight, ObjAngle, ObjTSP, ObjCX, ObjCY, ObjBD, ObjRender, ObjFlipX, ObjFlipY, ObjLoadImage]
        fileConductor.content = "'image'"
        btDeleteCR.content = "('image', None)"
        
        if pe.objects[idx].image != None: ADP_OIII(idx)
     
        else: OIII = None
    
    elif pe.objClass[idx] == "Text":
       objComponents = [ObjName, ObjX, ObjY, ObjText, ObjFontSize, ObjLoadFont, ObjColor, ObjTSP, ObjAngle, ObjCX, ObjCY, ObjTC, ObjRender, ObjFlipX, ObjFlipY]
       fileConductor.content = "'font'"
       btDeleteCR.content = "('font', None)"
       
    idxx = 1
    objComponents[0].rect.y = st.uiSOCP
    objComponents[0].startY = st.uiSOCP
    for i in objComponents[1:]:
        objCm = uiTSFont.render(re.sub(r'(?<!^)([A-Z])', r' \1', i.key).title(), 0, st.uiTColor)
        compiledTextes_FOC.append(objCm)
        i.rect.x = objCm.get_width() + 20
                
        i.rect.y = objComponents[idxx - 1].rect.y + objComponents[idxx - 1].rect.height + 20
        i.startY = objComponents[idxx - 1].rect.y + objComponents[idxx - 1].rect.height + 20
        idxx += 1
    
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
    
    if pe.objClass[idx] == "Text":
        ObjFontSize.text = str(pe.objects[idx].sfs)
    
    OPII = 0
    for i in objComponents:
        i.rect.y = i.startY
        if type(i) == input.Input:
            i.endText = 0
            i.checkText()

# button for start app
btStartApp = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "Run", borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = uiFont, func = startApp, x = st.width - st.uiBS - 10, y = st.height - st.uiBS - 10, image = uiEI["IP"], color = st.uiBC, pressedColor = st.uiBPC)

# button for console
btSCC = button.Button(st.win, height = st.height - st.AppHeight - 20, width = (st.height - st.AppHeight - 20) * 2, text = "console", borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = uiFont, func = showConsole, image = None, color = st.uiBC, pressedColor = st.uiBPC)

btSCC.rect.topleft = (st.width - btSCC.rect.width * 2 - 20, st.height - btSCC.rect.height - 10)

# button for close object info
btCloseInfo = button.Button(st.win, y = 10, x = st.width - st.uiBS - 10,  width = st.uiBS, height = st.uiBS, text = "X", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = closeObjectInfo, fontPath = uiFont, image = uiEI["IC"], color = st.uiBC, pressedColor = st.uiBPC)

# button for show panel for adding objects
btShowPanel = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "+", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = SOTCBC, fontPath = uiFont, x = btStartApp.rect.x, y = btStartApp.rect.y - st.uiBS - 10, color = st.uiBC, pressedColor = st.uiBPC, image = uiEI["IPlus"])

# button for return to choose project
btToCP = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "<", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = toCP, fontPath = uiFont, y = btShowPanel.rect.y - st.uiBS - 10, x = btShowPanel.rect.x, color = st.uiBC, pressedColor = st.uiBPC, image = uiEI["IB"])

# button open project assets
btOPA = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "D", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startPACR, fontPath = uiFont, y = btToCP.rect.y - st.uiBS - 10, x = btToCP.rect.x, image = uiEI["IF"], color = st.uiBC, pressedColor = st.uiBPC)

# button for down project
btPD = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "D", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = objectDown, fontPath = uiFont, y = btOPA.rect.y - st.uiBS - 10, x = btOPA.rect.x, image = uiEI["ID"], color = st.uiBC, pressedColor = st.uiBPC)

# button for up project
btPU = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "U", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = objectUp, fontPath = uiFont, y = btPD.rect.y - st.uiBS - 10, x = btPD.rect.x, image = uiEI["IU"], color = st.uiBC, pressedColor = st.uiBPC)

# button for copy object
btCopy = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "copy", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = copyObject, fontPath = uiFont, y = btPU.rect.y - st.uiBS - 10, x = btPU.rect.x, image = uiEI["Icopy"], color = st.uiBC, pressedColor = st.uiBPC)

# button for delete object
btDeleteObj = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "delete", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = deleteObj, fontPath = uiFont, y = btCopy.rect.y - st.uiBS - 10, x = btCopy.rect.x, image = uiEI["IT"], color = st.uiBC, pressedColor = st.uiBPC)

# button for cancel load file in conductor
btCancelCR = button.Button(st.win, y = 10, x = st.width - st.uiBS - 10, width = st.uiBS, height = st.uiBS, text = "cancel", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = closeCR, fontPath = uiFont, image = uiEI["IC"], color = st.uiBC, pressedColor = st.uiBPC)

# button for back in conductor
btBackCR = button.Button(st.win, x = btCancelCR.rect.x - st.uiBS - 10, y = btCancelCR.rect.y, width = st.uiBS, height = st.uiBS, text = "<", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = backCR, fontPath = uiFont, color = st.uiBC, pressedColor = st.uiBPC, image = uiEI["IB"])

# button for delete obj image or font in conductor
btDeleteCR = button.Button(st.win, y = btBackCR.rect.y, x = btBackCR.rect.x - st.uiBS - 10, width = st.uiBS, height = st.uiBS, text = "delete", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = changeObjProperty, fontPath = uiFont, content = "('image', None)", image = uiEI["IT"], color = st.uiBC, pressedColor = st.uiBPC)

# button for file to project assets conductor
btAddFile = button.Button(st.win, y = btBackCR.rect.y, x = btBackCR.rect.x - st.uiBS - 10, width = st.uiBS, height = st.uiBS, text = "+", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startCRfromPAC, fontPath = uiFont, color = st.uiBC, pressedColor = st.uiBPC, image = uiEI["IPlus"])

# button for create new folder in project assets conductor
btAddFolder = button.Button(st.win, y = btAddFile.rect.y, x = btAddFile.rect.x - st.uiBS - 10, width = st.uiBS, height = st.uiBS, text = "CF", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = createDirectory, fontPath = uiFont, color = st.uiBC, pressedColor = st.uiBPC, image = uiEI["ILD"])

# button for file to project assets conductor
btDeleteFile = button.Button(st.win, y = btAddFolder.rect.y, x = btAddFolder.rect.x - st.uiBS - 10, width = st.uiBS, height = st.uiBS, text = "delete", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = deleteFileInPAC, fontPath = uiFont, color = st.uiBC, pressedColor = st.uiBPC, image = uiEI["IT"])

# button for rename file in project assets conductor
btRenameFile = button.Button(st.win, y = btDeleteFile.rect.y, x = btDeleteFile.rect.x - st.uiBS - 10, width = st.uiBS, height = st.uiBS, text = "rename", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startRenameFilePAC, fontPath = uiFont, color = st.uiBC, pressedColor = st.uiBPC, image = uiEI["IR"])

# button for create new project
btCreateProject = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "+", borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = uiFont, func = createProject, x = st.width - st.uiBS - 10, y = st.height - st.uiBS - 10, color = st.uiBC, pressedColor = st.uiBPC, image = uiEI["IPlus"])

# button for delete project
btDeleteProject = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "del", borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = uiFont, func = deleteFolderInPM, x = btCreateProject.rect.x, y = btCreateProject.rect.y - st.uiBS - 10, color = st.uiBC, pressedColor = st.uiBPC, image = uiEI["IT"])

# button for copy project
btCopyProject = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "del", borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = uiFont, func = copyProject, x = btDeleteProject.rect.x, y = btDeleteProject.rect.y - st.uiBS - 10, color = st.uiBC, pressedColor = st.uiBPC, image = uiEI["Icopy"])

# button for rename project
btRenameProject = button.Button(st.win, width = st.uiBS, height = st.uiBS, text = "rename", borderRadius = st.uiWBBR, fontSize = st.uiBFS, fontPath = uiFont, func = startRenameProject, x = btCopyProject.rect.x, y = btCopyProject.rect.y - st.uiBS - 10, color = st.uiBC, pressedColor = st.uiBPC, image = uiEI["IR"])

# inputs for object inspector
ObjName = input.Input(st.win, changeObjProperty, noText = "Name...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "name", content = "(self.key)")

ObjX = input.Input(st.win, changeObjProperty, noText = "PosX...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "x", content = "(self.key)")

ObjY = input.Input(st.win, changeObjProperty, noText = "PosY...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "y", content = "(self.key)")

ObjWidth = input.Input(st.win, changeObjProperty, noText = "Width...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "width", content = "(self.key)")

ObjHeight = input.Input(st.win, changeObjProperty, noText = "Height...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "height", content = "(self.key)")

ObjAngle = input.Input(st.win, changeObjProperty, noText = "Angle...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "angle", content = "(self.key)")

ObjCX = input.Input(st.win, changeObjProperty, noText = "pos...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "cx", content = "(self.key)")

ObjCY = input.Input(st.win, changeObjProperty, noText = "pos...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "cy", content = "(self.key)")

ObjText = input.Input(st.win, changeObjProperty, noText = "text...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "text", content = "(self.key)")

ObjFontSize = input.Input(st.win, changeObjProperty, noText = "fontSize...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "fontSize", content = "(self.key)")

ObjColor = input.Input(st.win, changeObjProperty, noText = "color...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "color", content = "(self.key)")

ObjTSP = input.Input(st.win, changeObjProperty, noText = "transparent...", maxChars = 256, borderRadius = st.uiWIBR, width = st.uiIW, height = st.uiIH, fontSize = 40, fontPath = uiFont, color = st.uiIC, pressedColor = st.uiIPC, key = "transparent", content = "(self.key)")

# toggles button for object inspector
ObjRender = toggleButton.ToggleButton(st.win, "render", changeObjProperty, borderRadius = st.uiWIBR, fillSize = 5, image = CK, width = st.uiBS, height = st.uiBS, color = st.uiBC)

ObjFlipX = toggleButton.ToggleButton(st.win, "flipX", changeObjProperty, borderRadius = st.uiWIBR, fillSize = 5, image = CK, width = st.uiBS, height = st.uiBS, color = st.uiBC)

ObjFlipY = toggleButton.ToggleButton(st.win, "flipY", changeObjProperty, borderRadius = st.uiWIBR, fillSize = 5, image = CK, width = st.uiBS, height = st.uiBS, color = st.uiBC)

# buttons for object inspector
ObjLoadImage = button.Button(st.win, x = st.width - 110, y = 10, width = st.uiBS, height = st.uiBS, text = "set", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startCR, fontPath = uiFont, key = "image", image = uiEI["IL"], color = st.uiBC, pressedColor = st.uiBPC)

ObjBD = button.Button(st.win, x = st.width - 110, y = 10, width = st.uiBS, height = st.uiBS, text = "select", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startSelectorForObjectInspector, fontPath = uiFont, image = uiEI["ISB"], color = st.uiBC, pressedColor = st.uiBPC, key = "bodyType", content = f"(['None', 'dynamic', 'static'], self, 'bodyType')")

ObjTC = button.Button(st.win, x = st.width - 110, y = 10, width = st.uiBS, height = st.uiBS, text = "select", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startSelectorForObjectInspector, fontPath = uiFont, image = uiEI["Ipoint"], color = st.uiBC, pressedColor = st.uiBPC, key = "textCentering", content = f"(['left', 'center', 'right'], self, 'textCentering')")

ObjLoadFont = button.Button(st.win, x = st.width - 110, y = 10, width = st.uiBS, height = st.uiBS, text = "set", borderRadius = st.uiWBBR, fontSize = st.uiBFS, func = startCR, fontPath = uiFont, key = "font", image = uiEI["IL"], color = st.uiBC, pressedColor = st.uiBPC)

# selectors for object inspector
ObjSW = sohManager.SOH_Manager(st.win, changeObjProperty, fontPath = uiFont, borderRadius = btShowPanel.borderRadius, color = btShowPanel.color, elemColor = btShowPanel.pressedColor, width = st.width // 2, height = st.height // 4 if st.width < st.height else st.height // 2, content = "(self.key, self.elements[self.elemIdx])", maxD = 5, minD = 3.5, key = "bodyType")

# file conductor
fileConductor = conductor.Conductor(st.win, changeObjProperty, width = st.width, height = st.height, fontSize = 60, y = 20 + st.uiBS, color = st.uiCC, fontPath = uiFont, elemColor = st.uiCEC, images = [uiEI["dir"], uiEI["file"], uiEI["music"], uiEI["font"]], content = "'image'")

# projects assets conductor
PAC = conductor.Conductor(st.win, None, width = st.width, height = st.height, fontSize = 60, y = 20 + st.uiBS, color = st.uiCC, fontPath = uiFont, elemColor = st.uiCEC, images = [uiEI["dir"], uiEI["file"], uiEI["music"], uiEI["font"]], onlyView = True)

# input for rename file in project assets conductor
IFFIPAC = input.Input(st.win, endRenameFilePAC, noText = "Name...", maxChars = 256, width = PAC.elemWidth, height = PAC.elemHeight, fontSize = 40, fontPath = uiFont, color = PAC.elemColor, pressedColor = st.uiIPC, x = 10, ATL = False)

# project manager
PM = projectManager.ProjectManager(st.win, "eui.openProject", elements = st.projects.copy(), fontPath = uiFont, y = 10 + EI.get_height() + 50, borderRadius = st.uiWPEOEEBR, color = st.uiBgColor, elemColor = st.uiPEC, width = st.width // 1.5, x = st.width // 2 - (st.width // 1.5) // 2)

# input for rename project in project manager
IFRPIPM = input.Input(st.win, endRenameProject, noText = "Name...", maxChars = 256, width = PM.elemWidth, height = PM.elemHeight, fontSize = 40, fontPath = uiFont, color = PM.elemColor, pressedColor = st.uiIPC, x = PM.x, ATL = False)

# selection object hierarchy
SOHM = sohManager.SOH_Manager(st.win, setObjProperty, fontPath = uiFont, y = 10, x = 10, borderRadius = st.uiWPEOEEBR, color = st.uiSOHBGC, elemColor = st.uiSOHC, width = st.width // 1.3, height = st.height - 20, content = "(self.elements[self.elemIdx])")

# selection new object panel
SNOP = sohManager.SOH_Manager(st.win, createObject, fontPath = uiFont, y = btShowPanel.rect.y - st.height // 2 - 10, x = btShowPanel.rect.right - st.width // 1.5, borderRadius = btShowPanel.borderRadius, color = btShowPanel.color, elemColor = btShowPanel.pressedColor, width = st.width // 1.5, height = st.height // 2, content = "(self.elements[self.elemIdx])", elements = ["Object", "Text"], maxD = 5, minD = 3.5)

# engine console
_console = console.Console(st.win, height = st.AppHeight // 2, width = st.AppWidth, font = uiFont, y = st.AppHeight - st.AppHeight // 2)

# function for draw engine UI
def drawUI():
    
    if st.lastSelectionObject == None:
        btStartApp.update()
        btShowPanel.update()
        
        if not st.isCreateObject:
            btToCP.update()
            btOPA.update()
            
            if SOHM.elemIdx != -1:
                btPD.update()
                btPU.update()
                btCopy.update()
                btDeleteObj.update()
        SOHM.update()
        
        if st.isCreateObject: SNOP.update()
    
    else:
        # update the object components
        for i in objComponents:
            i.update()
        
        if st.lastSelectionObjectClass == "Object":
            if OIII != None:
                st.win.blit(OIII, (ObjLoadImage.rect.x + ObjLoadImage.rect.width + 50, ObjLoadImage.rect.bottom - OIIIH))
                pygame.draw.rect(st.win, st.uiBC, (ObjLoadImage.rect.x + ObjLoadImage.rect.width + 50, ObjLoadImage.rect.bottom - OIIIH, OIIIW, OIIIH), 3)
        
        btCloseInfo.update()
        
        # draw the object component name
        idx = 0
        for i in objComponents[1:]:
            objCmPos = compiledTextes_FOC[idx].get_rect(center=(10, i.startY + i.rect.height // 2 + OPII))
            st.win.blit(compiledTextes_FOC[idx], (10, objCmPos[1]))
            idx += 1
        
        if st.isSelector:
        	ObjSW.update()

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
        	_console.Log(f"UniPy Error: in script \"{filename.split('/')[-1]}\": in line [{line_num}]\n{e}", "error")
        	
    for obj in pe.objects[::-1]: obj.update()
    
    st.win.blit(st.winApp, (0, 0))
    
    if st.isConsole: _console.update()
    
    appFps = uiTSFont.render(f"Fps: {str(int(st.clock.get_fps()))}", 0, st.uiTColor)
    st.win.blit(appFps, (10, st.height - appFps.get_height() - 10))
    
    if error:
        appError = uiTSFont.render(f"[Error]", 0, (255, 0, 0))
        st.win.blit(appError, (appFps.get_width() + 30, st.height - appFps.get_height() - 10))

# draw conductor
def drawCR():
    fileConductor.update()
    btBackCR.update()
    btCancelCR.update()
    btDeleteCR.update()

# draw project assets conductor
def drawPAC():
    PAC.update()
    btBackCR.update()
    btCancelCR.update()
    
    if not PAC.viewText:
	    btAddFile.update()
	    btAddFolder.update()
	    
    if PAC.elemIdx != -1:
        btDeleteFile.update()
        btRenameFile.update()
    
    if st.isRenameFile:
        IFFIPAC.update()

# draw menu with projects
def drawProjects():
    PM.update()
    btCreateProject.update()
    
    if PM.elemIdx != -1:
        btDeleteProject.update()
        btCopyProject.update()
        btRenameProject.update()
    
    if st.isRenameProject:
        IFRPIPM.update()
    
    st.win.blit(EI, (10, 10))
    txENAV = uiTSFont.render(f"UniPy {st.version}", 0, st.uiTColor)
    txPos = txENAV.get_rect(center=(0, 10 + EI.get_height() // 2))
    st.win.blit(txENAV, (EI.get_width() + 20, txPos[1]))