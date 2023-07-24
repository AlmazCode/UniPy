from UniPy import (
	GetObj,
	SetBgColor,
	SaveVariable,
	LoadVariable,
	consoleLog
)

tx = GetObj("coins")
txCC = GetObj("text_CC")
txPrice = GetObj("tx_update")
bt = GetObj("button")
btUpdate = GetObj("btUpdate")

money = 0
CC = 0
price = 100

def Start():
    global money, CC, price
    
    consoleLog(f"Привет, это лог!")
    
    SetBgColor((70, 70, 70))
    
    money = LoadVariable("moneys")
    CC = LoadVariable("CC", 1)
    price = LoadVariable("price", price)
    tx.text = f"{int(money)}"
    txCC.text = f"{str(CC)[0:3]} за клик"
    txPrice.text = f"Улучшить\\n{price}\\nкоинов"

def addMoney(state: bool):
    global money
    
    money += CC if state else 0
    tx.text = f"{int(money)}"
    SaveVariable("moneys", money, "int")
    bt.anims = []
    txCC.anims = []
    bt.AddAnim([4, 4], f"width = {266 if state else 255}; height = {266 if state else 255}", [], [], True)
    txCC.AddAnim([2], f"fontSize = {36 if state else 32}", [], [], True)

def updateClicks():
	global price, money, CC

	if money >= price:
		money -= price
		price = int(price * 1.5)
		CC *= 1.2
		
		SaveVariable("CC", CC, "float")
		SaveVariable("price", price, "int")
		
		tx.text = f"{int(money)}"
		txCC.text = f"{str(CC)[0:3]} за клик"
		txPrice.text = f"Улучшить\\n{price}\\nкоинов"

bt.onPressed = addMoney
bt.onPressedContent = "(True)"
bt.onUnPressed = addMoney
bt.onUnPressedContent = "(False)"

btUpdate.onPressed = updateClicks