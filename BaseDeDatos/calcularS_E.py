import json

def calcular_y_normalizar_se():
    # 1. Carga de los datasets
    with open('pib.json', 'r') as f:
        pib_data = json.load(f)
    with open('interdependencia.json', 'r') as f:
        inter_data = json.load(f)

    se_results = {}

    # 2. Iteración sobre cada país y cada año
    for pais, anios in inter_data.items():
        if pais not in pib_data:
            continue
        
        se_results[pais] = {}
        for anio, indicadores in anios.items():
            if anio not in pib_data[pais]:
                continue
            
            pib = pib_data[pais][anio]
            if pib is None or pib == 0:
                continue

            # 3. Extracción de variables con limpieza de nulos
            financiero = indicadores.get('financiero', {})
            comercio = indicadores.get('comercio', {})

            oda = financiero.get('oda_recibida_usd') or 0
            remesas = financiero.get('remesas_recibidas_usd') or 0
            importaciones = comercio.get('importaciones') or 0
            exportaciones = comercio.get('exportaciones') or 0

            # 4. Cálculo del Subsidio Exterior (S_E)
            # Logica: (Importaciones - Exportaciones) + ODA + Remesas
            # Se normaliza como porcentaje del PIB
            s_e_raw = (importaciones - exportaciones) + oda + remesas
            s_e_pct = (s_e_raw / pib) * 100

            se_results[pais][anio] = {
                's_e_raw_usd': s_e_raw,
                's_e_pct_pib': s_e_pct,
                'pib_nominal': pib
            }

    # 5. Generación del archivo S_E.json
    with open('S_E.json', 'w') as f:
        json.dump(se_results, f, indent=4)
    
    print("Archivo 'S_E.json' generado correctamente.")

if __name__ == "__main__":
    calcular_y_normalizar_se()