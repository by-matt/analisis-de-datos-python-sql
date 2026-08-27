# =====================================================================
# 🎵 Desafío — Fundamentos del método científico y probabilidad
# Estudiante: Byron Calderón
# =====================================================================

# Hola profe, aquí está mi código para el desafío. 
# Importamos las librerías que aprendimos a usar en clases:
import pandas as pd
import numpy as np

# Fijamos la semilla de números aleatorios para que siempre nos dé los mismos resultados
np.random.seed(42)

# ---------------------------------------------------------------------
# Generación de la Población (Código entregado en el enunciado)
# ---------------------------------------------------------------------

# Creamos el diccionario con los datos simulados de 1000 usuarios
data = {
    'user_id': range(1, 1001),
    'pais': np.random.choice(['México', 'Colombia', 'Argentina', 'Chile'], 1000, p=[0.4, 0.3, 0.2, 0.1]),
    'tiene_premium': np.random.choice([True, False], 1000, p=[0.35, 0.65])
}

# Convertimos el diccionario a un DataFrame de Pandas
poblacion_df = pd.DataFrame(data)

# Buscamos los índices de los usuarios de Chile
idx_chile = poblacion_df[poblacion_df['pais'] == 'Chile'].index

# Obligamos a que exactamente 10 chilenos elegidos al azar tengan cuenta Premium
poblacion_df.loc[np.random.choice(idx_chile, 10, replace=False), 'tiene_premium'] = True

print("=== POBLACIÓN GENERADA CON ÉXITO ===")
print(f"Total de usuarios en la población: {len(poblacion_df)}")
print(poblacion_df.head(10))
print("-" * 50)


# =====================================================================
# 1. Probabilidad Teórica (Sobre la Población Total)
# =====================================================================
# Definimos los eventos solicitados:
# Evento A: Que un usuario sea de 'Chile'
# Evento B: Que un usuario tenga una suscripción 'Premium'

total_poblacion = len(poblacion_df)

# Contamos cuántos usuarios de Chile hay en total
usuarios_chile = len(poblacion_df[poblacion_df['pais'] == 'Chile'])

# Contamos cuántos usuarios Premium hay en total
usuarios_premium = len(poblacion_df[poblacion_df['tiene_premium'] == True])

# Contamos cuántos usuarios son de Chile Y además son Premium (Intersección)
usuarios_chile_y_premium = len(poblacion_df[(poblacion_df['pais'] == 'Chile') & (poblacion_df['tiene_premium'] == True)])

# Contamos cuántos usuarios son de Chile O Premium (Unión)
usuarios_chile_o_premium = len(poblacion_df[(poblacion_df['pais'] == 'Chile') | (poblacion_df['tiene_premium'] == True)])

# Ahora calculamos las probabilidades teóricas (casos favorables / casos totales)
P_A = usuarios_chile / total_poblacion
P_B = usuarios_premium / total_poblacion
P_A_interseccion_B = usuarios_chile_y_premium / total_poblacion
P_A_union_B = usuarios_chile_o_premium / total_poblacion

print("1. PROBABILIDAD TEÓRICA (POBLACIÓN TOTAL)")
print(f" - Casos en Chile (A): {usuarios_chile} | P(A) = {P_A:.4f} (o {P_A*100:.1f}%)")
print(f" - Casos Premium (B): {usuarios_premium} | P(B) = {P_B:.4f} (o {P_B*100:.1f}%)")
print(f" - Chile y Premium (A y B): {usuarios_chile_y_premium} | P(A y B) = {P_A_interseccion_B:.4f}")
print(f" - Chile o Premium (A o B): {usuarios_chile_o_premium} | P(A U B) = {P_A_union_B:.4f}")

# Comprobación de la regla de la adición: P(A U B) = P(A) + P(B) - P(A y B)
P_A_union_B_calculada = P_A + P_B - P_A_interseccion_B
print(f" - Verificación con fórmula P(A) + P(B) - P(A y B) = {P_A_union_B_calculada:.4f}")
print("-" * 50)


# =====================================================================
# 2. Muestreo Aleatorio Simple
# =====================================================================
# Obtenemos una muestra aleatoria simple de 150 usuarios de la población
# Usamos random_state=42 para que la muestra sea reproducible
muestra_simple_df = poblacion_df.sample(n=150, random_state=42)

# Contamos cuántos Premium hay en esta muestra
premium_muestra_simple = len(muestra_simple_df[muestra_simple_df['tiene_premium'] == True])

# La probabilidad empírica de tener premium en esta muestra es la proporción
P_B_simple = premium_muestra_simple / len(muestra_simple_df)

print("2. MUESTREO ALEATORIO SIMPLE (n=150)")
print(f" - Usuarios Premium en la muestra simple: {premium_muestra_simple}")
print(f" - Probabilidad Empírica P(B) en Muestra Simple = {P_B_simple:.4f} (o {P_B_simple*100:.1f}%)")
print("-" * 50)


# =====================================================================
# 3. Muestreo Estratificado
# =====================================================================
# Queremos que la proporción de usuarios de cada país en nuestra muestra de 150
# sea la misma que en la población.

# Primero, vemos cuál es la proporción de cada país en la población total:
proporciones_poblacion = poblacion_df['pais'].value_counts(normalize=True)

# Creamos una lista para ir guardando los subconjuntos (estratos) muestreados
muestras_estratos = []

# Iteramos sobre cada país y extraemos su muestra proporcional
for pais, prop in proporciones_poblacion.items():
    # Filtramos la población para obtener solo los usuarios de ese país
    poblacion_pais = poblacion_df[poblacion_df['pais'] == pais]
    
    # Calculamos cuántos usuarios de ese país necesitamos en la muestra (n = 150 * proporción)
    # Usamos round para tener un número entero de personas
    n_muestra_pais = int(round(150 * prop))
    
    # Tomamos la muestra para este país
    muestra_pais = poblacion_pais.sample(n=n_muestra_pais, random_state=42)
    muestras_estratos.append(muestra_pais)

# Unimos todas las submuestras en un único DataFrame
muestra_estratificada_df = pd.concat(muestras_estratos)

# Contamos cuántos Premium hay en esta muestra estratificada
premium_muestra_estrat = len(muestra_estratificada_df[muestra_estratificada_df['tiene_premium'] == True])

# Calculamos la probabilidad empírica de Premium
P_B_estrat = premium_muestra_estrat / len(muestra_estratificada_df)

print("3. MUESTREO ESTRATIFICADO (n=150)")
print(f" - Tamaño final de la muestra estratificada: {len(muestra_estratificada_df)}")
print(" - Distribución de usuarios por país en la muestra:")
for pais, cant in muestra_estratificada_df['pais'].value_counts().items():
    prop_original = proporciones_poblacion[pais] * 100
    prop_muestra = (cant / 150) * 100
    print(f"    * {pais}: {cant} usuarios ({prop_muestra:.1f}% en muestra vs {prop_original:.1f}% en población)")

print(f" - Usuarios Premium en la muestra estratificada: {premium_muestra_estrat}")
print(f" - Probabilidad Empírica P(B) en Muestra Estratificada = {P_B_estrat:.4f} (o {P_B_estrat*100:.1f}%)")
print("-" * 50)


# =====================================================================
# 4. Análisis corto de resultados
# =====================================================================
#
# ANÁLISIS DE LAS TRES PROBABILIDADES CALCULADAS PARA EL EVENTO B:
#
# 1. P(B) Poblacional:         {P_B:.4f} (o {P_B*100:.1f}%)
# 2. P(B) Muestreo Simple:     {P_B_simple:.4f} (o {P_B_simple*100:.1f}%)
# 3. P(B) Muestreo Estratificado: {P_B_estrat:.4f} (o {P_B_estrat*100:.1f}%)
#
# EXPLICACIÓN DE LAS DIFERENCIAS:
#
# Profe, al comparar las tres probabilidades del evento B, me di cuenta de lo siguiente:
#
# - Existe una diferencia entre las probabilidades empíricas de las muestras y la probabilidad 
#   teórica poblacional. Esto se debe al "Error de Muestreo" o variabilidad aleatoria. Al extraer 
#   solo un subconjunto de datos (n=150) de la población total (N=1000), siempre habrá pequeñas 
#   variaciones al azar; es muy difícil que una muestra pequeña sea un reflejo idéntico al 100% 
#   de la población.
#
# - En el Muestreo Aleatorio Simple, cada usuario tiene la misma posibilidad de ser elegido, pero 
#   no controlamos la distribución por país. Si por azar elegimos más personas de un país con 
#   tasas distintas de Premium, esto puede cambiar nuestro P(B) empírico de forma imprevista.
#
# - En el Muestreo Estratificado obligamos a la muestra a respetar las proporciones de los países 
#   que existen en la población total (México 40%, Colombia 30%, Argentina 20% y Chile 10%). 
#   Esto ayuda a reducir el sesgo y la variabilidad cuando los grupos de interés (países) son 
#   muy diferentes entre sí, dándonos una estimación que suele ser más representativa y robusta.
#
# =====================================================================

print("4. ANÁLISIS DE RESULTADOS")
print(f" - P(B) Poblacional:        {P_B:.4f}")
print(f" - P(B) Muestreo Simple:    {P_B_simple:.4f}")
print(f" - P(B) Estratificado:      {P_B_estrat:.4f}")
print("\n[Listo Profe! El análisis comparativo está escrito como comentario en el código source.]")
