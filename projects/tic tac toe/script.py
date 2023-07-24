import UniPy as up

state = "cross"
blocksCount = 9
blocksPressed = 0
end = False

up.DelObj(up.GetObj("cross"))
up.DelObj(up.GetObj("zero"))

def setTsp(nms):
    for obj in [*up.GetObjectsWithTag("cross"), *up.GetObjectsWithTag("zero")]:
        if obj.GetModule("pos")._pos not in nms:
            obj.transparent = 128

def checkBlocks(blocks):
    for j in ["cross", "zero"]:
        if (blocks[0]._content == j
        and blocks[1]._content == j
        and blocks[2]._content == j
            ):
                setTsp([0, 1, 2])
                return blocks[0]._content
        if (blocks[3]._content == j
        and blocks[4]._content == j
        and blocks[5]._content == j
            ):
                setTsp([3,4,5])
                return blocks[3]._content
        
        if (blocks[6]._content == j
        and blocks[7]._content == j
        and blocks[8]._content == j
            ):
                setTsp([6, 7, 8])
                return blocks[6]._content
        
        
        if (blocks[0]._content == j
        and blocks[3]._content == j
        and blocks[6]._content == j
            ):
                setTsp([0, 3, 6])
                return blocks[0]._content

        if (blocks[1]._content == j
        and blocks[4]._content == j
        and blocks[7]._content == j
            ):
                setTsp([1, 4, 7])
                return blocks[1]._content
        
        if (blocks[2]._content == j
        and blocks[5]._content == j
        and blocks[8]._content == j
            ):
                setTsp([2, 5, 8])
                return blocks[2]._content
        
        
        if (blocks[0]._content == j
        and blocks[4]._content == j
        and blocks[8]._content == j
            ):
                setTsp([0, 4, 8])
                return blocks[0]._content
        
        if (blocks[2]._content == j
        and blocks[4]._content == j
        and blocks[6]._content == j
            ):
                setTsp([2, 4, 6])
                return blocks[2]._content

    if blocksPressed == blocksCount:
        setTsp([])
        return "Draw!"

    return None

def onFingerDown(_id, _pos):
    global state, blocksPressed, end

    if _id == 0 and blocksPressed < blocksCount and not end:
        objs = up.GetObjectsWithTag("obj")

        for obj in objs:
            if obj.rect.collidepoint(_pos) and not obj.GetModule("block")._pressed:
                md = obj.GetModule("block")
                up.CloneObject(state)
                up.objects[-1].GetModule("pos")._pos = md.pos
                up.objects[-1].cx = f"objCX({obj.PARENT})"
                up.objects[-1].cy = f"objCY({obj.PARENT})"
                up.objects[-1].setPosObject()
                md._pressed = True
                md._content = state
                if state == "cross":
                    state = "zero"
                else:
                    state = "cross"
                blocksPressed += 1

                winner = checkBlocks([obj.GetModule("block") for obj in objs])
                if winner is not None:
                    end = True
                    up.GetObj("bg").render = True
                    up.GetObj("winner").render = True
                    up.GetObj("winner").text = f"{winner} won!" if winner != "Draw!" else winner
                break
    elif end:
        up.reloadApp()