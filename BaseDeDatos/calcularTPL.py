import json
import math
import os

def calcular_tpl():
    # 1. Rutas de archivo
    ruta_base = 'Base_Datos_MPS_Final_ERI.json'
    ruta_almacen = 'almacen_datos_maestro.json'
    ruta_salida = 'TPL_calculado.json'

    # Factor de atenuación: 
    # Si ERI es 1.0 (100% eficiente), con atenuación de 0.5, 
    # el impacto será 0.5 en lugar de 1.0. Esto evita el colapso de la TPL.
    # Puedes ajustar este valor entre 0.1 y 1.0 según la "tenuidad" que veas en Excel.
    factor_atenuacion = 0.5 

    with open(ruta_base, 'r', encoding='utf-8') as f:
        base_mps = json.load(f)
        
    with open(ruta_almacen, 'r', encoding='utf-8') as f:
        almacen = json.load(f)

    resultado = {}

    for pais, periodos in base_mps.items():
        resultado[pais] = {}
        for anio, indicadores in periodos.items():
            estructura = indicadores.get('estructura', 0.0)
            transferencias = indicadores.get('transferencias', 0.0)
            c_h = indicadores.get('ch', 0.0)
            eri_raw = indicadores.get('eri', 0.0)
            
            eta_norm = almacen.get(pais, {}).get(anio, {}).get('ETA_NORM', 0.0)
            
            # Normalización del ERI
            eri_normalizado = eri_raw / 100.0 if eri_raw > 1.0 else eri_raw
            
            # Aplicación estricta de la Ley de Aranda Muñoz
            try:
                # TPL_base igual a tu original
                tpl_base = (estructura ** (2 - eta_norm)) + math.sqrt(transferencias) + c_h
                
                # CORRECCIÓN DE EQUILIBRIO: 
                # Aplicamos el atenuador para que la mitigación del ERI sea más progresiva
                # y no "rompa" el equilibrio de la TPL.
                mitigacion = 1 - (eri_normalizado * factor_atenuacion)
                tpl = tpl_base * mitigacion
                
            except (ValueError, TypeError, OverflowError):
                tpl = 0.0
                
            resultado[pais][anio] = round(float(tpl), 4)

    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    print(f"--- ÉXITO: TPL calculada con atenuación ({factor_atenuacion}) guardada en {ruta_salida} ---")

if __name__ == "__main__":
    calcular_tpl()