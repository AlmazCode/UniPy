import random
from UniPy import GetObj

tx = GetObj("text")
tx2 = GetObj("txGenerate")
bt = GetObj("button")

MIN = 0
MAX = 10

tx2.text = f"Сгенерировать\\n{MIN}-{MAX}"

def Generate(Min, Max):
    tx.text = str(random.randint(Min, Max))

bt.onPressed = Generate
bt.onPressedContent = f"({MIN}, {MAX})"