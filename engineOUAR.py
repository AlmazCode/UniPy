from objects.object import Object
from objects.text import Text
import settings as st
import re, os

regex = re.compile(r',\s*\n')

defaultComponents = {
            "x": 0,
            "y": 0,
            "w": 0,
            "h": 0,
            "render": True,
            "image": None,
            "bd": "None",
            "a": 0,
            "sw": 0,
            "sh": 0,
            "fx": False,
            "fy": False,
            "sx": 0,
            "sy": 0,
            "cx": "None",
            "cy": "None",
            "tsp": 255,
            "ufa": False,
            "s": "None",
            "sc": {},
            "scc": {},
            "color": [255, 255, 255],
            "uc": False,
            "l": 0,
            "t": "obj",
            "text": "text",
            "fs": 32,
            "font": None,
            "sfs": 32,
            "tc": "left",
            "rt": False,
            "sm": False,
            }

def loadObjs(pe, path, IDX = -1):
    
    if not os.path.exists(path):
        with open(path, "w+") as f:
            f.write("")
    
    file = open(path, "r").read()
    get = file.split("!next!")
    
    if file != "":
        if IDX != -1: get = get[IDX: IDX+1]
        
        for idx, i in enumerate(get):
            get2 = regex.split(i)
            if IDX == -1:
                pe.objClass.append(get2[1].strip())
                pe.objName.append(get2[0].strip() if get2[0].strip() not in pe.objName else f"{get2[0].strip()} (rename it!)")
            cm = defaultComponents.copy()
            for _obj0xfg in get2[2:]:
                _obj0xfg = _obj0xfg.split(":", 1)
                try: val = eval(f"{_obj0xfg[1][1:]}")
                except: val = _obj0xfg[1][1:].strip()
                cm[_obj0xfg[0]] = val
                
            if get2[1].strip() == "Object":
                pe.objects.append(Object(st.winApp, cm["x"], cm["y"], cm["w"], cm["h"], cm["render"], cm["image"], cm["bd"], cm["a"], cm["sw"], cm["sh"], cm["fx"], cm["fy"], cm["sx"], cm["sy"], cm["cx"], cm["cy"], cm["tsp"], cm["ufa"], cm["s"], cm["sc"], cm["scc"], cm["color"], cm["uc"], get2[0].strip(), cm["l"], cm["t"]))
            elif get2[1].strip() == "Text":
                pe.objects.append(Text(st.winApp, cm["x"], cm["y"], cm["text"], cm["fs"], cm["font"], cm["color"], cm["tsp"], cm["a"], cm["render"], cm["fx"], cm["fy"], cm["cx"], cm["cy"], cm["sx"], cm["sy"], cm["sfs"], cm["tc"], cm["rt"], cm["s"], cm["sc"], cm["scc"], cm["uc"], get2[0].strip(), cm["l"], cm["t"], cm["sm"]))
        
def writeObj(pe, idx, _type):
    if _type == "Object":
        return f"""{pe.objName[idx]},
{_type},
x: {pe.objects[idx].x},
y: {pe.objects[idx].y},
w: {pe.objects[idx].width},
h: {pe.objects[idx].height},
render: {pe.objects[idx].render},
image: '{pe.objects[idx].imagePath}',
bd: '{pe.objects[idx].bodyType}',
a: {pe.objects[idx].angle},
sw: {pe.objects[idx].SW},
sh: {pe.objects[idx].SH},
fx: {pe.objects[idx].flipX},
fy: {pe.objects[idx].flipY},
sx: {pe.objects[idx].sx},
sy: {pe.objects[idx].sy},
cx: '{pe.objects[idx].cx}',
cy: '{pe.objects[idx].cy}',
tsp: {pe.objects[idx].transparent},
ufa: {pe.objects[idx].useFullAlpha},
s: '{pe.objects[idx].script}',
sc: {pe.objects[idx].S_CONTENT},
scc: {pe.objects[idx].SC_CHANGED},
color: {pe.objects[idx].color},
uc: {pe.objects[idx].useCamera},
t: '{pe.objects[idx].tag}',
l: {pe.objects[idx].layer}"""

    elif _type == "Text":
        return f"""{pe.objName[idx]},
{_type},
x: {pe.objects[idx].x},
y: {pe.objects[idx].y},
text: '{pe.objects[idx].text}',
fs: {pe.objects[idx].fontSize},
font: '{pe.objects[idx].fontPath}',
color: {pe.objects[idx].color},
tsp: {pe.objects[idx].transparent},
a: {pe.objects[idx].angle},
render: {pe.objects[idx].render},
fx: {pe.objects[idx].flipX},
fy: {pe.objects[idx].flipY},
cx: '{pe.objects[idx].cx}',
cy: '{pe.objects[idx].cy}',
sx: {pe.objects[idx].sx},
sy: {pe.objects[idx].sy},
sfs: {pe.objects[idx].sfs},
tc: '{pe.objects[idx].textCentering}',
rt: {pe.objects[idx].richText},
s: '{pe.objects[idx].script}',
sc: {pe.objects[idx].S_CONTENT},
scc: {pe.objects[idx].SC_CHANGED},
uc: {pe.objects[idx].useCamera},
l: {pe.objects[idx].layer},
t: '{pe.objects[idx].tag}',
sm: {pe.objects[idx].smooth}"""

def saveObjs(pe, path):
    file = open(path, "w")
    file.write("")
    file.close()
    file = open(path, "a")
    for idx, i in enumerate(pe.objClass):
        file.write(writeObj(pe, idx, i))
        if idx != len(pe.objClass) - 1:
            file.write("\n!next!\n")

def addObj(pe, path, newClass):
    file = open(path, "w")
    file.write("")
    file.close()
    
    if newClass in pe.objClass:
        name = f"{newClass}{pe.objClass.count(newClass) + 1}"
    else:
        name = f"{newClass}1"
    
    pe.objName.append(name)
    pe.objClass.append(newClass)
    
    if newClass == "Object":
        pe.objects.append(Object(st.winApp, 0, 0, 0, 0, True, "None", "None", 0, 0, 0, False, False, 0, 0, "None", "None", 255, False, "None", {}, {}, (255, 255, 255), True, name, 0, "obj"))
    elif newClass == "Text":
        pe.objects.append(Text(st.winApp, 0, 0, "text", 32, "None", (0, 0, 0), 255, 0, True, False, False, "None", "None", 0, 0, 32, "left", False, "None", {}, {}, True, name, 0, "obj", False))
    else: return 0
    
    file = open(path, "a")
    
    for idx, i in enumerate(pe.objClass):
        file.write(writeObj(pe, idx, i))
        if idx != len(pe.objClass) - 1:
            file.write("\n!next!\n")