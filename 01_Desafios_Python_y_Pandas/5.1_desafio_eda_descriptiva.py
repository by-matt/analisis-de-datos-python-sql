# desafio_eda_descriptiva.py
# Desafío - Fundamentos de análisis exploratorio y estadística descriptiva

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Establecer estilo visual para los gráficos
sns.set_theme(style="whitegrid")

# =====================================================================
# 1. Generación y Carga del Conjunto de Datos (1 Punto)
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 1: CARGA DEL CONJUNTO DE DATOS")
print("=========================================================")

# El archivo de datos se llama 'videojuegos.csv' o '06. videojuegos.csv'
archivo = "videojuegos.csv"
if not os.path.exists(archivo):
    archivo = "06. videojuegos.csv"

print(f"Cargando archivo: {archivo} ...")
df = pd.read_csv(archivo)
print("¡Archivo cargado correctamente!")
print("-" * 57 + "\n")


# =====================================================================
# 2. Análisis Exploratorio Inicial (IDA) (4 Puntos)
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 2: ANÁLISIS EXPLORATORIO INICIAL (IDA)")
print("=========================================================")

# a. Primeras 5 filas
print("a) Primeras 5 filas del DataFrame (df.head()):")
print(df.head())
print()

# b. Últimas 5 filas
print("b) Últimas 5 filas del DataFrame (df.tail()):")
print(df.tail())
print()

# c. Información general del DataFrame
print("c) Información general del DataFrame (df.info()):")
df.info()
print()

# Explicación de nulos y tipos de datos
print("Análisis de tipos de datos y valores nulos:")
print("  - Tipos de datos:")
print("    * Columnas cualitativas/categóricas: 'Nombre', 'Plataforma', 'Genero' (tipo object).")
print("    * Columnas cuantitativas/numéricas enteras: 'Anio_Lanzamiento' (tipo int64).")
print("    * Columnas cuantitativas/numéricas continuas: 'Ventas_NA', 'Ventas_EU', 'Ventas_JP', 'Critica_Puntaje' (tipo float64).")
print("  - Valores nulos:")
print("    * La columna 'Critica_Puntaje' contiene valores nulos (hay 91 registros no nulos frente a 101 totales, por lo que faltan 10 valores).")
print("    * Las demás columnas no presentan valores nulos.")
print()

# d. Dimensiones del DataFrame
dimensiones = df.shape
print(f"d) Dimensiones del DataFrame (Filas, Columnas): {dimensiones}")
print("-" * 57 + "\n")


# =====================================================================
# 3. Análisis Descriptivo y Univariado (5 Puntos)
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 3: ANÁLISIS DESCRIPTIVO Y UNIVARIADO")
print("=========================================================")

# --- Variables Numéricas ---
print("a) Estadísticos para variables numéricas:")
columnas_num = ['Ventas_NA', 'Ventas_EU', 'Ventas_JP', 'Critica_Puntaje']

for col in columnas_num:
    print(f"\nEstadísticas para la columna: {col}")
    media = df[col].mean()
    mediana = df[col].median()
    desviacion = df[col].std()
    
    # Rango = maximo - minimo
    minimo = df[col].min()
    maximo = df[col].max()
    rango = maximo - minimo
    
    print(f"  - Media (Promedio):           {media:.4f}")
    print(f"  - Mediana:                    {mediana:.4f}")
    print(f"  - Desviación Estándar:        {desviacion:.4f}")
    print(f"  - Rango:                      {rango:.4f} (Mín: {minimo:.4f}, Máx: {maximo:.4f})")
print()

# --- Visualización: Histogramas ---
print("b) Generando Histogramas de Ventas_NA y Critica_Puntaje...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histograma Ventas en NA
sns.histplot(df['Ventas_NA'].dropna(), ax=axes[0], kde=True, color='skyblue')
axes[0].set_title('Distribución de Ventas en NA')
axes[0].set_xlabel('Ventas (millones)')
axes[0].set_ylabel('Frecuencia')

# Histograma Puntaje de la Crítica
sns.histplot(df['Critica_Puntaje'].dropna(), ax=axes[1], kde=True, color='salmon')
axes[1].set_title('Distribución de Puntajes de la Crítica')
axes[1].set_xlabel('Puntaje (0-100)')
axes[1].set_ylabel('Frecuencia')

plt.tight_layout()
fig.savefig('histogramas.png')
plt.close()
print("  --> Gráfico guardado como 'histogramas.png'")
print("  --> Interpretación:")
print("      * Ventas_NA presenta un sesgo a la derecha muy marcado. La mayoría de los juegos")
print("        venden pocos millones de copias, mientras que solo unos pocos juegos logran ventas altas.")
print("      * Critica_Puntaje muestra una distribución más uniforme o ligeramente sesgada a la izquierda,")
print("        con mayor concentración de juegos calificados con puntajes intermedios y altos.")
print()

# --- Visualización: Boxplots ---
print("c) Generando Boxplots de ventas por región...")
# Preparar datos combinando las tres regiones de venta para graficarlos juntos
df_ventas = df[['Ventas_NA', 'Ventas_EU', 'Ventas_JP']].melt(var_name='Región', value_name='Ventas')

plt.figure(figsize=(10, 6))
sns.boxplot(x='Región', y='Ventas', data=df_ventas, palette='Set2')
plt.title('Distribución de Ventas y Outliers por Región')
plt.xlabel('Región de Ventas')
plt.ylabel('Copias Vendidas (millones)')

plt.savefig('boxplots.png')
plt.close()
print("  --> Gráfico guardado como 'boxplots.png'")
print("  --> Interpretación:")
print("      * Sí existen valores atípicos (outliers) en las tres regiones de ventas.")
print("      * Se observan varios puntos individuales más allá de los bigotes superiores,")
print("        lo que representa juegos con ventas excepcionalmente altas (éxitos de ventas).")
print()

# --- Variables Categóricas ---
print("d) Tablas de frecuencia para variables categóricas:")

print("\nFrecuencia por Plataforma:")
print(df['Plataforma'].value_counts())

print("\nFrecuencia por Género:")
print(df['Genero'].value_counts())
print()

# --- Gráfico de Barras: Género ---
print("e) Generando Gráfico de barras de cantidad de juegos por género...")
plt.figure(figsize=(10, 5))
sns.countplot(
    x='Genero', 
    data=df, 
    order=df['Genero'].value_counts().index, 
    palette='viridis'
)
plt.title('Cantidad de Videojuegos por Género')
plt.xlabel('Género')
plt.ylabel('Cantidad de Juegos')
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('barras_genero.png')
plt.close()
print("  --> Gráfico guardado como 'barras_genero.png'")

genero_comun = df['Genero'].value_counts().index[0]
cantidad_comun = df['Genero'].value_counts().values[0]
print(f"  --> El género más común en este conjunto de datos es '{genero_comun}' con {cantidad_comun} juegos.")
print("=========================================================")
