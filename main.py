import pygame
import eventer
import settings as st
import engineUI as eui
import UniPy as pe

draws = {
    -1: eui.drawProjects,
    0: eui.drawUI,
    1: eui.drawApp,
    2: eui.drawCR,
    3: eui.drawPAC,
    4: eui.drawExportProject
}

while 1:
    pe.deltaTime = st.clock.tick(st.fps) / 1000.0
    st.win.fill(st.uiBgColor)
    st.MP = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        eventer.check_event(event)
    
    eui.srollObjectComponents()
    draws[st.drawingLayer]()
    
    messages_to_remove = []
    for msg in eui.message.messages:
        if msg.ifDel:
            messages_to_remove.append(msg)
        else:
            msg.update()
    for msg in messages_to_remove:
        eui.message.messages.remove(msg)
        
    try: pygame.display.flip()
    except: pass