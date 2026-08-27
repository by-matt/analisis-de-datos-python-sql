# prueba_obtencion_preparacion.py
# Prueba - Obtención y preparación de datos

import pandas as pd

# ---------------------------------------------------------------------
# Preparación de datos (DataFrames provistos)
# ---------------------------------------------------------------------
# DataFrame con información de empleados
data_empleados = { 
    'id_empleado': [101, 102, 103, 104, 105, 106, 107, 108], 
    'nombre': ['Ana', 'Luis', 'Sofía', 'Carlos', 'Elena', 'Pedro', 'Laura', 'David'], 
    'salario': [55000, 58000, 72000, 48000, 75000, 85000, 62000, 88000], 
    'id_departamento': ['V_01', 'V_01', 'T_01', 'M_01', 'T_01', 'D_01', 'M_01', 'D_01'] 
} 
df_empleados = pd.DataFrame(data_empleados)

# DataFrame con información de departamentos
data_departamentos = { 
    'id_departamento': ['V_01', 'T_01', 'M_01', 'D_01'], 
    'nombre_depto': ['Ventas', 'Tecnología', 'Marketing', 'Dirección'], 
    'ubicacion': ['Norte', 'Sur', 'Norte', 'Norte'] 
} 
df_departamentos = pd.DataFrame(data_departamentos)


# =====================================================================
# 1. Combinación de Datos (Requerimiento 1)
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 1: COMBINACIÓN DE DATOS (MERGE)")
print("=========================================================")

# Realizar una unión (merge) de tipo inner/left sobre 'id_departamento'
df_completo = pd.merge(df_empleados, df_departamentos, on='id_departamento', how='inner')

print("DataFrame completo (df_completo):")
print(df_completo)
print("-" * 57 + "\n")


# =====================================================================
# 2. Agrupamiento y Agregación (Requerimiento 2)
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 2: AGRUPAMIENTO Y AGREGACIÓN (GROUPBY)")
print("=========================================================")

# Agrupar por nombre_depto y ubicacion, calculando el salario promedio
# de forma precisa. Usamos reset_index() para mantener una estructura de tabla plana.
df_agrupado = df_completo.groupby(['nombre_depto', 'ubicacion'])['salario'].mean().reset_index()

print("Salario promedio agrupado por Departamento y Ubicación:")
print(df_agrupado)
print("-" * 57 + "\n")


# =====================================================================
# 3. Pivoteo de Datos (Requerimiento 3)
# =====================================================================
print("=========================================================")
print("REQUERIMIENTO 3: PIVOTEO DE DATOS (PIVOT TABLE)")
print("=========================================================")

# Reestructurar los datos agrupados: 
# - Índice: nombre_depto
# - Columnas: ubicacion
# - Valores: salario (promedio calculado previamente)
df_pivote = df_agrupado.pivot(index='nombre_depto', columns='ubicacion', values='salario')

print("Tabla Pivote Final (Salarios promedio por Ubicación):")
print(df_pivote)
print("=========================================================")
