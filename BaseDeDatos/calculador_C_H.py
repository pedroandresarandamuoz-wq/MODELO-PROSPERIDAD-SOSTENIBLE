# -*- coding: utf-8 -*-
"""
Módulo de Cálculo de Carga Oculta (C_H) - Modelo de Propiedad Sostenible (MPS)
Desarrollado para: Pedro Andrés Aranda Muñoz
Motto: Pan, Patria y Justicia

Este script calcula la Carga Oculta de forma exponencial pura, sin límites
artificiales, asegurando que la inseguridad jurídica actúe como un catalizador
geométrico de la ineficiencia estatal para maximizar el R2 en las regresiones.
"""

import json
import os

def obtener_carga_oculta_exponencial_pura(datos):
    """
    FÓRMULA MAESTRA EXPONENCIAL DEL MPS (Pedro Andrés Aranda Muñoz).
    Calcula la Carga Oculta (C_H) permitiendo que la corrupción y la falta de ley
    ejerzan un castigo exponencial puro sobre la base del modelo.
    
    Parámetros:
    -----------
    datos : dict
        Diccionario con las puntuaciones de los indicadores (escala 0-10).
        
    Retorno:
    --------
    float : Valor de la Carga Oculta (C_H) con crecimiento exponencial.
    """
    # 1. Coeficientes individuales de fricción (escala 0-100, donde 100 es peor)
    # Transforma la libertad/eficiencia oficial en fricción y coste real
    c_integridad = (10 - datos.get('IIJ', 0)) * 10
    c_juridico   = (10 - datos.get('WJP_ROL', 0)) * 10 
    c_regulacion = (10 - datos.get('FRASER_REG', 0)) * 10
    c_soe        = (10 - datos.get('FRASER_SOE', 0)) * 10
    c_fiscal     = (10 - datos.get('FRASER_FISCAL', 0)) * 10

    # 2. Carga Bruta (Suma de ineficiencias, escala original de 0 a 500)
    carga_bruta = c_integridad + c_juridico + c_regulacion + c_soe + c_fiscal

    # 3. Base de cálculo original de Pedro (escala de 0 a 50)
    base = carga_bruta / 10.0

    # 4. Exponente Dinámico basado en la Calidad de la Justicia (WJP_ROL)
    # Convertimos WJP_ROL (0-10) a escala probabilística (0-1) sólo para el exponente
    wjp_prob = datos.get('WJP_ROL', 0) / 10.0

    # Exponente: 1.85 - wjp_prob (rango: 0.85 a 1.85)
    # - Si la justicia es nula (WJP=0): exponente = 1.85 (Aceleración exponencial máxima)
    # - Si la justicia es excelente (WJP=10): exponente = 0.85 (Amortiguación del daño)
    exponente = 1.85 - wjp_prob

    # 5. Cálculo Exponencial Puro (Sin limitaciones ni compresores de varianza)
    # Si base es 50 (peor caso) y exponente es 1.85, c_h alcanza un valor de ~1411.8
    # Si base es 50 (peor caso) pero con justicia excelente (exponente 0.85), c_h cae a ~27.8
    c_h = base ** exponente

    return c_h


def calcular_ch():
    """
    Función principal que ejecuta el procesamiento por lotes para todos
    los países y periodos históricos de la base de datos central.
    """
    ruta_datos = 'almacen_datos_maestro.json'
    ruta_salida = 'ch_calculado.json'
    
    # Verificación de seguridad de existencia de archivos
    if not os.path.exists(ruta_datos):
        print(f"Error de ejecución: No se ha encontrado el archivo {ruta_datos} en el directorio actual.")
        return

    print("Iniciando lectura de 'almacen_datos_maestro.json'...")
    with open(ruta_datos, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    resultado = {}
    
    # Procesamiento forense de series temporales
    for pais, periodos in datos.items():
        resultado[pais] = {}
        for anio, indicadores in periodos.items():
            # Aplicamos la fórmula exponencial real sin capar
            c_h_calculada = obtener_carga_oculta_exponencial_pura(indicadores)
            
            # Almacenamos el resultado redondeando a 4 decimales para las regresiones
            resultado[pais][anio] = round(float(c_h_calculada), 4)
            
    # Escritura de los resultados definitivos
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)
        
    print("=" * 80)
    print("PROCESAMIENTO DE INGENIERÍA INVERSA COMPLETADO CON ÉXITO")
    print("=" * 80)
    print("-> Lógica: Exponente Dinámico No Lineal Puro [1.85 - (WJP_ROL / 10)]")
    print("-> Base de cálculo: Carga Bruta / 10 (Escala 0 a 50)")
    print("-> Se ha eliminado el compresor lineal para restaurar la varianza original.")
    print(f"-> Base de datos guardada correctamente en: '{ruta_salida}'")
    print("=" * 80)


if __name__ == "__main__":
    calcular_ch()