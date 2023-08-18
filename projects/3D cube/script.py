import UniPy as up

obj = up.GetObj("obj")
tx = up.GetObj("inf")
d = 0

def Start():
    global obj
    obj = obj.GetModule("cube")

def Update():
    global d
    
    tx.text = f"""
x: {obj.this.x}
y: {obj.this.y}
z: {obj.z}
angle_x: {obj.angle_x}
angle_y: {obj.angle_y}
    """.strip()
    obj.angle_x += 0.05
    if d == 0:
        obj.z = up.Math.lerp(obj.z, 450, 0.03)
        if obj.z >= 400: d = 1
    else:
        obj.z = up.Math.lerp(obj.z, 150, 0.03)
        if obj.z <= 200: d = 0