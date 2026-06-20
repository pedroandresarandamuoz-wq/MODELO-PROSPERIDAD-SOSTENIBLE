import json

def generar_dataset_eri(fichero_mps, fichero_ch, archivo_salida):
    # 1. Cargar los dos archivos de datos
    with open(fichero_mps, 'r', encoding='utf-8') as f:
        data_mps = json.load(f)
    with open(fichero_ch, 'r', encoding='utf-8') as f:
        data_ch = json.load(f)
    
    nuevo_dataset = {}

    # 2. Procesar el cruce de datos
    for pais, anios in data_mps.items():
        if pais not in nuevo_dataset:
            nuevo_dataset[pais] = {}
            
        for anio, valores in anios.items():
            inversion = valores.get('inversion', 0)
            
            # Obtener el CH del segundo fichero (teniendo en cuenta posibles errores de formato)
            ch_val = data_ch.get(pais, {}).get(anio, 0)
            
            # Calcular ERI: Inversión / CH
            # Controlamos la división por cero
            eri = (inversion / ch_val) if ch_val and ch_val != 0 else 0
            
            # Guardar estructura completa con el nuevo valor
            nuevo_dataset[pais][anio] = {
                "estructura": valores.get('estructura'),
                "transferencias": valores.get('transferencias'),
                "inversion": inversion,
                "ch": ch_val,
                "eri": round(eri, 4)
            }
    
    # 3. Guardar el nuevo fichero
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(nuevo_dataset, f, indent=4)
    
    print(f"Éxito: '{archivo_salida}' generado con la variable ERI (Inversión/CH).")

if __name__ == "__main__":
    # Asegúrate de tener los dos ficheros en la misma carpeta
    generar_dataset_eri('Base_Datos_MPS_Definitiva.json', 
                        'ch_calculado.json', 
                        'Base_Datos_MPS_Final_ERI.json')