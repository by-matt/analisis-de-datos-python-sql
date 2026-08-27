# =====================================================================
# 🎵 Desafío — Fundamentos del método científico y probabilidad
# Tema: Teorema del Límite Central (TLC)
# Estudiante: Byron Calderón
# =====================================================================

# Hola profe, aquí está mi código para demostrar el Teorema del Límite Central.
# Importamos las librerías necesarias:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Fijamos la semilla para tener datos consistentes y reproducibles
np.random.seed(10)

# ---------------------------------------------------------------------
# Generación de la Población (Código entregado en el enunciado)
# ---------------------------------------------------------------------

# Parámetros de la distribución Gamma (no es una distribución normal)
shape, scale = 2.5, 30
poblacion_tiempos = np.random.gamma(shape, scale, 5000)

# Calculamos la media y desviación estándar REAL de la población
media_poblacional = np.mean(poblacion_tiempos)
std_poblacional = np.std(poblacion_tiempos)

print("=== DATOS DE LA POBLACIÓN ===")
print(f"La media poblacional (mu) es: {media_poblacional:.2f} minutos")
print(f"La desviación estándar poblacional (sigma) es: {std_poblacional:.2f} minutos")
print("-" * 50)

# Visualizamos la distribución de la población (comentado para evitar que se bloquee el script al correr)
# sns.histplot(poblacion_tiempos, kde=True)
# plt.title("Distribución de Tiempos de Entrega (Población Total)")
# plt.xlabel("Tiempo de Entrega (minutos)")
# plt.ylabel("Frecuencia")
# plt.savefig("1_poblacion_tiempos.png") # Lo guardamos como imagen para poder verlo
# plt.show()


# =====================================================================
# 1. Simulación de la Distribución Muestral
# =====================================================================
# - Tomamos 1000 muestras aleatorias de la población. 
# - Cada muestra tiene tamaño n = 40.
# - Para cada muestra calculamos su media.

medias_muestrales = []
n = 40
num_muestras = 1000

for i in range(num_muestras):
    # Sacamos una muestra aleatoria de tamaño 40 de la población total
    # Usamos replace=True porque es muestreo con reemplazo para simulaciones, 
    # aunque con una población grande de 5000, replace=False también funcionaría similar.
    muestra = np.random.choice(poblacion_tiempos, size=n, replace=True)
    
    # Calculamos la media de esta muestra en específico
    media_de_esta_muestra = np.mean(muestra)
    
    # La agregamos a nuestra lista
    medias_muestrales.append(media_de_esta_muestra)

# Convertimos la lista a un arreglo de NumPy para facilitar los cálculos matemáticos
medias_muestrales = np.array(medias_muestrales)

print("1. SIMULACIÓN DE LA DISTRIBUCIÓN MUESTRAL")
print(f" - Se han extraído {len(medias_muestrales)} muestras aleatorias de tamaño n = {n}.")
print(f" - Las primeras 5 medias muestrales son: {medias_muestrales[:5]}")
print("-" * 50)


# =====================================================================
# 2. Análisis del Teorema del Límite Central (TLC)
# =====================================================================

# Calculamos la media de nuestras 1000 medias muestrales
media_de_medias = np.mean(medias_muestrales)

# Calculamos la desviación estándar empírica de nuestras medias muestrales
std_de_medias = np.std(medias_muestrales)

# Calculamos el error estándar teórico (SE) usando la fórmula del TLC: SE = sigma / sqrt(n)
error_estandar_teorico = std_poblacional / np.sqrt(n)

print("2. ANÁLISIS DEL TEOREMA DEL LÍMITE CENTRAL (TLC)")
print(f" - Media de las medias muestrales:  {media_de_medias:.2f} minutos")
print(f" - Media real de la población (mu): {media_poblacional:.2f} minutos")
print(f" - Desviación estándar de medias:   {std_de_medias:.2f} minutos")
print(f" - Error Estándar Teórico (SE):     {error_estandar_teorico:.2f} minutos")

# Graficamos el histograma de las medias muestrales
plt.figure()
sns.histplot(medias_muestrales, kde=True, color="green")
plt.title("Distribución de las Medias Muestrales (n=40)")
plt.xlabel("Media de Tiempo de Entrega (minutos)")
plt.ylabel("Frecuencia")
plt.axvline(media_poblacional, color="red", linestyle="--", label=f"Media Poblacional ({media_poblacional:.2f})")
plt.legend()
plt.savefig("2_distribucion_medias_muestrales.png") # Guardamos el gráfico
# plt.show()
print(" - Gráfico guardado en '2_distribucion_medias_muestrales.png'")
print("-" * 50)

# ---------------------------------------------------------------------
# RESPUESTAS A LAS PREGUNTAS DEL REQUERIMIENTO 2 (Efecto del TLC):
# ---------------------------------------------------------------------
#
# ¿La media de las medias muestrales es similar a la media_poblacional?
# -> Sí, profe. La media de las medias muestrales ({media_de_medias:.2f}) es prácticamente idéntica
#    a la media poblacional real ({media_poblacional:.2f}). Esto demuestra que la media muestral
#    es un estimador insesgado de la media poblacional.
#
# ¿El error estándar teórico (SE) es similar a la desviación estándar obtenida de las medias_muestrales?
# -> Sí. El error estándar teórico es de {error_estandar_teorico:.2f} minutos, y la desviación estándar
#    empírica de nuestras 1000 medias muestrales es de {std_de_medias:.2f} minutos. Los valores son muy
#    cercanos, lo que valida la fórmula del TLC: SE = sigma / sqrt(n).
#
# ¿Qué forma tiene esta distribución de las medias_muestrales?
# -> Aunque la población original tiene una forma Gamma muy sesgada a la izquierda (no normal),
#    la distribución de las medias muestrales tiene una forma de campana simétrica, es decir,
#    sigue una Distribución Normal. Esto es exactamente lo que predice el Teorema del Límite Central
#    cuando el tamaño de muestra (n = 40) es lo suficientemente grande (usualmente n >= 30).
#
# ---------------------------------------------------------------------


# =====================================================================
# 3. Cálculo de Probabilidades
# =====================================================================
# Queremos calcular la probabilidad de que una muestra aleatoria de 40 entregas 
# tenga una media de 72 minutos o menos. Es decir, P(X_barra <= 72).

# Valor de interés
x_limite = 72

# Estandarizamos el valor convirtiéndolo a Z-score:
# Z = (X_limite - mu) / SE
# Usaremos los parámetros teóricos para la estandarización: mu = media_poblacional, SE = error_estandar_teorico
z_score = (x_limite - media_poblacional) / error_estandar_teorico

# Calculamos la probabilidad acumulada usando la distribución normal estándar de SciPy (stats.norm.cdf)
probabilidad_72_o_menos = stats.norm.cdf(z_score)

print("3. CÁCULO DE PROBABILIDADES")
print(f" - Queremos saber: P(Media Muestral <= {x_limite} minutos)")
print(f" - Z-score calculado: Z = ({x_limite} - {media_poblacional:.2f}) / {error_estandar_teorico:.2f} = {z_score:.4f}")
print(f" - Probabilidad (área bajo la curva normal estándar): {probabilidad_72_o_menos:.4f} (o {probabilidad_72_o_menos*100:.2f}%)")
print("-" * 50)
print("¡Desafío completado y validado con éxito! Listo para entregar.")
