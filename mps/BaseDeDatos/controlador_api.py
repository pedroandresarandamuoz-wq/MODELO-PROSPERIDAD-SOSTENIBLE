import requests

def obtener_indicadores_pais(pais_code, anio_inicio=2008, anio_fin=2025):
    """
    Descarga en una sola llamada los tres indicadores para un país y rango de años.
    """
    # Mapeo de tus indicadores MPS
    indicadores = {
        "consumo": "NE.CON.GOVT.ZS",
        "transferencias": "GC.XPN.SOPI.ZS", # El nuevo que pediste
        "inversion": "NE.GDI.TOTL.ZS"
    }
    
    resultados = {str(anio): {"consumo": 0.0, "transferencias": 0.0, "inversion": 0.0} 
                  for anio in range(anio_inicio, anio_fin + 1)}
    
    for cat, ind_code in indicadores.items():
        url = f"https://api.worldbank.org/v2/country/{pais_code}/indicator/{ind_code}?date={anio_inicio}:{anio_fin}&format=json&per_page=50"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1 and data[1]:
                    for item in data[1]:
                        anio = item["date"]
                        valor = item["value"]
                        if anio in resultados:
                            resultados[anio][cat] = float(valor) if valor is not None else 0.0
        except Exception as e:
            print(f"Error consultando {ind_code} para {pais_code}: {e}")
            
    return resultados

# --- Ejemplo de uso ---
# paises = ["ESP", "FRA", "DEU"]
# for p in paises:
#     print(f"Datos de {p}:", obtener_indicadores_pais(p))