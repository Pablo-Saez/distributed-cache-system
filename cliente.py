import json
import time
import requests
import random

import redis

# Conexión a las tres instancias de Redis
r1 = redis.Redis(host='localhost', port=6378, db=0)
r2 = redis.Redis(host='localhost', port=6380, db=0)
r3 = redis.Redis(host='localhost', port=6381, db=0)

def encode_uid(uid):
    # Dividir el UID en sus partes componentes
    parts = uid.split('-')
    number = int(parts[0])
    name1 = parts[1]
    
    # Calcular un valor único basado en las partes del UID
    value = (number * len(name1)) % 30
    
    # Si el UID tiene una segunda parte de nombre, incluirla en el cálculo
    if len(parts) == 3:
        name2 = parts[2]
        value = (value + len(name2)) % 30
    
    # Devolver el valor calculado
    return value

with open('uids.txt', 'r') as f:
    uids = f.read().splitlines()

# Definir la cantidad de consultas que se desean hacer
n = 4000
sample_uids = random.choices(uids, k=n)
AcumuladorCache = 0
contadorCache = 0
AcumuladorAPI = 0
contadorAPI = 0


# Hacer n consultas a la API, escogiendo los UIDs de manera aleatoria
for uid in sample_uids:
    valor_rango = encode_uid(uid)

    # size = data['size']
    # species = data['species']
    # nombre_comun = data['name']['spanish']
    if (valor_rango > 0 and valor_rango <=9):
        start_time = time.time()
        result = r1.get(uid)
        if result is not None:
            print("cache hit in cache 1")
            end_time = time.time()
            contadorCache = contadorCache +1
            AcumuladorCache = AcumuladorCache + end_time - start_time
        else:
            print("cache miss")
            try:
                valor_rango = encode_uid(uid)
                url = f'https://aves.ninjas.cl/api/birds/{uid}'
                response = requests.get(url)
                data = json.loads(response.text)
                size = data['size']
                species = data['species']
                nombre_comun = data['name']['spanish']
                r1.set(uid, f"{nombre_comun}, {size}, {species}")
                print("fetched from api")
                end_time = time.time()
                contadorAPI = contadorAPI+1
                AcumuladorAPI = AcumuladorAPI + end_time - start_time
                
            except json.decoder.JSONDecodeError:
                print("Error decoding JSON. Continuing with next iteration.")
                continue
            
        print(f"UID: {uid}, Resultado: {result}, Tiempo: {end_time - start_time}")

    elif (valor_rango >9 and valor_rango <=19):
        start_time = time.time()
        result = r2.get(uid)
        if result is not None:
            print("cache hit in cache 2")
            end_time = time.time()
            contadorCache = contadorCache +1
            AcumuladorCache = AcumuladorCache + end_time - start_time
        else:
            print("cache miss")
            try:
                valor_rango = encode_uid(uid)
                url = f'https://aves.ninjas.cl/api/birds/{uid}'
                response = requests.get(url)
                data = json.loads(response.text)
                size = data['size']
                species = data['species']
                nombre_comun = data['name']['spanish']
                r2.set(uid, f"{nombre_comun}, {size}, {species}")
                print("fetched from api")
                end_time = time.time()
                contadorAPI = contadorAPI+1
                AcumuladorAPI = AcumuladorAPI + end_time - start_time
            except json.decoder.JSONDecodeError:
                print("Error decoding JSON. Continuing with next iteration.")
                continue
            
        print(f"UID: {uid}, Resultado: {result}, Tiempo: {end_time - start_time}")
        
    elif (valor_rango >19 and valor_rango<=29):
        start_time = time.time()
        result = r3.get(uid)
        if result is not None:
            print("cache hit in cache 3")
            end_time = time.time()
            contadorCache = contadorCache +1
            AcumuladorCache = AcumuladorCache + end_time - start_time
        else:
            print("cache miss")
            try:
                valor_rango = encode_uid(uid)
                url = f'https://aves.ninjas.cl/api/birds/{uid}'
                response = requests.get(url)
                data = json.loads(response.text)
                size = data['size']
                species = data['species']
                nombre_comun = data['name']['spanish']
                r3.set(uid, f"{nombre_comun}, {size}, {species}")
                print("fetched from api")
                end_time = time.time()
                contadorAPI = contadorAPI+1
                AcumuladorAPI = AcumuladorAPI + end_time - start_time
                
            except json.decoder.JSONDecodeError:
                print("Error decoding JSON. Continuing with next iteration.")
                continue
            
        print(f"UID: {uid}, Resultado: {result}, \n Tiempo: {end_time - start_time}")

promCache = AcumuladorCache/contadorCache
promApi = AcumuladorAPI/contadorAPI
print("el promedio de tiempo de cache es : " + str(promCache))
print("el promedio de tiempo de API   es : " + str(promApi))