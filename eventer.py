import UniPy as pe
import engineUI as eui
import settings as st
import pather as pt
import traceback
import pygame

def check_event(event):
    if event.type == pygame.QUIT:
            exit()
    elif event.type == pygame.ACTIVEEVENT:
        if event.gain != 0:
            if st.projectIdx != -1:
                st.files, st.dirs = eui.loadAllFilesFromDir(f"{eui.PATH}{pt.s}{st.projects[st.projectIdx]}")
                for i in st.files:
                    if i.split(".")[-1] in pe._imgTypes and i not in pe.textures:
                        pe.textures[i], pe.texturesTSP[i] = eui.loadImage(f"{st.dirs[st.files.index(i)]}{pt.s}{i}")
                    	
                    elif i.split(".")[-1] in pe._audioTypes and i not in pe.audios:
                        pe.audios[i] = pygame.mixer.Sound(f"{st.dirs[st.files.index(i)]}{pt.s}{i}")
                if st.drawingLayer == 3 and not eui.PAC.viewText:
                    eui.PAC.reOpenPath()
                elif st.drawingLayer == 2 and st.lastSelectionObject is not None:
                    eui.fileConductor.reOpenPath()
                    	
    elif event.type == pygame.VIDEORESIZE:
        if pt._platform == "Android":
            st.win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE, vsync = 1)
        st.width, st.height = event.size
        st.AppWidth, st.AppHeight = st.width, st.height - (80 if pt._platform == "Android" else 40)
        st.winApp = pygame.Surface((st.AppWidth, st.AppHeight))
        st.WR = pygame.Rect(0, 0, st.AppWidth, st.AppHeight)
        pe.Camera.camera = pygame.Rect(0, 0, st.AppWidth, st.AppHeight)
        pe.Camera.width = st.AppWidth
        pe.Camera.height = st.AppHeight
        pe.wWidth, pe.wHeight = st.AppWidth, st.AppHeight

        if pt._platform == "Android":
            st.uiTFontSize = st.height // 20  if st.height > st.width else st.height // 10
            st.uiTSFontSize = st.height // 32 if st.height > st.width else st.height // 18
            st.uiIW = st.width // 2 if st.height > st.width else st.width // 4
            st.uiIH = st.uiIW // 4
            st.uiBS = st.width // 8 if st.height > st.width else st.width // 18
        else:
            st.uiTFontSize = st.height // 32  if st.height > st.width else st.height // 18
            st.uiTSFontSize = st.height // 50 if st.height > st.width else st.height // 25
            st.uiIW = st.width // 2 if st.height > st.width else st.width // 4
            st.uiIH = st.uiIW // 6
            st.uiISIOI /= 2
            st.uiBS = st.width // 10 if st.height > st.width else st.width // 20
        
        st.uiTFont = pygame.font.Font(st.uiFont, st.uiTFontSize)
        st.uiTSFont = pygame.font.Font(st.uiFont, st.uiTSFontSize)

        for bt in eui.button.BUTTONS:
            bt.width = st.uiBS
            bt.height = st.uiBS
            bt.adjust_dimensions_and_positions()
        for input in eui.input.INPUTS:
            input.width = st.uiIW
            input.height = st.uiIH
            input.adjust_dimensions_and_positions()
        for tBt in eui.toggleButton.toggle_buttons:
            tBt.width = st.uiBS
            tBt.height = st.uiBS
            tBt.adjust_dimensions_and_positions()
        eui.btExportProject.width *= 2
        eui.btExportProject.adjust_dimensions_and_positions()
        eui.AEPME()
        if st.lastSelectionObject:
            eui.setObjProperty(st.lastSelectionObject, False)
        eui.btSCC.width = (st.height - st.AppHeight - 10) * 2
        eui.btSCC.height = st.height - st.AppHeight - 10
        eui.btSCC.adjust_dimensions_and_positions()
        if st.drawingLayer == 1:
            eui.btStartApp.height = st.height - st.AppHeight - 10
            eui.btStartApp.width = eui.btStartApp.height * 2
            eui.btStartApp.adjust_dimensions_and_positions()
            for obj in pe.objects:
                obj.win = st.winApp
                obj.adapt()
            for obj in pe.objects: obj.setPos()
            for obj in pe.objects: obj.setPosObject()
        eui.uiEngineImages["ENGINE_ICON"] = pygame.transform.smoothscale(eui.uiEngineImages["engineIcon"], (int(st.width / 7.5) if st.width < st.height else st.width // 15, int(st.width / 7.5) if st.width < st.height else st.width // 15))
        eui.PAC.surface = pygame.Surface((st.width, st.height))
        eui.PAC.ADP()
        eui.PAC.setPath(eui.PAC.thisPath)
        eui.PAC.y = 20 + st.uiBS
        eui.fileConductor.surface = pygame.Surface((st.width, st.height))
        eui.fileConductor.ADP()
        eui.fileConductor.setPath(eui.fileConductor.thisPath)
        eui.fileConductor.y = 20 + st.uiBS
        eui.SOHM.surface = pygame.Surface((st.width // 1.3, st.height - 20))
        eui.SOHM.elem_height_div = 15 if st.width < st.height else 10
        eui.SOHM.normalize()
        eui.SNOP.surface = pygame.Surface((st.width // 1.5 if st.width < st.height else st.width // 3, st.height // 2))
        eui.SNOP.normalize()
        eui.SNOP.y = eui.btShowPanel.rect.y - eui.SNOP.surface.get_height() - 10
        eui.SNOP.x = eui.btShowPanel.rect.right - eui.SNOP.surface.get_width()
        eui.PM.surface = pygame.Surface((eui.PM.win.get_width()//1.5, eui.PM.win.get_height()))
        eui.PM.elem_height_div = 10 if st.width < st.height else 8
        eui.PM.normalize()
        eui.PM.x = st.width // 2 - (st.width // 1.5) // 2
        eui.PM.y = 10 + eui.uiEngineImages["ENGINE_ICON"].get_height() + 50
        eui.IFRPIPM.width = eui.PM.elem_width
        eui.IFRPIPM.height = eui.PM.elem_height
        eui.IFFIPAC.width = eui.PAC.elem_width
        eui.IFFIPAC.height = eui.PAC.elem_height
        eui.IFFIPAC.adjust_dimensions_and_positions()
        eui.IFRPIPM.adjust_dimensions_and_positions()
        eui.IFFIPAC.rect.x = eui.PAC.x + 10
        eui.IFRPIPM.rect.x = eui.PM.x
        if st.isRenameFile:
            eui.IFFIPAC.rect.y = eui.PAC.get_idx_pos(eui.PAC.elem_idx)
        if st.isRenameProject:
            eui.IFRPIPM.rect.y = eui.PM.get_idx_pos(eui.PM.elem_idx)
        eui.ObjSW.surface = pygame.Surface((st.width // 2 if st.width < st.height else st.width // 3, st.height // 4 if st.width < st.height else st.height // 2))
        if st.LPBFS is not None:
            eui.ObjSW.x = st.LPBFS.rect.x
            eui.ObjSW.y = st.LPBFS.rect.y - eui.ObjSW.surface.get_height() - 10
        eui.ObjSW.normalize()
        eui._console.surface = pygame.Surface((st.AppWidth, st.AppHeight // 2))
        eui._console.y = st.AppHeight - st.AppHeight // 2
        eui._console.ADP()
        h = st.height // 4 if st.height > st.width else st.height // 2
        w = st.width // 1.2 if st.height > st.width else st.width // 2.4
        eui.PB.surface = pygame.Surface((w, h))
        eui.PB.x = st.width // 2 - w // 2
        eui.PB.y = st.height // 2 - h // 2
        eui.PB.ADP()
        oy = 0
        for msg in eui.message.messages:
            msg.oY = oy
            msg.width = msg.surface.get_width() // 2
            msg.height = msg.surface.get_height() // 24 if msg.surface.get_width() < msg.surface.get_height() else msg.surface.get_height() // 12
            msg.ADP()
            msg.x = msg.surface.get_width() // 2 - msg.width // 2 + msg.oX
            msg.y = msg.surface.get_height() - msg.height - 10 + msg.oY
            oy -= msg.height - 10
            
        for script in st.modules:
            try:
                if hasattr(script, "onWindowResized"): script.onWindowResized(event.size)
            except Exception as e:
                eui.error = True
                tb = e.__traceback__
                filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
            
        for script in pe.OWS:
            try:
                if hasattr(script, "onWindowResized"): script.onWindowResized(event.size)
            except Exception as e:
                eui.error = True
                tb = e.__traceback__
                filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
        
    elif event.type == pygame.FINGERDOWN:
        pe.fingersPos[event.finger_id] = [int(event.x*st.width), int(event.y*st.height)]
        	
        if st.drawingLayer == 1:
            for i in pe.objects[::-1]:
                try:
                    if hasattr(i, "onPressed") and i.finger_id == -1:
                        i.HasPressed(pe.fingersPos[event.finger_id], event.finger_id)
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error" if type(i.onPressed) == type(lambda: None) else "warning")
        		
            for script in st.modules:
                try:
                    if hasattr(script, "onFingerDown"):
                        script.onFingerDown(event.finger_id, pe.fingersPos[event.finger_id])
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
	        	
            for script in pe.OWS:
                try:
                    if hasattr(script, "onFingerDown"):
                        script.onFingerDown(event.finger_id, pe.fingersPos[event.finger_id])
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
        	
    elif event.type == pygame.FINGERUP:
        pe.fingersPos[event.finger_id] = None
            
        if st.drawingLayer == 1:
            for i in pe.objects[::-1]:
                try:
                    if hasattr(i, "onUnPressed"):
                        i.HasUnPressed(event.finger_id)
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
                
            for script in st.modules:
                try:
                    if hasattr(script, "onFingerUp"):
                        script.onFingerUp(event.finger_id, pe.fingersPos[event.finger_id])
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
                
            for script in pe.OWS:
                try:
                    if hasattr(script, "onFingerUp"):
                        script.onFingerUp(event.finger_id, pe.fingersPos[event.finger_id])
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
            
    elif event.type == pygame.FINGERMOTION:
        pe.fingersPos[event.finger_id] = [int(event.x*st.width), int(event.y*st.height)]
            
        if st.drawingLayer == 1:
            for script in st.modules:
                try:
                    if hasattr(script, "onFingerMotion"):
                        script.onFingerMotion(event.finger_id, pe.fingersPos[event.finger_id])
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
	        
            for script in pe.OWS:
                try:
                    if hasattr(script, "onFingerMotion"):
                        script.onFingerMotion(event.finger_id, pe.fingersPos[event.finger_id])
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
                    
    elif event.type == pygame.MOUSEMOTION:
        if pt._platform != "Android" and st.drawingLayer == 1 and st.MBP:
            pe.fingersPos[0] = event.pos
            for script in st.modules:
                try:
                    if hasattr(script, "onFingerMotion"): script.onFingerMotion(0, event.pos)
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
            for script in pe.OWS:
                try:
                    if hasattr(script, "onFingerMotion"): script.onFingerMotion(0, event.pos)
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
        
    elif event.type == pygame.MOUSEBUTTONUP:
        st.MBP = pygame.mouse.get_pressed()[0]
        if pt._platform != "Android" and st.drawingLayer == 1:
            pe.fingersPos[0] = None
            for i in pe.objects[::-1]:
                try:
                    if hasattr(i, "onUnPressed"):
                        i.HasUnPressed(0)
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
                
            for script in st.modules:
                try:
                	if hasattr(script, "onFingerUp"):
                            script.onFingerUp(0, event.pos)
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
                
            for script in pe.OWS:
                try:
                	if hasattr(script, "onFingerUp"):
                            script.onFingerUp(0, event.pos)
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
        
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if pt._platform != "Android" and st.drawingLayer == 1:
            pe.fingersPos[0] = event.pos
            for i in pe.objects[::-1]:
                try:
                    if hasattr(i, "onPressed") and i.finger_id == -1: i.HasPressed(event.pos, 0)
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
                
            for script in st.modules:
                try:
                    if hasattr(script, "onFingerDown"): script.onFingerDown(0, event.pos)
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
                
            for script in pe.OWS:
                try:
                    if hasattr(script, "onFingerDown"): script.onFingerDown(0, event.pos)
                except Exception as e:
                    eui.error = True
                    tb = e.__traceback__
                    filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
            
        st.MBP = pygame.mouse.get_pressed()[0]
        st.scrollPos = event.pos
        eui.PAC.lastMousePos = event.pos
        eui.fileConductor.lastMousePos = event.pos
        eui._console.lastMousePos = event.pos
        eui.PM.lastMousePos = event.pos
        eui.SOHM.lastMousePos = event.pos
        eui.SNOP.lastMousePos = event.pos
            
        if st.drawingLayer == 3 and st.isRenameFile or st.drawingLayer == -1 and st.isRenameProject:
            if st.lastPressedInput.has_unpress(event.pos):
                st.lastPressedInput = None
                st.isRenameProject = False
                st.isRenameFile = False
            
        if st.drawingLayer == 3 and st.isRenameFile or st.drawingLayer == -1 and st.isRenameProject:
            st.lastPressedInput.has_press(event.pos)
            
        if st.drawingLayer == 0 and st.MBP and st.lastSelectionObject != None and st.isSelector:
            eui.ObjSW.press(event.pos)
            if eui.ObjSW.surface.get_rect(bottomleft=(eui.ObjSW.x, eui.ObjSW.y + eui.ObjSW.surface.get_height())).collidepoint(event.pos):
                return
            
        if st.drawingLayer == 0 and st.MBP and st.lastSelectionObject != None:
            for i in eui.objComponents:
                if type(i) == eui.input.Input and i.has_press(event.pos):
                    if st.lastPressedInput != None:
                        st.lastPressedInput.has_unpress(event.pos, False)
                    st.lastPressedInput = i
                    i.has_press(event.pos)
                    break
            
            for i in eui.objComponents:
                if i.rect.collidepoint(event.pos) and type(i).__name__ == "ToggleButton":
                    i.press()
            
        if st.lastPressedInput != None and st.lastPressedInput.has_unpress(event.pos):
            st.lastPressedInput = None
            
        if st.drawingLayer == 2 and (st.MBP or event.button in [4, 5]):
            eui.fileConductor.Press(st.MP)
            eui.fileConductor.drag(event.button, st.MP)
        elif st.drawingLayer == 3 and (st.MBP or event.button in [4, 5]) and not st.isRenameFile:
            eui.PAC.Press(st.MP)
            eui.PAC.drag(event.button, st.MP)
        if st.drawingLayer == 0 and (st.MBP or event.button in [4, 5]) and st.lastSelectionObject == None and not st.isCreateObject:
            eui.SOHM.press(event.pos)
            eui.SOHM.drag(event.button, st.MP)
        if st.drawingLayer == -1 and (st.MBP or event.button in [4, 5]) and not st.isRenameProject:
            eui.PM.press(event.pos)
            eui.PM.drag(event.button, st.MP)
        if st.drawingLayer == 0 and (st.MBP or event.button in [4, 5]) and st.isCreateObject:
            eui.SNOP.press(event.pos)
            eui.SNOP.drag(event.button, st.MP)
            
        if st.isConsole and event.button in [4, 5]:
            eui._console.drag(event.button, st.MP)
            
        if st.lastSelectionObject is not None and st.drawingLayer == 0 and event.button in [4, 5]:
            if event.button == 4:
                eui.OPII += st.mouseScrollSpeed
                for i in eui.objComponents:
                    i.rect.y += st.mouseScrollSpeed
                if st.isSelector:
                    eui.ObjSW.y += st.mouseScrollSpeed
            else:
                eui.OPII -= st.mouseScrollSpeed
                for i in eui.objComponents:
                    i.rect.y -= st.mouseScrollSpeed
                if st.isSelector:
                    eui.ObjSW.y -= st.mouseScrollSpeed
        
        if st.drawingLayer == 4:
            if eui.InputSetExportProjectVersion.has_press(event.pos):
                st.lastPressedInput = eui.InputSetExportProjectVersion
        
    elif event.type == pygame.TEXTINPUT:
        if st.lastPressedInput != None: st.lastPressedInput.press(event.text)
            
        for script in st.modules:
            try:
                if hasattr(script, "onKeyPressed"): script.onKeyPressed(event.text)
            except Exception as e:
                eui.error = True
                tb = e.__traceback__
                filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
            
        for script in pe.OWS:
            try:
                if hasattr(script, "onKeyPressed"): script.onKeyPressed(event.text)
            except Exception as e:
                eui.error = True
                tb = e.__traceback__
                filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
                            
    elif event.type == pygame.KEYDOWN:
        for script in st.modules:
            try:
                if hasattr(script, "onKeyDown"): script.onKeyDown(event.key)
            except Exception as e:
                eui.error = True
                tb = e.__traceback__
                filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
            
        for script in pe.OWS:
            try:
                if hasattr(script, "onKeyDown"): script.onKeyDown(event.key)
            except Exception as e:
                eui.error = True
                tb = e.__traceback__
                filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
                    
    elif event.type == pygame.KEYUP:
        for script in st.modules:
            try:
                if hasattr(script, "onKeyUp"): script.onKeyUp(event.key)
            except Exception as e:
                eui.error = True
                tb = e.__traceback__
                filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
            
        for script in pe.OWS:
            try:
                if hasattr(script, "onKeyUp"): script.onKeyUp(event.key)
            except Exception as e:
                eui.error = True
                tb = e.__traceback__
                filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                eui._console.Log(f"UniPy Error: in script \"{filename.split(pt.s)[-1]}\": in line [{line_num}]\n{e}", "error")
        	
        key = ""
        if event.key == pygame.K_BACKSPACE: key = "BS"
        elif event.key == pygame.K_RETURN: key = "ETR"
            
        if st.lastPressedInput != None: st.lastPressedInput.press(key)