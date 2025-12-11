# SIC-Sistema-de-prediccion-espacio-temporal-de-zonas-de-alto-riesgo-delictivo-en-Ecuador

**Índice:**
- [Descripción del proyecto](#descripción-del-proyecto)
- [Integrantes del grupo](#integrantes-del-grupo)
- [Instalación](#instalacion)
- [Instalación](#instalacion)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#ejecución)
- [Ejecución](#ejecución)
    - [Sola la aplicación](#solo-la-aplicación)
    - [Todo el proyecto](#todo-el-proyecto)
- [Uso](#uso)
- [Herramientas Implementadas](#herramientas-implementadas)

---

# Descripción del proyecto
Este proyecto tiene como objetivo desarrollar un sistema de inteligencia artificial capaz de identificar y predecir zonas de alto riesgo delictivo en Ecuador, integrando registros de detenidos con datos de llamadas de emergencia. Para ello, se realiza un procesamiento y análisis geoespacial de la información, se entrenan modelos de predicción (XGBoost) y se generan visualizaciones mediante mapas interactivos.
---

# Integrantes del Grupo
- Angie Alfonso
- Christian Zavala
- Fernando Alvarez 
- Fiorella Quijana
- Joseph Carrera
---

# Instalación

## Requisitos
- Python 3.11+ (Recomendado)
- Git
- Git LFS

## Pasos
1. **Clonar el repositorio**
    ```bash
    git clone https://github.com/fundestpuente/SIC-Sistema-de-prediccion-espacio-temporal-de-zonas-de-alto-riesgo-delictivo-en-Ecuador.git
    cd SIC-Sistema-de-prediccion-espacio-temporal-de-zonas-de-alto-riesgo-delictivo-en-Ecuador
    ```

2. **Crear y activar el entorno virtual (Recomendado)**
    ```bash
    python -m venv venv
    ```
    Activar entorno en Linux/MacOS
    ```bash
    source venv/bin/activate
    ```
    Activar entorno en Windows
    ```bash
    .\venv\Scripts\activate
    ```

3. **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```

---

# Estructura del proyecto
    SIC-Sistema-de-prediccion-espacio-temporal-de-zonas-de-alto-riesgo-delictivo-en-Ecuador/
    |
    ├── data/
    │   ├── raw/                 <- Datos originales
    │   └── processed/           <- Datasets procesados
    |
    ├── models/                  <- modelos guardados
    |
    ├── src/                          
    │   ├── features/            <- Scripts para el preprocesamiento
    │   └── models/              <- Scripts de entrenamiento y predicción
    │
    ├── app.py                   <- app versión 1 (frontend/backend)
    ├── api.py                   <- app versión 2 (backend)
    ├── index.html               <- app versión 2 (frontend)
    ├── requirements.txt         <- librerias necesarias
    |
    └── README.md

---

# Ejecución

## Solo la aplicación

### Versión 1

En la carpeta del proyecto ejecutar el siguiente comando:
```bash
streamlit run app.py
```
El comando inicia un servidor y abre de manera local la aplicación.

### Versión 2
En la carpeta del proyecto ejecutar el siguiente comando:
```bash
python api.py
```
El comando inicia el servidor de manera local y la aplicación se accede mediante el archivo `index.html`

## Todo el proyecto

1. **Preprocesamiento**

    Estando en la carpeta `src/features` se ejecutan los archivos en el siguiente orden:
    ```bash
    python preprocesamiento_datos_detenidosaprehendidos.py
    python preprocesamiento_datos_ecu911.py
    python consultaCoordParroquias.py
    python preprocesamiento_datos_entrenamiento.py
    ```
    Cada uno de estos archivos de python devuelven un archivo `.csv` en la carpeta `data/processed`.

    El tiempo de ejecución de cada archivo depende de la potencia de su computador.

2. **Entrenamiento del modelo**

    Estando en la carpeta `src/models` se ejecuta solamente el archivo de entrenamiento.
    ```bash
    python entrenamiento.py
    ```
    Este archivo devuelve el modelo de IA guardado en la carpeta `models`.

    El tiempo de ejecución depende de la potencia de su computador

3. **Ejecución de la app**
    Para la ejecución de la app regrese a la sección [Solo la aplicación](#solo-la-aplicación)

---

# Uso
El funcionamiento de la aplicación es el mismo sin importar su versión.

1. Seleccione el día mediante el calendario
2. Seleccione la provincia
3. Presione el botón **Predecir** o **Generar Predicción**
4. Ya puede visualizar el mapa con la predicción delictiva de ese día y provincia

---

# Herramientas Implementadas
- **Lenguaje:** Python 3.1x
- **Librerías principales:** pandas, joblib, xgboost, scikit-learn