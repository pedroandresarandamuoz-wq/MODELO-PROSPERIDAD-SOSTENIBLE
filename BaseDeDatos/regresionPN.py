import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.stats.diagnostic import acorr_breusch_godfrey

def ejecutar_auditoria_total():
    # 1. Carga y preparación
    df = pd.read_json('dataset_mps_final.json')
    df = df.sort_values(['pais', 'anio'])

    # 2. Cálculo de variaciones (Delta) para análisis dinámico
    df['d_ln_pib'] = df.groupby('pais')['ln_pib'].diff()
    df['d_ln_tpl'] = df.groupby('pais')['ln_tpl'].diff()
    df_dinamico = df.dropna(subset=['d_ln_pib', 'd_ln_tpl'])

    # 3. Regresión Estructural con Efectos Fijos y Errores Robustos (Clusterizados)
    formula = 'ln_pib ~ ln_tpl + C(pais)'
    modelo_robust = smf.ols(formula, data=df).fit(
        cov_type='cluster', 
        cov_kwds={'groups': df['pais']}
    )

    # 4. Breusch-Godfrey para verificar independencia de residuos
    bg_test = acorr_breusch_godfrey(modelo_robust, nlags=1)

    # 5. Generación del Ticket Completo
    ticket = f"""
============================================================
           INFORME TÉCNICO: MODELO DE PROSPERIDAD (MPS)
============================================================
Fecha: 2026-06-14 | Estatus: AUDITORÍA BLINDADA Y TOTAL
Autor: Pedro Andrés Aranda Muñoz
------------------------------------------------------------

[1. ESTRUCTURA DEL MODELO]
Variable Dependiente: ln_pib
Variable Independiente: ln_tpl
Control: Efectos Fijos por País (Clusterizado)
R-Cuadrado: {modelo_robust.rsquared:.4f}

[2. SIGNIFICANCIA ESTRUCTURAL]
Coeficiente TPL: {modelo_robust.params['ln_tpl']:.4f}
P-valor (Robust): {modelo_robust.pvalues['ln_tpl']:.4e}
Resultado: {'VALIDADO' if modelo_robust.pvalues['ln_tpl'] < 0.05 else 'NO VALIDADO'}

[3. ANÁLISIS DINÁMICO (Variación Anual)]
Coeficiente Delta (d_ln_tpl): {smf.ols('d_ln_pib ~ d_ln_tpl', data=df_dinamico).fit().params['d_ln_tpl']:.4f}
P-valor (Dinámico): {smf.ols('d_ln_pib ~ d_ln_tpl', data=df_dinamico).fit().pvalues['d_ln_tpl']:.4e}

[4. AUTOCORRELACIÓN (Breusch-Godfrey)]
P-valor: {bg_test[1]:.4e}
Interpretación: {'Independencia observada' if bg_test[1] > 0.05 else 'Persistencia detectada'}

[5. LEY DE ARANDA MUÑOZ]
El Estado succiona el {abs(modelo_robust.params['ln_tpl'])*100:.2f}% del valor marginal del PIB.
============================================================
    """
    
    # 6. Guardado de archivos
    with open('mps_ticket_final.txt', 'w', encoding='utf-8') as f:
        f.write(ticket)
        f.write("\n\n--- DETALLE DE EFECTOS POR PAÍS ---\n")
        f.write(modelo_robust.summary().as_text())
    
    print(ticket)
    print("\nTicket completo guardado en 'mps_ticket_final.txt'.")

if __name__ == "__main__":
    ejecutar_auditoria_total()