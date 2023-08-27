from UniPy import (
	GetObj,
	SetBgColor,
	SaveVariable,
	LoadVariable,
	log
)

tx = GetObj("coins")
txCC = GetObj("text_CC")
txPrice = GetObj("tx_update")
bt = GetObj("button")
btUpdate = GetObj("btUpdate")

money = 0
CC = 0
price = 100
isPressed = False
bw, bh, tfs = bt.width, bt.height, txCC.fontSize

def Start():
    global money, CC, price
    
    SetBgColor((70, 70, 70))
    
    money = LoadVariable("moneys")
    CC = LoadVariable("CC", 1)
    price = LoadVariable("price", price)
    tx.text = f"{int(money)}"
    g = str(CC).split(".", 1)
    if len(g) == 1: g.append("0")
    txCC.text = f"{g[0]}.{g[1][0]} за клик"
    txPrice.text = f"Улучшить\n{price}\nкоинов"
    
def onClick():
    global isPressed, bw, bh, tfs
    
    bt.anims = []
    txCC.anims = []
    
    if not isPressed:
        addMoney()
        bt.AddAnim([4, 4], f"width = {bw + 10}; height = {bh + 10}", [], [], True)
        txCC.AddAnim([2], f"fontSize = {tfs + 4}", [], [], True)
        isPressed = True
        bw += 10
        bh += 10
        tfs += 4
        
    else:
        bt.AddAnim([4, 4], f"width = {bw - 10}; height = {bh -+ 10}", [], [], True)
        txCC.AddAnim([2], f"fontSize = {tfs -+ 4}", [], [], True)
        isPressed = False
        bw -= 10
        bh -= 10
        tfs -= 4
    
def addMoney():
    global money
    
    money += CC
    tx.text = f"{int(money)}"
    SaveVariable("moneys", money, int)

def updateClicks():
	global price, money, CC

	if money >= price:
		money -= price
		price = int(price * 1.2)
		CC *= 1.2
		
		SaveVariable("moneys", money, int)
		SaveVariable("CC", CC, float)
		SaveVariable("price", price, int)
		
		tx.text = f"{int(money)}"
		g = str(CC).split(".", 1)
		if len(g) == 1: g.append("0")
		txCC.text = f"{g[0]}.{g[1][0]} за клик"
		txPrice.text = f"Улучшить\n{price}\nкоинов"

bt.onPressed = onClick
bt.onUnPressed = onClick
btUpdate.onPressed = updateClicks