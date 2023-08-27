import UniPy as up
import pygame

player = up.GetObj("player")
newBlockView = up.GetObj("newBlockView")
btJ = up.GetObj("btJ")
btCreateBlock = up.GetObj("btCreateBlock")
tx = up.GetObj("info")
joystick = up.GetObj("joystick")

speed = 5
force = 12
start_pos = (player.x, player.y)
block_size = (up.GetObj("block").width, up.GetObj("block").height)
up.SetCamera("player")

def jump():
    if player.bottomCollided:
        player.addForce(force)

def Update():
    tx.text = f"x: $(0, 0, 255){player.rect.x}$(0,0,0), y: $(255, 0, 0){player.rect.y}"
    if player.rect.y > 4000:
        player.x, player.y = start_pos
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        player.rect.x += speed
        player.flipX = False
    
    if keys[pygame.K_a]:
        player.rect.x -= speed
        player.flipX = True
    
    if keys[pygame.K_SPACE]:
        jump()

def onFingerMotion(_id, pos):
    if _id == 0 and not joystick.GetModule("joystick")._ih1p:
        newBlockView.x = round((pos[0] - up.Camera.camera.x) / block_size[0]) * block_size[0]
        newBlockView.y = round((pos[1] - up.Camera.camera.y) / block_size[1]) * block_size[1]

def CreateNewBlock():
    for obj in up.objects:
        if hasattr(obj, "rect") and obj.bodyType == "static" and obj.rect.collidepoint((newBlockView.x, newBlockView.y)):
            return
    block = up.CloneObject("block")
    block.x = newBlockView.x
    block.y = newBlockView.y

btJ.onPressed = jump
btCreateBlock.onPressed = CreateNewBlock