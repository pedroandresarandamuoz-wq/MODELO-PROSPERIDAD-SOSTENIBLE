import wbgapi as wb
import pandas as pd
import json
import os

# Asegurar que estamos en el directorio correcto
os.makedirs('data', exist_ok=True)

def obtener_datos_pib_ppa():
    # Indicador de PIB per cápita, PPA (constantes 2017 a precios internacionales)
    indicador = 'NY.GDP.PCAP.PP.KD'
    print(f"Extrayendo {indicador} desde el Banco Mundial...")
    
    # Descarga los datos
    # 'economy="all"' captura todos los países/regiones
    df = wb.data.DataFrame(indicador, economy='all', time=range(2008, 2024), skipBlanks=True)
    
    # Limpieza de nombres de columnas (quita el prefijo YR)
    df.columns = [c.replace('YR', '') for c in df.columns]
    
    # Rellenar nulos con 0 para mantener la consistencia numérica
    df = df.fillna(0)
    
    # Formateo a estructura de diccionario
    datos_finales = {}
    for pais, anios in df.to_dict('index').items():
        datos_finales[str(pais)] = {str(anio): float(valor) for anio, valor in anios.items()}
    
    # Guardar en archivo JSON
    ruta_salida = 'data/pib_ppa_2008_2023.json'
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(datos_finales, f, indent=4, ensure_ascii=False)
        
    print(f"Proceso finalizado. Datos guardados en {ruta_salida}")
    return datos_finales

if __name__ == "__main__":
    obtener_datos_pib_ppa()