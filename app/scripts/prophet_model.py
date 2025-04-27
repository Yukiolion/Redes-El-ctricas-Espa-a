import pickle
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import numpy as np
from scipy.stats import zscore
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error, mean_squared_error

# # CONFIGURAMOS QUE LOS GRAFICOS SE ABRAN EN WEB PARA PODER VERLOS INTERACTIVOS
# import plotly.io as pio
# pio.renderers.default = 'browser'

def prophet_model(df, rango):

    # Filtrar el DataFrame para solo contener las filas con el indicador 'demanda'
    df = df[df['indicador'] == 'demanda']
    df['fecha'] = pd.to_datetime(df['fecha'])
    df = df.sort_values('fecha')

    # FILTRAR POR FECHA Y VALOR POR QUE EL MODELO PROPHET SOLO CONTEMPLA ESTAS COLUMNAS
    df_filtrado = df[['fecha', 'valor']].rename(columns={'fecha': 'ds', 'valor': 'y'})

    # PREPARACIÓN DE LOS DATOS.
    df_filtrado = df_filtrado.dropna()
    df_filtrado['y'] = pd.to_numeric(df_filtrado['y'], errors='coerce')
    df_filtrado = df_filtrado[np.isfinite(df_filtrado['y'])]

    if df_filtrado.empty:
        print("Advertencia: No hay datos en df_filtrado después del preprocesamiento.")
        return None, None, None

    lower_limit = np.percentile(df_filtrado['y'], 1)

    # HAREMOS UNA LIMPIEZA DE DATOS ALGO AGRESIVA DEBIDO A
    # LA GRAN MAGNITUD DE VALORES QUE SE MANEJAN.
    z_scores = zscore(df_filtrado['y'])
    df_filtrado = df_filtrado[np.abs(z_scores) < 3]

    lower_limit = np.percentile(df_filtrado['y'], 1)
    upper_limit = np.percentile(df_filtrado['y'], 99)
    df_filtrado = df_filtrado[(df_filtrado['y'] >= lower_limit) & (df_filtrado['y'] <= upper_limit)]

    # ESCALAMOS LOS DATOS DEBIDO A QUE TIENEN VALORES MUY GRANDES
    # Y ASI EVITAMOS QUE EL MODELO TENGA UN COLAPSO INTERNO.
    df_filtrado['y'] = np.log(df_filtrado['y'] + 1)

    # CONFIGURACIÓN DEL MODELO PROPHET DE META PARA HACER LAS PREDICCIONES.
    # DEJAMOS EL DAILY Y EL WEEKLY POR QUE SON LOS QUE NOS HACEN FALTA REALMENTE.
    modelo = Prophet(yearly_seasonality=False, daily_seasonality=True, weekly_seasonality=True)
    modelo.fit(df_filtrado)

    # DEFINIR EL RANGO DE FECHAS A PREDECIR.
    future = modelo.make_future_dataframe(periods=rango, freq='D')

    forecast = modelo.predict(future)

    # HACEMOS LAS PREDICCIONES PARA EL RANGO DE FECHAS SELECCIONADO Y LAS AÑADIMOS A UNA LISTA
    # PARA PODER VISUALIZARLAS DESPUES.
    futuro = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(rango)

    df_futuro = pd.DataFrame(futuro)

    return df_futuro, forecast
















# # Cálculo de métricas
#         y_true = df_filtrado['y'][-rango:]  # Los valores reales del período de predicción
#         y_pred = forecast['yhat'][-rango:]  # Las predicciones realizadas por Prophet

#         mae = mean_absolute_error(y_true, y_pred)
#         mse = mean_squared_error(y_true, y_pred)
#         rmse = np.sqrt(mse)
#         r2 = r2_score(y_true, y_pred)

#         print(f"Métricas para {region} - {indicador}:")
#         print(f"MAE: {mae}")
#         print(f"MSE: {mse}")
#         print(f"RMSE: {rmse}")
#         print(f"R²: {r2}")