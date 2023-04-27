import engineUI as eui
import settings as st
import os, inspect

objClass = []
objName = []
objects = []
oldObjects = []
fingersPos = [[-99, -99] for i in range(10)]

textures = {}

_varTypes = ["str", "int", "float", "bool"]

# возвращает ссылку на объект
def GetObj(name: str):
    if name in objName:
        idx = objName.index(name)
        return objects[idx]
    else:
        eui._console.Log(f"UniPy Error: obj001: \"{name}\" is not defined", "error")
        eui.error = True

# задает цвет фона программы
def SetBgColor(color: tuple):
    if all(isinstance(c, int) and 0 <= c <= 255 for c in color):
        st.GBGC = color
    else:
        eui._console.Log(f"UniPy Error: color: \"{color}\" invalid color", "warning")

# сохраняет значение переменной по ключу
def SaveVariable(keyName: str, variable, type):
	
	if not os.path.exists(f"{st.GPTP()}$data"):
		os.makedirs(f"{st.GPTP()}$data")
		
	if type in _varTypes:
		with open(f"{st.GPTP()}$data/{keyName}.txt", "w") as f:
		   f.write(f"{type}: {variable}")
	else:
		eui._console.Log(f"UniPy Error: varType: \"{type}\" invalid variable type", "warning")

# загружает значение переменной по ключу
def LoadVariable(keyName: str, SERT = 0):
    try:
	    with open(f"{st.GPTP()}$data/{keyName}.txt", "r") as f:
	            get = f.read().split(":", 1)
	            return eval(f"{_varTypes[_varTypes.index(get[0])]}({get[1][1:]})")
                
    except:
        eui._console.Log(f"UniPy Error: file: \"{keyName}\" is not defined", "warning")
        return SERT
        
def consoleLog(text: str):
	caller_frame = inspect.currentframe().f_back
	file = caller_frame.f_code.co_filename
	line = caller_frame.f_lineno
	eui._console.Log(text, "log", file.split("/")[-1], line)

# exit from app
def appQuit():
	eui.returnToEditor()

# reload the app
def reloadApp():
	eui.startApp()