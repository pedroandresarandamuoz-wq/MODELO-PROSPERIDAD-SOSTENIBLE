import re

# Al estar ya en la carpeta BaseDeDatos, buscamos el archivo directamente por su nombre
archivo_entrada = 'Base_Datos_MPS.json' 
archivo_salida = 'Base_Datos_MPS_Limpia.json'

with open(archivo_entrada, 'r', encoding='utf-8') as f:
    texto = f.read()

bloques = re.findall(r'"([A-Z]{3})":\s*({.*?})', texto, re.DOTALL)

if not bloques:
    print("No se encontraron países. Asegúrate de que el archivo se llame exactamente 'Base_Datos_MPS.json'")
else:
    resultado = ["{"]
    for i, (codigo, contenido) in enumerate(bloques):
        # Limpiar decimales a 3 posiciones
        contenido_limpio = re.sub(r'(\d+\.\d{3})\d+', r'\1', contenido)
        
        coma = "," if i < len(bloques) - 1 else ""
        resultado.append(f'  "{codigo}": {contenido_limpio}{coma}')
    
    resultado.append("}")

    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write("\n".join(resultado))

    print(f"Éxito: Procesados {len(bloques)} países en '{archivo_salida}'.")