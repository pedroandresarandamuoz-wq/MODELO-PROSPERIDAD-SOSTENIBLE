# BaseDeDatos/calculador_C_H.py

import json
from coeficientesch import calcular_todos_los_coeficientes, obtener_carga_oculta_final

def calcular_ch():
    with open('almacen_datos_maestro.json', 'r') as f:
        datos = json.load(f)

    resultado = {}
    EXPONENTE = 1.85 # Exponente fijo para estabilidad total
    
    for pais, periodos in datos.items():
        resultado[pais] = {}
        for anio, ind in periodos.items():
            # 1. Obtener carga bruta
            coefs = calcular_todos_los_coeficientes(ind)
            carga_bruta = obtener_carga_oculta_final(coefs)
            
            # 2. Base de cálculo
            base = carga_bruta / 10 
            
            # 3. Cálculo final con exponente fijo
            # La base ya incluye el WJP_ROL dentro de la carga bruta, 
            # así que el exponente fijo es suficiente para penalizar.
            c_h = base ** EXPONENTE
            
            resultado[pais][anio] = round(float(c_h), 4)
            
    with open('ch_calculado.json', 'w') as f:
        json.dump(resultado, f, indent=4)
    print("Éxito: Cálculo realizado con exponente fijo 1.85 (configuración estable).")

if __name__ == "__main__":
    calcular_ch()