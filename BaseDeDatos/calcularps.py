import json

def calcular_ps(pn_json, se_json, output_filename):
    # Cargar los datos
    # PN tiene estructura: {"PAIS": {"AÑO": valor_PN}}
    with open(pn_json, 'r', encoding='utf-8') as f:
        pn_data = json.load(f)
    
    # S_E tiene estructura: {"PAIS": {"AÑO": {"s_e_pct_pib": valor, ...}}}
    with open(se_json, 'r', encoding='utf-8') as f:
        se_data = json.load(f)

    ps_final = {}

    # Iterar sobre los países del archivo PN
    for pais, años in pn_data.items():
        if pais not in ps_final:
            ps_final[pais] = {}
        
        for año, pn_valor in años.items():
            # Buscar el valor correspondiente en S_E
            try:
                se_valor = se_data[pais][año]['s_e_pct_pib']
                
                # Calcular PS = PN + S_E
                ps_valor = pn_valor + se_valor
                
                # Guardar resultado
                ps_final[pais][año] = ps_valor
            except KeyError:
                # Si el país o año no existen en S_E, saltamos este registro
                continue

    # Guardar en PS.json
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(ps_final, f, indent=4, ensure_ascii=False)
    
    print(f"Archivo '{output_filename}' generado correctamente.")

# Ejecutar el cálculo
# Asegúrate de que los nombres de los archivos coincidan exactamente
if __name__ == "__main__":
    calcular_ps('PN.json', 'S_E.json', 'PS.json')