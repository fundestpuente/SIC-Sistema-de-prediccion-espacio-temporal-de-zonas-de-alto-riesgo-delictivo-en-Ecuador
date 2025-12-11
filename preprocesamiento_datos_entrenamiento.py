import pandas as pd
import numpy as np

#carga datasets
df_apre = pd.read_csv("aprehendidos_limpio_final.csv")
df_911 = pd.read_csv("ecu911_limpio_final.csv")

# Normalizacion de fechas
df_911["fecha"] = pd.to_datetime(df_911["fecha_dt"], errors="coerce").dt.date
df_apre["fecha"] = pd.to_datetime(df_apre["fecha"], errors="coerce").dt.date

#union de datasets por celdas 
df_union = df_apre.merge(
    df_911,
    on=["lat_grid", "lon_grid", "fecha"],
    how="outer",
    suffixes=("_apre", "_911")
)


# Eliminar franja_horaria porque no contiene datos importantes
if "franja_horaria" in df_union.columns:
    df_union.drop(columns=["franja_horaria"], inplace=True)

# features
features = [
    "lat_grid", "lon_grid",
    "mes", "dia", "dia_semana",
    "franja_horaria",
    "conteo_delitos",
    "conteo_delitos_graves",
    "conteo_llamadas_riesgo"
]

# asegurarse de que las columnas existan
features = [c for c in features if c in df_union.columns]

df_final = df_union[features].copy()

# guardar dataset final
df_final.to_csv("dataset_entrenamiento_final.csv", index=False)
print("dataset de entramiento guardado: dataset_entranamiento_final.csv")
print("Registros totales:", len(df_final))
print("Columnas:", df_final.columns.tolist())