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

# ===== CONFIGURACIÓN DE LA PÁGINA =====
st.set_page_config(
    page_title="Sistema de Predicción Delictiva",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "Sistema de predicción de riesgo delictivo basado en Machine Learning"
    }
)

# ===== IMPORTAR ICONOS =====
# Añadir Font Awesome para iconos modernos
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# ===== ESTILOS CSS PERSONALIZADOS =====
st.markdown("""
<style>
    /* Ajustes generales */
    .main {
        padding: 2rem 3rem;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        text-align: center;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    
    /* Cards de controles */
    .control-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #e8e8e8;
        transition: all 0.3s ease;
        min-height: 120px;
    }
    
    .control-card:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Asegurar que los labels sean visibles */
    .control-card label {
        display: block !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Labels personalizados */
    .stDateInput label, .stSelectbox label {
        font-weight: 600;
        font-size: 1rem;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    /* Botones */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Sección de información */
    .info-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1.5rem 0;
    }
    
    .info-box h3 {
        color: #2c3e50;
        margin-top: 0;
        font-size: 1.2rem;
    }
    
    .info-box p {
        color: #5a6c7d;
        margin-bottom: 0;
        font-size: 0.95rem;
    }
    
    /* Iconos personalizados */
    .icon-wrapper {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .icon-wrapper i {
        font-size: 1.2rem;
    }
    
    /* Stats cards */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        text-align: center;
        border-top: 3px solid #667eea;
    }
    
    .stat-card h4 {
        color: #667eea;
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .stat-card p {
        color: #7f8c8d;
        font-size: 0.9rem;
        margin: 0;
    }
    
    /* Mensajes de éxito/error mejorados */
    .stSuccess, .stError, .stWarning {
        border-radius: 10px;
        border: none;
        padding: 1rem 1.5rem;
    }
    
    /* Mapa container */
    .map-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        margin-top: 2rem;
    }
    
    /* Divider personalizado */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #667eea, transparent);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .main {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ===== HEADER PRINCIPAL =====
st.markdown("""
<div class="main-header">
    <h1><i class="fas fa-shield-alt"></i> Sistema de Predicción Delictiva</h1>
    <p><i class="fas fa-brain"></i> Análisis predictivo de riesgo delictivo mediante Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# ===== CARGA DE RECURSOS =====
@st.cache_resource
def get_modelo():
    return cargar_modelo()

@st.cache_resource
def get_dataset():
    return cargar_dataset()

with st.spinner("🔄 Inicializando sistema..."):
    modelo = get_modelo()
    df = get_dataset()

# ===== SECCIÓN DE INSTRUCCIONES =====
with st.expander("ℹ️ ¿Cómo usar este sistema?", expanded=False):
    st.markdown("""
    <div class="info-box">
        <h3><i class="fas fa-info-circle"></i> Pasos para generar una predicción:</h3>
        <p>
        <i class="fas fa-calendar-alt"></i> <strong>1. Selecciona la fecha</strong> para la cual deseas predecir el riesgo delictivo<br>
        <i class="fas fa-map-marked-alt"></i> <strong>2. Elige la zona geográfica</strong> de interés<br>
        <i class="fas fa-mouse-pointer"></i> <strong>3. Haz clic en "Generar Predicción"</strong> para visualizar el mapa de calor<br>
        <i class="fas fa-chart-area"></i> <strong>4. Analiza las zonas</strong> según la intensidad del color (rojo = mayor riesgo)
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== CONTROLES DE ENTRADA =====
st.markdown("### <i class='fas fa-sliders-h'></i> Parámetros de Predicción", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    fecha_seleccionada = st.date_input(
        "📅 Fecha de predicción",
        help="Selecciona la fecha para la cual deseas realizar la predicción"
    )

with col2:
    zona_seleccionada = st.selectbox(
        "🗺️ Zona geográfica",
        list(ZONAS.keys()),
        help="Selecciona el área geográfica a analizar"
    )

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    btn_predecir = st.button("🔮 Generar Predicción", type="primary")

st.markdown("<br>", unsafe_allow_html=True)

# ===== EJECUCIÓN DE PREDICCIÓN =====
if btn_predecir:
    if fecha_seleccionada is None:
        st.error("⚠️ Por favor, selecciona una fecha válida.")
        st.stop()

    with st.spinner("🔄 Procesando datos y generando predicción..."):
        fecha_dt = pd.to_datetime(str(fecha_seleccionada))
        
        # Preparación y predicción
        df_grid = preparar_grid(df, fecha_dt)
        df_pred = predecir_riesgo(modelo, df_grid)
        
        limites = ZONAS[zona_seleccionada]
        df_zona = filtrar_por_zona(df_pred, limites)

        if df_zona.empty:
            st.error("❌ No hay datos disponibles en esta zona para generar el mapa.")
            st.stop()

        # Guardar en session state
        st.session_state["df_zona"] = df_zona
        st.session_state["info"] = {
            "zona": zona_seleccionada,
            "fecha": fecha_dt.date()
        }
        
        st.success("✅ Predicción generada exitosamente")

# ===== VISUALIZACIÓN DEL MAPA =====
if "df_zona" in st.session_state:
    df_zona = st.session_state["df_zona"]
    info = st.session_state["info"]
    
    st.markdown("---")
    st.markdown("### <i class='fas fa-map-marked-alt'></i> Mapa de Riesgo Delictivo", unsafe_allow_html=True)
    
    # Estadísticas rápidas
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.markdown(f"""
        <div class="stat-card">
            <p><i class="fas fa-map-pin"></i> Zona Analizada</p>
            <h4>{info['zona']}</h4>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown(f"""
        <div class="stat-card">
            <p><i class="fas fa-calendar-day"></i> Fecha de Predicción</p>
            <h4>{info['fecha'].strftime('%d/%m/%Y')}</h4>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat3:
        puntos_analizados = len(df_zona)
        st.markdown(f"""
        <div class="stat-card">
            <p><i class="fas fa-crosshairs"></i> Puntos Analizados</p>
            <h4>{puntos_analizados:,}</h4>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generar mapa
    center_lat = df_zona["lat_grid"].mean()
    center_lon = df_zona["lon_grid"].mean()
    
    mapa = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles='CartoDB positron'
    )
    
    # Normalizar los valores de riesgo para mejor visualización
    riesgo_min = df_zona["prediccion_riesgo"].min()
    riesgo_max = df_zona["prediccion_riesgo"].max()
    
    # Si todos los valores son muy similares, ajustar la escala
    if riesgo_max - riesgo_min < 0.1:
        # Usar percentiles para mejor distribución
        riesgo_min = df_zona["prediccion_riesgo"].quantile(0.1)
        riesgo_max = df_zona["prediccion_riesgo"].quantile(0.9)
    
    # Normalizar valores entre 0 y 1
    df_zona_norm = df_zona.copy()
    df_zona_norm["riesgo_norm"] = (
        (df_zona["prediccion_riesgo"] - riesgo_min) / (riesgo_max - riesgo_min)
    ).clip(0, 1)
    
    heat_data = df_zona_norm[["lat_grid", "lon_grid", "riesgo_norm"]].values.tolist()
    
    HeatMap(
        heat_data,
        radius=15,
        blur=20,
        max_zoom=13,
        min_opacity=0.3,
        max_opacity=0.8,
        gradient={
            0.0: 'blue',
            0.2: 'cyan',
            0.4: 'lime',
            0.6: 'yellow',
            0.8: 'orange',
            1.0: 'red'
        }
    ).add_to(mapa)
    
    # Mostrar mapa
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st_folium(mapa, width=None, height=600, returned_objects=[])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Leyenda
    st.markdown("""
    <div class="info-box" style="margin-top: 1.5rem;">
        <h3><i class="fas fa-palette"></i> Interpretación del Mapa de Calor</h3>
        <p>
        <i class="fas fa-circle" style="color: #0000ff;"></i> <strong>Azul:</strong> Riesgo muy bajo &nbsp;&nbsp;
        <i class="fas fa-circle" style="color: #00ffff;"></i> <strong>Cyan:</strong> Riesgo bajo &nbsp;&nbsp;
        <i class="fas fa-circle" style="color: #00ff00;"></i> <strong>Verde:</strong> Riesgo moderado &nbsp;&nbsp;
        <i class="fas fa-circle" style="color: #ffff00;"></i> <strong>Amarillo:</strong> Riesgo medio-alto &nbsp;&nbsp;
        <i class="fas fa-circle" style="color: #ff8800;"></i> <strong>Naranja:</strong> Riesgo alto &nbsp;&nbsp;
        <i class="fas fa-circle" style="color: #ff0000;"></i> <strong>Rojo:</strong> Riesgo crítico
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón de limpiar
    st.markdown("<br>", unsafe_allow_html=True)
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        if st.button("🔄 Nueva Predicción", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# ===== FOOTER =====
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">
    <p><i class="fas fa-shield-alt"></i> Sistema de Predicción Delictiva | <i class="fas fa-robot"></i> Powered by Machine Learning</p>
</div>
""", unsafe_allow_html=True)