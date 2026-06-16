import json
import os

def generar_pizarra_mps():
    # Detecta dónde está el script (BaseDeDatos)
    dir_script = os.path.dirname(os.path.abspath(__file__))
    
    # Define las rutas absolutas
    archivos = {
        "bd_mps": os.path.join(dir_script, "Base_Datos_MPS_Definitiva.json"),
        "ch_data": os.path.join(dir_script, "ch_calculado.json"),
        "tpl_data": os.path.join(dir_script, "TPL_calculado.json"),
        "pn_data": os.path.join(dir_script, "PN.json")
    }

    datos = {}
    
    # Intentamos abrir cada archivo
    for nombre, ruta in archivos.items():
        if not os.path.exists(ruta):
            print(f"ERROR: No encuentro el archivo en: {ruta}")
            return
        with open(ruta, 'r', encoding='utf-8') as f:
            datos[nombre] = json.load(f)

    # Consolidación
    bd_mps = datos["bd_mps"]
    ch_data = datos["ch_data"]
    tpl_data = datos["tpl_data"]
    pn_data = datos["pn_data"]

    dashboard_master = {}

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

    ruta_salida = os.path.join(dir_script, 'Pizarra_MPS_Master.json')
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(dashboard_master, f, indent=4)
    
    print(f"¡Éxito! Archivo creado en: {ruta_salida}")

if __name__ == "__main__":
    generar_pizarra_mps()