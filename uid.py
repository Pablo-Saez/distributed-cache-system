import json
import requests
import random


url = "https://aves.ninjas.cl/api/birds"

response = requests.get(url)
data = response.json()

uids = [bird["uid"] for bird in data]


try:
    response = requests.get("https://aves.ninjas.cl/api/birds")
    data = json.loads(response.text)
except json.decoder.JSONDecodeError:
    print("Error decoding JSON. Continuing with next iteration.")
    


with open('uids.txt', 'w') as f:
    for bird in data:
        uid = bird['uid']
        f.write(uid + '\n')


# Leer los UIDs desde el archivo txt generado anteriormente
with open('uids.txt', 'r') as f:
    uids = f.read().splitlines()

# Definir la cantidad de consultas que se desean hacer
n = 10

# Hacer n consultas a la API, escogiendo los UIDs de manera aleatoria
for i in range(n):
    try:
        uid = random.choice(uids)
        url = f'https://aves.ninjas.cl/api/birds/{uid}'
        response = requests.get(url)
        data = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        print("Error decoding JSON. Continuing with next iteration.")
        continue

    print(f"Nombre común: {data['name']['spanish']} ")
    print(f"Tamaños: {data['size']}")
    print(f"Especie: {data['species']}")

