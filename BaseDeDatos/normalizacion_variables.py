import pandas as pd
import json

def unificar_fuentes():
    # 1. Cargar datasets
    with open('Pizarra_MPS_Master.json', 'r') as f:
        master = json.load(f)
    with open('dataset_normalizado_mps.json', 'r') as f:
        # Si es una lista de objetos
        raw_list = json.load(f)
        pib_df = pd.DataFrame(raw_list)

    # 2. Convertir el 'Master' a un DataFrame plano
    records = []
    for pais, anios in master.items():
        for anio, vars in anios.items():
            reg = {'pais': pais, 'anio': int(anio)}
            reg.update(vars)
            records.append(reg)
    master_df = pd.DataFrame(records)

    # 3. Asegurar que las llaves de unión sean idénticas
    pib_df['anio'] = pib_df['anio'].astype(int)
    
    # 4. Unir (Merge)
    # Unimos por 'pais' y 'anio'
    final_df = pd.merge(master_df, pib_df, on=['pais', 'anio'], how='inner')

    # 5. Normalización sobre el PIB real (usamos pib_ppa como base)
    # Calculamos el PIB absoluto estimado a partir de ln_pib o pib_ppa
    # Usaremos pib_ppa si está disponible, es más preciso
    pib_base = final_df['pib_ppa']
    
    final_df['PN_relativa'] = (final_df['PN'] / pib_base) * 100
    final_df['estructura_pct'] = (final_df['estructura'] / pib_base) * 100
    final_df['TPL_pct'] = (final_df['TPL'] / pib_base) * 100
    final_df['CH_pct'] = (final_df['carga_oculta'] / pib_base) * 100

    # 6. Guardar JSON final estructurado
    final_dict = {}
    for _, row in final_df.iterrows():
        p = row['pais']
        a = str(row['anio'])
        if p not in final_dict: final_dict[p] = {}
        final_dict[p][a] = row.drop(['pais', 'anio']).to_dict()

    with open('MPS_Normalizado.json', 'w') as f:
        json.dump(final_dict, f, indent=4)
        
    print(f"Éxito: Se han unificado {len(final_df)} registros en 'MPS_Normalizado.json'.")

if __name__ == "__main__":
    unificar_fuentes()