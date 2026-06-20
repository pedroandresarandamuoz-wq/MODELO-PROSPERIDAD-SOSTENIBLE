# BaseDeDatos/MetaDatos/columnas.py

# Estructuramos por grupos para facilitar el filtrado en el Frontend
METADATOS_MPS = {
    "MACRO": {
        "FRASER_FISCAL": {"label": "Gasto Fiscal", "tipo": "numeric", "fuente": "Fraser"},
        "FRASER_SOE": {"label": "SOE (Empresas Estatales)", "tipo": "numeric", "fuente": "Fraser"},
    },
    "INSTITUCIONAL": {
        "WJP_ROL": {"label": "Estado de Derecho (WJP)", "tipo": "numeric", "fuente": "WJP"},
        "IIJ": {"label": "Integridad Institucional", "tipo": "numeric", "fuente": "Cálculo"},
        "FRASER_REG": {"label": "Calidad Regulatoria", "tipo": "numeric", "fuente": "Fraser"},
    },
    "MPS_RESULTADOS": {
        "PROSPERIDAD_NETA": {"label": "Prosperidad Neta", "tipo": "metric", "fuente": "MPS"},
        "CARGA_OCULTA": {"label": "Carga Oculta", "tipo": "metric", "fuente": "MPS"},
        "CARGA_PARASITARIA": {"label": "Carga Parasitaria Total", "tipo": "metric", "fuente": "MPS"},
        "ETA_NORM": {"label": "Eta (Factor de Eficiencia)", "tipo": "numeric", "fuente": "MPS"},
    }
}

def obtener_etiqueta(codigo):
    """Devuelve el label legible para gráficos usando el código técnico."""
    for categoria in METADATOS_MPS.values():
        if codigo in categoria:
            return categoria[codigo]["label"]
    return codigo # Si no lo encuentra, devuelve el código tal cual

def obtener_columnas_por_categoria(categoria):
    """Útil para el frontend: devuelve solo las columnas de un grupo específico."""
    return METADATOS_MPS.get(categoria, {})

def obtener_todo():
    """Carcasa completa para la zona de Pages."""
    return METADATOS_MPS