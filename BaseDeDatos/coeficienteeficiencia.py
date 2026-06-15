# BaseDeDatos/Formulas/coeficienteeficiencia.py

def calcular_coeficiente_ineficiencia(datos_pais_anio):
    """
    Calcula el Coeficiente de Ineficiencia utilizando ETA_NORM.
    
    La fórmula integra la normalización del Área 1 del Fraser (Eta)
    para determinar la carga oculta.
    
    Args:
        datos_pais_anio (dict): Registro del almacén para un país y año específico.
        
    Returns:
        float: El valor del coeficiente de ineficiencia.
    """
    # Obtenemos ETA_NORM del registro (pre-calculado en el ensamblador)
    eta = datos_pais_anio.get('ETA_NORM', 0)
    
    # Aplicamos la fórmula de ineficiencia basada en tu modelo
    # (Eta + 2.5) / 5 garantiza que el resultado esté en escala [0, 1]
    c_ineficiencia = (eta + 2.5) / 5
    
    return c_ineficiencia