import json
import os

def generar_pizarra_mps():
    # Lista de los archivos que necesitamos
    archivos = {
        "bd_mps": "Base_Datos_MPS_Definitiva.json",
        "ch_data": "ch_calculado.json",
        "tpl_data": "TPL_calculado.json",
        "pn_data": "PN.json"
    }

    datos = {}
    
    # Intentamos abrir cada archivo
    for nombre, ruta in archivos.items():
        if not os.path.exists(ruta):
            print(f"ERROR: No encuentro el archivo: {ruta}")
            return
        with open(ruta, 'r', encoding='utf-8') as f:
            datos[nombre] = json.load(f)

    dashboard_master = {}
    
    # Consolidación
    bd_mps = datos["bd_mps"]
    ch_data = datos["ch_data"]
    tpl_data = datos["tpl_data"]
    pn_data = datos["pn_data"]

    for pais in bd_mps:
        dashboard_master[pais] = {}
        for anio in bd_mps[pais]:
            dashboard_master[pais][anio] = {
                "estructura": bd_mps[pais][anio].get("estructura", 0),
                "transferencias": bd_mps[pais][anio].get("transferencias", 0),
                "carga_oculta": ch_data.get(pais, {}).get(anio, 0),
                "TPL": tpl_data.get(pais, {}).get(anio, 0),
                "PN": pn_data.get(pais, {}).get(anio, 0)
            }

    with open('Pizarra_MPS_Master.json', 'w', encoding='utf-8') as f:
        json.dump(dashboard_master, f, indent=4)
    
    print("¡Éxito! Archivo 'Pizarra_MPS_Master.json' generado correctamente.")

if __name__ == "__main__":
    generar_pizarra_mps()