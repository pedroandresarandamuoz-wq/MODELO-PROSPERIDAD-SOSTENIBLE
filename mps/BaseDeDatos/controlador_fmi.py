import json

def generar_pizarra_mps():
    # 1. Cargamos todos los ficheros de datos
    # Asegúrate de que todos estén en la misma carpeta BaseDeDatos
    try:
        with open('Base_Datos_MPS_Definitiva.json', 'r') as f: bd_mps = json.load(f)
        with open('ch_calculado.json', 'r') as f: ch_data = json.load(f)
        with open('TPL_calculado.json', 'r') as f: tpl_data = json.load(f)
        with open('PN.json', 'r') as f: pn_data = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: No se encuentra un archivo necesario: {e}")
        return

    dashboard_master = {}

    # 2. Consolidación jerárquica: Pais -> Anio -> Variables
    # Usamos las llaves de bd_mps como base (paises)
    for pais in bd_mps:
        dashboard_master[pais] = {}
        for anio in bd_mps[pais]:
            # Construimos el objeto con el orden exacto de tu modelo
            dashboard_master[pais][anio] = {
                "estructura": bd_mps[pais][anio].get("estructura", 0),
                "transferencias": bd_mps[pais][anio].get("transferencias", 0),
                "carga_oculta": ch_data.get(pais, {}).get(anio, 0),
                "TPL": tpl_data.get(pais, {}).get(anio, 0),
                "PN": pn_data.get(pais, {}).get(anio, 0)
            }

    # 3. Guardado del Dashboard maestro
    with open('Pizarra_MPS_Master.json', 'w') as f:
        json.dump(dashboard_master, f, indent=4)
    
    print("Éxito: Pizarra_MPS_Master.json generado correctamente.")

if __name__ == "__main__":
    generar_pizarra_mps()