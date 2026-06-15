import json

def calcular_prosperidad_neta():
    # 1. Cargamos el archivo TPL_calculado.json
    try:
        with open('TPL_calculado.json', 'r') as f:
            tpl_data = json.load(f)
    except FileNotFoundError:
        print("Error: No encuentro 'TPL_calculado.json'. Asegúrate de ejecutar el ensamblador primero.")
        return

    pn_resultados = {}

    # 2. Aplicamos la fórmula: PN = 100 - (TPL * 1.18)
    for pais, anios_data in tpl_data.items():
        pn_resultados[pais] = {}
        
        for anio, tpl in anios_data.items():
            if tpl is not None:
                # Aplicamos la fórmula de Prosperidad Neta
                pn = 100 - (tpl * 1.18)
                pn_resultados[pais][anio] = round(float(pn), 4)
            else:
                pn_resultados[pais][anio] = None

    # 3. Guardar el archivo resultante
    with open('PN.json', 'w') as f:
        json.dump(pn_resultados, f, indent=4)
    
    print("Éxito: PN.json generado. La Prosperidad Neta ya está calculada.")

if __name__ == "__main__":
    calcular_prosperidad_neta()