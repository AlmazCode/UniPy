from engine.object import Object
from engine.text import Text

import pygame, importlib
import engine.engineOUAR as ouar
import engine.UniPy as pe
import engine.settings as st
import engine.pather as pt
import copy, sys, collections, os

pygame.mixer.init()

def loadResourses():
    st.modules = []
    loadModules()
    
    for i in st.files:
    	if i.split(".")[-1] in pe._imgTypes and i != st.EIK:
    		txs = pygame.image.load(f"{st.dirs[st.files.index(i)]}{pt.s}{i}").convert_alpha()
    		pe.texturesTSP[i] = pygame.image.load(f"{st.dirs[st.files.index(i)]}{pt.s}{i}").convert_alpha()
    		pe.textures[i] = pygame.image.load(f"{st.dirs[st.files.index(i)]}{pt.s}{i}").convert()
    		
    		replacement_color = (1, 1, 1)
    		for x in range(txs.get_width()):
    		    for y in range(txs.get_height()):
    		        if list(txs.get_at((x, y)))[-1] == 0:
    		            txs.set_at((x, y), replacement_color)
    		            f = True
    		
    		pe.textures[i] = pygame.Surface(txs.get_size()).convert()
    		pe.textures[i].blit(txs, (0, 0))
    		pe.textures[i].set_colorkey(replacement_color)
    	
    	elif i.split(".")[-1] in pe._audioTypes: pe.audios[i] = pygame.mixer.Sound(f"{st.dirs[st.files.index(i)]}{pt.s}{i}")

def startLogo():
    try: img = pygame.image.load(f"res{pt.s}{st.EIK}").convert()
    except:
        img = pygame.Surface((64,64))
        img.fill((0, 255, 0))
    img = pygame.transform.smoothscale(img, (int(st.AppWidth / 3) if st.AppWidth <= 720 else st.AppWidth // 6, int(st.AppWidth / 3) if st.AppWidth <= 720 else st.AppWidth // 6))
    
    font = pygame.font.SysFont("roboto", st.AppHeight // 40 if st.AppHeight > 720 else st.AppHeight // 20)
    tx = font.render("Created in UniPy", 1, (255, 255, 255))
    
    st.winApp.blit(img, (st.AppWidth // 2 - img.get_width() // 2, st.AppHeight // 2 - img.get_height() // 2))
    st.winApp.blit(tx, (st.AppWidth // 2 - tx.get_width() // 2, st.AppHeight // 2 - img.get_height() // 2 + img.get_height() + 30))
    pygame.display.flip()

def loadAllFilesFromDir(directory):
    _all = []
    DIRS = []
    for root, dirs, files in os.walk(directory):
        for i in files:
            DIRS.append(root)
            _all.append(i)
    return _all, DIRS

def loadModules():
    
    for script in st.modules:	
        try: sys.modules.pop(script.__name__)
        except: pass
    st.modules = []
    
    st.files, st.dirs = loadAllFilesFromDir(f"res{pt.s}")
    for file in st.files:
        if file[-3:] == ".py":
            try:
                mds = st.dirs[st.files.index(file)].split(pt.s)
                for i in mds:
                    if i.strip() == "": mds.remove(i)
                syb = "." if len(mds) > 1 else ""
                st.modules.append(__import__(f"{st.dirs[st.files.index(file)].replace(pt.s, '.')}{syb}{file[:-3]}", fromlist=["*"]))
            except Exception as e: ...
            
            
def loadObjectScriptLinks(one = False):
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
                    else: ...
                except Exception as e:
                    continue
            
            for idx, ojj in enumerate(scripts):
                if ojj in mn and ojj in obj.S_CONTENT:
                    try: _v = [var for var in dir(obj.S_LINKS[idx]) if not callable(getattr(obj.S_LINKS[idx], var)) and not var.startswith("__")]
                    except: continue
                    if "this" in _v: _v.remove("this")
                    for jjj in _v:
                        if jjj in obj.S_CONTENT[ojj] and obj.SC_CHANGED[ojj][jjj]:
                            vv = obj.S_CONTENT[ojj][jjj][0]
                            vvt = obj.S_CONTENT[ojj][jjj][1]
                            exec(f"obj.S_LINKS[{idx}].{jjj} = vv")
                
# start app
def startApp():
    
    pe.objects = []
    pe.objClass = []
    pe.objName = []
    pe.objLayers = {}
    ouar.loadObjs(pe, f"res{pt.s}ObjectInfo.txt")
    pe.OON = pe.objName.copy()
    pe.OWS = []
    pe.Camera.target = None
    pe.Camera.x, pe.Camera.y = 0, 0
    pe.GRAVITY = pe.STARTGRAVITY
    
    MHFS = []
    st.MHFU = []
    st.GBGC = st.GBGSC
    
    loadModules()
    loadObjectScriptLinks()
    
    for i in st.modules:
        if hasattr(i, "Start"): MHFS.append(i)
        if hasattr(i, "Update"): st.MHFU.append(i)
    
    for i in pe.OWS:
        if hasattr(i, "Start"): MHFS.append(i)
        if hasattr(i, "Update"): st.MHFU.append(i)
    
    for obj in pe.objects: obj.setPos()
    for obj in pe.objects: obj.setPosObject()
    
    for script in MHFS:
        try: script.Start()
        except Exception as e: ...

def drawApp():
    
    st.winApp.fill(st.GBGC)
        
    for script in st.MHFU:
    	try: script.Update()
    	except Exception as e: ...

    pe.Camera.update()
    
    objLayers = {}
    for obj in pe.objects[::-1]:
        if obj.layer not in objLayers: objLayers[obj.layer] = []
        objLayers[obj.layer].append(obj)
    objLayers = collections.OrderedDict(sorted(objLayers.items()))
    
    for layer in objLayers:
        for obj in objLayers[layer]: obj.update()