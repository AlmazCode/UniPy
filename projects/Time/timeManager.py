import datetime
from UniPy import GetObj

tx = GetObj("text")

def Update():
    now = datetime.datetime.now()
    time_formatted = now.strftime("%H:%M:%S")
    
    tx.text = time_formatted