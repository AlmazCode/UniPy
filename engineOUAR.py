from object import Object
from text import Text
import settings as st

def loadObjs(pe, path, mode = "d", iddx = 0):
    # load objects
    file = open(path, "r").read()
    get = file.split("!next!")
    
    if file != "":
    
        idx = 0
        for i in get:
            get2 = i.split(",")
            
            if mode == "d": pe.objClass.append(get2[1].strip())
            
            if get2[1].strip() == "Object":
                
                try: x = int(get2[2][3:])
                except: x = 0
                try: y = int(get2[3][3:])
                except: y = 0
                try: w = int(get2[4][3:])
                except: w = 0
                try: h = int(get2[5][3:])
                except: h = 0
                try: render = int(get2[6][8:])
                except: render = 1
                try: image = get2[7][8:]
                except: image = None
                try: bd = get2[8][4:].strip()
                except: bd = "None"
                try: a = int(get2[9][3:])
                except: a = 0
                try: sw = int(get2[10][4:])
                except: sw = 0
                try: sh = int(get2[11][4:])
                except: sh = 0
                try: fx = int(get2[12][4:])
                except: fx = 0
                try: fy = int(get2[13][4:])
                except: fy = 0
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
                
                if mode == "d":
                    pe.objName.append(get2[0].strip())
                    pe.objects.append(Object(st.winApp, x, y, w, h, render, image, bd, a, sw, sh, fx ,fy, sx, sy, cx, cy, tsp))
                    
                elif mode == "r":
                    pe.objName[idx] = get2[0].strip()
                    pe.objects[idx] = Object(st.winApp, x, y, w, h, render, image, bd, a, sw, sh, fx, fy, sx, sy, cx, cy, tsp)
            
            elif get2[1].strip() == "Text":
                
                try: x = int(get2[2][3:])
                except: x = 0
                try: y = int(get2[3][3:])
                except: y = 0
                try: text = get2[4][7:]
                except: text = "text"
                try: fs = int(get2[5][4:])
                except: fs = 32
                try: font = get2[6][6:].strip()
                except: font = "None"
                try: color = get2[7][7:].strip()
                except: color = "0 0 0"
                try: tsp = int(get2[8][5:])
                except: tsp = 255
                try: a = int(get2[9][3:])
                except: a = 0
                try: render = int(get2[10][8:])
                except: render = 0
                try: fx = int(get2[11][4:])
                except: fx = 0
                try: fy = int(get2[12][4:])
                except: fy = 0
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
                
                if mode == "d":
                    pe.objName.append(get2[0].strip())
                    pe.objects.append(Text(st.winApp, x, y, text, fs, font, color, tsp, a, render, fx, fy, cx, cy, sx, sy, sfs, tc))
                    
                elif mode == "r":
                    pe.objName[idx] = get2[0].strip()
                    pe.objects[idx] = Text(st.winApp, x, y, text, fs, font, color, tsp, a, render, fx, fy, cx, cy, sx, sy, sfs, tc)
            
            idx += 1
    
def saveObjs(pe, path):
    file = open(path, "w")
    file.write("")
    file.close()
    
    file = open(path, "a")
    idx = 0
    for i in pe.objClass:
        if i == "Object":
            render = 1 if pe.objects[idx].render else 0
            fx = 1 if pe.objects[idx].flipX else 0
            fy = 1 if pe.objects[idx].flipY else 0
            file.write(f"{pe.objName[idx]},\n{i},\nx: {pe.objects[idx].x},\ny: {pe.objects[idx].y},\nw: {pe.objects[idx].width},\nh: {pe.objects[idx].height},\nrender: {render},\nimage: {pe.objects[idx].imagePath},\nbd: {pe.objects[idx].bodyType},\na: {pe.objects[idx].angle},\nsw: {pe.objects[idx].SW},\nsh: {pe.objects[idx].SH},\nfx: {fx},\nfy: {fy},\nsx: {pe.objects[idx].sx},\nsy: {pe.objects[idx].sy},\ncx: {pe.objects[idx].cx},\ncy: {pe.objects[idx].cy},\ntsp: {pe.objects[idx].transparent}")
            
        elif i == "Text":
            render = 1 if pe.objects[idx].render else 0
            fx = 1 if pe.objects[idx].flipX else 0
            fy = 1 if pe.objects[idx].flipY else 0
            color = f"{pe.objects[idx].color[0]} {pe.objects[idx].color[1]} {pe.objects[idx].color[2]}"
            
            file.write(f"{pe.objName[idx]},\n{i},\nx: {pe.objects[idx].x},\ny: {pe.objects[idx].y},\ntext: {pe.objects[idx].text},\nfs: {pe.objects[idx].fontSize},\nfont: {pe.objects[idx].fontPath},\ncolor: {color},\ntsp: {pe.objects[idx].transparent},\na: {pe.objects[idx].angle},\nrender: {render},\nfx: {fx},\nfy: {fy},\ncx: {pe.objects[idx].cx},\ncy: {pe.objects[idx].cy},\nsx: {pe.objects[idx].sx},\nsy: {pe.objects[idx].sy},\nsfs: {pe.objects[idx].sfs},\ntc: {pe.objects[idx].textCentering}")
            
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
        pe.objects.append(Object(st.winApp, 0, 0, 0, 0, 1, "None", "None", 0, 0, 0, 0, 0, 0, 0, "None", "None", 255))
    elif newClass == "Text":
        pe.objects.append(Text(st.winApp, 0, 0, "text", 32, "None", "0 0 0", 255, 0, 1, 0, 0, "None", "None", 0, 0, 32, "left"))
    
    file = open(path, "a")
    idx = 0
    
    for i in pe.objClass:
        if i == "Object":
            render = 1 if pe.objects[idx].render else 0
            fx = 1 if pe.objects[idx].flipX else 0
            fy = 1 if pe.objects[idx].flipY else 0
            file.write(f"{pe.objName[idx]},\n{i},\nx: {pe.objects[idx].x},\ny: {pe.objects[idx].y},\nw: {pe.objects[idx].width},\nh: {pe.objects[idx].height},\nrender: {render},\nimage: {pe.objects[idx].imagePath},\nbd: {pe.objects[idx].bodyType},\na: {pe.objects[idx].angle},\nsw: {pe.objects[idx].SW},\nsh: {pe.objects[idx].SH},\nfx: {fx},\nfy: {fy},\nsx: {pe.objects[idx].sx},\nsy: {pe.objects[idx].sy},\ncx: {pe.objects[idx].cx},\ncy: {pe.objects[idx].cy},\ntsp: {pe.objects[idx].transparent}")
        
        elif i == "Text":
            render = 1 if pe.objects[idx].render else 0
            fx = 1 if pe.objects[idx].flipX else 0
            fy = 1 if pe.objects[idx].flipY else 0
            color = f"{pe.objects[idx].color[0]} {pe.objects[idx].color[1]} {pe.objects[idx].color[2]}"
            
            file.write(f"{pe.objName[idx]},\n{i},\nx: {pe.objects[idx].x},\ny: {pe.objects[idx].y},\ntext: {pe.objects[idx].text},\nfs: {pe.objects[idx].fontSize},\nfont: {pe.objects[idx].fontPath},\ncolor: {color},\ntsp: {pe.objects[idx].transparent},\na: {pe.objects[idx].angle},\nrender: {render},\nfx: {fx},\nfy: {fy},\ncx: {pe.objects[idx].cx},\ncy: {pe.objects[idx].cy},\nsx: {pe.objects[idx].sx},\nsy: {pe.objects[idx].sy},\nsfs: {pe.objects[idx].sfs},\ntc: {pe.objects[idx].textCentering}")
        
        if idx != len(pe.objClass) - 1:
            file.write("\n!next!\n")
        idx += 1