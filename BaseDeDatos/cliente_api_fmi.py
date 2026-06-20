import wbgapi as wb
import pandas as pd
import json

# Importamos tu diccionario de países
from BaseDeDatos.MetaDatos.paises import PAISES_MPS

def extraer_datos_mps():
    # 1. Definir los indicadores necesarios
    # ODA: Ayudas, Balanza: Cuenta Corriente, Tech: Alta tecnología, 
    # Inflación: IPC, PIB: Nominal
    indicadores = {
        'DT.ODA.ODAT.CD': 'Ayudas_ODA',
        'BN.CAB.XOKA.CD': 'Balanza_Corriente',
        'TX.VAL.TECH.CD': 'Exportaciones_Alta_Tech',
        'FP.CPI.TOTL.ZG': 'Inflacion',
        'NY.GDP.MKTP.CD': 'PIB_Nominal'
    }
    
    codigos_paises = list(PAISES_MPS.values())
    anios = range(2008, 2024) # Rango solicitado
    
    print("Iniciando extracción masiva de datos...")
    
    # 2. Descargar datos en formato panel (Wide format)
    df = wb.data.DataFrame(indicadores.keys(), codigos_paises, time=anios, labels=False)
    
    # 3. Procesamiento y limpieza
    # La API devuelve columnas tipo 'YR2008'. Las limpiamos.
    df.columns = [c.replace('YR', '') for c in df.columns]
    
    # 4. Transformar a estructura de árbol que requiere tu MPS
    # Índice multi-nivel: País, Indicador
    df = df.reset_index().rename(columns={'index': 'pais'})
    df = df.melt(id_vars=['pais'], var_name='anio', value_name='valor')
    
    # Crear un DataFrame pivotado para tener indicadores en columnas
    df_pivot = df.pivot_table(index=['pais', 'anio'], columns='level_1', values='valor').reset_index()
    
    # 5. Estructurar en JSON
    mps_data = {}
    for _, row in df_pivot.iterrows():
        pais = row['pais']
        anio = str(int(row['anio']))
        
        if pais not in mps_data:
            mps_data[pais] = {}
            
        mps_data[pais][anio] = {
            "Ayudas_ODA_Recibidas": row.get('DT.ODA.ODAT.CD'),
            "Balanza_Cuenta_Corriente": row.get('BN.CAB.XOKA.CD'),
            "Exportaciones_Alta_Tecnologia": row.get('TX.VAL.TECH.CD'),
            "Inflacion": row.get('FP.CPI.TOTL.ZG'),
            "pib_nominal": row.get('NY.GDP.MKTP.CD')
        }
        
    # 6. Guardar
    with open('mps_data_raw.json', 'w', encoding='utf-8') as f:
        json.dump(mps_data, f, indent=4, ensure_ascii=False)
        
    print("Extracción completada. Archivo guardado como 'mps_data_raw.json'")

if __name__ == "__main__":
    extraer_datos_mps()