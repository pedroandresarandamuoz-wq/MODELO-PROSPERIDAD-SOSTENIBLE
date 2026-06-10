import pandas as pd
import numpy as np
import json
import statsmodels.formula.api as smf
from statsmodels.stats.stattools import durbin_watson
import os

def generar_test_stress():
    # 1. Cargar el dataset
    archivo_input = 'dataset_normalizado_mps.json'
    with open(archivo_input, 'r') as f:
        df = pd.DataFrame(json.load(f))
    
    # 2. Calcular variables necesarias que faltan en el JSON
    df = df.sort_values(['pais', 'anio'])
    
    # Calculamos d_ln_pib y d_ln_tpl aquí mismo para que existan
    df['d_ln_pib'] = df.groupby('pais')['ln_pib'].diff()
    df['d_ln_tpl'] = df.groupby('pais')['ln_tpl'].diff()
    
    # Creamos las variables de asimetría
    df['up'] = df['d_ln_tpl'].apply(lambda x: x if x > 0 else 0)
    df['down'] = df['d_ln_tpl'].apply(lambda x: abs(x) if x < 0 else 0)
    
    # Limpiamos NaNs generados por los diff()
    df_clean = df.dropna(subset=['d_ln_pib', 'd_ln_tpl', 'ln_pib', 'ln_tpl'])

    output_lines = ["--- INFORME DE STRESS TEST ECONOMÉTRICO: MODELO MPS ---", ""]
    
    # 3. OLS Global
    m1 = smf.ols('ln_pib ~ ln_tpl', data=df_clean).fit()
    output_lines.append("[TEST 1: OLS GLOBAL]")
    output_lines.append(str(m1.summary().tables[1]))

    # 4. Efectos Fijos
    m2 = smf.ols('ln_pib ~ ln_tpl + C(pais)', data=df_clean).fit()
    output_lines.append("\n[TEST 2: PANEL EFECTOS FIJOS (Entities)]")
    output_lines.append(f"R-squared: {m2.rsquared:.4f}")
    
    # 5. Dinámica (Lags)
    df_clean['ln_tpl_lag1'] = df_clean.groupby('pais')['ln_tpl'].shift(1)
    m3 = smf.ols('ln_pib ~ ln_tpl + ln_tpl_lag1', data=df_clean.dropna()).fit()
    output_lines.append("\n[TEST 3: DINÁMICA Y REZAGOS]")
    output_lines.append(str(m3.summary().tables[1]))

    # 6. Asimetría
    m4 = smf.ols('d_ln_pib ~ up + down', data=df_clean).fit()
    output_lines.append("\n[TEST 4: ASIMETRÍA ESTRUCTURAL (Daño vs Recuperación)]")
    output_lines.append(str(m4.summary().tables[1]))

    # 7. Durbin-Watson
    dw = durbin_watson(m1.resid)
    output_lines.append(f"\n[TEST 5: DURBIN-WATSON]: {dw:.4f}")

    # Guardar archivo .txt
    with open('resultado_stress_test_mps.txt', 'w') as f:
        f.write("\n".join(output_lines))
    
    print("--- ESTUDIO COMPLETADO ---")
    print("Archivo 'resultado_stress_test_mps.txt' generado con éxito.")

if __name__ == "__main__":
    generar_test_stress()