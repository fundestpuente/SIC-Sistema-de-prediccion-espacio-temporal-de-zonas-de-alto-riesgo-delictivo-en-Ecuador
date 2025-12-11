#preprocesamiento datos de aprehendidos/detenidos
import pandas as pd
import numpy as np

#CARGA DE DATOS
nombre_archivo = 'detenidosaprehendidos/dataset/mdi_detenidosaprehendidos_pm_2025_enero_octubre.xlsx'

try:
    print("Cargando archivo Excel... esto puede tardar unos segundos...")
    df_apre = pd.read_excel(
        nombre_archivo,
        sheet_name=1,
        dtype={'codigo_parroquia': str},
        engine='openpyxl'
    )
    print(f"Registros totales: {len(df_apre)}")

except Exception as e:
    print("Error cargando el Excel:", e)



# Seleccionar columnas de interés
cols_interes = [
    "fecha_completa", "fecha", "latitud", "longitud",
    "codigo_parroquia", "nombre_parroquia",
    "presunta_infraccion", "tipo", "arma", "movilizacion"
]

df_apre_clean = df_apre[cols_interes].copy()

# Crear características de tiempo
df_apre_clean["franja_horaria"] = df_apre_clean["fecha_completa"].dt.hour
df_apre_clean["dia"] = df_apre_clean["fecha_completa"].dt.day
df_apre_clean["mes"] = df_apre_clean["fecha_completa"].dt.month
df_apre_clean["dia_semana"] = df_apre_clean["fecha_completa"].dt.dayofweek