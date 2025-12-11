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

# NORMALIZACIÓN DE DATOS DE LATITUD Y LONGITUD
for col in ["latitud", "longitud"]:
    df_apre[col] = (
        df_apre[col]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )
    df_apre[col] = pd.to_numeric(df_apre[col], errors="coerce")

# ELIMINAR COLUMNAS INVÁLIDAS
df_apre = df_apre.dropna(subset=["latitud", "longitud"])
df_apre = df_apre[(df_apre["latitud"] != 0) & (df_apre["longitud"] != 0)]


# PROCESAR FECHA Y HORA
try:
    df_apre["fecha"] = pd.to_datetime(df_apre["fecha_detencion_aprehension"], errors="coerce")

    #HORA COMO STRING LIMPIO
    df_apre["hora_limpia"] = (
        df_apre["hora_detencion_aprehension"]
        .astype(str)
        .str.replace(" ", "")
        .str.strip()
    )

    #COMBINAR FECHA Y HORA
    df_apre["fecha_completa"] = pd.to_datetime(
        df_apre["fecha"].astype(str) + " " + df_apre["hora_limpia"],
        errors="coerce"
    )

except Exception as e:
    print("Advertencia procesando fecha/hora:", e)

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

#grid espacial
df_apre_clean["lat_grid"] = df_apre_clean["latitud"].round(3)
df_apre_clean["lon_grid"] = df_apre_clean["longitud"].round(3)


#conteo de delios por dia y zona
grouped = (
    df_apre_clean
    .groupby(["lat_grid", "lon_grid", "fecha"])
    .size()
    .reset_index(name="conteo_delitos")
)
# unir conteo al dataframe principal
df_apre_clean = df_apre_clean.merge(
    grouped,
    on=["lat_grid", "lon_grid", "fecha"],
    how="left"
)


#guardar dataset limpio
print("\n=== Dataset final limpio ===")
print(df_apre_clean.head())
print(f"Total registros finales: {len(df_apre_clean)}")