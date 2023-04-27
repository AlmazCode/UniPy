import UniPy as up

player = up.GetObj("player")
btL = up.GetObj("btL")
btR = up.GetObj("btR")
btJ = up.GetObj("btJ")
tx = up.GetObj("tx!")

speed = 5
force = 50

def jump():
	player.addForce(force)

def Update():
    
    if btL.pressed():
    	player.rect.x -= speed
    	player.flipX = True
    if btR.pressed():
    	player.rect.x += speed
    	player.flipX = False
    tx.text = f"player pos:\\n{player.rect.topleft}"

btJ.onPressed = jump