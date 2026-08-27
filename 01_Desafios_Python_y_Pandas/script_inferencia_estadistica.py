# =====================================================================
# 📚 Prueba — Inferencia estadística
# Caso: Nivel de Satisfacción - Plataforma de Tecnología Educativa
# Estudiante: Byron Calderón
# =====================================================================

# Hola profe. Aquí está mi código para resolver la prueba de inferencia estadística.
# Importamos las librerías necesarias:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Fijamos una semilla aleatoria para tener consistencia al generar los datos
np.random.seed(24)

# =====================================================================
# 1. Carga y exploración de datos (2 puntos)
# =====================================================================

# Generamos datos simulados de 200 estudiantes:
datos_estudiantes = {
    'edad': np.random.randint(18, 46, size=200),  # Edades entre 18 y 45 años
    'genero': np.random.choice(['Femenino', 'Masculino', 'Otro'], size=200, p=[0.48, 0.47, 0.05]),
    'puntaje_satisfaccion': np.random.normal(loc=7.3, scale=1.4, size=200).clip(1, 10).round(1),
    'horas_estudio_semanal': np.random.uniform(3, 25, size=200).round(1)
}

# Creamos el DataFrame en Pandas
df = pd.DataFrame(datos_estudiantes)

print("=== 1. EXPLORACIÓN DE DATOS (MUESTRA SIMULADA) ===")
print("Primeras 5 filas del DataFrame:")
print(df.head())
print(f"\nTotal de registros: {len(df)}")
print("-" * 50)

# Estadísticas descriptivas básicas de las variables numéricas
print("Estadísticas descriptivas de variables numéricas:")
print(df.describe().loc[['mean', '50%', 'std']])  # Media, mediana (50%) y desviación estándar
print("-" * 50)

# Verificamos si existen valores nulos en el DataFrame
nulos = df.isnull().sum()
print("Cantidad de valores nulos por columna:")
print(nulos)
print("-" * 50)

# ---------------------------------------------------------------------
# EXPLICACIÓN SOBRE EL MANEJO DE VALORES NULOS:
# ---------------------------------------------------------------------
# Profe, en esta simulación no hay valores nulos (todos dan 0). Pero si existieran en un caso real,
# yo los manejaría de las siguientes maneras dependiendo de la variable:
# 
# 1. Eliminación de registros (Listwise Deletion): Si la cantidad de nulos es muy pequeña (menor al 5%
#    del total), simplemente borraría las filas afectadas para no complicar el análisis.
# 
# 2. Imputación por medidas de tendencia central: 
#    - Para variables numéricas continuas (como 'horas_estudio_semanal' o 'edad'), rellenaría los nulos 
#      usando la media o la mediana de la columna.
#    - Para la variable de interés 'puntaje_satisfaccion', imputar con la media podría alterar
#      los resultados de la inferencia, por lo que preferiría eliminar esos registros específicos o 
#      utilizar imputación predictiva.
#    - Para variables categóricas (como 'genero'), rellenaría los nulos con la moda (el valor más común) 
#      o crearía una categoría nueva llamada "No Especifica".
# ---------------------------------------------------------------------


# =====================================================================
# 2. Distribución y visualización (2 puntos)
# =====================================================================

# Graficamos el histograma de los puntajes de satisfacción
plt.figure(figsize=(8, 5))
sns.histplot(df['puntaje_satisfaccion'], kde=True, color='skyblue', bins=10)
plt.title('Distribución de Puntajes de Satisfacción')
plt.xlabel('Puntaje de Satisfacción (1 al 10)')
plt.ylabel('Frecuencia')
plt.axvline(df['puntaje_satisfaccion'].mean(), color='red', linestyle='--', label=f"Media: {df['puntaje_satisfaccion'].mean():.2f}")
plt.legend()
plt.savefig('satisfaccion_histograma.png')  # Guardamos el gráfico como imagen
# plt.show()

# Calculamos la media y varianza usando NumPy
media_satisfaccion = np.mean(df['puntaje_satisfaccion'])
varianza_satisfaccion = np.var(df['puntaje_satisfaccion'])  # Varianza poblacional de la muestra

print("=== 2. DISTRIBUCIÓN Y MEDIDAS CON NUMPY ===")
print(f" - Media del puntaje de satisfacción:    {media_satisfaccion:.4f}")
print(f" - Varianza del puntaje de satisfacción: {varianza_satisfaccion:.4f}")
print(" - Histograma guardado con éxito en 'satisfaccion_histograma.png'")
print("-" * 50)

# ---------------------------------------------------------------------
# INTERPRETACIÓN DE LA NORMALIDAD DE LOS DATOS:
# ---------------------------------------------------------------------
# Profe, basándome en el histograma y la curva KDE:
# Los datos parecen aproximarse bastante bien a una distribución normal. La curva tiene una 
# forma de campana simétrica centrada alrededor de la media (~7.3). Aunque hay algunos picos
# por efecto de la discretización a un decimal y el límite superior de 10, no se observan 
# sesgos extremos ni colas anormales. Por lo tanto, es razonable asumir normalidad para los
# análisis inferenciales, especialmente dado que n=200 es mayor que 30 (aplicando el TLC).
# ---------------------------------------------------------------------


# =====================================================================
# 3. Intervalo de confianza (2 puntos)
# =====================================================================
# Calculamos el intervalo de confianza al 95% para la media de satisfacción.
# Como no conocemos la desviación estándar poblacional, usamos la distribución t-Student.

n_estudiantes = len(df)
media_muestral = df['puntaje_satisfaccion'].mean()
desviacion_muestral = df['puntaje_satisfaccion'].std()

# Grados de libertad y t-crítico para 95% (dos colas)
df_libertad = n_estudiantes - 1
t_critico = stats.t.ppf(0.975, df=df_libertad)

# Calculamos el margen de error
error_estandar = desviacion_muestral / np.sqrt(n_estudiantes)
margen_error = t_critico * error_estandar

limite_inferior = media_muestral - margen_error
limite_superior = media_muestral + margen_error

print("=== 3. INTERVALO DE CONFIANZA (95%) ===")
print(f" - Desviación estándar muestral (s): {desviacion_muestral:.4f}")
print(f" - Error estándar de la media:       {error_estandar:.4f}")
print(f" - Margen de error calculado:        {margen_error:.4f}")
print(f" - Intervalo de Confianza al 95%:    [{limite_inferior:.4f}, {limite_superior:.4f}]")
print("-" * 50)

# ---------------------------------------------------------------------
# INTERPRETACIÓN DEL INTERVALO EN EL CONTEXTO DEL ESTUDIO:
# ---------------------------------------------------------------------
# Profe, la interpretación en términos prácticos es:
# "Tenemos un 95% de confianza (certeza estadística) de que el verdadero puntaje promedio de 
# satisfacción de toda la población de estudiantes con el nuevo curso en línea se encuentra 
# dentro del rango de {limite_inferior:.2f} y {limite_superior:.2f} puntos."
# Esto significa que si tomáramos 100 muestras distintas, en 95 de ellas el intervalo calculado 
# contendría el valor promedio real del nivel de satisfacción global.
# ---------------------------------------------------------------------


# =====================================================================
# 4. Prueba de hipótesis (3 puntos)
# =====================================================================
# Queremos contrastar si: "El puntaje promedio de satisfacción es igual a 7".
#
# Planteamiento de hipótesis:
# H0 (Hipótesis Nula):        mu = 7  (El puntaje promedio de satisfacción es igual a 7)
# H1 (Hipótesis Alternativa): mu != 7 (El puntaje promedio de satisfacción es diferente de 7)

# Realizamos una prueba t para una muestra (One-sample t-test)
t_stat, p_valor = stats.ttest_1samp(df['puntaje_satisfaccion'], popmean=7)

print("=== 4. PRUEBA DE HIPÓTESIS ===")
print(" - Hipotesis Nula (H0):        mu = 7")
print(" - Hipotesis Alternativa (H1): mu != 7")
print(f" - Estadístico t calculado: {t_stat:.4f}")
print(f" - Valor p (p-value):       {p_valor:.6f}")

# Definimos el nivel de significancia (alfa = 0.05)
alfa = 0.05

if p_valor < alfa:
    print(f" - Conclusión estadística: Como el valor p ({p_valor:.6f}) es menor que alfa ({alfa}),")
    print("   RECHAZAMOS la hipótesis nula (H0) a favor de la hipótesis alternativa (H1).")
else:
    print(f" - Conclusión estadística: Como el valor p ({p_valor:.6f}) es mayor o igual que alfa ({alfa}),")
    print("   NO RECHAZAMOS la hipótesis nula (H0).")

# ---------------------------------------------------------------------
# INTERPRETACIÓN DEL RESULTADO PARA LA EMPRESA:
# ---------------------------------------------------------------------
# En términos prácticos para la empresa de tecnología educativa:
# Existe suficiente evidencia estadística para afirmar que la satisfacción promedio de los 
# estudiantes es significativamente diferente de 7 (de hecho, es mayor, dado que la media 
# muestral es de {media_satisfaccion:.2f}). 
# Esto es una excelente noticia para la empresa, ya que el nivel de satisfacción con el 
# nuevo curso en línea está significativamente por encima del valor neutro/esperado de 7. 
# El curso está funcionando mejor de lo presupuestado.
# ---------------------------------------------------------------------
print("-" * 50)


# =====================================================================
# 5. Reflexión final (1 punto)
# =====================================================================
#
# REFLEXIÓN SOBRE EL ROL DE LA ESTADÍSTICA INFERENCIAL EN LA TOMA DE DECISIONES:
#
# Profe, aquí mi reflexión final de 4 líneas:
# La estadística inferencial permite a las empresas tomar decisiones basadas en datos reales
# sin tener que encuestar a toda su población, lo cual ahorra costos y tiempo. Al medir el margen
# de error y los intervalos de confianza, reduce la incertidumbre empresarial y valida si las
# mejoras en productos o servicios (como este curso) logran un impacto estadísticamente significativo.
#
# =====================================================================

print("=== 5. REFLEXIÓN FINAL ===")
print("La reflexión final ha sido escrita como un comentario en la sección 5 del código fuente.")
print("¡Prueba terminada y lista para su revisión!")
