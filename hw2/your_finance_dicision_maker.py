import json, urllib.request

from sys import exit

text0 = 'Thanks bittrex.com for awesome api...'

print(text0)

text1 = 'Please write two currencies (insert them upper case upper case)'

text2 = 'Your first currency should be one of these: '

text3 = 'Your second currency should be one of these: '

text4 = 'And the result of your inputs will be last price from the bittrex.com/home/markets which is :'

text5 = 'Again thanks bittrex'


currency_api = 'https://bittrex.com/api/v1.1/public/getcurrencies'

req_api = urllib.request.urlopen(currency_api).read()

req_api_utf = req_api.decode("utf-8")

currency_list = json.loads(req_api_utf)["result"]



market_currency_list = ["BTC", "ETH", "USDT"]

currency_list_name = []

for i in range(0, 191):
    if "Currency" in currency_list[i]:
        currency_list_name.append(currency_list[i]['Currency'])

print(text1, text2)

for i in range(3):
    print(market_currency_list[i], end=", ")

print("\n", text3)

for i in range(0, 191):
    print(currency_list_name[i], end=", ")

print("\n")



a = input("Your first currency please it will be the market actually: ")

if a not in market_currency_list:
    print("There are only 3 markets available and we already told you what they are")
    exit(0)



b = input("Your second currency please: ")

if b not in currency_list_name:
    print("191 currencies available and we already printed them")
    exit(0)


url = 'https://bittrex.com/api/v1.1/public/getticker?market={}-{}'.format(a,b)

x = urllib.request.urlopen(url)

y = x.read()

z = y.decode("utf-8")

data = json.loads(z)["result"]['Last']

print(text4, data, text5)

