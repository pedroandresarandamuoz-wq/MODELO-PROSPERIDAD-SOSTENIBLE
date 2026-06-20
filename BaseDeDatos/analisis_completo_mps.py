import pandas as pd
import json
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

def ejecutar_analisis_completo():
    # 1. Carga y Preparación Única
    try:
        with open('dataset_normalizado_mps.json', 'r') as f:
            df = pd.DataFrame(json.load(f))
    except Exception as e:
        print(f"Error cargando archivo: {e}")
        return

    # Limpieza necesaria para todos los modelos
    df['anio'] = pd.to_numeric(df['anio'])
    df['ln_pib'] = pd.to_numeric(df['ln_pib'])
    df['ln_tpl'] = pd.to_numeric(df['ln_tpl'])
    df = df.dropna(subset=['ln_pib', 'ln_tpl', 'anio'])

    print("="*60)
    print("INFORME MAESTRO: MPS - MODELO DE PROSPERIDAD SOSTENIBLE")
    print("="*60)

    # --- MODELO 1: Global (La "Foto" de la Ley) ---
    y = df['ln_pib']
    X = sm.add_constant(df['ln_tpl'])
    modelo_ols = sm.OLS(y, X).fit()
    print("\n[1] TEST GLOBAL (OLS):")
    print(f"Coeficiente TPL: {modelo_ols.params['ln_tpl']:.4f} (R2: {modelo_ols.rsquared:.4f})")

    # --- MODELO 2: Efectos Fijos (El Aislamiento) ---
    df_panel = df.set_index(['pais', 'anio'])
    formula = 'ln_pib ~ 1 + ln_tpl + EntityEffects'
    modelo_fe = PanelOLS.from_formula(formula, data=df_panel).fit(cov_type='clustered', cluster_entity=True)
    print("\n[2] TEST EFECTOS FIJOS (Aislamiento por País):")
    print(f"Coeficiente TPL: {modelo_fe.params['ln_tpl']:.4f} (P-value: {modelo_fe.pvalues['ln_tpl']:.4f})")

    # --- MODELO 3: Dinámico (El Freno Mecánico) ---
    df = df.sort_values(['pais', 'anio'])
    df['d_ln_pib'] = df.groupby('pais')['ln_pib'].diff()
    df['d_ln_tpl'] = df.groupby('pais')['ln_tpl'].diff()
    df_dinamico = df.dropna(subset=['d_ln_pib', 'd_ln_tpl'])
    y_d = df_dinamico['d_ln_pib']
    X_d = sm.add_constant(df_dinamico['d_ln_tpl'])
    modelo_din = sm.OLS(y_d, X_d).fit()
    print("\n[3] TEST DINÁMICO (Variación Anual):")
    print(f"Coeficiente Delta TPL: {modelo_din.params['d_ln_tpl']:.4f} (R2: {modelo_din.rsquared:.4f})")
    
    print("\n" + "="*60)
    print("ANÁLISIS COMPLETADO. Todo está bajo control.")

if __name__ == "__main__":
    ejecutar_analisis_completo()