# desafio_correlacion_modelamiento.py
# Desafío - Correlación y modelamiento

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Establecer estilo visual para los gráficos
sns.set_theme(style="whitegrid")

# =====================================================================
# 1. Preparación de Datos (2 Puntos)
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 1: PREPARACIÓN DE DATOS")
print("=========================================================")

# Buscar el archivo 'videojuegos.csv' o su variante local
archivo = "videojuegos.csv"
if not os.path.exists(archivo):
    archivo = "06. Apoyo desafío - Videojuegos.csv"

print(f"Cargando archivo: {archivo} ...")
df = pd.read_csv(archivo)

# a. Crear la columna Ventas_Globales
df['Ventas_Globales'] = df['Ventas_NA'] + df['Ventas_EU'] + df['Ventas_JP']

# b. Contar nulos antes de imputar
nulos_antes = df['Critica_Puntaje'].isnull().sum()

# Calcular la mediana de la columna Critica_Puntaje
mediana_critica = df['Critica_Puntaje'].median()

# Rellenar valores nulos con la mediana
df['Critica_Puntaje'] = df['Critica_Puntaje'].fillna(mediana_critica)

# Contar nulos después de imputar
nulos_despues = df['Critica_Puntaje'].isnull().sum()

print(f"Columna 'Ventas_Globales' creada con éxito.")
print(f"Cantidad de valores nulos en 'Critica_Puntaje':")
print(f"  - Antes de imputar:  {nulos_antes}")
print(f"  - Mediana utilizada: {mediana_critica}")
print(f"  - Después de imputar: {nulos_despues}")
print("-" * 57 + "\n")


# =====================================================================
# 2. Visualización de la Correlación (2 Puntos)
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 2: VISUALIZACIÓN DE LA CORRELACIÓN")
print("=========================================================")

# a. Generar gráfico de dispersión
print("Generando gráfico de dispersión (scatterplot)...")
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Critica_Puntaje', y='Ventas_Globales', data=df, color='darkblue', alpha=0.7)
plt.title('Relación entre Puntaje de la Crítica y Ventas Globales')
plt.xlabel('Puntaje de la Crítica (0-100)')
plt.ylabel('Ventas Globales (millones de copias)')

plt.savefig('dispersion.png')
plt.close()
print("  --> Gráfico guardado como 'dispersion.png'")

# b. Calcular coeficiente de correlación de Pearson
r_pearson = df['Critica_Puntaje'].corr(df['Ventas_Globales'], method='pearson')
print(f"Coeficiente de correlación de Pearson (r-Pearson): {r_pearson:.4f}")

# c. Interpretación dinámica de la correlación
direccion = "positiva" if r_pearson > 0 else "negativa"
signo_relacion = "> 0" if r_pearson > 0 else "< 0"
fuerza = "débil" if abs(r_pearson) < 0.3 else ("moderada" if abs(r_pearson) < 0.7 else "fuerte")

print("\nInterpretación de la correlación:")
print(f"  - Dirección: La dirección es {direccion} (r {signo_relacion}). Esto significa que a mayores")
print(f"    puntajes de la crítica, tienden a registrarse {'mayores' if r_pearson > 0 else 'menores'} ventas globales en promedio.")
print(f"  - Fuerza: El valor absoluto de r-Pearson ({abs(r_pearson):.4f}) es muy bajo (cercano a 0).")
print(f"    Esto nos indica una relación lineal {direccion} extremadamente {fuerza} (casi inexistente).")
print("-" * 57 + "\n")


# =====================================================================
# 3. Causalidad vs. Correlación (2 Puntos)
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 3: CAUSALIDAD VS. CORRELACIÓN")
print("=========================================================")

print("¿Un puntaje alto causa un aumento en las ventas globales?")
print("  No se puede afirmar que una puntuación alta de la crítica CAUSE directamente")
print("  un aumento en las ventas globales. La razón de esto es la siguiente:")
print("  - Correlación: Nos indica únicamente que dos variables se mueven juntas (existe una")
print("    asociación estadística entre ellas), pero no explica por qué se mueven juntas.")
print("  - Causalidad: Implica que una variable es el origen y causa el cambio en la otra variable.")
print("  - En este caso, puede haber variables de confusión (como el presupuesto de marketing, la popularidad")
print("    del estudio desarrollador o la franquicia) que influyen tanto en que los críticos den una nota alta")
print("    como en que el público compre más el juego. Por lo tanto, correlación no implica causalidad.")
print("-" * 57 + "\n")


# =====================================================================
# 4 y 6. Implementación del Modelo (2 Puntos)
# =====================================================================
print("=========================================================")
print("REQUERIMIENTOS 4 y 6: IMPLEMENTACIÓN DEL MODELO DE REGRESIÓN")
print("=========================================================")

# Definir variables dependiente (y) e independiente (x)
y = df['Ventas_Globales']
x = df['Critica_Puntaje']

# Añadir una constante a la variable independiente para estimar el intercepto
x_con_constante = sm.add_constant(x)

# Ajustar el modelo usando Mínimos Cuadrados Ordinarios (OLS)
modelo = sm.OLS(y, x_con_constante).fit()

# Mostrar el resumen estadístico descriptivo del modelo
print(modelo.summary())
print("-" * 57 + "\n")


# =====================================================================
# 5 y 7. Interpretación del Modelo (2 Puntos)
# =====================================================================
print("=========================================================")
print("REQUERIMIENTOS 5 y 7: INTERPRETACIÓN DEL MODELO")
print("=========================================================")

# Extraer coeficientes para explicarlos dinámicamente
constante = modelo.params['const']
coef_puntaje = modelo.params['Critica_Puntaje']
r_cuadrado = modelo.rsquared

cambio_ventas = "un incremento" if coef_puntaje > 0 else "un decremento"

print("Interpretación de los Coeficientes de Regresión:")
print(f"  - Constante / Intercepto (b0) = {constante:.4f}")
print("    * Significado: Representa las ventas globales estimadas en millones de copias cuando")
print("      la puntuación de la crítica es 0. Físicamente, establece la base de ventas del modelo.")
print(f"  - Coeficiente de Critica_Puntaje (b1) = {coef_puntaje:.4f}")
print("    * Significado: Por cada punto adicional de incremento en la puntuación de la crítica,")
print(f"      las ventas globales del videojuego se estima que tendrán {cambio_ventas} promedio de {abs(coef_puntaje):.4f} millones")
print("      de copias (aproximadamente, según la estimación lineal del modelo).")
print()
print("Interpretación de R-cuadrado (R2):")
print(f"  - Valor de R-cuadrado (R2) = {r_cuadrado:.4f} (es decir, {r_cuadrado * 100:.2f}%)")
print(f"  - Significado: El modelo lineal simple de Critica_Puntaje explica únicamente el {r_cuadrado * 100:.2f}%")
print("    de la variabilidad total en las ventas globales de videojuegos. El porcentaje restante")
print("    es explicado por otros factores no incluidos en este modelo (como marketing, plataforma, etc.).")
print("    Esto ratifica que la relación lineal es sumamente débil y que un modelo univariado es insuficiente.")
print("=========================================================")
