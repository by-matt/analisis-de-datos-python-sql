import pandas as pd
import numpy as np
import os

csv_path = r"c:\Users\VN\Downloads\ANALISIS DE DATOS\09\02. Unidad 2 Representación de datos\05. transformacion_digital_dataset.csv"
df = pd.read_csv(csv_path, encoding='latin1')

print("--- TECHCORP DATASET SUMMARY ---")
print(f"Total meses analizados: {len(df)}")
print(f"Columnas ({len(df.columns)}):", df.columns.tolist())

# Summary metrics across time
print("\n--- INICIO (Mes 1: 2023-07) vs ACTUAL (Mes 18: 2024-12) ---")
m1 = df.iloc[0]
m18 = df.iloc[-1]

key_metrics = [
    'productividad_manufactura', 
    'tasa_defectos_porcentaje', 
    'costo_operacional_millones', 
    'ahorro_eficiencia_millones',
    'nps_score',
    'procesos_digitalizados_porcentaje',
    'uso_plataforma_digital_porcentaje',
    'roi_transformacion_porcentaje',
    'horas_extra_promedio',
    'rotacion_personal_porcentaje',
    'vacantes_tech_sin_cubrir',
    'resistencia_cambio_score'
]

for km in key_metrics:
    val_init = m1[km]
    val_final = m18[km]
    diff = val_final - val_init
    print(f"{km:35s}: Mes 1 = {val_init:6.2f} | Mes 18 = {val_final:6.2f} | Var = {diff:+6.2f}")

print("\n--- ANÁLISIS DE CORRELACIONES CLAVE ---")
corr_prod_dig = df['productividad_manufactura'].corr(df['procesos_digitalizados_porcentaje'])
corr_rot_hrsextra = df['rotacion_personal_porcentaje'].corr(df['horas_extra_promedio'])
corr_res_vacantes = df['resistencia_cambio_score'].corr(df['vacantes_tech_sin_cubrir'])

print(f"Correlación Digitalización vs Productividad: {corr_prod_dig:.4f}")
print(f"Correlación Horas Extra vs Rotación Personal: {corr_rot_hrsextra:.4f}")
print(f"Correlación Vacantes Tech vs Resistencia al Cambio: {corr_res_vacantes:.4f}")
