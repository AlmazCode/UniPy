import requests
from UniPy import GetObj

tx = GetObj("text")

# Список криптовалют, для которых нужно получить курс
cryptos = ['bitcoin', 'ethereum', 'binancecoin', "dogcoin", "cardano"]

def Start():
    endTx = ""
    # Запрашиваем данные с CoinGecko API
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=' + ','.join(cryptos) + '&vs_currencies=usd')
    # Проверяем статус ответа на запрос
    
    if response.status_code == 200:
        # Если запрос успешен, получаем курс криптовалют из ответа
        data = response.json()
        for crypto in cryptos:
            price = data[crypto]['usd']
            endTx += f"{crypto.capitalize()} price: {price} USD\\n"
        
        tx.text = endTx
    
    else:
        # Если запрос неудачный, выводим сообщение об ошибке
        tx.text = 'Error:', response.status_code