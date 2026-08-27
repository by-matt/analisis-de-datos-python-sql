# prueba_aed_visualizacion.py
# Prueba - Análisis exploratorio de datos

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Establecer estilo visual para los gráficos
sns.set_theme(style="whitegrid")

# =====================================================================
# Carga de Datos
# =====================================================================
archivo = "videojuegos.csv"
if not os.path.exists(archivo):
    archivo = "09. videojuegos.csv"

print(f"Cargando archivo de datos: {archivo} ...")
df = pd.read_csv(archivo)
print("¡Archivo cargado correctamente!\n")


# =====================================================================
# PARTE 1: ANÁLISIS VISUAL CON SEABORN
# =====================================================================
print("=========================================================")
print("PARTE 1: ANÁLISIS VISUAL CON SEABORN")
print("=========================================================")

# --- 1. Gráfico de Pares (pairplot) ---
print("1. Generando gráfico de pares (pairplot) agrupado por Plataforma...")
# Variables numéricas especificadas
columnas_num = ['Ventas_NA', 'Ventas_EU', 'Ventas_JP', 'Critica_Puntaje']

# Crear el pairplot utilizando el parámetro hue para diferenciar por Plataforma
pair_plot = sns.pairplot(
    data=df, 
    vars=columnas_num, 
    hue='Plataforma', 
    palette='Set1'
)
pair_plot.fig.suptitle('Gráfico de Pares (Pairplot) de Ventas y Puntajes por Plataforma', y=1.02)
pair_plot.savefig('grafico_pares.png')
print("  --> Gráfico de pares guardado como 'grafico_pares.png'")
print()

# --- 2. Gráfico de Violín (violinplot) ---
print("2. Generando gráfico de violín (violinplot) de Critica_Puntaje por Plataforma...")
plt.figure(figsize=(10, 6))
sns.violinplot(
    x='Plataforma', 
    y='Critica_Puntaje', 
    data=df, 
    palette='Pastel1'
)
plt.title('Distribución de Puntajes de la Crítica por Plataforma')
plt.xlabel('Plataforma')
plt.ylabel('Puntaje de la Crítica (0-100)')

plt.savefig('grafico_violin.png')
plt.close()
print("  --> Gráfico de violín guardado como 'grafico_violin.png'")
print()

# --- 3. Mapa de Calor (heatmap) ---
print("3. Generando mapa de calor (heatmap) de la matriz de correlación...")
# Filtrar sólo las columnas numéricas para calcular la correlación
matriz_correlacion = df[columnas_num].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(
    matriz_correlacion, 
    annot=True,          # Mostrar los valores numéricos
    cmap='coolwarm',     # Mapa de colores divergente
    fmt=".3f",           # Tres decimales para mayor precisión
    linewidths=0.5       # Línea divisoria
)
plt.title('Mapa de Calor de la Matriz de Correlación')
plt.tight_layout()

plt.savefig('mapa_calor.png')
plt.close()
print("  --> Mapa de calor guardado como 'mapa_calor.png'")
print("-" * 57 + "\n")


# =====================================================================
# PARTE 2: PERSONALIZACIÓN DE GRÁFICOS CON MATPLOTLIB
# =====================================================================
print("=========================================================")
print("PARTE 2: PERSONALIZACIÓN CON MATPLOTLIB")
print("=========================================================")

# --- 4. Preparación de Datos ---
print("4. Preparando los datos de ventas por género...")
# Calcular el total de ventas globales
df['Ventas_Globales'] = df['Ventas_NA'] + df['Ventas_EU'] + df['Ventas_JP']

# Agrupar por Genero y calcular la media de Ventas_Globales
df_genero = df.groupby('Genero')['Ventas_Globales'].mean().reset_index()
# Ordenamos de mayor a menor para una visualización más estructurada
df_genero = df_genero.sort_values(by='Ventas_Globales', ascending=False)

print("Promedios de ventas globales agrupados:")
print(df_genero)
print()

# --- 5 y 6. Creación y Personalización del Gráfico de Barras ---
print("5-6. Creando y personalizando el gráfico de barras...")
plt.figure(figsize=(10, 6))

# Dibujar las barras usando Matplotlib
# - color: steelblue (azul acero)
# - edgecolor: black (borde negro)
barras = plt.bar(
    df_genero['Genero'], 
    df_genero['Ventas_Globales'], 
    color='steelblue', 
    edgecolor='black'
)

# Añadir títulos y etiquetas claras
plt.title('Promedio de Ventas Globales por Género de Videojuego', fontsize=14, fontweight='bold')
plt.xlabel('Género del Videojuego', fontsize=12)
plt.ylabel('Ventas Globales Promedio (millones de copias)', fontsize=12)

# Fijar los límites del eje Y para dejar un espacio sobre el valor máximo
valor_maximo = df_genero['Ventas_Globales'].max()
plt.ylim(0, valor_maximo * 1.15) # Deja un 15% de espacio adicional para las anotaciones

# Añadir las anotaciones de texto sobre cada barra con el promedio exacto
for barra in barras:
    alto = barra.get_height()
    # Escribir el valor justo encima de la barra
    plt.text(
        barra.get_x() + barra.get_width() / 2.0, 
        alto + (valor_maximo * 0.02), # Pequeña separación vertical
        f"{alto:.3f}", 
        ha='center', 
        va='bottom', 
        fontsize=10, 
        fontweight='bold'
    )

plt.xticks(rotation=45)
plt.tight_layout()

# Guardar el gráfico final
grafico_salida = 'ventas_por_genero_personalizado.png'
plt.savefig(grafico_salida)
plt.close()

print(f"  --> Gráfico personalizado guardado como '{grafico_salida}'")
print("=========================================================")
