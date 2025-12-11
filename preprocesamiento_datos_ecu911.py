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