#desarrollo de interfaz de la solucion
import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

from predictor import (
    cargar_modelo, cargar_dataset,
    preparar_grid, predecir_riesgo, filtrar_por_zona
)

from zonas import ZONAS

# Configuración UI

st.set_page_config(page_title="Sistema de Predicción Delictiva", layout="wide")
st.title("Sistema de Predicción de Riesgo Delictivo")
st.markdown("Selecciona una fecha y una zona para generar el mapa de riesgo.")


# Carga de recursos

@st.cache_resource
def get_modelo():
    return cargar_modelo()

@st.cache_resource
def get_dataset():
    return cargar_dataset()

modelo = get_modelo()
df = get_dataset()


# Controles de entrada

col1, col2 = st.columns(2)

with col1:
    fecha_seleccionada = st.date_input("Fecha de predicción:")

with col2:
    zona_seleccionada = st.selectbox("Zona geográfica:", list(ZONAS.keys()))

st.markdown("---")


# Ejecución de predicción
if st.button("Predecir Riesgos"):

    if fecha_seleccionada is None:
        st.error("Debes seleccionar una fecha válida.")
        st.stop()

    with st.spinner("Generando predicción..."):

        fecha_dt = pd.to_datetime(str(fecha_seleccionada))

        df_grid = preparar_grid(df, fecha_dt)
        df_pred = predecir_riesgo(modelo, df_grid)

        limites = ZONAS[zona_seleccionada]
        df_zona = filtrar_por_zona(df_pred, limites)

        if df_zona.empty:
            st.error("No hay datos en esta zona para generar el mapa.")
            st.stop()

        st.session_state["df_zona"] = df_zona
        st.session_state["info"] = {
            "zona": zona_seleccionada,
            "fecha": fecha_dt.date()
        }
        st.success("Mapa generado correctamente.")


# Mostrar mapa 
if "df_zona" in st.session_state:

    df_zona = st.session_state["df_zona"]

    center_lat = df_zona["lat_grid"].mean()
    center_lon = df_zona["lon_grid"].mean()

    mapa = folium.Map(location=[center_lat, center_lon], zoom_start=11)
    heat_data = df_zona[["lat_grid", "lon_grid", "prediccion_riesgo"]].values.tolist()

    HeatMap(heat_data, radius=12, blur=15).add_to(mapa)
    st_folium(mapa, width=1200, height=600)

    if st.button("Limpiar Mapa"):
        st.session_state.clear()
        st.rerun()