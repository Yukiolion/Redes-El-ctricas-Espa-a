from scripts.extraccion import extraccion
# from scripts.limpieza import limpiar_datos
# from scripts.carga import upload_db

dataframes = extraccion()

for nombre, df in dataframes.items():
    print(f"DataFrame {nombre}:\n{df.head()}")

    # df_limpio = limpiar_datos(df)