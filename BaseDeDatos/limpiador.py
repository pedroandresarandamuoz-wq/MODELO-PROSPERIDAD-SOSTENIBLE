import json

# 1. Carga de los ficheros
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# Cargar archivos (asumiendo nombres de fichero)
pn_data = load_json('PN.json')
fin_data = load_json('datos_financieros_mps.json')['paises']
balanza_data = load_json('balanza_sectorial.json')['paises']
comercio_data = load_json('BaseDatos_Comercio.json')

# 2. Diccionario de mapeo Nombre -> ISO
# Nota: Necesitarás completar este diccionario con todos tus países
mapping = {
    "Albania": "ALB", "Austria": "AUT", "Botswana": "BWA", 
    "Canada": "CAN", "China": "CHN", "Costa Rica": "CRI",
    # ... añadir resto de países
}

# 3. Estructura de normalización
normalizado = {}

# Inicializar con la estructura de PN.json (la base maestra)
for iso, años in pn_data.items():
    if iso not in normalizado:
        normalizado[iso] = {}
    for año in años.keys():
        normalizado[iso][año] = {"pn_valor": años[año]}

# 4. Integrar datos de otros ficheros basándose en el ISO
def integrar_datos(data_origen, tipo_datos, es_por_nombre=False):
    for pais_key, años in data_origen.items():
        iso = mapping.get(pais_key) if es_por_nombre else pais_key
        if iso in normalizado:
            for año, valores in años.items():
                if año in normalizado[iso]:
                    normalizado[iso][año][tipo_datos] = valores

integrar_datos(fin_data, "financiero")
integrar_datos(balanza_data, "sectorial")
# BaseDatos_Comercio tiene estructura diferente, requiere ajuste fino:
for nombre, años in comercio_data.items():
    iso = mapping.get(nombre)
    if iso in normalizado:
        for año, vals in años.items():
            if año in normalizado[iso]:
                normalizado[iso][año]["comercio"] = vals

# 5. Guardar resultado
with open('data_normalizada.json', 'w') as f:
    json.dump(normalizado, f, indent=4)