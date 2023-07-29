import UniPy as up

# gettings objects
player = up.GetObj("player")
player.gravity = 0

# set game bg color
up.SetBgColor((161, 37, 27))

dialogText = None
DT = up.GetObj("DT")
di = 0
endStartScene = False
newGame = True
sceneLayer = 0
timeToSpawn = 1
t = 0

# start dialog
sd = [
    "Капитан Росс: Эдвард, все готово для твоего выхода на Марс?",
    "Эдвард: Да, Капитан Росс. Все системы проверены и работают исправно. \nЯ готов начать свою миссию и исследовать эту загадочную планету.",
    "Капитан Росс: Отлично, Эдвард. Но помни, что это опасное предприятие. Марс \nможетбыть весьма непредсказуемым. Ты должен оставаться бдительным и\nделать все возможное, чтобы вернуться на Землю в одном куске.",
    "Эдвард: Полностью согласен, капитан. Я хорошо подготовлен и готов к любым\nтрудностям, которые могут возникнуть. Я не собираюсь останавливаться,\nпока не достигну цели.",
    "Капитан Росс: Я верю в тебя, Эдвард. Ты первый человек, отправляющийся на\nМарс, и твоя миссия имеет огромное значение для науки и человечества.\nУ тебя есть все необходимое оборудование и ресурсы, чтобы успешно\nвыполнить свою задачу.",
    "Эдвард: Спасибо, капитан. Я чувствую себя гордым и честью быть частью\nэтой миссии. Я обещаю, что сделаю все возможное, чтобы принести пользу\nнауке и обеспечить безопасный возврат на Землю.",
    "Капитан Росс: Ты сильный и решительный человек, Эдвард. Уверен, что ты\nсправишься со всеми вызовами, которые встретишь на своем пути. Удачи,\nи вернись к нам в целости и сохранности.",
    "Эдвард: Спасибо за поддержку, капитан Капитан Росс. Обещаю вернуться\nдомой иподелиться своими открытиями с вами и всеми на Земле."
]

def StartGame():
    global sceneLayer, endStartScene
    
    up.SetCamera("player")
    sceneLayer = 0
    endStartScene = True
    
    up.GetObj("rocket").rect.topleft = (0,0)
    up.GetObj("rocketHitBox").rect.bottom = up.GetObj("rocket").rect.bottom
    up.GetObj("sceneBg").render = False
    up.GetObj("stone").render = True
    up.GetObj("player").render = True
    up.GetObj("handler").render = True
    up.GetObj("handlerBg").render = True
    
    for _ in range(10):
        up.CloneObject("stone")
    
    for _ in range(100):
        up.CloneObject("particleGround")

def onFingerDown(_id, _pos):
    global di, endStartScene, sceneLayer
    
    if not endStartScene and sceneLayer == 0:
        if di != len(sd) - 1 and _id == 0:
            di += 1
            DT.text = sd[di]
            dialogText.Restart()
        else:
            up.GetObj("sceneBg").image = up.GetTexture("rocketClimbedBg")
            up.GetObj("DT").render = False
            up.GetObj("rocket").render = True
            up.GetObj("dialogBg").render = False
            up.GetObj("rocket").AddAnim([1], f'y = {up.GetObj("rocket").y - 50}')
            up.GetObj("rocket").AddAnim([10], f'y = {up.GetObj("rocket").y - 1150}', [StartGame])
            sceneLayer = 1

def Start():
    global dialogText
    
    if newGame:
        dialogText = up.GetObj("DT").GetModule("anim")
        DT.text = sd[di]
        dialogText.Restart()
    else: StartGame()

def Update():
    global t
    
    if sceneLayer == 1:
        t += 1
        if t == timeToSpawn:
            up.CloneObject("particle")
            t = 0