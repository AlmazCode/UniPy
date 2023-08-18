import os, shutil, ast, re, pygame
import settings as st
import pather as pt
import UniPy as pe
from random import randint

FTE = ["engineOUAR.py", "pather.py", "UniPy.py", f"objects{pt.s}object.py", f"objects{pt.s}text.py", f"objects{pt.s}camera.py", f"exporter{pt.s}engine.py", f"exporter{pt.s}settings.py", f"modules{pt.s}Math.py"]

class ImportVisitor(ast.NodeTransformer):
    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == "UniPy":
                alias.name = "engine.UniPy"
        return node

    def visit_ImportFrom(self, node):
        if node.module == "UniPy":
            node.module = "engine.UniPy"
        return node

def createProject(create_path, path_to_project, project_name, program_name, program_size, program_version):
    
    lpv = None
    df = False
    
    if os.path.exists(f"{create_path}{pt.s}{project_name}"):
        try:
            with open(f"{create_path}{pt.s}{project_name}{pt.s}engine{pt.s}settings.py", "r") as f:
                inf = f.read()
                g = re.findall(r'version = "([^"]*)"', inf)
                lpv = g[0] if g else None
            if os.path.exists(f"{create_path}{pt.s}{project_name}{pt.s}res{pt.s}$data"):
                shutil.move(f"{create_path}{pt.s}{project_name}{pt.s}res{pt.s}$data", f"exporter{pt.s}")
                df = True
        except: pass
        shutil.rmtree(f"{create_path}{pt.s}{project_name}")
    
    os.makedirs(f"{create_path}{pt.s}{project_name}")
    os.makedirs(f"{create_path}{pt.s}{project_name}{pt.s}res")
    os.makedirs(f"{create_path}{pt.s}{project_name}{pt.s}engine")
    
    files = os.listdir(path_to_project)
    for file in files:
        if file not in ["__pycache__", "project_info.txt", "$data"]:
            if os.path.isdir(f"{path_to_project}{pt.s}{file}"):
                try: shutil.copytree(f"{path_to_project}{pt.s}{file}", f"{create_path}{pt.s}{project_name}{pt.s}res{pt.s}{file}")
                except: pass
            else:
                try:
                    shutil.copy(f"{path_to_project}{pt.s}{file}", f"{create_path}{pt.s}{project_name}{pt.s}res")
                except: pass
    
    try: shutil.copy(f"assets{pt.s}engineIcon.png", f"{create_path}{pt.s}{project_name}{pt.s}engine")
    except: pass
    
    for file in FTE:
        try:
            shutil.copy(file, f"{create_path}{pt.s}{project_name}{pt.s}engine")
        except: pass
    try: shutil.copy(f"exporter{pt.s}main.py", f"{create_path}{pt.s}{project_name}")
    except: pass
    
    for file in os.listdir(f"{create_path}{pt.s}{project_name}{pt.s}engine"):
        
        if file not in ["engine.py", "engineIcon.png"]:
            f = open(f"{create_path}{pt.s}{project_name}{pt.s}engine{pt.s}{file}", "r")
            inf = f.read()
            inf = inf.replace("eui._console", "return 0 #")
            inf = inf.replace("engineUI", "engine.engine", 1)
            inf = inf.replace("settings", "engine.settings", 1)
            inf = inf.replace("pather", "engine.pather", 1)
            inf = inf.replace("UniPy", "engine.UniPy", 1)
            if file in ["engineOUAR.py", "UniPy.py"]:
                inf = inf.replace("modules", "engine", 1)
                inf = inf.replace("objects", "engine", 2)
            f.close()
            f = open(f"{create_path}{pt.s}{project_name}{pt.s}engine{pt.s}{file}", "w")
            f.write(inf)
            f.close()
            
    _files = []
    DIRS = []
    for root, dirs, files in os.walk(f"{create_path}{pt.s}{project_name}{pt.s}res"):
        for i in files:
            DIRS.append(root)
            _files.append(i)
    
    for file in _files:
        if file[-3:] == ".py":
            f = open(f"{DIRS[_files.index(file)]}{pt.s}{file}", "r")
            inf = f.read()
            tree = ast.parse(inf)
            visitor = ImportVisitor()
            new_tree = visitor.visit(tree)
            inf = ast.unparse(new_tree)
            f.close()
            f = open(f"{DIRS[_files.index(file)]}{pt.s}{file}", "w")
            f.write(inf)
            f.close()
    
    sf = open(f"{create_path}{pt.s}{project_name}{pt.s}engine{pt.s}settings.py", "r")
    inf = sf.read()
    inf = inf.replace("{AppName}", program_name, 1)
    EIK = ""
    while 1:
        EIK = "".join([str(randint(0, 9)) for i in range(5)]) + ".png"
        if EIK not in _files:
            inf = inf.replace('EIK = "00000.png"', f'EIK = "{EIK}"')
            os.rename(f"{create_path}{pt.s}{project_name}{pt.s}engine{pt.s}engineIcon.png", f"{create_path}{pt.s}{project_name}{pt.s}engine{pt.s}{EIK}")
            shutil.move(f"{create_path}{pt.s}{project_name}{pt.s}engine{pt.s}{EIK}", f"{create_path}{pt.s}{project_name}{pt.s}res")
            break
    
    if lpv != None and lpv != program_version and df:
        shutil.move(f"exporter{pt.s}$data", f"{create_path}{pt.s}{project_name}{pt.s}res")
    elif df:
        shutil.rmtree(f"exporter{pt.s}$data")
    
    inf = inf.replace("projectSize = (0, 0)", f"projectSize = {program_size}", 1)
    inf = inf.replace("{EV}", st.version)
    inf = inf.replace("{VR}", program_version)
    sf.close()
    sf = open(f"{create_path}{pt.s}{project_name}{pt.s}engine{pt.s}settings.py", "w")
    sf.write(inf)
    sf.close()
    
    upf = open(f"{create_path}{pt.s}{project_name}{pt.s}engine{pt.s}UniPy.py", "r")
    inf = upf.read()
    inf = inf.replace("def appQuit(): eui.returnToEditor()", "def appQuit(): exit()", 1)
    inf = inf.replace('.{pt.s}projects{pt.s}{st.projects[st.projectIdx]}', 'res')
    inf = inf.replace("{eui.PATH}{pt.s}{st.projects[st.projectIdx]}", "res")
    inf = inf.replace('eui._console.Log(text, "log", file.split("{pt.s}")[-1], line)', "")
    upf.close()
    upf = open(f"{create_path}{pt.s}{project_name}{pt.s}engine{pt.s}UniPy.py", "w")
    upf.write(inf)
    upf.close()
    
    f = open(f"{create_path}{pt.s}{project_name}{pt.s}res{pt.s}ObjectInfo.txt", "r")
    inf = f.read()
    inf = inf.replace(f"font: .{pt.s}projects{pt.s}{project_name}", "font: res")
    f.close()
    f = open(f"{create_path}{pt.s}{project_name}{pt.s}res{pt.s}ObjectInfo.txt", "w")
    f.write(inf)
    f.close()