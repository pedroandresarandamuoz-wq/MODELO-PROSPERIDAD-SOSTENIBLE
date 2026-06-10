import json
import math
import os

def calcular_tpl():
    # 1. Rutas de los archivos fuente
    ruta_base = 'Base_Datos_MPS_Definitiva.json'
    ruta_almacen = 'almacen_datos_maestro.json'
    ruta_ch = 'ch_calculado.json'
    ruta_salida = 'TPL_calculado.json'

    # Carga de datos
    with open(ruta_base, 'r', encoding='utf-8') as f:
        base_mps = json.load(f)
    with open(ruta_almacen, 'r', encoding='utf-8') as f:
        almacen = json.load(f)
    with open(ruta_ch, 'r', encoding='utf-8') as f:
        carga_oculta = json.load(f)

    resultado = {}

    # 2. Bucle de cálculo: país por país, año por año
    for pais, periodos in base_mps.items():
        resultado[pais] = {}
        for anio, indicadores in periodos.items():
            # Extraer variables del país y año correspondiente
            estructura = indicadores.get('estructura', 0)
            transferencias = indicadores.get('transferencias', 0)
            
            # ETA_NORM del mismo país y año en el almacén maestro
            eta_norm = almacen.get(pais, {}).get(anio, {}).get('ETA_NORM', 0)
            
            # CH del mismo país y año en la carga oculta
            c_h = carga_oculta.get(pais, {}).get(anio, 0)
            
            # 3. Aplicación directa de la fórmula
            try:
                tpl = (estructura ** (2 - eta_norm)) + math.sqrt(transferencias) + c_h
            except (ValueError, TypeError, OverflowError):
                tpl = 0.0
                
            # Guardar el dato exactamente en su país y año correspondientes
            resultado[pais][anio] = round(float(tpl), 4)

    # 4. Guardar archivo de salida
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    print(f"--- ÉXITO: TPL calculada y guardada en {ruta_salida} ---")

if __name__ == "__main__":
    calcular_tpl()