# currency: str = "Dollar - $"
# dollar_sign: str = currency.replace(" ", "").split("-")[1]
# print(dollar_sign)
#
# rows = ["1", "2", "3"]
#
# print(rows[:-2])

import requests
a = sum([-10])
print(a)
exchange = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=11')
print(exchange.json())
