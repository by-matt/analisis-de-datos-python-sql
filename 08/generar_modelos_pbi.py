import pandas as pd
import numpy as np
import os

# Base paths
base_dir = r"c:\Users\VN\Downloads\ANALISIS DE DATOS\08\01. Unidad 1 Fundamentos de BI y Obtención de Datos"
ventas_path = os.path.join(base_dir, "ventas.csv")
inventario_path = os.path.join(base_dir, "inventario.xlsx")

# 1. Load raw data
df_ventas = pd.read_csv(ventas_path)
df_inventario = pd.read_excel(inventario_path)

print("--- VENTAS RAW ---")
print(df_ventas)
print("\n--- INVENTARIO RAW ---")
print(df_inventario)

# 2. Power Query Clean up simulation
df_ventas.columns = [c.strip() for c in df_ventas.columns]
df_inventario.columns = [c.strip() for c in df_inventario.columns]

# Data type corrections
df_ventas['Fecha'] = pd.to_datetime(df_ventas['Fecha'])
df_ventas['Cantidad'] = df_ventas['Cantidad'].astype(int)
df_ventas['Precio_Unitario'] = df_ventas['Precio_Unitario'].astype(float)
df_ventas['Total'] = df_ventas['Total'].astype(float)

# Filter sales > 10 units (Desafío 2 requirement)
df_ventas_filtrado = df_ventas[df_ventas['Cantidad'] > 10].copy()

# Add DAX calculated column for Inventory Status
def clasificar_stock(stock):
    if stock < 30:
        return "Bajo"
    elif stock <= 80:
        return "Medio"
    else:
        return "Alto"

df_inventario['Estado_Stock_DAX'] = df_inventario['Stock_Actual'].apply(clasificar_stock)

# Merge tables
df_merge = pd.merge(df_ventas_filtrado, df_inventario, on='Producto', how='inner', suffixes=('', '_Inv'))

print("\n--- VENTAS FILTRADAS (>10 unidades) ---")
print(df_ventas_filtrado)

print("\n--- INVENTARIO CON ESTADO DAX ---")
print(df_inventario[['ID_Producto', 'Producto', 'Stock_Actual', 'Estado_Stock_DAX']])

print("\n--- MERGED DATASET ---")
print(df_merge[['ID_Venta', 'Fecha', 'Tienda', 'Categoria_Producto', 'Producto', 'Cantidad', 'Total', 'Stock_Actual', 'Estado_Stock_DAX']])

# DAX Measures calculations
ventas_totales = df_ventas_filtrado['Total'].sum()
promedio_venta_categoria = df_ventas_filtrado.groupby('Categoria_Producto')['Total'].mean()
ventas_por_tienda_cat = df_ventas_filtrado.groupby(['Tienda', 'Categoria_Producto'])['Total'].sum().reset_index()

print(f"\n[DAX] Ventas Totales: ${ventas_totales:,.2f}")
print("\n[DAX] Promedio Venta por Categoría:")
print(promedio_venta_categoria)

print("\n[DAX Tabla Calculada] Ventas Acumuladas por Categoría:")
tabla_calculada = df_ventas_filtrado.groupby('Categoria_Producto')['Total'].sum().reset_index()
tabla_calculada.columns = ['Categoria_Producto', 'Ventas_Acumuladas']
print(tabla_calculada)
