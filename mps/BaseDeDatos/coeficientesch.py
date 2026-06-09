# BaseDeDatos/Formulas/coeficientesch.py

def calcular_todos_los_coeficientes(datos):
    c_integridad = (10 - datos.get('IIJ', 0)) * 10
    c_juridico = (10 - datos.get('WJP_ROL', 0)) * 10 
    c_regulacion = (10 - datos.get('FRASER_REG', 0)) * 10
    c_soe = (10 - datos.get('FRASER_SOE', 0)) * 10
    c_fiscal = (10 - datos.get('FRASER_FISCAL', 0)) * 10
    
    return {
        "C_INTEGRIDAD": c_integridad,
        "C_JURIDICO": c_juridico,
        "C_REGULACION": c_regulacion,
        "C_SOE": c_soe,
        "C_FISCAL": c_fiscal
    }

def obtener_carga_oculta_final(coeficientes):
    # Suma acumulativa para que el daño sea proporcional a la suma de ineficiencias
    return (
        coeficientes["C_INTEGRIDAD"] + 
        coeficientes["C_JURIDICO"] + 
        coeficientes["C_REGULACION"] + 
        coeficientes["C_SOE"] + 
        coeficientes["C_FISCAL"]
    )