-- ====================================================================
-- DESAFÍO 2: EXPLORANDO RELACIONES Y CONSULTAS AVANZADAS EN SQL
-- ====================================================================

-- --------------------------------------------------------------------
-- Requerimiento 1: Aplicación de combinaciones entre tablas (JOIN)
-- --------------------------------------------------------------------

-- Consulta 1.1: Nombre del cliente, producto comprado y nombre de la tienda, 
-- solo para ventas realizadas en julio.
-- Explicación: Hacemos INNER JOIN entre 'ventas', 'clientes', 'productos' y 'sucursales'.
-- Luego filtramos para obtener las ventas entre el 1 y el 31 de julio de 2024.
SELECT clientes.nombre AS nombre_cliente, 
       productos.nombre_producto, 
       sucursales.nombre_sucursal
FROM ventas
INNER JOIN clientes ON ventas.id_cliente = clientes.id_cliente
INNER JOIN productos ON ventas.id_producto = productos.id_producto
INNER JOIN sucursales ON ventas.id_sucursal = sucursales.id_sucursal
WHERE ventas.fecha BETWEEN '2024-07-01' AND '2024-07-31';


-- Consulta 1.2: Total de ventas (suma de montos) por ciudad de tienda.
-- Explicación: Unimos 'ventas' con 'sucursales', agrupamos por la ciudad de la sucursal
-- y sumamos la columna 'total' de las ventas.
SELECT sucursales.ciudad, 
       SUM(ventas.total) AS total_ventas_ciudad
FROM ventas
INNER JOIN sucursales ON ventas.id_sucursal = sucursales.id_sucursal
GROUP BY sucursales.ciudad;


-- --------------------------------------------------------------------
-- Requerimiento 2: Uso de funciones de agregación y cláusula HAVING
-- --------------------------------------------------------------------

-- Consulta 2.1: Nombre de producto y cantidad total vendida, 
-- pero solo para productos con más de 1 unidad vendida.
-- Explicación: Unimos 'ventas' y 'productos', agrupamos por el nombre del producto,
-- sumamos las cantidades vendidas y usamos HAVING para filtrar solo aquellos cuya suma supera 1.
SELECT productos.nombre_producto, 
       SUM(ventas.cantidad) AS cantidad_total
FROM ventas
INNER JOIN productos ON ventas.id_producto = productos.id_producto
GROUP BY productos.nombre_producto
HAVING SUM(ventas.cantidad) > 1;


-- Consulta 2.2: Cuántas ventas realizó cada sucursal y el promedio de total vendido por venta.
-- Explicación: Unimos 'ventas' y 'sucursales', agrupamos por el nombre de la sucursal
-- y usamos COUNT para contar las ventas y AVG para obtener el promedio de la columna 'total'.
SELECT sucursales.nombre_sucursal, 
       COUNT(ventas.id_venta) AS cantidad_ventas, 
       AVG(ventas.total) AS promedio_venta
FROM ventas
INNER JOIN sucursales ON ventas.id_sucursal = sucursales.id_sucursal
GROUP BY sucursales.nombre_sucursal;


-- --------------------------------------------------------------------
-- Requerimiento 3: Subconsultas para análisis específico
-- --------------------------------------------------------------------

-- Consulta 3.1: Clientes que han realizado compras mayores al promedio general de ventas.
-- Explicación: Seleccionamos los datos de los clientes cuyo ID está en la lista de ventas
-- donde el total de la compra individual es mayor que el promedio general obtenido con (SELECT AVG(total) FROM ventas).
SELECT clientes.nombre, 
       clientes.correo
FROM clientes
WHERE clientes.id_cliente IN (
    SELECT ventas.id_cliente
    FROM ventas
    WHERE ventas.total > (SELECT AVG(total) FROM ventas)
);


-- Consulta 3.2: Nombre del producto más caro vendido.
-- Explicación: Filtramos los productos para obtener aquel cuyo precio sea igual al precio máximo (MAX) 
-- de todos los productos que registran al menos una venta en la tabla de ventas.
SELECT productos.nombre_producto
FROM productos
WHERE productos.precio = (
    SELECT MAX(precio)
    FROM productos
    WHERE id_producto IN (SELECT id_producto FROM ventas)
);
