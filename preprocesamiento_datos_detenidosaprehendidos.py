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