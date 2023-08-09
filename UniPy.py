import engineUI as eui
import settings as st
import os, inspect, collections
import pather as pt
from objects import camera

OON = []
objClass = []
objName = []
objects = []
fingersPos = [[-99, -99]] * 10
OWS = []
Camera = camera.Camera(st.AppWidth, st.AppHeight)

wWidth, wHeight = st.AppWidth, st.AppHeight
pWidth, pHeight = st.projectSize

textures = {}
texturesTSP = {}
audios = {}

_varTypes = [
                "str",
                "int",
                "float",
                "bool",
                "list",
                "tuple",
                "dict",
                "set"
                    ]
_audioTypes = [
                    "mp3",
                    "ogg",
                    "wav",
                    "flac"
                        ]
_imgTypes = [
                "png",
                "jpg",
                "jpeg"
                    ]

def Error(file, line, error, _type):
    if _type == "error": eui.error = True
    
    eui._console.Log(f"UniPy {_type.capitalize()}: in script \"{file.split(pt.s)[-1]}\": in line [{line}]\n{error}", _type)

# возвращает ссылку на объект
def GetObj(name: str):
    
    if name in objName:
        idx = objName.index(name)
        return objects[idx]
    else:
        caller_frame = inspect.currentframe().f_back
        file = caller_frame.f_code.co_filename
        line = caller_frame.f_lineno
        Error(file, line, f"\"{name}\" is not defined", "error")

# задает цвет фона программы
def SetBgColor(color: tuple):
    if all(isinstance(c, int) and 0 <= c <= 255 for c in color):
        st.GBGC = color
    else:
        caller_frame = inspect.currentframe().f_back
        file = caller_frame.f_code.co_filename
        line = caller_frame.f_lineno
        Error(file, line, f"\"{color}\" invalid color", "warning")

# сохраняет значение переменной по ключу
def SaveVariable(keyName: str, variable, _type):
    if not os.path.exists(f".{pt.s}projects{pt.s}{st.projects[st.projectIdx]}{pt.s}$data"):
        os.makedirs(f".{pt.s}projects{pt.s}{st.projects[st.projectIdx]}{pt.s}$data")
    
    if _type in _varTypes:
        with open(f".{pt.s}projects{pt.s}{st.projects[st.projectIdx]}{pt.s}$data{pt.s}{keyName}.txt", "w") as f:
            f.write(f"{_type}: {variable}")
    else:
        caller_frame = inspect.currentframe().f_back
        file = caller_frame.f_code.co_filename
        line = caller_frame.f_lineno
        Error(file, line, f"\"{_type}\" invalid variable type", "warning")

# загружает значение переменной по ключу
def LoadVariable(keyName: str, SERT = 0):
    try:
	    with open(f".{pt.s}projects{pt.s}{st.projects[st.projectIdx]}{pt.s}$data{pt.s}{keyName}.txt", "r") as f:
	        get = f.read().split(":", 1)
	        return eval(f"{_varTypes[_varTypes.index(get[0])]}({get[1][1:]})")
                
    except:
        caller_frame = inspect.currentframe().f_back
        file = caller_frame.f_code.co_filename
        line = caller_frame.f_lineno
        Error(file, line, f"\"{keyName}\" is not defined", "warning")
    return SERT

def GetModule(name: str):
    for module in st.modules:
        if name == module.__name__.split(".")[-1]: return module
    
    caller_frame = inspect.currentframe().f_back
    file = caller_frame.f_code.co_filename
    line = caller_frame.f_lineno
    Error(file, line, f"\"{name}\" is not defined", "warning")

def log(text: str):
	caller_frame = inspect.currentframe().f_back
	file = caller_frame.f_code.co_filename
	line = caller_frame.f_lineno
	eui._console.Log(text, "log", file.split(pt.s)[-1], line)

def CloneObject(name):
    global objLayers
    
    if name in OON:
        if OWS != []: owsIdx = OWS.index(OWS[-1])+1
        else: owsIdx = 0
        
        eui.ouar.loadObjs(eui.pe, f"{eui.PATH}{pt.s}{st.projects[st.projectIdx]}{pt.s}ObjectInfo.txt", OON.index(name))
        objects[-1].setPos()
        objects[-1].setPosObject()
        eui.loadObjectScriptLinks(True)
        
        for i in OWS[owsIdx:]:
            
            if hasattr(i, "Start"): i.Start()
            if hasattr(i, "Update"): st.MHFU.append(i)
        return objects[-1]
    
    else:
        caller_frame = inspect.currentframe().f_back
        file = caller_frame.f_code.co_filename
        line = caller_frame.f_lineno
        Error(file, line, f"\"{name}\" is not defined", "warning")

def GetTexture(name: str, fullAlpha: bool = False):
    ftxs = [i for i in textures] if not fullAlpha else [i for i in texturesTSP]
    txs = [i.split(pt.s)[-1].rsplit(".", 1)[0] for i in textures] if not fullAlpha else [i for i in texturesTSP]
    
    if name in txs:

        return textures[ftxs[txs.index(name)]] if not fullAlpha else texturesTSP[ftxs[txs.index(name)]]
    else:
        caller_frame = inspect.currentframe().f_back
        file = caller_frame.f_code.co_filename
        line = caller_frame.f_lineno
        Error(file, line, f"\"{name}\" is not defined", "warning")
        
def GetSound(name: str):
    faus = [i for i in audios]
    aus = [i.split(pt.s)[-1].rsplit(".", 1)[0] for i in audios]
    
    if name in aus:

        return audios[faus[aus.index(name)]]
    else:
        caller_frame = inspect.currentframe().f_back
        file = caller_frame.f_code.co_filename
        line = caller_frame.f_lineno
        Error(file, line, f"\"{name}\" is not defined", "warning")

def SetCamera(name: str):
    if name in objName:
        Camera.target = objects[objName.index(name)]
    else:
        caller_frame = inspect.currentframe().f_back
        file = caller_frame.f_code.co_filename
        line = caller_frame.f_lineno
        Error(file, line, f"\"{name}\" is not defined", "warning")

def DelObj(obj):
    global objects, OWS, objLayers
    
    if obj in objects:
        for script in obj.S_LINKS:
            OWS.remove(script)
            if script in st.MHFU: st.MHFU.remove(script)
        if obj.PARENT in objName: objName.remove(obj.PARENT)
        objects.remove(obj)
    else:
        caller_frame = inspect.currentframe().f_back
        file = caller_frame.f_code.co_filename
        line = caller_frame.f_lineno
        Error(file, line, f"\"{obj}\" is not defined", "warning")

def distance(obj1, obj2):
    caller_frame = inspect.currentframe().f_back
    file = caller_frame.f_code.co_filename
    line = caller_frame.f_lineno

    if obj1 not in objects:
        Error(file, line, f"\"{obj1}\" is not defined", "warning")
        return -1
    if obj2 not in objects:
        Error(file, line, f"\"{obj2}\" is not defined", "warning")
        return -1

    return ((obj2.rect.x - obj1.rect.x) ** 2 + (obj2.rect.y - obj1.rect.y) ** 2) ** (0.5)
    
def GetObjectsWithTag(name: str):
    return [obj for obj in objects if obj.tag == name]

def appQuit(): eui.returnToEditor()
def reloadApp(): eui.startApp()