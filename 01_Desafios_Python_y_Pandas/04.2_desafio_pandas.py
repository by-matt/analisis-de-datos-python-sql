# desafio_pandas.py
# Desafío - Exploración de datos con Pandas

import pandas as pd

# Datos iniciales provistos por las instrucciones
datos_ventas = {
    'Producto': ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Webcam', 'Audífonos', 'Laptop', 'Mouse', 'Mouse'],
    'Categoría': ['Electrónica', 'Accesorios', 'Accesorios', 'Electrónica', 'Accesorios', 'Accesorios', 'Electrónica', 'Accesorios', 'Accesorios'],
    'Precio': [1200, 25, 45, 300, 50, 75, 1250, 27, 26],
    'Unidades_Vendidas': [5, 30, 25, 10, 20, 15, 3, 40, 35]
}

# Creación del DataFrame
df_ventas = pd.DataFrame(datos_ventas)


# =====================================================================
# 1. Exploración Inicial (4 Puntos)
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 1: EXPLORACIÓN INICIAL")
print("=========================================================")

# a. Resumen conciso de tipos de datos y valores no nulos
print("a) Resumen del DataFrame (df_ventas.info()):")
df_ventas.info()
print()

# b. Visualizar las primeras 5 filas
print("b) Primeras 5 filas del DataFrame (df_ventas.head()):")
print(df_ventas.head())
print()

# c. Resumen estadístico descriptivo para columnas numéricas
print("c) Resumen estadístico descriptivo (df_ventas.describe()):")
print(df_ventas.describe())
print("-" * 57 + "\n")


# =====================================================================
# 2. Selección y Filtrado (3 Puntos)
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 2: SELECCIÓN Y FILTRADO")
print("=========================================================")

# a. Seleccionar y mostrar únicamente la columna Producto (como Serie)
print("a) Columna 'Producto' como Serie:")
serie_producto = df_ventas['Producto']
print(serie_producto)
print(f"Tipo del resultado: {type(serie_producto)}")
print()

# b. Seleccionar y mostrar las columnas Producto y Precio
print("b) Columnas 'Producto' y 'Precio' (DataFrame):")
df_producto_precio = df_ventas[['Producto', 'Precio']]
print(df_producto_precio)
print()

# c. Filtrar y mostrar ventas con Precio superior a 100
print("c) Ventas con Precio superior a 100:")
df_filtrado_precio = df_ventas[df_ventas['Precio'] > 100]
print(df_filtrado_precio)
print("-" * 57 + "\n")


# =====================================================================
# 3. Sumarización de Datos (3 Puntos)
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 3: SUMARIZACIÓN DE DATOS")
print("=========================================================")

# a. Precio promedio de todos los productos
precio_promedio = df_ventas['Precio'].mean()
print(f"a) Precio promedio de todos los productos: ${precio_promedio:.2f}")
print()

# b. Total de unidades vendidas de la categoría "Accesorios"
df_accesorios = df_ventas[df_ventas['Categoría'] == 'Accesorios']
total_unidades_accesorios = df_accesorios['Unidades_Vendidas'].sum()
print(f"b) Total de unidades vendidas de 'Accesorios': {total_unidades_accesorios}")
print()

# c. Cantidad de veces que aparece cada producto (frecuencia de valores únicos)
print("c) Frecuencia de aparición de cada producto:")
conteo_productos = df_ventas['Producto'].value_counts()
print(conteo_productos)
print("=========================================================")
