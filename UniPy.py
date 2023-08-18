import engineUI as eui
import settings as st
import os, inspect, collections
import pather as pt
from objects import camera
from modules import Math

OON = []
objClass = []
objName = []
objects = []
fingersPos = [None] * 10
OWS = []
Camera = camera.Camera(st.AppWidth, st.AppHeight)

wWidth, wHeight = st.AppWidth, st.AppHeight
pWidth, pHeight = st.projectSize

textures = {}
texturesTSP = {}
audios = {}

_audioTypes = ["mp3", "ogg", "wav", "flac"]
_imgTypes = ["png", "jpg", "jpeg", "bmp"]
_bodyTypes = ["None", "dynamic", "static", "kinematic"]
_mathSybs = {*"01234567890+-*/.()^ "}

def Error(file, line, error, _type):
    if _type == "error": eui.error = True
    
    eui._console.Log(f"UniPy {_type.capitalize()}: in script \"{file.split(pt.s)[-1]}\": in line [{line}]\n{error}", _type)

def GetObj(name: str):
    
    if name in objName:
        idx = objName.index(name)
        return objects[idx]
    else:
        caller_frame = inspect.currentframe().f_back
        file = caller_frame.f_code.co_filename
        line = caller_frame.f_lineno
        Error(file, line, f"\"{name}\" is not defined", "error")


def SetBgColor(color: tuple):
    if all(isinstance(c, int) and 0 <= c <= 255 for c in color):
        st.GBGC = color
    else:
        caller_frame = inspect.currentframe().f_back
        file = caller_frame.f_code.co_filename
        line = caller_frame.f_lineno
        Error(file, line, f"\"{color}\" invalid color", "warning")

def SaveVariable(key: str, value: any, _type: any):
    path = f".{pt.s}projects{pt.s}{st.projects[st.projectIdx]}{pt.s}$data"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(f"{path}{pt.s}{key}.txt", "w") as f:
        f.write(f"{_type.__name__}: {value}")

def LoadVariable(key: str, notFoundValue = 0):
    try:
	    with open(f".{pt.s}projects{pt.s}{st.projects[st.projectIdx]}{pt.s}$data{pt.s}{key}.txt", "r") as f:
	        get = f.read().split(":", 1)
	        value = f"{get[0].strip()}({get[1].strip()})"
	        return eval(value)
    except:
        caller_frame = inspect.currentframe().f_back
        file = caller_frame.f_code.co_filename
        line = caller_frame.f_lineno
        Error(file, line, f"\"{key}\" is not defined", "warning")
        return notFoundValue

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
    
def GetObjectsWithTag(name: str):
    return [obj for obj in objects if obj.tag == name]

def appQuit(): eui.returnToEditor()
def reloadApp(): eui.startApp()