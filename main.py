import requests, re, time, json
import pandas as pd
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'}

print('Reading items...')
with open('./item_name.json', 'r', encoding='utf-8') as f:
    item_name = f.read()
    item_name = json.loads(item_name)

print('Searching for prices...')
s = 0
res = []
for x in item_name.keys():
    url = 'https://warframe.market/items/' + x
    r = requests.get(url, headers=headers).text
    order_type = re.findall('"order_type": "(.*?)"', r)
    mod_rank = re.findall('"mod_rank": (.*?)},', r)
    price = re.findall(r'"platinum": (.*?),', r)
    status = re.findall(r'"status": "(.*?)"', r)
    name = re.findall(r'"ingame_name": "(.*?)"', r)
    price0 = []
    price10 = []
    for t in range(0, len(price)):
        if order_type[t] == 'sell' and status[t] == 'ingame':
            if mod_rank[t] == '0':
                price0.append(float(price[t]))
            elif mod_rank[t] == '10':
                price10.append(float(price[t]))
    selling_num_10 = len(price10)
    price_0 = list(set(price0))
    price_0.sort()
    price_10 = list(set(price10))
    price_10.sort()
    if len(price_0) == 0 or len(price_10) == 0:
        res.append([item_name[x], x, 'no selling'])
    elif len(price_0) == 1:
        res.append([item_name[x], x, price_0[0], price_10[0], price_10[0] - price_0[0], selling_num_10])
    else:
        res.append([item_name[x], x, price_0[1], price_10[0], price_10[0] - price_0[1], selling_num_10])

    s = s + 1
    print('\rCurrent Progress:{0}/{1}'.format(s, len(item_name)), end=' ')

data = pd.DataFrame(res, columns=['name', 'name', 'rank0', 'rank10', 'profit', 'selling_number_10'])
timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
os.makedirs('./results', exist_ok=True)
data.to_csv('./results/warframe_values' + timestamp + '.csv', encoding="ANSI")
