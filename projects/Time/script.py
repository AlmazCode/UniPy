import datetime
import UniPy as up

tx = up.GetObj("text")

def Update():
    now = datetime.datetime.now()
    time_formatted = now.strftime("%H:%M:%S")
    
    tx.text = time_formatted