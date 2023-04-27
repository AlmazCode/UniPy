import pygame
import settings as st
import engineUI as eui
import UniPy as pe
import traceback

from UI import (
	input,
	toggleButton
)

from engineUI import (
	drawUI,
	drawApp,
	drawCR,
	drawProjects,
	drawPAC
)

# for scrolling widget
scrollPos1 = (0, 0)

#scrolling the widget along the y axis
def checkScrollY(widget, IF):
	 if eval(IF) and widget.surface.get_rect(bottomleft=(widget.x, widget.y + widget.surface.get_height())).collidepoint(scrollPos1):
	       mBT = pygame.mouse.get_pressed()
	       if mBT[0]:
	           scrollPos2 = pygame.mouse.get_pos()
	           widget.oY += (scrollPos2[1] - scrollPos1[1]) // st.scrollForceShowdown
	           if widget.oY > 0: widget.oY = 0
	           if abs(widget.oY) > widget.lastY:
	           	widget.oY = -widget.lastY

# scrolling the widget along the xy axis
def checkScrollXY(widget, IF):
	 if eval(IF):
	       mBT = pygame.mouse.get_pressed()
	       if mBT[0]:
	           scrollPos2 = pygame.mouse.get_pos()
	           widget.tX += (scrollPos2[0] - scrollPos1[0]) // st.scrollForceShowdown
	           widget.tY += (scrollPos2[1] - scrollPos1[1]) // st.scrollForceShowdown
	           if widget.tX > 0: widget.tX = 0
	           if widget.tY > 0: widget.tY = 0

# engine loop
while 1:
    
    st.dt = st.clock.tick(st.fps)
    st.win.fill(st.uiBgColor)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            
        elif event.type == pygame.FINGERDOWN:
        	pe.fingersPos[event.finger_id] = [int(event.x*st.width), int(event.y*st.height)]
        	
        	if st.layer == 1:
        		for i in pe.objects:
        			try:
        				if hasattr(i, "onPressed") and i.onPressed != None and i.finger_id == -1: i.HasPressed(pe.fingersPos[event.finger_id], event.finger_id)
        			except Exception as e:
        				eui.error = True
        				tb = e.__traceback__
        				filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
        				eui._console.Log(f"UniPy Error: in script \"{filename.split('/')[-1]}\": in line [{line_num}]\n{e}", "error" if type(i.onPressed == type(lambda: None)) else "warning")
        		
        		for script in st.modules:
	        		try:
	        			if hasattr(script, "onFingerDown"): script.onFingerDown(event.finger_id, [int(event.x*st.width), int(event.y*st.height)])
	        		except Exception as e:
	        			eui.error = True
	        			tb = e.__traceback__
	        			filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
	        			eui._console.Log(f"UniPy Error: in script \"{filename.split('/')[-1]}\": in line [{line_num}]\n{e}", "error")
        	
        elif event.type == pygame.FINGERUP:
            pe.fingersPos[event.finger_id] = [-99, -99]
            
            if st.layer == 1:
                for i in pe.objects:
                    try:
                        if hasattr(i, "onUnPressed") and i.onUnPressed != None: i.HasUnPressed(event.finger_id)
                    except Exception as e:
                    	eui.error = True
                    	tb = e.__traceback__
                    	filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                    	eui._console.Log(f"UniPy Error: in script \"{filename.split('/')[-1]}\": in line [{line_num}]\n{e}", "error" if type(i.onUnPressed == type(lambda: None)) else "warning")
                
                for script in st.modules:
                	try:
                		if hasattr(script, "onFingerUp"): script.onFingerUp(event.finger_id, [int(event.x*st.width), int(event.y*st.height)])
                	except Exception as e:
                		eui.error = True
                		tb = e.__traceback__
                		filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
                		eui._console.Log(f"UniPy Error: in script \"{filename.split('/')[-1]}\": in line [{line_num}]\n{e}", "error")
            
        elif event.type == pygame.FINGERMOTION:
            pe.fingersPos[event.finger_id] = [int(event.x*st.width), int(event.y*st.height)]
            
            if st.layer == 1:
	            for script in st.modules:
	            	try:
	            		if hasattr(script, "onFingerMotion"): script.onFingerMotion(event.finger_id, [int(event.x*st.width), int(event.y*st.height)])
	            	except Exception as e:
	            		eui.error = True
	            		tb = e.__traceback__
	            		filename, line_num, _, _ = traceback.extract_tb(tb)[-1]
	            		eui._console.Log(f"UniPy Error: in script \"{filename.split('/')[-1]}\": in line [{line_num}]\n{e}", "error")
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mBT = pygame.mouse.get_pressed()
            
            if st.layer == 3 and st.isRenameFile or st.layer == -1 and st.isRenameProject:
                st.lastPressedInput.hasUnPress(event.pos)
                    	
            scrollPos1 = event.pos
            
            if st.layer == 3 and st.isRenameFile or st.layer == -1 and st.isRenameProject:
                st.lastPressedInput.hasPress(event.pos)
            
            if st.layer == 0 and mBT[0] and st.lastSelectionObject != None and st.isSelector:
            	eui.ObjSW.Press(event.pos)
            	if eui.ObjSW.surface.get_rect(bottomleft=(eui.ObjSW.x, eui.ObjSW.y + eui.ObjSW.surface.get_height())).collidepoint(event.pos):
            		continue
            
            # проверка на нажатия инпутов в инспекторе объекта
            if st.layer == 0 and mBT[0] and st.lastSelectionObject != None:
                for i in eui.objComponents:
                	if type(i) == input.Input and i.hasPress(event.pos):
                		if st.lastPressedInput != None: st.lastPressedInput.hasUnPress(event.pos, False)
                		st.lastPressedInput = i
                		i.hasPress(event.pos)
                		break
                if st.lastPressedInput != None and st.lastPressedInput.hasUnPress(event.pos): st.lastPressedInput = None
            
                # проверка на нажатия кнопок переключения
                for i in toggleButton.toggleButtons:
                    if i.rect.collidepoint(event.pos):
                        i.active = not i.active
                        if i.func != None: i.func(i.key)
            
            if st.layer == 2 and mBT[0]:
                eui.fileConductor.Press()
            if st.layer == 3 and mBT[0]:
                eui.PAC.Press()
            if st.layer == 0 and mBT[0] and st.lastSelectionObject == None and not st.isCreateObject:
                eui.SOHM.Press(event.pos)
            if st.layer == -1 and mBT[0] and not st.isRenameProject:
                eui.PM.Press()
            if st.layer == 0 and mBT[0] and st.isCreateObject:
                eui.SNOP.Press(event.pos)
        
        elif event.type == pygame.TEXTINPUT:
                        if st.lastSelectionObject != None and st.lastPressedInput != None or st.layer == 3 or st.layer == -1: st.lastPressedInput.Press(event.text)
                            
        elif event.type == pygame.KEYUP:
        	key = ""
        	if event.key == pygame.K_BACKSPACE: key = "BS"
        	elif event.key == pygame.K_RETURN: key = "ETR"
        	
        	if st.lastSelectionObject != None and st.lastPressedInput != None or st.layer == 3 or st.layer == -1: st.lastPressedInput.Press(key)
    
    # скроллинг объектов в инспекторе объекта                    
    if st.lastSelectionObject != None and st.layer == 0:
        mBT = pygame.mouse.get_pressed()
        if mBT[0]:
            # objects pos in inspector 2
            scrollPos2 = pygame.mouse.get_pos()
            eui.OPII += (scrollPos2[1] - scrollPos1[1]) // st.scrollForceShowdown
            for i in eui.objComponents:
                i.rect.y += (scrollPos2[1] - scrollPos1[1]) // st.scrollForceShowdown
            if st.isSelector:
            	eui.ObjSW.y += (scrollPos2[1] - scrollPos1[1]) // st.scrollForceShowdown
            if eui.OPII > 0:
                eui.OPII = 0
                for i in eui.objComponents:
                    i.rect.y = i.startY
                if st.isSelector:
                	eui.ObjSW.y = st.LPBFS.rect.y - eui.ObjSW.surface.get_height() - 10
            if abs(eui.OPII) > eui.objComponents[-1].startY:
                eui.OPII = -eui.objComponents[-1].startY
                for i in eui.objComponents:
                    i.rect.y = i.startY + eui.OPII
                if st.isSelector:
               	 eui.ObjSW.y = st.LPBFS.rect.y - eui.ObjSW.surface.get_height() - 10
                    
    # скроллинг проводника
    checkScrollY(eui.fileConductor, "st.layer == 2")
    # скроллинг проводника ассетов проекта
    checkScrollY(eui.PAC, "st.layer == 3 and not st.isRenameFile")
    checkScrollXY(eui.PAC, "st.layer == 3 and eui.PAC.viewText")
    # скроллинг проектов
    checkScrollY(eui.PM, "st.layer == -1 and not st.isRenameProject")
    # скроллинг объектов в иерархии
    checkScrollY(eui.SOHM, "st.layer == 0 and st.lastSelectionObject == None and len(eui.SOHM.elemName) > 0 and not st.isCreateObject")
    
    checkScrollXY(eui._console, "st.layer == 1 and st.isConsole")
        
    # draw projects
    if st.layer == -1: drawProjects()
    
    # draw editor UI
    elif st.layer == 0: drawUI()
    
    # draw app
    elif st.layer == 1: drawApp()
    
    # draw conductor
    elif st.layer == 2: drawCR()
    
    # draw project assets conductor
    elif st.layer == 3: drawPAC()
    
    # update display
    pygame.display.update()