import json
import math
import os

def calcular_tpl():
    # 1. Ruta del archivo fuente unificado y el almacén maestro para ETA_NORM
    ruta_base = 'Base_Datos_MPS_Final_ERI.json'
    ruta_almacen = 'almacen_datos_maestro.json'
    ruta_salida = 'TPL_calculado.json'

    # Carga de datos con codificación UTF-8
    print(f"Cargando origen de datos: {ruta_base}...")
    with open(ruta_base, 'r', encoding='utf-8') as f:
        base_mps = json.load(f)
        
    print(f"Cargando almacén maestro: {ruta_almacen}...")
    with open(ruta_almacen, 'r', encoding='utf-8') as f:
        almacen = json.load(f)

    resultado = {}

    # 2. Bucle de cálculo: país por país, año por año
    for pais, periodos in base_mps.items():
        resultado[pais] = {}
        for anio, indicadores in periodos.items():
            # Extracción de variables directamente de la nueva base de datos unificada
            estructura = indicadores.get('estructura', 0.0)
            transferencias = indicadores.get('transferencias', 0.0)
            c_h = indicadores.get('ch', 0.0)
            eri_raw = indicadores.get('eri', 0.0)
            
            # ETA_NORM del mismo país y año en el almacén maestro
            eta_norm = almacen.get(pais, {}).get(anio, {}).get('ETA_NORM', 0.0)
            
            # 3. Normalización del ERI a escala 0-1 (Tanto por uno)
            # Como en tu JSON viene como 4.2217, lo dividimos entre 100 para que sea 0.042217
            eri_normalizado = eri_raw / 100.0 if eri_raw > 1.0 else eri_raw
            
            # 4. Aplicación estricta de la Ley de Aranda Muñoz modificada
            try:
                # Fricción o Isquemia Base (Consumo Exponencial + Raíz Transferencias + Carga Oculta)
                tpl_base = (estructura ** (2 - eta_norm)) + math.sqrt(transferencias) + c_h
                
                # Mitigación por la Tasa de Eficiencia de Inversión (1 - ERI)
                tpl = tpl_base * (1 - eri_normalizado)
                
            except (ValueError, TypeError, OverflowError):
                tpl = 0.0
                
            # Guardar el dato exactamente en su país y año correspondientes
            resultado[pais][anio] = round(float(tpl), 4)

    # 5. Guardar archivo de salida unificado
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    print(f"\n--- ÉXITO: TPL con factor minorador (1-ERI) guardada en {ruta_salida} ---")

if __name__ == "__main__":
    calcular_tpl()