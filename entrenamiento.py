import joblib
import pandas as pd

df = pd.read_csv("dataset_entrenamiento_final.csv")
df.head()
target = "conteo_delitos" # columna objetivo
from sklearn.model_selection import train_test_split

X = df.drop(columns=[target])
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
from xgboost import XGBRegressor

model = XGBRegressor(
    n_estimators=400,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.7,
    colsample_bytree=0.7,
    objective="reg:squarederror"
)

model.fit(X_train, y_train)
from sklearn.metrics import mean_squared_error

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5

print("RMSE:", rmse)

# GUARDAR EL MODELO
joblib.dump(model, "modelo_riesgo_delictivo.pkl")
