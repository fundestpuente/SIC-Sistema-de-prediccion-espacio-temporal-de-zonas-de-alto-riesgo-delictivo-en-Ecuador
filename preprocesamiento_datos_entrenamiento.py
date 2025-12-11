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
