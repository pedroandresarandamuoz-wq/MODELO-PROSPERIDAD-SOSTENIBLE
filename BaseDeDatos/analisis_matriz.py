import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import json

def ejecutar_analisis():
    # 1. Cargar el dataset que ya tiene la ERI calculada (Diccionario anidado)
    with open('Base_Datos_MPS_Final_ERI.json', 'r') as f:
        data_eri = json.load(f)
    
    rows_eri = []
    for pais, anios in data_eri.items():
        for anio, val in anios.items():
            val['pais'] = pais
            val['anio'] = int(anio)
            rows_eri.append(val)
    df_eri = pd.DataFrame(rows_eri)

    # 2. Cargar el dataset final (Lista de objetos)
    df_mps = pd.read_json('dataset_mps_final.json')
    
    # 3. Fusión inteligente por 'pais' y 'anio'
    # Aseguramos que los tipos sean iguales
    df_mps['anio'] = df_mps['anio'].astype(int)
    df = pd.merge(df_eri, df_mps, on=['pais', 'anio'])
    
    # 4. Análisis: Clustering de Riesgo
    # Usamos ln_tpl (Carga) y eri (Eficiencia)
    df = df.dropna(subset=['ln_tpl', 'eri'])
    X = df[['ln_tpl', 'eri']]
    
    kmeans = KMeans(n_clusters=4, n_init=10).fit(X)
    df['cluster'] = kmeans.labels_
    
    # 5. Visualización de la Matriz de Posicionamiento
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df['ln_tpl'], df['eri'], c=df['cluster'], cmap='RdYlGn', alpha=0.6)
    plt.colorbar(scatter, label='Cuadrante de Riesgo')
    plt.xlabel('Carga Parasitaria (ln_tpl)')
    plt.ylabel('Eficiencia de Inversión (ERI)')
    plt.title('Matriz de Posicionamiento Estratégico MPS')
    plt.grid(True)
    
    plt.savefig('matriz_posicionamiento.png')
    df.to_json('MPS_Matriz_Final.json', orient='records')
    
    print("¡Análisis completado! Archivo 'MPS_Matriz_Final.json' guardado.")

if __name__ == "__main__":
    ejecutar_analisis()