import math
from BaseDeDatos import coeficientesch as ch
from BaseDeDatos import coeficienteeficiencia as ef

def calcular_mps_final(datos):
    # 1. Obtener coeficientes
    coeffs = ch.calcular_todos_los_coeficientes(datos)
    c_ineficiencia = ef.calcular_coeficiente_ineficiencia(datos)
    
    # 2. Carga Oculta (Manejo de signo para evitar error matemático)
    promedio_oculta = (coeffs["C_INTEGRIDAD"] + coeffs["C_JURIDICO"] + 
                       coeffs["C_REGULACION"] + coeffs["C_SOE"] + coeffs["C_FISCAL"]) / 5
    
    wjp = datos.get('WJP_ROL', 0)
    exponente = (1.85 - wjp)
    
    # Aplicamos la potencia conservando el signo del promedio_oculta
    if promedio_oculta < 0:
        carga_oculta = -1 * math.pow(abs(promedio_oculta), exponente)
    else:
        carga_oculta = math.pow(promedio_oculta, exponente)
    
    # 3. Carga Parasitaria Total
    g_cons = datos.get('FRASER_FISCAL', 0)
    g_trans = datos.get('FRASER_SOE', 0)
    
    # Manejo de la raíz: si g_trans es negativo, lo tratamos como 0 para la raíz
    # (asumiendo que una raíz de un negativo destruiría la lógica del modelo)
    val_trans = max(0, g_trans)
    
    carga_parasitaria = (g_cons * (2 - c_ineficiencia)) + math.sqrt(val_trans) + carga_oculta
    
    # 4. Prosperidad Neta
    prosperidad_neta = 100 - (carga_parasitaria * 1.18)
    
    return {
        "CARGA_OCULTA": round(carga_oculta, 2),
        "CARGA_PARASITARIA": round(carga_parasitaria, 2),
        "PROSPERIDAD_NETA": round(prosperidad_neta, 2)
    }