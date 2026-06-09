import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="MPS - Pan, Patria y Justicia", layout="wide")
st.title("Modelo de Prosperidad Sostenible (MPS)")
st.subheader("Investigación de indicadores macroeconómicos y parasitismo institucional")

# 2. Carga de datos
@st.cache_data
def load_data():
    ruta_json = os.path.join('BaseDeDatos', 'Pizarra_MPS_Master.json')
    if not os.path.exists(ruta_json):
        st.error(f"No se encuentra el archivo en: {ruta_json}")
        return pd.DataFrame()
    with open(ruta_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    flat_data = []
    for pais, anios in data.items():
        for anio, vars in anios.items():
            row = vars.copy()
            row['pais'] = pais
            row['anio'] = int(anio)
            flat_data.append(row)
    return pd.DataFrame(flat_data)

df = load_data()

if not df.empty:
    menu = ["Histórico Global", "Análisis por País", "Gráfica de Dispersión"]
    choice = st.sidebar.selectbox("Selecciona la Vista", menu)

    if choice == "Histórico Global":
        st.header("Tabla Dinámica por Año")
        anio_tabla = st.selectbox("Selecciona el año:", sorted(df['anio'].unique(), reverse=True))
        df_filtrado = df[df['anio'] == anio_tabla].sort_values(by='TPL')
        st.dataframe(df_filtrado, use_container_width=True)

    elif choice == "Análisis por País":
        st.header("Dossier de País")
        pais_sel = st.selectbox("Selecciona un país", sorted(df['pais'].unique()))
        datos_pais = df[df['pais'] == pais_sel].sort_values('anio')
        fig_indiv = px.line(datos_pais, x="anio", y=["TPL", "PN", "estructura", "carga_oculta"], 
                            title=f"Evolución MPS: {pais_sel}", markers=True)
        st.plotly_chart(fig_indiv, use_container_width=True)
        st.table(datos_pais.set_index('anio'))

    elif choice == "Gráfica de Dispersión":
        st.header("Análisis de Tendencias (Puntos)")
        anio_disp = st.selectbox("Selecciona el año para la dispersión:", sorted(df['anio'].unique(), reverse=True))
        df_anio = df[df['anio'] == anio_disp]
        
        metric_x = st.selectbox("Eje X", ["TPL", "estructura", "carga_oculta"], index=0)
        metric_y = st.selectbox("Eje Y", ["PN", "transferencias"], index=0)
        
        fig_scatter = px.scatter(df_anio, x=metric_x, y=metric_y, color="pais", 
                                 size="estructura", hover_name="pais",
                                 title=f"Tendencia: {metric_x} vs {metric_y} en {anio_disp}")
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")
    with st.expander("⚠️ Metodología y Fuentes de Datos"):
        st.warning("Nota Metodológica: Datos armonizados (BM, FMI, BCE, OCDE). TPL (Parasitismo), PN (Prosperidad).")
else:
    st.error("No se han podido cargar los datos.")