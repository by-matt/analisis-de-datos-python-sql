# 1. Entrada de Datos
# Solicitar datos del producto al usuario con mensajes claros
nombre_producto = input("Ingrese el nombre del producto: ")
precio_base = float(input("Ingrese el precio base del producto ($): "))
distancia_envio = float(input("Ingrese la distancia de envío en kilómetros: "))

# 2. Cálculos de Precios
# Calcular el IVA (19% del precio base)
monto_iva = precio_base * 0.19

# Calcular el costo de envío ($1.000 por cada kilómetro)
# Si la distancia es menor a 1 km, el envío es gratis
if distancia_envio < 1:
    costo_envio = 0.0
else:
    costo_envio = distancia_envio * 1000.0

# Calcular el precio final de la venta
precio_final = precio_base + monto_iva + costo_envio

# Calcular el total de impuestos y recargos (IVA + costo de envío)
impuestos_y_recargos = monto_iva + costo_envio

# Formatear montos a formato de pesos chilenos con 2 decimales (punto para miles y coma para decimales)
precio_base_clp = f"${precio_base:,.2f}".replace(",", "x").replace(".", ",").replace("x", ".")
monto_iva_clp = f"${monto_iva:,.2f}".replace(",", "x").replace(".", ",").replace("x", ".")
costo_envio_clp = f"${costo_envio:,.2f}".replace(",", "x").replace(".", ",").replace("x", ".")
precio_final_clp = f"${precio_final:,.2f}".replace(",", "x").replace(".", ",").replace("x", ".")
impuestos_y_recargos_clp = f"${impuestos_y_recargos:,.2f}".replace(",", "x").replace(".", ",").replace("x", ".")

# 3. Presentación de Resultados y Mensaje Final
# Mostrar un único resumen unificado y profesional con todos los datos y mensajes requeridos
print("\n=== RESUMEN DE LA VENTA ===")
print(f"Producto:         {nombre_producto}")
print(f"Precio Base:      {precio_base_clp}")
print(f"Monto de IVA:     {monto_iva_clp}")
print(f"Costo de Envío:   {costo_envio_clp}")
print(f"Precio Final:     {precio_final_clp}")
print("---------------------------")

# Determinar y mostrar el mensaje final sobre el despacho (gratis si es menor a 1 km)
if distancia_envio < 1:
    print("Mensaje de envío: El envío es gratis dado que la distancia es menor a 1 km.")
else:
    print(f"Mensaje de envío: Se aplica costo de envío (el envío es gratis si la distancia es menor a 1 km).")

# Mostrar el total de impuestos y recargos (IVA + envío)
print(f"Total de impuestos y recargos (IVA + envío): {impuestos_y_recargos_clp}")
print("===========================")
