import os
from pathlib import Path

print("OS:",os.curdir)
for f in os.listdir(os.path.abspath("..")):
    print("OS:",f)


ruta_padre = Path("..","..","data")
datos = ruta_padre.joinpath("raw","detenidosaprehendidos","dataset","mdi_detenidosaprehendidos_pm_2025_enero_octubre.xlsx")
ruta_datos = ruta_padre.joinpath("raw","ecu911","dataset")
ruta_procesados = ruta_padre.joinpath("processed")
print(ruta_padre)
print(datos)
print(ruta_procesados)
for f in ruta_datos.iterdir():
    print(f)

print("\nOS\n")

# --- Replicando la construcción de rutas ---

# 1. Replicar ruta_padre = Path("..","..","data")
#    En 'os', usamos os.path.join y os.pardir ('..')
ruta_padre = os.path.join(os.pardir, os.pardir, "data")

# 2. Replicar la construcción de la ruta de datos
#    datos = ruta_padre.joinpath("raw", "detenidosaprehendidos", "dataset", "mdi_detenidosaprehendidos_pm_2025_enero_octubre.xlsx")
datos = os.path.join(
    ruta_padre, 
    "raw", 
    "detenidosaprehendidos", 
    "dataset", 
    "mdi_detenidosaprehendidos_pm_2025_enero_octubre.xlsx"
)

# 3. Replicar ruta_datos y ruta_procesados
#    ruta_datos = ruta_padre.joinpath("raw", "ecu911", "dataset")
ruta_datos = os.path.join(ruta_padre, "raw", "ecu911", "dataset")

#    ruta_procesados = ruta_padre.joinpath("processed")
ruta_procesados = os.path.join(ruta_padre, "processed")


# --- Replicando la salida de impresión ---
print(ruta_padre)
print(datos)
print(ruta_procesados)

# --- Replicando el bucle for ---

# 4. Replicar for f in ruta_datos.iterdir(): print(f)
#    En 'os', usamos os.listdir() para obtener los nombres de archivos/carpetas.
#    Luego, unimos la ruta_datos con el nombre del archivo para obtener la ruta completa.
print("\n--- Contenido de ruta_datos ---")
try:
    for f_nombre in os.listdir(ruta_datos):
        # Es buena práctica unir la ruta padre con el nombre para tener la ruta completa
        ruta_completa_archivo = os.path.join(ruta_datos, f_nombre)
        print(ruta_completa_archivo)
except FileNotFoundError:
    print(f"Error: El directorio '{ruta_datos}' no fue encontrado.")
except Exception as e:
    print(f"Ocurrió un error al listar el directorio: {e}")




