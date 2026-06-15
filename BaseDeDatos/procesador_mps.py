import pandas as pd
import numpy as np
import json
import statsmodels.formula.api as smf
import os

def procesar_mps_final():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_pib = os.path.join(base_dir, 'pib_ppa_2008_2023.json')
    path_tpl = os.path.join(base_dir, 'TPL_calculado.json')

    # 1. Carga y Estructuración
    with open(path_pib, 'r', encoding='utf-8') as f:
        data_pib = json.load(f)
    with open(path_tpl, 'r', encoding='utf-8') as f:
        data_tpl = json.load(f)

    # Convertir JSONs a formato largo
    df_pib = pd.DataFrame(data_pib).stack().reset_index().rename(columns={'level_0': 'anio', 'level_1': 'pais', 0: 'pib_ppa'})
    df_tpl = pd.DataFrame(data_tpl).stack().reset_index().rename(columns={'level_0': 'anio', 'level_1': 'pais', 0: 'tpl'})
    
    df = pd.merge(df_pib, df_tpl, on=['anio', 'pais'], how='inner')

    # 2. Limpieza robusta y manejo de ceros
    eps = 1e-9
    df['pib_ppa'] = df['pib_ppa'].clip(lower=eps)
    df['tpl'] = df['tpl'].clip(lower=eps)

    # Transformación Logarítmica
    df['ln_pib'] = np.log(df['pib_ppa'])
    df['ln_tpl'] = np.log(df['tpl'])

    # 3. FILTRADO DE NOISE (Eliminar extremos para limpiar la regresión)
    # Quitamos el 1% más alto y más bajo para que los outliers no descuadren el modelo
    low, high = df['tpl'].quantile([0.01, 0.99])
    df = df[(df['tpl'] >= low) & (df['tpl'] <= high)]

    # 4. ESTANDARIZACIÓN (Z-Score): Planchar la escala para que sean comparables
    df['ln_pib_std'] = (df['ln_pib'] - df['ln_pib'].mean()) / df['ln_pib'].std()
    df['ln_tpl_std'] = (df['ln_tpl'] - df['ln_tpl'].mean()) / df['ln_tpl'].std()

    print("--- DIAGNÓSTICO DEL MODELO ESTANDARIZADO ---")
    print(f"Registros procesados (tras limpieza): {len(df)}")
    
    # 

    # 5. REGRESIÓN ESTRUCTURAL (Ahora sobre datos estandarizados)
    # Esta regresión es mucho más estable y menos sensible a errores de escala
    model = smf.ols('ln_pib_std ~ ln_tpl_std + C(pais)', data=df).fit()
    
    print("\n--- RESULTADOS DEL MODELO ESTRUCTURAL (Efectos Fijos) ---")
    print(model.summary().tables[1]) # Imprime los coeficientes clave
    print(f"\nR-cuadrado: {model.rsquared:.4f}")

    # Guardar para tu archivo histórico
    df.to_json(os.path.join(base_dir, 'dataset_mps_final.json'), orient='records', indent=4)
    print("\nProceso finalizado. Dataset 'dataset_mps_final.json' guardado.")

if __name__ == "__main__":
    procesar_mps_final()