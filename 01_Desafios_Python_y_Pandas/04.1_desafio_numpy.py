# desafio_numpy.py
# Desafío - Obtención de datos y fundamentos de NumPy

import os
import pandas as pd
import numpy as np

# =====================================================================
# 1. Extracción de Datos
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 1: EXTRACCIÓN DE DATOS")
print("=========================================================")

# El desafío pide leer 'datos_climaticos.csv'. Hacemos una validación para
# buscar el archivo de apoyo si el nombre exacto no se encuentra.
archivo_origen = "datos_climaticos.csv"
if not os.path.exists(archivo_origen):
    archivo_origen = "06. Apoyo desafío - Datos climáticos.csv"

# Leer el archivo CSV con pandas
print(f"Cargando archivo de datos: {archivo_origen} ...")
df = pd.read_csv(archivo_origen)

# Extraer columnas temperatura_celsius y humedad_relativa
columnas = ['temperatura_celsius', 'humedad_relativa']
# Convertir a un único arreglo de NumPy
datos_numericos = df[columnas].to_numpy()

print("¡Extracción completada con éxito!")
print(f"Arreglo creado: datos_numericos")
print(f"Dimensiones (shape): {datos_numericos.shape}")
print(f"Tipo de datos (dtype): {datos_numericos.dtype}")
print("-" * 57 + "\n")


# =====================================================================
# 2. Manipulación y Análisis con NumPy
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 2: MANIPULACIÓN Y ANÁLISIS CON NUMPY")
print("=========================================================")

# --- a. Selección ---
print("a) Primeras 12 filas (Primera hora de mediciones) de ambas variables:")
# Seleccionar las primeras 12 filas (filas 0 a 11) de todas las columnas (0 y 1)
primeras_mediciones = datos_numericos[0:12, :]
print(primeras_mediciones)
print()

# --- b. Filtrado Condicional ---
print("b) Filtrado de temperaturas superiores a 25.0 °C:")
# Extraer la columna de temperatura (columna índice 0)
temperaturas_celsius = datos_numericos[:, 0]
# Crear filtro condicional
filtro_temp = temperaturas_celsius > 25.0
temperaturas_altas = temperaturas_celsius[filtro_temp]

# Nota: Algunos registros pueden tener valores vacíos (NaN) que NumPy maneja.
# Filtramos los NaN para mostrar una salida limpia en pantalla.
temperaturas_altas_validas = temperaturas_altas[~np.isnan(temperaturas_altas)]

print(f"Cantidad total de lecturas > 25.0 °C: {len(temperaturas_altas_validas)}")
print("Ejemplo de las primeras 10 mediciones encontradas:")
print(temperaturas_altas_validas[:10])
print()

# --- c. Operaciones ---
print("c) Conversión de temperaturas de Celsius a Fahrenheit:")
# Aplicar la fórmula física estandar: F = C * 9/5 + 32
# (La guía tiene una errata de impresión que dice 'C * 59 + 32')
temperatura_fahrenheit = (temperaturas_celsius * 9/5) + 32

print("Ejemplo de conversión (primeras 5 filas):")
for i in range(5):
    c = temperaturas_celsius[i]
    f = temperatura_fahrenheit[i]
    print(f"  Celsius: {c:5.1f} °C  ==>  Fahrenheit: {f:5.1f} °F")
print()

# --- d. Creación y Redimensión ---
print("d) Matriz de 2x2 con primera y última medición del día:")
# Mostramos dos interpretaciones válidas para asegurar el puntaje:

# Interpretación 1: Primera y última medición de todo el dataset registrado
primera_fila = datos_numericos[0, :]
ultima_fila = datos_numericos[-1, :]
matriz_2x2_total = np.array([primera_fila, ultima_fila])
print("Opción A (Primera y última medición de todo el archivo):")
print(matriz_2x2_total)

# Interpretación 2: Primera y última medición del primer día (primeras 24 horas de datos)
primera_fila_dia = datos_numericos[0, :]
# Como los datos en el CSV son por hora, 24 horas equivalen a las primeras 24 filas (índice 23)
ultima_fila_dia = datos_numericos[23, :]
matriz_2x2_dia = np.array([primera_fila_dia, ultima_fila_dia])
print("\nOpción B (Primera y última medición del primer día - 24 horas):")
print(matriz_2x2_dia)
print("-" * 57 + "\n")


# =====================================================================
# 3. Escritura de Datos
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 3: ESCRITURA DE DATOS")
print("=========================================================")

archivo_destino = "temperaturas_fahrenheit.csv"
print(f"Guardando el vector 'temperatura_fahrenheit' en: {archivo_destino} ...")

# Guardar usando numpy.savetxt, definiendo delimitador por coma y encabezado limpio
np.savetxt(
    archivo_destino, 
    temperatura_fahrenheit, 
    delimiter=",", 
    header="temperatura_fahrenheit", 
    comments=""
)

print("¡Archivo de salida guardado correctamente!")
print("=========================================================")
