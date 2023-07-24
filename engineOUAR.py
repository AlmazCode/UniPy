from objects.object import Object
from objects.text import Text
import settings as st
import re

def loadObjs(pe, path, IDX = -1):
    # load objects
    file = open(path, "r").read()
    get = file.split("!next!")
    regex = re.compile(r',\s*\n')
    
    if file != "":
        
        if IDX != -1: get = get[IDX: IDX+1]
        idx = 0
        for i in get:
            get2 = regex.split(i)
            if IDX == -1: pe.objClass.append(get2[1].strip())
            
            if get2[1].strip() == "Object":
                
                try: x = int(get2[2][3:])
                except: x = 0
                try: y = int(get2[3][3:])
                except: y = 0
                try: w = int(get2[4][3:])
                except: w = 0
                try: h = int(get2[5][3:])
                except: h = 0
                try: render = eval(get2[6][8:])
                except: render = True
                try: image = get2[7][7:]
                except: image = None
                try: bd = get2[8][4:].strip()
                except: bd = "None"
                try: a = int(get2[9][3:])
                except: a = 0
                try: sw = int(get2[10][4:])
                except: sw = 0
                try: sh = int(get2[11][4:])
                except: sh = 0
                try: fx = eval(get2[12][4:])
                except: fx = False
                try: fy = eval(get2[13][4:])
                except: fy = False
                try: sx = int(get2[14][4:])
                except: sx = 0
                try: sy = int(get2[15][4:])
                except: sy = 0
                try: cx = get2[16][4:].strip()
                except: cx = "None"
                try: cy = get2[17][4:].strip()
                except: cy = "None"
                try: tsp = int(get2[18][5:])
                except: tsp = 255
                try: ufa = eval(get2[19][5:])
                except: ufa = False
                try: s = get2[20][3:].strip()
                except: s = "None"
                try: sc = eval(get2[21][4:])
                except: sc = {}
                try: scc = eval(get2[22][5:])
                except: scc = {}
                try: c = eval(get2[23][3:].strip())
                except: c = (255, 255, 255)
                try: uc = eval(get2[24][4:])
                except: uc = True
                try: l = eval(get2[25][3:])
                except: l = 0
                try: t = get2[26][3:].strip()
                except: t = "obj"
                
                if IDX == -1: pe.objName.append(get2[0].strip())
                pe.objects.append(Object(st.winApp, x, y, w, h, render, image, bd, a, sw, sh, fx ,fy, sx, sy, cx, cy, tsp, ufa, s, sc, scc, c, uc, get2[0].strip(), l, t))
            
            elif get2[1].strip() == "Text":
                
                try: x = int(get2[2][3:])
                except: x = 0
                try: y = int(get2[3][3:])
                except: y = 0
                try: text = get2[4][6:]
                except: text = "text"
                try: fs = int(get2[5][4:])
                except: fs = 32
                try: font = get2[6][6:].strip()
                except: font = "None"
                try: color = eval(get2[7][7:].strip())
                except: color = (0, 0, 0)
                try: tsp = int(get2[8][5:])
                except: tsp = 255
                try: a = int(get2[9][3:])
                except: a = 0
                try: render = eval(get2[10][8:])
                except: render = True
                try: fx = eval(get2[11][4:])
                except: fx = False
                try: fy = eval(get2[12][4:])
                except: fy = False
                try: cx = get2[13][4:].strip()
                except: cx = "None"
                try: cy = get2[14][4:].strip()
                except: cy = "None"
                try: sx = int(get2[15][4:])
                except: sx = 0
                try: sy = int(get2[16][4:])
                except: sy = 0
                try: sfs = int(get2[17][5:])
                except: 32
                try: tc = get2[18][4:].strip()
                except: tc = "left"
                try: rt = eval(get2[19][3:])
                except: rt = False
                try: s = get2[20][3:].strip()
                except: s = "None"
                try: sc = eval(get2[21][4:])
                except: sc = {}
                try: scc = eval(get2[22][5:])
                except: scc = {}
                try: uc = eval(get2[23][4:])
                except: uc = True
                try: l = eval(get2[24][3:])
                except: l = 0
                try: t = get2[25][3:].strip()
                except: t = "obj"
                try: sm = eval(get2[26][4:])
                except: sm = False
                
                if IDX == -1: pe.objName.append(get2[0].strip())
                pe.objects.append(Text(st.winApp, x, y, text, fs, font, color, tsp, a, render, fx, fy, cx, cy, sx, sy, sfs, tc, rt, s, sc, scc, uc, get2[0].strip(), l, t, sm))
            
            idx += 1

def writeObj(pe, idx, _type):
    if _type == "Object":
        return f"""{pe.objName[idx]},
{_type},
x: {pe.objects[idx].x},
y: {pe.objects[idx].y},
w: {pe.objects[idx].width},
h: {pe.objects[idx].height},
render: {pe.objects[idx].render},
image: {pe.objects[idx].imagePath},
bd: {pe.objects[idx].bodyType},
a: {pe.objects[idx].angle},
sw: {pe.objects[idx].SW},
sh: {pe.objects[idx].SH},
fx: {pe.objects[idx].flipX},
fy: {pe.objects[idx].flipY},
sx: {pe.objects[idx].sx},
sy: {pe.objects[idx].sy},
cx: {pe.objects[idx].cx},
cy: {pe.objects[idx].cy},
tsp: {pe.objects[idx].transparent},
ufa: {pe.objects[idx].useFullAlpha},
s: {pe.objects[idx].script},
sc: {pe.objects[idx].S_CONTENT},
scc: {pe.objects[idx].SC_CHANGED},
c: {pe.objects[idx].color},
uc: {pe.objects[idx].useCamera},
l: {pe.objects[idx].layer},
t: {pe.objects[idx].tag}"""

    elif _type == "Text":
        return f"""{pe.objName[idx]},
{_type},
x: {pe.objects[idx].x},
y: {pe.objects[idx].y},
text: {pe.objects[idx].text},
fs: {pe.objects[idx].fontSize},
font: {pe.objects[idx].fontPath},
color: {pe.objects[idx].color},
tsp: {pe.objects[idx].transparent},
a: {pe.objects[idx].angle},
render: {pe.objects[idx].render},
fx: {pe.objects[idx].flipX},
fy: {pe.objects[idx].flipY},
cx: {pe.objects[idx].cx},
cy: {pe.objects[idx].cy},
sx: {pe.objects[idx].sx},
sy: {pe.objects[idx].sy},
sfs: {pe.objects[idx].sfs},
tc: {pe.objects[idx].textCentering},
rt: {pe.objects[idx].richText},
s: {pe.objects[idx].script},
sc: {pe.objects[idx].S_CONTENT},
scc: {pe.objects[idx].SC_CHANGED},
uc: {pe.objects[idx].useCamera},
l: {pe.objects[idx].layer},
t: {pe.objects[idx].tag},
sm: {pe.objects[idx].smooth}"""

def saveObjs(pe, path):
    file = open(path, "w")
    file.write("")
    file.close()
    
    file = open(path, "a")
    idx = 0
    for i in pe.objClass:

        if i == "Object":
            file.write(writeObj(pe, idx, i))
            
        elif i == "Text":
            file.write(writeObj(pe, idx, i))
            
        if idx != len(pe.objClass) - 1:
            file.write("\n!next!\n")
        idx += 1

def addObj(pe, path, newClass):
    file = open(path, "w")
    file.write("")
    file.close()
    
    pe.objName.append(f"obj{len(pe.objName)+1}")
    pe.objClass.append(newClass)
    
    if newClass == "Object":
        pe.objects.append(Object(st.winApp, 0, 0, 0, 0, True, "None", "None", 0, 0, 0, False, False, 0, 0, "None", "None", 255, False, "None", {}, {}, (255, 255, 255), True, f"obj{len(pe.objName)+1}", 0, "obj"))
    elif newClass == "Text":
        pe.objects.append(Text(st.winApp, 0, 0, "text", 32, "None", (0, 0, 0), 255, 0, True, False, False, "None", "None", 0, 0, 32, "left", False, "None", {}, {}, True, f"obj{len(pe.objName)+1}", 0, "obj", False))
    
    file = open(path, "a")
    idx = 0
    
    for i in pe.objClass:
        if i == "Object":
            file.write(writeObj(pe, idx, i))
        
        elif i == "Text":
            file.write(writeObj(pe, idx, i))
        
        if idx != len(pe.objClass) - 1:
            file.write("\n!next!\n")
        idx += 1