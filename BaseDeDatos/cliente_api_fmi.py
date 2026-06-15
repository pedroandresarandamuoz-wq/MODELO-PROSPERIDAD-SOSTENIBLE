import sdmx

def conectar_y_descargar(dataset_id, key, anio):
    try:
        # El FMI en SDMX 3.0 prefiere el cliente con la fuente configurada para este formato
        imf = sdmx.Client('IMF_DATA')
        
        # Usamos el dataset GFS_SOO (que es el que has encontrado)
        # key ahora puede ser simplificada al formato SDMX 3.0
        data_msg = imf.data(
            resource_id=dataset_id, 
            key=key, 
            params={'startPeriod': str(anio), 'endPeriod': str(anio)}
        )
        return sdmx.to_pandas(data_msg)
    except Exception as e:
        print(f"DEBUG: Error en SDMX 3.0: {e}")
        return None