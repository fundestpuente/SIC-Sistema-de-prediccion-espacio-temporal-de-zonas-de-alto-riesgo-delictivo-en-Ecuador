import pandas as pd
import glob
import os
#carga de dataset ecu911
ruta_carpeta_911 = "ecu911/dataset/"
archivos_csv = glob.glob(os.path.join(ruta_carpeta_911, "*.csv"))

lista_dfs = []

for archivo in archivos_csv:
    try:
        df_temp = pd.read_csv(
            archivo,
            sep=";",
            encoding="UTF-8",
            dtype={"Cod_Parroquia": str},
            on_bad_lines="skip"
        )
        
        # Normalizacion de columnas
        df_temp.columns = (
            df_temp.columns.astype(str)
            .str.replace("ï»¿", "")
            .str.strip()
            .str.lower()
        )
        
        # Filtrar seguridad ciudadana
        if "servicio" in df_temp.columns:
            df_temp = df_temp[df_temp["servicio"] == "Seguridad Ciudadana"]
        
        lista_dfs.append(df_temp)

    except Exception as e:
        print(f"Error procesando {archivo}: {e}")

df_911 = pd.concat(lista_dfs, ignore_index=True)

# Fechas
df_911["fecha_dt"] = pd.to_datetime(df_911["fecha"], errors="coerce", dayfirst=True)
df_911 = df_911.dropna(subset=["fecha_dt"])

# Códigos parroquia normalizados
df_911["cod_parroquia"] = (
    df_911["cod_parroquia"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.zfill(6)
)