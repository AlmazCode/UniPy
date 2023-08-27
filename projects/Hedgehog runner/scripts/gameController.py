import UniPy as up

spawnSpeed = 90
particleSpawnSpeed = 15
tick = 0
tick2 = 0
moveSpeed = 5
end = False
score = 0
bestScore = up.LoadVariable("bestScore", 0)

up.SetBgColor((0, 180, 0))
up.GRAVITY = 0.0
lt = up.GetObj("leftTouch")
rt = up.GetObj("rightTouch")
player = up.GetObj("player")
thisScore = up.GetObj("thisScore")
bestScoreTx = up.GetObj("bestScore")
bestScoreTx.text = f"Best Score: {bestScore}"
player.gravity = 0
lt.width = up.wWidth // 2
lt.height = up.wHeight
rt.width = up.wWidth // 2
rt.height = up.wHeight
rt.setPos()

def onPlayerCollided():
    global end
    
    if player.collidedObj.tag == "log":
        end = True
        for obj in up.GetObjectsWithTag("log"):
            obj.GetModule("gifAnim").play = False
        up.GetObj("loseText1").render = True
        up.GetObj("loseText2").render = True

def onLogDeleted():
    global score, bestScore, moveSpeed, spawnSpeed
    
    score += 1
    if score > bestScore:
        bestScore = score
        bestScoreTx.text = f"Best Score: {bestScore}"
        up.SaveVariable("bestScore", bestScore, int)
        
    thisScore.text = f"Score: {score}"
    
    if score % 10 == 0:
        moveSpeed = int(moveSpeed * 1.2)
        for obj in up.GetObjectsWithTag("log"):
            obj.GetModule("logController")._speed = moveSpeed
        for obj in up.GetObjectsWithTag("particle"):
            obj.GetModule("particleController")._speed = moveSpeed
    
    if score % 20 == 0 and spawnSpeed > 20:
        spawnSpeed -= 10

def onFingerDown(_id, pos):
    if end: up.reloadApp()

def Update():
    global tick, tick2
    
    if not end:
        
        tick += 1
        tick2 += 1
        if tick == spawnSpeed:
            up.CloneObject("log")
            tick = 0
        if tick2 == particleSpawnSpeed:
            up.CloneObject("particle")
            tick2 = 0
        
        if lt.pressed():
            player.x -= moveSpeed
            if player.x < 0: player.x = 0
        if rt.pressed():
            player.x += moveSpeed
            if player.x + player.width  > up.wWidth:
                player.x = up.wWidth - player.width

player.onCollided = onPlayerCollided