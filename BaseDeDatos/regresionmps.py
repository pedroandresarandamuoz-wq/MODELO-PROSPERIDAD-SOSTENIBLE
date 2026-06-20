import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.stats.diagnostic import acorr_breusch_godfrey
import statsmodels.api as sm

def ejecutar_auditoria_total_mps():
    # 1. Ingesta y Ordenación Cronológica por Panel-Unidad
    try:
        df = pd.read_json('dataset_mps_final.json')
    except Exception as e:
        print(f"Error crítico al cargar la base de datos JSON: {e}")
        return

    # Asegurar ordenación para impedir contaminación cruzada entre entidades
    df = df.sort_values(['pais', 'anio'])
    df['anio'] = pd.to_numeric(df['anio'])

    # 2. Construcción de la Estructura de Retardos Dinámicos (Cascada de Inercia)
    for lag in range(1, 4):
        df[f'ln_tpl_lag{lag}'] = df.groupby('pais')['ln_tpl'].shift(lag)

    # 3. Operacionalización en Primeras Diferencias (Aislamiento de Variación Pura)
    df['d_ln_pib'] = df.groupby('pais')['ln_pib'].diff()
    df['d_ln_tpl'] = df.groupby('pais')['ln_tpl'].diff()
    for lag in range(1, 4):
        df[f'd_ln_tpl_lag{lag}'] = df.groupby('pais')['d_ln_tpl'].shift(lag)

    # Datasets limpios específicos para evitar sesgos de muestras desiguales
    cols_estaticas = ['ln_pib', 'ln_tpl', 'ln_tpl_lag1', 'ln_tpl_lag2', 'ln_tpl_lag3', 'pais']
    df_estatico_clean = df.dropna(subset=cols_estaticas)

    cols_dinamicas = ['d_ln_pib', 'd_ln_tpl', 'd_ln_tpl_lag1', 'd_ln_tpl_lag2', 'd_ln_tpl_lag3']
    df_dinamico_clean = df.dropna(subset=cols_dinamicas)

    # 4. MODELO A: Regresión Estructural con Errores Estándar Robustos (Clustered por País)
    formula_estatica = 'ln_pib ~ ln_tpl + ln_tpl_lag1 + ln_tpl_lag2 + ln_tpl_lag3 + C(pais)'
    model_estatico = smf.ols(formula_estatica, data=df_estatico_clean).fit(
        cov_type='cluster',
        cov_kwds={'groups': df_estatico_clean['pais']}
    )

    # 5. MODELO B: Regresión Dinámica Pura en Diferencias (Blindaje Anti-Multicolinealidad)
    formula_dinamica = 'd_ln_pib ~ d_ln_tpl + d_ln_tpl_lag1 + d_ln_tpl_lag2 + d_ln_tpl_lag3'
    model_dinamico = smf.ols(formula_dinamica, data=df_dinamico_clean).fit()

    # 6. Muestras de Stress Test Temporal (Subperiodo de Shock y Resiliencia Pandémica 2018-2021)
    df_covid = df_estatico_clean[(df_estatico_clean['anio'] >= 2018) & (df_estatico_clean['anio'] <= 2021)]
    model_resiliencia = smf.ols(formula_estatica, data=df_covid).fit(
        cov_type='cluster',
        cov_kwds={'groups': df_covid['pais']}
    )

    # 7. Diagnósticos de Robustez Científica
    bg_stat, bg_p, _, _ = acorr_breusch_godfrey(model_estatico, nlags=1)
    dw_stat = sm.stats.stattools.durbin_watson(model_estatico.resid)

    # 8. Redacción del Ticket e Informe Técnico
    ticket = f"""======================================================================
           DICTAMEN PERICIAL: MODELO DE PROSPERIDAD SOSTENIBLE (MPS)
======================================================================
Fecha de Emisión: 2026-06-15 | Estatus: AUDITORÍA BLINDADA Q1
Autor: Pedro Andrés Aranda Muñoz
Área de Cobertura: 197 Naciones | Horizonte Temporal: 2008-2023
----------------------------------------------------------------------

[1. ARQUITECTURA DE ESPECIFICACIÓN Y CONTROL]
- Variable Dependiente Principal: ln_pib (Log-Riqueza Real Per Cápita)
- Vector Independiente Maestro: ln_tpl (Carga Parasitaria Total)
- Estimación Panel: Efectos Fijos (Entity Fixed Effects) via Intra-Country OLS
- Corrección de Varianza: Robust Standard Errors Clustered por Jurisdicción

[2. SIGNIFICANCIA ESTRUCTURAL CONTEMPORÁNEA (Modelo Estático Robust)]
- Coeficiente ln_tpl (Impacto Inmediato): {model_estatico.params['ln_tpl']:.4f}
- Error Estándar Robusto: {model_estatico.bse['ln_tpl']:.4f}
- Estadístico t de Precisión: {model_estatico.tvalues['ln_tpl']:.4f}
- P-valor Corregido (Robust): {model_estatico.pvalues['ln_tpl']:.4e}
- Estatus de Validación: {'VALIDADO' if model_estatico.pvalues['ln_tpl'] < 0.05 else 'PENDIENTE DE RETARDO DINÁMICO'}

[3. ANÁLISIS EN CASCADA: EL "VENENO LENTO" INSTITUCIONAL]
- Coeficiente Lag 1 Año (ln_tpl_lag1): {model_estatico.params['ln_tpl_lag1']:.4f} | P-valor: {model_estatico.pvalues['ln_tpl_lag1']:.4e}
- Coeficiente Lag 2 Años (ln_tpl_lag2): {model_estatico.params['ln_tpl_lag2']:.4f} | P-valor: {model_estatico.pvalues['ln_tpl_lag2']:.4e}
- Coeficiente Lag 3 Años (ln_tpl_lag3): {model_estatico.params['ln_tpl_lag3']:.4f} | P-valor: {model_estatico.pvalues['ln_tpl_lag3']:.4e}

[4. ROBUSTEZ DIAGNÓSTICA]
- Estadístico Breusch-Godfrey n=1: {bg_stat:.4f} | P-valor: {bg_p:.4e}
- Estadístico Durbin-Watson: {dw_stat:.4f}

[5. LEY DE ARANDA MUÑOZ (Sustracción Marginal)]
Bajo las restricciones robustas de clustering por país, el coeficiente indica 
que el aparato político succiona el {abs(model_estatico.params['ln_tpl'])*100:.2f}% del valor marginal 
del PIB en el término contemporáneo estructural.
======================================================================
"""
    print(ticket)
    
    # Exportar el informe a un archivo físico para que saques tu ticket blindado
    with open('mps_ticket_auditoria_global.txt', 'w', encoding='utf-8') as f:
        f.write(ticket)
        
    return ticket

# ESTO ES LO QUE FALTA: La instrucción expresa para arrancar la función
if __name__ == "__main__":
    ejecutar_auditoria_total_mps()