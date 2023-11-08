import json
import os
import msgpack

with open('products_46.json') as f:
    data = json.load(f)

products = dict()

for item in data:
    if item['name'] in products:
        products[item['name']].append(item['price'])
    else:
        products[item['name']] = [item['price']]

results = list()

for name, prices in products.items():
    results.append(
        {
            'name': name,
            'max': max(prices),
            'min': min(prices),
            'avr': sum(prices) / len(prices),
        }
    )

with open('products_result.json', 'w') as r_json:
    r_json.write(json.dumps(results))

with open('products_result.msgpack', 'wb') as r_msgpack:
    r_msgpack.write(msgpack.dumps(results))

print(f'json    = {os.path.getsize('products_result.json')}')
print(f'msgpack = {os.path.getsize('products_result.msgpack')}')
