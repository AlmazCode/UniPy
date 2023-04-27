import UniPy as pe
import settings as st

# functions
def centerx():
    idx = pe.objName.index(st.lastSelectionObject)
    return st.AppWidth // 2 - pe.objects[idx].width // 2

def centery():
    idx = pe.objName.index(st.lastSelectionObject)
    return st.AppHeight // 2 - pe.objects[idx].height // 2

def top(): return 0
def left(): return 0

def bottom():
    idx = pe.objName.index(st.lastSelectionObject)
    return st.AppHeight - pe.objects[idx].height

def right():
    idx = pe.objName.index(st.lastSelectionObject)
    return st.AppWidth - pe.objects[idx].width

def ww(): return st.AppWidth
def wh(): return st.AppHeight