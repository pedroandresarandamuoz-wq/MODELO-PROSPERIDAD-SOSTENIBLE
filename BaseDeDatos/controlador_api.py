import json
import requests
import time

# 1. Cargar configuraciones y datos
with open('cliente_api_bm.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    base_url = config.get('base_url', 'https://api.worldbank.org/v2/country')

with open('interdependencia.json', 'r', encoding='utf-8') as f:
    interdependencia = json.load(f)

pib_data = {}

# 2. Iterar sobre todos los países y años
print("Iniciando la descarga de datos del BM. Esto puede tardar unos minutos...")

for iso, años in interdependencia.items():
    pib_data[iso] = {}
    for año in años.keys():
        url = f"{base_url}/{iso}/indicator/NY.GDP.MKTP.CD?date={año}&format=json"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Extraer valor si existe
                if len(data) > 1 and data[1] and data[1][0]['value']:
                    pib_data[iso][año] = data[1][0]['value']
                else:
                    pib_data[iso][año] = None
            else:
                pib_data[iso][año] = None
        except Exception:
            pib_data[iso][año] = None
        
        # Pausa breve para no sobrecargar la API
        time.sleep(0.2)
    
    print(f"✅ Procesado: {iso}")

# 3. Guardar pib.json
with open('pib.json', 'w', encoding='utf-8') as f:
    json.dump(pib_data, f, indent=4, ensure_ascii=False)

print("¡Proceso finalizado! Archivo 'pib.json' generado con éxito.")