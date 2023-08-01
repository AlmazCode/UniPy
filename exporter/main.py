import pygame

import engine.settings as st
import engine.engine as eui
eui.startLogo()
import engine.UniPy as pe
import engine.pather as pt

eui.loadResourses()
eui.startApp()

# engine loop
while 1:
    
    st.clock.tick(st.fps)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
        elif event.type == pygame.VIDEORESIZE:
            if pt._platform == "Android":
                st.winApp = pygame.display.set_mode(event.size, pygame.RESIZABLE, vsync = 1)
            st.AppWidth, st.AppHeight = event.size
            st.WR = pygame.Rect(0, 0, st.AppWidth, st.AppHeight)
            pe.Camera.camera = pygame.Rect(0, 0, st.AppWidth, st.AppHeight)
            pe.Camera.width = st.AppWidth
            pe.Camera.height = st.AppHeight
            pe.wWidth, pe.wHeight = st.AppWidth, st.AppHeight
            
            for obj in pe.objects:
                obj.win = st.winApp
                obj.adapt()
            for obj in pe.objects: obj.setPos()
            for obj in pe.objects: obj.setPosObject()
            
            for script in st.modules:
                try:
                    if hasattr(script, "onWindowResized"): script.onWindowResized(event.size)
                except Exception as e: ...
            
            for script in pe.OWS:
                try:
                    if hasattr(script, "onWindowResized"): script.onWindowResized(event.size)
                except Exception as e: ...
        
        elif event.type == pygame.KEYDOWN:
            for script in st.modules:
                try:
                    if hasattr(script, "onKeyDown"): script.onKeyDown(event.unicode)
                except Exception as e: ...
            
            for script in pe.OWS:
                try:
                    if hasattr(script, "onKeyDown"): script.onKeyDown(event.unicode)
                except Exception as e: ...
        
        elif event.type == pygame.KEYUP:
            for script in st.modules:
                try:
                    if hasattr(script, "onKeyUp"): script.onKeyUp(event.unicode)
                except Exception as e: ...
            
            for script in pe.OWS:
                try:
                    if hasattr(script, "onKeyUp"): script.onKeyUp(event.unicode)
                except Exception as e: ...
        
        elif event.type == pygame.TEXTINPUT:
            for script in st.modules:
                try:
                    if hasattr(script, "onKeyPressed"): script.onKeyPressed(event.text)
                except Exception as e: ...
            
            for script in pe.OWS:
                try:
                    if hasattr(script, "onKeyPressed"): script.onKeyPressed(event.text)
                except Exception as e: ...
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            st.MBP = pygame.mouse.get_pressed()[0]
            if pt._platform != "Android":
                pe.fingersPos[0] = event.pos
                for i in pe.objects[::-1]:
                    try:
                        if hasattr(i, "onPressed") and i.finger_id == -1: i.HasPressed(event.pos, 0)
                    except Exception as e: ...
                
                for script in st.modules:
                    try:
                        if hasattr(script, "onFingerDown"): script.onFingerDown(0, event.pos)
                    except Exception as e: ...
                
                for script in pe.OWS:
                    try:
                        if hasattr(script, "onFingerDown"): script.onFingerDown(0, event.pos)
                    except Exception as e: ...
        
        elif event.type == pygame.MOUSEBUTTONUP:
            st.MBP = pygame.mouse.get_pressed()[0]
            if pt._platform != "Android":
                pe.fingersPos[0] = (-99, -99)
                for i in pe.objects[::-1]:
                    try:
                        if hasattr(i, "onUnPressed"): i.HasUnPressed(0)
                    except Exception as e: ...
                
                for script in st.modules:
                	try:
                		if hasattr(script, "onFingerUp"): script.onFingerUp(0, event.pos)
                	except Exception as e: ...
                
                for script in pe.OWS:
                	try:
                		if hasattr(script, "onFingerUp"): script.onFingerUp(0, event.pos)
                	except Exception as e: ...
        
        elif event.type == pygame.MOUSEMOTION:
            if pt._platform != "Android" and st.MBP:
                pe.fingersPos[0] = event.pos
                for script in st.modules:
                    try:
                        if hasattr(script, "onFingerMotion"): script.onFingerMotion(0, event.pos)
                    except Exception as e: ...
                
                for script in pe.OWS:
                    try:
                        if hasattr(script, "onFingerMotion"): script.onFingerMotion(0, event.pos)
                    except Exception as e: ...
        
        elif event.type == pygame.FINGERDOWN:
        	pe.fingersPos[event.finger_id] = [int(event.x*st.AppWidth), int(event.y*st.AppHeight)]

        	for i in pe.objects[::-1]:
        		try:
        			if hasattr(i, "onPressed")  and i.finger_id == -1: i.HasPressed(pe.fingersPos[event.finger_id], event.finger_id)
        		except Exception as e: ...
        		
        	for script in st.modules:
	        	try:
	        		if hasattr(script, "onFingerDown"): script.onFingerDown(event.finger_id, pe.fingersPos[event.finger_id])
	        	except Exception as e: ...
	        for script in pe.OWS:
	        	try:
	        	    if hasattr(script, "onFingerDown"): script.onFingerDown(event.finger_id, pe.fingersPos[event.finger_id])
	        	except Exception as e: ...
        	
        elif event.type == pygame.FINGERUP:
            pe.fingersPos[event.finger_id] = [-99, -99]
            for i in pe.objects[::-1]:
                try:
                    if hasattr(i, "onUnPressed"): i.HasUnPressed(event.finger_id)
                except Exception as e: ...
               
            for script in st.modules:
            	try:
                	if hasattr(script, "onFingerUp"): script.onFingerUp(event.finger_id, pe.fingersPos[event.finger_id])
            	except Exception as e: ...
                
            for script in pe.OWS:
            	try:
                	if hasattr(script, "onFingerUp"): script.onFingerUp(event.finger_id, pe.fingersPos[event.finger_id])
            	except Exception as e: ...
            
        elif event.type == pygame.FINGERMOTION:
            pe.fingersPos[event.finger_id] = [int(event.x*st.AppWidth), int(event.y*st.AppHeight)]
            
            for script in st.modules:
             	try:
             	    if hasattr(script, "onFingerMotion"): script.onFingerMotion(event.finger_id, pe.fingersPos[event.finger_id])
             	except Exception as e: ...
             
            for script in pe.OWS:
             	try:
             	    if hasattr(script, "onFingerMotion"): script.onFingerMotion(event.finger_id, pe.fingersPos[event.finger_id])
             	except Exception as e: ...
	            	
    
    eui.drawApp()
    try: pygame.display.flip()
    except: ...