import json, urllib.request
from sys import exit

print("Thanks bittrex.com for awesome api...")
text1 = """"Please write two currencies (insert them upper case upper case)
Your first currency should be one of these: """

currency_api = 'https://bittrex.com/api/v1.1/public/getcurrencies'
currency_list = json.loads(urllib.request.urlopen(currency_api).read().decode("utf-8"))["result"]

market_currency_list = ["BTC", "ETH", "USDT"]
currency_list_name = []

for i in range(0, len(currency_list)):
    if "Currency" in currency_list[i]:
        currency_list_name.append(currency_list[i]['Currency'])

print(text1)
print(*market_currency_list, end=", ")
print("\n", "Your second currency should be one of these:")
print(*currency_list_name, sep=", ")
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
data = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))["result"]['Last']
print("And the result of your inputs will be last price from the bittrex.com/home/markets which is : ", data, "Again thanks bittrex", sep="\n")

