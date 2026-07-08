import json

def read_big_json(filename):
    with open(filename,"r",encoding='utf-8') as json_file:
        for line in json_file:
            yield json.loads(line.strip())

gen = read_big_json('cars.ndjson')

for car in gen:
    if car.get('price') >= 1000:
        print(car['title'],'стоит',car['price'])