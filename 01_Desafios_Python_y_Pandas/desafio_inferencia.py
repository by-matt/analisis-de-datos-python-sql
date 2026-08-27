# =====================================================================
# ☕ Desafío — Inferencia y pruebas de hipótesis
# Caso: "Café Rápido"
# Estudiante: Byron Calderón
# =====================================================================

# Hola profe. Aquí está mi código para resolver el desafío de inferencia.
# Primero importamos las librerías que usaremos en el desarrollo:
import pandas as pd
import numpy as np
import math  # Para redondear al entero superior
from scipy import stats  # Para obtener los valores críticos de t y z

# ---------------------------------------------------------------------
# Generar datos poblacionales simulados (Código del enunciado)
# ---------------------------------------------------------------------
np.random.seed(42) 
datos_poblacion = { 
    'calificacion': np.random.normal(loc=8.5, scale=1.5, size=5000).clip(1, 10), 
    'recomienda': np.random.choice([1, 0], size=5000, p=[0.75, 0.25]) 
} 
poblacion_df = pd.DataFrame(datos_poblacion) 
poblacion_df['calificacion'] = poblacion_df['calificacion'].round(1) 

# Extraemos la muestra de 100 clientes para nuestro estudio inferencial
muestra_df = poblacion_df.sample(n=100, random_state=101) 

print("=== MUESTRA DE DATOS GENERADA ===")
print("Primeras 5 filas de la muestra:") 
print(muestra_df.head()) 
print(f"\nEl tamano de la muestra es de {len(muestra_df)} clientes.") 
print("-" * 60)


# =====================================================================
# 1. Inferencia sobre la Media con Desviación Estándar Conocida
# =====================================================================
# Históricamente sabemos que la desviación estándar poblacional (sigma) es 1.5.

# Paso 1: Calculamos la media muestral
media_muestral = muestra_df['calificacion'].mean()
n = len(muestra_df)
sigma_conocida = 1.5
z_critico_95 = 1.96

# Paso 2: Calculamos el intervalo de confianza (IC = media +/- z * (sigma / sqrt(n)))
error_estandar_conocido = sigma_conocida / np.sqrt(n)
margen_error_1 = z_critico_95 * error_estandar_conocido

limite_inferior_1 = media_muestral - margen_error_1
limite_superior_1 = media_muestral + margen_error_1

print("1. INFERENCIA SOBRE LA MEDIA (SIGMA CONOCIDA = 1.5)")
print(f" - Media de calificacion en la muestra: {media_muestral:.4f}")
print(f" - Margen de error: {margen_error_1:.4f}")
print(f" - Intervalo de Confianza 95%: [{limite_inferior_1:.4f}, {limite_superior_1:.4f}]")

# Paso 3: Interpretación del resultado
# Profe, la interpretación en una frase sería:
# "Tenemos un 95% de confianza de que la calificacion promedio real de satisfaccion de todos 
# los clientes de Cafe Rapido se encuentra entre {limite_inferior_1:.2f} y {limite_superior_1:.2f} puntos."
print(f" - Interpretacion: Tenemos un 95% de confianza de que la calificacion promedio poblacional")
print(f"   esta entre {limite_inferior_1:.2f} y {limite_superior_1:.2f} puntos.")
print("-" * 60)


# =====================================================================
# 2. Inferencia sobre la Media con Desviación Estándar Desconocida
# =====================================================================
# Aquí no asumimos que conocemos la desviación estándar de la población.

# Paso 1: Calculamos la media y la desviación estándar muestral (s)
s_muestral = muestra_df['calificacion'].std()

# Paso 2: Usamos la distribución t-Student. Calculamos el t crítico para 95%
# Grados de libertad (df) = n - 1
grados_libertad = n - 1
# Usamos ppf(0.975) porque es una prueba de dos colas (deja 0.025 en cada cola)
t_critico_95 = stats.t.ppf(0.975, df=grados_libertad)

error_estandar_desconocido = s_muestral / np.sqrt(n)
margen_error_2 = t_critico_95 * error_estandar_desconocido

limite_inferior_2 = media_muestral - margen_error_2
limite_superior_2 = media_muestral + margen_error_2

print("2. INFERENCIA SOBRE LA MEDIA (SIGMA DESCONOCIDA)")
print(f" - Desviacion estandar de la muestra (s): {s_muestral:.4f}")
print(f" - Valor critico t (df={grados_libertad}): {t_critico_95:.4f}")
print(f" - Margen de error: {margen_error_2:.4f}")
print(f" - Intervalo de Confianza 95%: [{limite_inferior_2:.4f}, {limite_superior_2:.4f}]")

# Paso 3: Comparación con el Requerimiento 1
# Profe, mi análisis comparativo es:
# El intervalo del Requerimiento 2 es un poco mas ANCHO (o amplio) que el del Requerimiento 1.
# Esto pasa por dos razones:
# 1. Al no conocer la desviación estándar real de la población, usamos la desviación estándar de la
#    muestra (s = {s_muestral:.4f}), la cual puede introducir incertidumbre adicional.
# 2. La distribución t-Student tiene colas mas pesadas que la normal estándar para compensar esta 
#    incertidumbre adicional de muestras pequeñas. Por ello, el valor critico t (t = {t_critico_95:.2f}) 
#    es mayor que el valor critico z (z = 1.96).
print("-" * 60)


# =====================================================================
# 3. Inferencia sobre una Proporción
# =====================================================================
# Experiencia excelente = Recomienda (1) en la columna 'recomienda'

# Paso 1: Calculamos la proporción muestral (p_gorro)
recomendaciones = muestra_df['recomienda'].sum()
p_gorro = recomendaciones / n

# Paso 2: Calculamos el intervalo de confianza de la proporción
# Usamos la aproximación normal para la proporción (z = 1.96)
z_proporcion = 1.96
error_estandar_prop = np.sqrt((p_gorro * (1 - p_gorro)) / n)
margen_error_prop = z_proporcion * error_estandar_prop

limite_inferior_prop = p_gorro - margen_error_prop
limite_superior_prop = p_gorro + margen_error_prop

print("3. INFERENCIA SOBRE UNA PROPORCIÓN")
print(f" - Casos favorables en la muestra: {recomendaciones} de {n}")
print(f" - Proporcion muestral (p_gorro): {p_gorro:.4f} (o {p_gorro*100:.1f}%)")
print(f" - Margen de error para la proporcion: {margen_error_prop:.4f}")
print(f" - Intervalo de Confianza 95%: [{limite_inferior_prop:.4f}, {limite_superior_prop:.4f}]")

# Paso 3: Conclusión
# La conclusión sobre la verdadera proporción de clientes satisfechos:
# "Con base en la muestra, se estima con un 95% de confianza que el porcentaje real de todos los 
# clientes que calificarian como excelente su experiencia en Cafe Rapido y recomendarian el cafe 
# se encuentra en el rango de {limite_inferior_prop*100:.1f}% y {limite_superior_prop*100:.1f}%."
print(f" - Conclusion: La verdadera proporcion de clientes satisfechos se encuentra")
print(f"   probablemente entre el {limite_inferior_prop*100:.1f}% y el {limite_superior_prop*100:.1f}%.")
print("-" * 60)


# =====================================================================
# 4. Impacto del Nivel de Confianza
# =====================================================================
# Volvemos a calcular el IC de la media con sigma desconocida, pero al 99% de confianza.

# Paso 1: Obtener el valor crítico de t para un 99% de confianza (deja 0.005 en cada cola)
t_critico_99 = stats.t.ppf(0.995, df=grados_libertad)

# Paso 2: Calcular el nuevo intervalo
margen_error_99 = t_critico_99 * error_estandar_desconocido
limite_inferior_99 = media_muestral - margen_error_99
limite_superior_99 = media_muestral + margen_error_99

print("4. IMPACTO DEL NIVEL DE CONFIANZA (99% CON CONF. Y SIGMA DESCONOCIDA)")
print(f" - Valor critico t al 99%: {t_critico_99:.4f}")
print(f" - Margen de error: {margen_error_99:.4f}")
print(f" - Intervalo de Confianza 99%: [{limite_inferior_99:.4f}, {limite_superior_99:.4f}]")

# Paso 3: Explicación de cómo y por qué afecta la amplitud
# Profe, la explicación es:
# El aumento en el nivel de confianza de 95% a 99% hace que el intervalo sea mas ANCHO. 
# Esto ocurre porque para estar mas seguros (99% de certeza) de capturar la media verdadera dentro del 
# intervalo, necesitamos cubrir un area de probabilidad mas amplia. Esto hace que el valor critico t 
# aumente de {t_critico_95:.4f} a {t_critico_99:.4f}, aumentando directamente el margen de error y la amplitud.
print("-" * 60)


# =====================================================================
# 5. Cálculo del Tamaño de la Muestra
# =====================================================================
# Margen de error máximo permitido: E = 0.04 (4%)
# Confianza: 95% (z = 1.96)
# Estimador inicial: p_gorro calculado en el requerimiento 3

# Paso 1: Aplicamos la fórmula del tamaño muestral para proporción
E = 0.04
z_calc = 1.96

# n = (z^2 * p * (1 - p)) / E^2
n_calculado = (z_calc ** 2 * p_gorro * (1 - p_gorro)) / (E ** 2)

# Paso 2: Redondeamos hacia el entero superior usando math.ceil
n_requerido = math.ceil(n_calculado)

print("5. CÁLCULO DEL TAMAÑO DE LA MUESTRA")
print(f" - Margen de error maximo deseado (E): {E} (4%)")
print(f" - Proporcion estimada (p_gorro): {p_gorro:.4f}")
print(f" - Valor de n calculado por formula: {n_calculado:.4f}")
print(f" - Tamaño de muestra final requerido (redondeado hacia arriba): {n_requerido} clientes.")
print("-" * 60)
print("¡Analisis estadistico inferencial finalizado con éxito!")
