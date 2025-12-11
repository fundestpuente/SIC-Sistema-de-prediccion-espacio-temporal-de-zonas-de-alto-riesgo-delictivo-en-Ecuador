import pandas as pd
import requests
import time

API_KEY = os.getenv("google_maps_api_key")

df = pd.read_excel("CODIFICACIÓN_2025.xlsx", sheet_name="PARROQUIAS")

# Renombrar columnas
df.columns = [
    "tmp", "cod_prov", "provincia", "cod_canton", 
    "canton", "cod_parroquia", "parroquia", 
    "cod_urb", "parroquia_urb"
]

df = df[["cod_parroquia", "provincia", "canton", "parroquia"]].dropna()

# Crear columna dirección
df["direccion_busqueda"] = (
    df["parroquia"] + ", " + df["canton"] + ", " + df["provincia"] + ", Ecuador"
)

latitudes = []
longitudes = []

for i, row in df.iterrows():
    lugar = row["direccion_busqueda"]

    url = (
        f"https://maps.googleapis.com/maps/api/geocode/json"
        f"?address={lugar}&key={API_KEY}"
    )

    response = requests.get(url).json()

    if response["status"] == "OK":
        loc = response["results"][0]["geometry"]["location"]
        latitudes.append(loc["lat"])
        longitudes.append(loc["lng"])
    else:
        latitudes.append(None)
        longitudes.append(None)

    print(f"{i+1}/{len(df)} → {lugar} → {latitudes[-1]}, {longitudes[-1]}")

    time.sleep(0.2)  # evita límites de la API

df["lat"] = latitudes
df["lon"] = longitudes

df.to_csv("catalogo_parroquias_ecuador.csv", index=False)
print("LISTO: catalogo_parroquias_ecuador.csv generado.")
